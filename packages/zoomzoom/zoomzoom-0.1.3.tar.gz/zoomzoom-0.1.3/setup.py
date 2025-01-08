from setuptools import setup, find_packages

setup(
    name="zoomzoom",
    version="0.1.3",
    author="Jim",
    author_email="your.email@example.com",
    description="A Zoom meeting assistant",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jimeverest/zoomzoom",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "requests",
        "uiautomation",
        "pywin32",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'zoomzoom=zoomzoom.__main__:main',
        ],
    },
) 