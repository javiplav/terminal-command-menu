from setuptools import setup, find_packages

setup(
    name="terminal-command-menu",
    version="1.0.0",
    description="A developer productivity tool for frequently used terminal commands",
    author="Javier Plavnick",
    packages=find_packages(),
    install_requires=[
        "textual>=0.45.0",
        "rich>=13.7.0", 
        "click>=8.1.0",
        "pyfzf>=0.3.1",
        "pydantic>=2.5.0"
    ],
    entry_points={
        "console_scripts": [
            "history-menu=terminal_menu.main:main",
            "cmdmenu=terminal_menu.main:main",
        ],
    },
    python_requires=">=3.8",
)
