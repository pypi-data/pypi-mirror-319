import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from datetime import datetime
import queue
import uiautomation as auto
from .core import TranscriptManager, monitor_transcript
import re
import configparser
from .gpt4o import ask
import os
from .config_manager import ConfigManager

class NotificationWindow:
    def __init__(self, parent, message, duration=4):
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)  # 移除窗口装饰
        
        # 设置窗口样式
        self.window.configure(bg='#333333')
        
        # 创建消息标签
        self.label = tk.Label(
            self.window,
            text=message,
            fg='white',
            bg='#333333',
            padx=20,
            pady=10,
            font=('Arial', 10)
        )
        self.label.pack()
        
        # 获取主窗口位置和大小
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        
        # 计算通知窗口位置（右上角）
        window_width = self.label.winfo_reqwidth() + 40  # 加上padding
        window_height = self.label.winfo_reqheight() + 20
        
        # 设置窗口位置
        x = parent_x + parent_width - window_width - 20
        y = parent_y + 20
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 设置定时器关闭窗口
        self.window.after(duration * 1000, self.close)
    
    def close(self):
        self.window.destroy()

class ConfigDialog:
    def __init__(self, parent, config_manager, callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Configuration")
        self.top.geometry("800x800")
        self.config_manager = config_manager  # 使用 ConfigManager 实例
        self.config = self.config_manager.get_config() # 获取配置对象
        self.callback = callback
        
        # 创建notebook
        self.notebook = ttk.Notebook(self.top)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建各个标签页
        self.create_defaults_tab(self.notebook)
        self.create_prompts_tab(self.notebook)
        self.create_genai_tab(self.notebook)
        
        # 创建按钮区域
        button_frame = ttk.Frame(self.top)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Update", command=self.save_config).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=5)
        
        # 使对话框模态
        self.top.transient(parent)
        self.top.grab_set()
    
    def create_defaults_tab(self, notebook):
        """创建Defaults标签页"""
        defaults_frame = ttk.Frame(notebook)
        notebook.add(defaults_frame, text="Defaults")
        
        # 创建默认值配置项
        self.default_vars = {}
        row = 0
        
        # 单行输入项
        single_line_items = ['duration', 'username', 'language', 'live_freq', 'notification_showtime']
        for key in single_line_items:
            ttk.Label(defaults_frame, text=key).grid(row=row, column=0, padx=5, pady=2)
            var = tk.StringVar(value=self.config.get('Defaults', key, fallback=''))
            ttk.Entry(defaults_frame, textvariable=var).grid(row=row, column=1, padx=5, pady=2)
            self.default_vars[key] = var
            row += 1
        
        # 多行文本框
        multiline_items = ['context', 'agenda', 'topics', 'stakeholders', 'notes']
        for key in multiline_items:
            ttk.Label(defaults_frame, text=key).grid(row=row, column=0, padx=5, pady=2)
            text_widget = tk.Text(defaults_frame, height=4, width=50)
            text_widget.grid(row=row, column=1, padx=5, pady=2)
            text_widget.insert("1.0", self.config.get('Defaults', key, fallback=''))
            self.default_vars[key] = text_widget
            row += 1
    
    def create_prompts_tab(self, notebook):
        """创建Prompts标签页"""
        prompts_frame = ttk.Frame(notebook)
        notebook.add(prompts_frame, text="Prompts")
        
        # 创建prompt配置项
        self.prompt_vars = {}
        prompts = [
            ('summarize_prompt', 'Summarize Prompt'),
            ('viewpoints_prompt', 'Viewpoints Prompt'),
            ('navigate_prompt', 'Navigation Prompt'),
            ('minutes_prompt', 'Meeting Minutes Prompt')
        ]
        
        for row, (key, label) in enumerate(prompts):
            ttk.Label(prompts_frame, text=label).grid(row=row, column=0, padx=5, pady=5)
            text_widget = tk.Text(prompts_frame, height=8, width=60)
            text_widget.grid(row=row, column=1, padx=5, pady=5)
            text_widget.insert("1.0", self.config.get('Prompts', key, fallback=''))
            self.prompt_vars[key] = text_widget
    
    def create_genai_tab(self, notebook):
        """创建GenAI标签页"""
        genai_frame = ttk.Frame(notebook)
        notebook.add(genai_frame, text="GenAI")
        
        # 创建GenAI配置项
        self.genai_vars = {}
        row = 0
        for key in ['openai_token', 'openai_token_url', 'openai_health_url', 
                   'openai_mm_url', 'openai_chat_url', 'openai_user_name', 
                   'openai_password', 'openai_application_id', 'openai_application_name',
                   'head_token_key']:
            ttk.Label(genai_frame, text=key).grid(row=row, column=0, padx=5, pady=2)
            var = tk.StringVar(value=self.config.get('GenAI', key, fallback=''))
            ttk.Entry(genai_frame, textvariable=var).grid(row=row, column=1, padx=5, pady=2)
            self.genai_vars[key] = var
            row += 1
    
    def save_config(self):
        """保存配置"""
        # 更新Defaults部分
        for key, var in self.default_vars.items():
            if isinstance(var, tk.Text):
                value = var.get("1.0", tk.END).strip()
            else:
                value = var.get()
            self.config.set('Defaults', key, value)
        
        # 更新Prompts部分
        for key, var in self.prompt_vars.items():
            value = var.get("1.0", tk.END).strip()
            self.config.set('Prompts', key, value)
        
        # 更新GenAI部分
        for key, var in self.genai_vars.items():
            self.config.set('GenAI', key, var.get())
        
        # 使用 ConfigManager 保存配置
        self.config_manager.save_config()
        
        # 调用回调函数更新主程序的配置
        self.callback()
        
        # 关闭对话框
        self.top.destroy()
    
    def cancel(self):
        """取消配置"""
        self.top.destroy()

class MeetingNavigator:
    def __init__(self, root):
        # 使用配置管理器
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()
        
        self.root = root
        self.root.title("Meeting Navigator")
        self.root.geometry("1200x800")
        
        # 创建消息队列用于线程间通信
        self.message_queue = queue.Queue()
        self.llm_queue = queue.Queue()
        
        # 初始化按钮相关的属性
        self.buttons = {}  # 初始化按钮字典
        self.button_states = {  # 初始化按钮状态
            'summarize': False,
            'viewpoints': False,
            'navigate': False,
            'submit': False
        }
        
        # 初始化Transcript相关变量
        self.transcript_thread = None
        self.transcript_manager = None
        self.last_update = datetime.now()
        
        # 初始化变量
        self.init_variables()
        
        # 创建主分割区域
        self.create_main_layout()
        
        # 启动UI更新循环
        self.update_ui()
        
        # 启动转录监控
        self.start_transcript_monitor()
        
        # 获取通知显示时间
        self.notification_duration = int(self.config['Defaults'].get('notification_showtime', '4'))
    
    def init_variables(self):
        """初始化所有变量"""
        # 加载默认值
        defaults = self.config['Defaults']
        
        # 控制栏变量
        self.duration_var = tk.StringVar(value=defaults.get('duration', '60min'))
        self.username_var = tk.StringVar(value=defaults.get('username', 'Default User'))
        self.language_var = tk.StringVar(value=defaults.get('language', 'En'))
        self.freq_var = tk.StringVar(value=defaults.get('live_freq', '30'))
        self.live_var = tk.BooleanVar(value=False)
        
        # 设置文本框默认值
        self.default_context = defaults.get('context', '')
        self.default_agenda = defaults.get('agenda', '')
        self.default_topics = defaults.get('topics', '')
        self.default_stakeholders = defaults.get('stakeholders', '')
        self.default_notes = defaults.get('notes', '')
    
    def create_main_layout(self):
        """创建主布局"""
        # 创建左右分割的主面板
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧面板
        left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(left_frame, weight=1)
        
        # 右侧面板
        right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(right_frame, weight=1)
        
        # 创建左侧内容
        self.create_left_panel(left_frame)
        # 创建右侧内容
        self.create_right_panel(right_frame)
    
    def create_left_panel(self, parent):
        """创建左侧面板"""
        # 创建一个主Frame来容纳所有sections
        self.left_main_frame = ttk.Frame(parent)
        self.left_main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Live Transcript区域
        self.transcript_frame = ttk.Frame(self.left_main_frame)
        self.transcript_frame.pack(fill=tk.X)
        
        # Transcript标题（可点击）
        self.transcript_header = ttk.Label(
            self.transcript_frame,
            text="▼ Live Transcript",
            cursor="hand2"
        )
        self.transcript_header.pack(fill=tk.X, padx=5, pady=2)
        self.transcript_header.bind('<Button-1>', lambda e: self.toggle_transcript())
        
        # Transcript内容
        self.transcript_content = ttk.Frame(self.transcript_frame)
        self.transcript_content.pack(fill=tk.BOTH, expand=True)
        self.transcript_text = scrolledtext.ScrolledText(self.transcript_content)
        self.transcript_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        # Live Summary区域
        self.summary_frame = ttk.Frame(self.left_main_frame)
        self.summary_frame.pack(fill=tk.X)
        
        self.summary_header = ttk.Label(
            self.summary_frame,
            text="▼ Live Summary",
            cursor="hand2"
        )
        self.summary_header.pack(fill=tk.X, padx=5, pady=2)
        self.summary_header.bind('<Button-1>', lambda e: self.toggle_summary())
        
        self.summary_content = ttk.Frame(self.summary_frame)
        self.summary_content.pack(fill=tk.BOTH, expand=True)
        self.summary_text = scrolledtext.ScrolledText(self.summary_content)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        # Each one's view区域
        self.views_frame = ttk.Frame(self.left_main_frame)
        self.views_frame.pack(fill=tk.X)
        
        self.views_header = ttk.Label(
            self.views_frame,
            text="▼ Each one's view",
            cursor="hand2"
        )
        self.views_header.pack(fill=tk.X, padx=5, pady=2)
        self.views_header.bind('<Button-1>', lambda e: self.toggle_views())
        
        self.views_content = ttk.Frame(self.views_frame)
        self.views_content.pack(fill=tk.BOTH, expand=True)
        self.views_text = scrolledtext.ScrolledText(self.views_content)
        self.views_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        # Navigation guidance区
        self.nav_frame = ttk.Frame(self.left_main_frame)
        self.nav_frame.pack(fill=tk.X)
        
        self.nav_header = ttk.Label(
            self.nav_frame,
            text="▼ Navigation guidance",
            cursor="hand2"
        )
        self.nav_header.pack(fill=tk.X, padx=5, pady=2)
        self.nav_header.bind('<Button-1>', lambda e: self.toggle_nav())
        
        self.nav_content = ttk.Frame(self.nav_frame)
        self.nav_content.pack(fill=tk.BOTH, expand=True)
        self.nav_text = scrolledtext.ScrolledText(self.nav_content)
        self.nav_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
    
    def toggle_summary(self):
        """切换Summary区域的展开/折叠状态"""
        if self.summary_content.winfo_viewable():
            self.summary_content.pack_forget()
            self.summary_header.configure(text="▶ Live Summary")
            self.summary_frame.configure(height=25)
        else:
            self.summary_frame.configure(height=0)
            self.summary_content.pack(fill=tk.BOTH, expand=True)
            self.summary_header.configure(text="▼ Live Summary")
        self.redistribute_space()
    
    def toggle_views(self):
        """切换Views区域的展开/折叠状态"""
        if self.views_content.winfo_viewable():
            self.views_content.pack_forget()
            self.views_header.configure(text="▶ Each one's view")
            self.views_frame.configure(height=25)
        else:
            self.views_frame.configure(height=0)
            self.views_content.pack(fill=tk.BOTH, expand=True)
            self.views_header.configure(text="▼ Each one's view")
        self.redistribute_space()
    
    def toggle_nav(self):
        """切换Navigation区域的展开/折叠状态"""
        if self.nav_content.winfo_viewable():
            self.nav_content.pack_forget()
            self.nav_header.configure(text="▶ Navigation guidance")
            self.nav_frame.configure(height=25)
        else:
            self.nav_frame.configure(height=0)
            self.nav_content.pack(fill=tk.BOTH, expand=True)
            self.nav_header.configure(text="▼ Navigation guidance")
        self.redistribute_space()
    
    def toggle_transcript(self):
        """切换Transcript区域的展开/折叠状态"""
        if self.transcript_content.winfo_viewable():
            self.transcript_content.pack_forget()
            self.transcript_header.configure(text="▶ Live Transcript")
            self.transcript_frame.configure(height=25)  # 折叠时的最小高度
        else:
            self.transcript_frame.configure(height=0)  # 重置高度限制
            self.transcript_content.pack(fill=tk.BOTH, expand=True)
            self.transcript_header.configure(text="▼ Live Transcript")
        self.redistribute_space()
    
    def redistribute_space(self):
        """重新分配空间"""
        # 获取所有frame
        all_frames = [
            (self.transcript_frame, self.transcript_content, self.transcript_text),
            (self.summary_frame, self.summary_content, self.summary_text),
            (self.views_frame, self.views_content, self.views_text),
            (self.nav_frame, self.nav_content, self.nav_text)
        ]
        
        # 计算展开的sections数量
        expanded_count = sum(1 for _, content, _ in all_frames if content.winfo_viewable())
        
        # 设置每个frame的权重
        for frame, content, text_widget in all_frames:
            if content.winfo_viewable():
                # 展开状态：设置frame可扩展，并分配相等的空间
                frame.pack(fill=tk.BOTH, expand=True)
                text_widget.configure(height=10)  # 设置一个基础高度
            else:
                # 叠状态：固定高度，不扩展
                frame.pack(fill=tk.X, expand=False)
                frame.configure(height=25)  # 标题行高度
        
        # 更新UI
        self.root.update_idletasks()
    
    def get_context(self):
        """获取所有上下文信息"""
        return {
            "duration": self.duration_var.get(),
            "username": self.username_var.get(),
            "language": self.language_var.get(),
            "live_freq": self.freq_var.get(),
            "live_on": self.live_var.get(),
            "context": self.context_text.get("1.0", tk.END).strip(),
            "agenda": self.agenda_text.get("1.0", tk.END).strip(),
            "topics": self.topics_text.get("1.0", tk.END).strip(),
            "stakeholders": self.stakeholders_text.get("1.0", tk.END).strip(),
            "notes": self.notes_text.get("1.0", tk.END).strip()
        }
    
    def update_transcript_display(self, transcript_item):
        """更新转录内容显示"""
        try:
            # 获取所有当前显示的内容
            current_text = self.transcript_text.get("1.0", tk.END)
            lines = current_text.splitlines()
            
            # 查找是否存在相同时间戳和说话者的行
            found = False
            for i, line in enumerate(lines):
                if not line:  # 跳过空行
                    continue
                # 解析行内容
                match = re.match(r'\[([\d:]+)\] ([^:]+):', line)
                if match:
                    timestamp, speaker = match.groups()
                    # 如果找到相同时间戳和说话者的行
                    if timestamp == transcript_item.timestamp and speaker == transcript_item.speaker:
                        found = True
                        # 获取当前行的内容
                        current_content = line.split(':', 1)[1].strip()
                        # 如果新内容更长，则替换这一行
                        if len(transcript_item.content) > len(current_content):
                            # 清除所有内容
                            self.transcript_text.delete("1.0", tk.END)
                            # 重建内容：保持之前的行
                            for j, old_line in enumerate(lines):
                                if j == i:  # 在这个位置插入新内容
                                    self.transcript_text.insert(tk.END, f"{transcript_item.to_string()}\n")
                                elif old_line:  # 插入其他非空行
                                    self.transcript_text.insert(tk.END, f"{old_line}\n")
                        break
            
            # 如果没有找到相同的行，追加新内容
            if not found:
                self.transcript_text.insert(tk.END, f"{transcript_item.to_string()}\n")
            
            # 自动滚动到底部
            self.transcript_text.see(tk.END)
            
        except Exception as e:
            print(f"更新转录显示错误: {e}")
    
    def create_right_panel(self, parent):
        """创建右侧面板"""
        # 顶部控制栏
        self.create_control_bar(parent)
        
        # Meeting Context
        context_frame = ttk.LabelFrame(parent, text="Meeting Context")
        context_frame.pack(fill=tk.X, padx=5, pady=5)
        self.context_text = scrolledtext.ScrolledText(context_frame, height=4)
        self.context_text.pack(fill=tk.BOTH, expand=True)
        
        # Meeting Agenda/Target
        agenda_frame = ttk.LabelFrame(parent, text="Meeting Agenda/Target")
        agenda_frame.pack(fill=tk.X, padx=5, pady=5)
        self.agenda_text = scrolledtext.ScrolledText(agenda_frame, height=4)
        self.agenda_text.pack(fill=tk.BOTH, expand=True)
        
        # Meeting Topics
        topics_frame = ttk.LabelFrame(parent, text="Meeting Topics")
        topics_frame.pack(fill=tk.X, padx=5, pady=5)
        self.topics_text = scrolledtext.ScrolledText(topics_frame, height=4)
        self.topics_text.pack(fill=tk.BOTH, expand=True)
        
        # Meeting Stakeholders
        stakeholders_frame = ttk.LabelFrame(parent, text="Meeting Stakeholders")
        stakeholders_frame.pack(fill=tk.X, padx=5, pady=5)
        self.stakeholders_text = scrolledtext.ScrolledText(stakeholders_frame, height=4)
        self.stakeholders_text.pack(fill=tk.BOTH, expand=True)
        
        # Notes
        notes_frame = ttk.LabelFrame(parent, text="Notes")
        notes_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=4)
        self.notes_text.pack(fill=tk.BOTH, expand=True)
        
        # 底部按钮栏
        self.create_button_bar(parent)
        
        # 设置默认值
        self.context_text.insert("1.0", self.default_context)
        self.agenda_text.insert("1.0", self.default_agenda)
        self.topics_text.insert("1.0", self.default_topics)
        self.stakeholders_text.insert("1.0", self.default_stakeholders)
        self.notes_text.insert("1.0", self.default_notes)
    
    def create_control_bar(self, parent):
        """创建顶部控制栏"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Duration
        ttk.Label(control_frame, text="Duration").pack(side=tk.LEFT, padx=2)
        ttk.Combobox(control_frame, textvariable=self.duration_var, 
                    values=["30min", "60min", "90min", "120min"], 
                    width=8).pack(side=tk.LEFT, padx=2)
        
        # For (username) - 使用已初始化的变量
        ttk.Label(control_frame, text="For").pack(side=tk.LEFT, padx=2)
        ttk.Entry(control_frame, textvariable=self.username_var, 
                 width=15).pack(side=tk.LEFT, padx=2)
        
        # Language
        ttk.Label(control_frame, text="Language").pack(side=tk.LEFT, padx=2)
        self.language_var = tk.StringVar(value="En")
        ttk.Entry(control_frame, textvariable=self.language_var,
                 width=5).pack(side=tk.LEFT, padx=2)
        
        # LIVE Freq
        ttk.Label(control_frame, text="LIVE Freq").pack(side=tk.LEFT, padx=2)
        self.freq_var = tk.StringVar(value="30")
        ttk.Entry(control_frame, textvariable=self.freq_var,
                 width=5).pack(side=tk.LEFT, padx=2)
        
        # LIVE on switch
        self.live_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="LIVE on",
                       variable=self.live_var).pack(side=tk.LEFT, padx=2)
    
    def create_button_bar(self, parent):
        """创建底部按钮栏"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 左对齐的Config按钮
        self.buttons['config'] = ttk.Button(button_frame, text="Config", 
                                          command=self.show_config_dialog)
        self.buttons['config'].pack(side=tk.LEFT, padx=5)
        
        # 右对齐按钮
        self.buttons['save'] = ttk.Button(button_frame, text="Save", 
                                        command=self.save_all)
        self.buttons['save'].pack(side=tk.RIGHT, padx=5)
        
        self.buttons['summarize'] = ttk.Button(button_frame, text="Summarize", 
                                             command=self.manual_summarize)
        self.buttons['summarize'].pack(side=tk.RIGHT, padx=5)
        
        self.buttons['viewpoints'] = ttk.Button(button_frame, text="Viewpoints", 
                                              command=self.manual_viewpoints)
        self.buttons['viewpoints'].pack(side=tk.RIGHT, padx=5)
        
        self.buttons['navigate'] = ttk.Button(button_frame, text="Navigate", 
                                            command=self.manual_navigation)
        self.buttons['navigate'].pack(side=tk.RIGHT, padx=5)
        
        self.buttons['submit'] = ttk.Button(button_frame, text="Submit", 
                                          command=self.submit_all)
        self.buttons['submit'].pack(side=tk.RIGHT, padx=5)
    
    def start_transcript_monitor(self):
        """启动转录监控线程"""
        def run_monitor():
            try:
                with auto.UIAutomationInitializerInThread():
                    print("Debug: Starting monitor_transcript...")
                    # 获取manager实例和监控循环函数
                    manager, monitor_loop = monitor_transcript(
                        lambda msg_type, content: self.message_queue.put((msg_type, content))
                    )
                    # 设置manager
                    self.transcript_manager = manager
                    # 运行控循环
                    monitor_loop()
            except Exception as e:
                print(f"Debug: Error in run_monitor: {e}")
                self.message_queue.put(("error", f"Transcript monitor error: {str(e)}"))
        
        if self.transcript_thread is None or not self.transcript_thread.is_alive():
            print("Debug: Creating new transcript monitor thread")
            self.transcript_thread = threading.Thread(target=run_monitor)
            self.transcript_thread.daemon = True
            self.transcript_thread.start()
            print("Debug: Transcript monitor thread started")
    
    def update_ui(self):
        """更新UI的周期性任务"""
        try:
            # 处理transcript消息队列
            while not self.message_queue.empty():
                msg_type, msg_content = self.message_queue.get_nowait()
                if msg_type == "transcript":
                    self.update_transcript_display(msg_content)
                elif msg_type == "error":
                    self.show_error(msg_content)
            
            # 处理LLM响应消息队列
            while not self.llm_queue.empty():
                msg_type, content = self.llm_queue.get_nowait()
                if msg_type == "summary":
                    self.summary_text.delete("1.0", tk.END)
                    self.summary_text.insert("1.0", content)
                elif msg_type == "viewpoints":
                    self.views_text.delete("1.0", tk.END)
                    self.views_text.insert("1.0", content)
                elif msg_type == "navigation":
                    self.nav_text.delete("1.0", tk.END)
                    self.nav_text.insert("1.0", content)
                elif msg_type == "error":
                    self.show_error(content)
            
            # 如果实时功能开启，执行实时更新
            if self.live_var.get():
                self.update_live_features()
            
            # 继续周期性更新
            self.root.after(1000, self.update_ui)
            
        except Exception as e:
            print(f"UI更新错误: {e}")
            self.root.after(1000, self.update_ui)
    
    def update_live_features(self):
        """更新实时功能"""
        try:
            # 获取更新频率
            freq = int(self.freq_var.get())
            current_time = datetime.now()
            
            # 检查是否需要更新
            if (current_time - self.last_update).total_seconds() >= freq:
                self.manual_summarize()
                self.manual_viewpoints()
                self.manual_navigation()
                self.last_update = current_time
        except Exception as e:
            print(f"实时更新错误: {e}")
    
    def show_error(self, error_message):
        """显示错误消息"""
        # 这里可以实现错误提示UI
        print(f"Error: {error_message}")
    
    # 按钮回调函数
    def save_all(self):
        """保存所有内容"""
        try:
            if self.transcript_manager:
                # 使用TranscriptManager的save_to_file方法保存transcript
                output_path = self.transcript_manager._get_output_path()
                self.transcript_manager.save_to_file()
                
                # 显示成功通知
                message = f"保存成功!\n文件路径: {output_path}"
                self.show_notification(message)
                
                print("Transcript保存成功")
            else:
                raise Exception("Transcript manager未初始化")
            
        except Exception as e:
            self.show_error(f"保存失败: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def get_transcript_text(self):
        """获取有transcript内容"""
        try:
            print("\nDebug: Getting transcript text...")
            
            if not self.transcript_manager:
                print("Debug: transcript_manager is None")
                return ""
            
            print(f"Debug: transcript_manager exists, transcripts count: {len(self.transcript_manager.transcripts)}")
            
            if not self.transcript_manager.transcripts:
                print("Debug: transcripts dictionary is empty")
                return ""
            
            # 获取所有转录内容并按时间排序
            sorted_items = sorted(
                self.transcript_manager.transcripts.values(),
                key=lambda x: datetime.strptime(x.timestamp, '%H:%M:%S')
            )
            
            print(f"Debug: Sorted items count: {len(sorted_items)}")
            
            # 将每个条目转换为字符串并连接
            transcript_text = "\n".join(item.to_string() for item in sorted_items)
            
            print("Debug: Current transcript:")
            print("-" * 50)
            print(transcript_text)
            print("-" * 50)
            print(f"Debug: Transcript text length: {len(transcript_text)}")
            
            return transcript_text
            
        except Exception as e:
            print(f"获取transcript文本时出错: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def get_prompt(self, prompt_name):
        """安全地获取prompt模板"""
        try:
            if 'Prompts' not in self.config:
                raise KeyError("配置文件中缺少 [Prompts] 部分")
            if prompt_name not in self.config['Prompts']:
                raise KeyError(f"配置文件中缺少 {prompt_name} 配置")
            return self.config['Prompts'][prompt_name]
        except Exception as e:
            raise Exception(f"获取prompt失败: {str(e)}")
    
    def call_llm_async(self, msg_type, msgs, button_name):
        """异步调用LLM"""
        def run_llm():
            try:
                # 开始动画
                self.button_states[button_name.lower()] = True
                self.root.after(0, self.update_button_animation)
                
                response = ask(msgs)
                self.llm_queue.put((msg_type, response))
                
            except Exception as e:
                self.llm_queue.put(("error", f"LLM调用失败: {str(e)}"))
            finally:
                # 停止动画
                self.button_states[button_name.lower()] = False
                # 恢复按钮文字
                self.root.after(0, lambda: self.buttons[button_name.lower()].configure(
                    text=button_name.capitalize()))
        
        thread = threading.Thread(target=run_llm)
        thread.daemon = True
        thread.start()
    
    def manual_summarize(self):
        """手动触发总结"""
        try:
            # 准备prompt参数
            params = {
                "transcript": self.get_transcript_text(),
                "meeting_topic": self.topics_text.get("1.0", tk.END).strip(),
                "meeting_goals": self.agenda_text.get("1.0", tk.END).strip(),
                "background": self.context_text.get("1.0", tk.END).strip(),
                "language": self.language_var.get()
            }
            
            # 获取prompt模板并格式化
            prompt = self.get_prompt('summarize_prompt').format(**params)
            
            # 异步调用LLM
            msgs = [
                {"role": "system", "content": "You are a helpful meeting assistant."},
                {"role": "user", "content": prompt}
            ]
            self.call_llm_async("summary", msgs, "Summarize")
            
        except Exception as e:
            self.show_error(f"总结生成失败: {str(e)}")
    
    def manual_viewpoints(self):
        """手动触发观点分析"""
        try:
            params = {
                "transcript": self.get_transcript_text(),
                "meeting_topic": self.topics_text.get("1.0", tk.END).strip(),
                "meeting_goals": self.agenda_text.get("1.0", tk.END).strip(),
                "user_name": self.username_var.get(),
                "key_stakeholders": self.stakeholders_text.get("1.0", tk.END).strip(),
                "language": self.language_var.get()
            }
            
            prompt = self.get_prompt('viewpoints_prompt').format(**params)
            msgs = [
                {"role": "system", "content": "You are a helpful meeting assistant."},
                {"role": "user", "content": prompt}
            ]
            self.call_llm_async("viewpoints", msgs, "Viewpoints")
            
        except Exception as e:
            self.show_error(f"观点分析失败: {str(e)}")
    
    def manual_navigation(self):
        """手动触发导航建议"""
        try:
            params = {
                "transcript": self.get_transcript_text(),
                "meeting_topic": self.topics_text.get("1.0", tk.END).strip(),
                "meeting_goals": self.agenda_text.get("1.0", tk.END).strip(),
                "key_stakeholders": self.stakeholders_text.get("1.0", tk.END).strip(),
                "user_name": self.username_var.get(),
                "language": self.language_var.get(),
                "notes": self.notes_text.get("1.0", tk.END).strip()
            }
            
            prompt = self.get_prompt('navigate_prompt').format(**params)
            msgs = [
                {"role": "system", "content": "You are a helpful meeting assistant."},
                {"role": "user", "content": prompt}
            ]
            self.call_llm_async("navigation", msgs, "Navigate")
            
        except Exception as e:
            self.show_error(f"导航建议生成失败: {str(e)}")
    
    def submit_all(self):
        """生成会议纪要并提交"""
        try:
            params = {
                "transcript": self.get_transcript_text(),
                "meeting_topic": self.topics_text.get("1.0", tk.END).strip(),
                "meeting_goals": self.agenda_text.get("1.0", tk.END).strip(),
                "language": self.language_var.get()
            }
            
            prompt = self.get_prompt('minutes_prompt').format(**params)
            msgs = [
                {"role": "system", "content": "You are a helpful meeting assistant."},
                {"role": "user", "content": prompt}
            ]
            response = ask(msgs)
            
            # TODO: 实现保存会议纪要的逻辑
            print("会议纪要生成成功")
            print(response)
            
        except Exception as e:
            self.show_error(f"提交失败: {str(e)}")
    
    def update_button_animation(self):
        """更新按钮动画"""
        for button_name, is_active in self.button_states.items():
            if is_active:
                current_text = self.buttons[button_name].cget('text')
                base_text = button_name.capitalize()
                dots = current_text[len(base_text):].count('.')
                
                # 更新点的数量（0-6循环）
                new_dots = (dots + 1) % 7
                self.buttons[button_name].configure(text=f"{base_text}{'.' * new_dots}")
        
        # 继续动画
        if any(self.button_states.values()):
            self.root.after(300, self.update_button_animation)
    
    def show_notification(self, message):
        """显示通知"""
        NotificationWindow(self.root, message, self.notification_duration)
    
    def show_config_dialog(self):
        """显示配置对话框"""
        ConfigDialog(self.root, self.config_manager, self.reload_config) # 传递 ConfigManager 实例
    
    def reload_config(self):
        """重新加载配置"""
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()
        
        # 更新通知显示时间
        self.notification_duration = int(self.config['Defaults'].get('notification_showtime', '4'))
        
        # 显示成功通知
        self.show_notification("配置已更新")

def main():
    root = tk.Tk()
    app = MeetingNavigator(root)
    root.mainloop()

if __name__ == "__main__":
    main()