# 🚀 Terminal Command Menu

> A powerful developer productivity tool that transforms your shell history into a searchable, interactive command palette.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey.svg)

**Terminal Command Menu** revolutionizes how you interact with your command history by providing a beautiful, searchable interface to your most frequently used commands. No more scrolling through endless shell history or retyping complex commands!

## ✨ Key Features

### 🎯 **Smart Command Discovery**
- **Intelligent History Parsing**: Automatically analyzes your Zsh, Bash, or Fish history
- **Frequency Analysis**: Commands sorted by usage frequency with execution counts
- **Auto-Categorization**: Commands intelligently grouped (Git, Docker, Kubernetes, Python, etc.)
- **Fuzzy Search**: Lightning-fast real-time filtering as you type

### 🖥️ **Beautiful Terminal Interface**
- **Modern TUI**: Full-screen terminal interface built with Textual
- **Color-Coded Categories**: Visual organization for quick command identification
- **Live Statistics**: Real-time insights into your command usage patterns
- **Keyboard-First Design**: Complete keyboard navigation with intuitive shortcuts

### ⚡ **Instant Execution**
- **One-Click Execution**: Run commands directly from the menu
- **Safety Checks**: Built-in detection of potentially dangerous commands
- **Confirmation Options**: Optional prompts before command execution
- **Shell Integration**: Seamless execution in your current shell environment

## 🎬 Demo

```bash
$ history-menu
```

```
┌─ Terminal Command Menu ──────────────────────────────────────┐
│                                                              │
│ 🔍 Search commands...                                        │
│                                                              │
│ ┌─ STATISTICS ──────────┐ ┌─ COMMANDS ─────────────────────┐ │
│ │ 📊 Total: 2,024       │ │ Category    Command       Count│ │
│ │ 🔢 Unique: 814        │ │ [K8s]       k get pods -A  35x│ │
│ │                       │ │ [Other]     ssh root@...   48x│ │
│ │ 📁 CATEGORIES         │ │ [System]    ll             30x│ │
│ │ Other: 1456           │ │ [Docker]    docker ps      12x│ │
│ │ Kubernetes: 313       │ │ [Git]       git status      8x│ │
│ │ System: 141           │ │ ...                            │ │
│ │ Npm: 54               │ │                                │ │
│ └───────────────────────┘ └────────────────────────────────┘ │
│                                                              │
│ ↑↓ Navigate • Enter Execute • / Search • Ctrl+Q Quit        │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Installation

#### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/terminal-command-menu.git
cd terminal-command-menu

# Run the automated setup script
./setup.sh
```

#### Option 2: Manual Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/terminal-command-menu.git
cd terminal-command-menu

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and package
pip install -e .
```

### Usage

```bash
# Activate the virtual environment (if not already active)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Launch the interactive menu
history-menu

# Alternative command
cmdmenu

# View your command statistics
history-menu --stats

# Skip confirmation prompts
history-menu --no-confirm

# Deactivate virtual environment when done
deactivate
```

## ⌨️ Keyboard Shortcuts

| Key Combination | Action | Description |
|----------------|--------|-------------|
| `↑` `↓` or `j` `k` | Navigate | Move through command list |
| `Enter` | Execute | Run the selected command |
| `/` or `Ctrl+F` | Search | Focus the search box |
| `Escape` | Clear/Exit | Clear search or quit application |
| `Ctrl+R` | Refresh | Reload command history |
| `Ctrl+C` `Ctrl+Q` | Quit | Exit the application |

## 🛠️ Advanced Usage

### Command Line Options

```bash
# Show help and all options
history-menu --help

# Force specific shell type
history-menu --shell zsh

# Limit displayed commands
history-menu --max-commands 50

# View configuration paths
history-menu --config

# Refresh cached history
history-menu --refresh
```

### Configuration

Settings are stored in `~/.config/terminal-command-menu/`:

```json
{
  "max_commands": 100,
  "confirm_execution": true,
  "sort_method": "frequency",
  "excluded_patterns": ["ls", "cd", "pwd", "clear", "exit"],
  "category_filters": []
}
```

## 📊 Shell Support

| Shell | History File | Parsing Status | Notes |
|-------|-------------|----------------|-------|
| **Zsh** | `~/.zsh_history` | ✅ Full Support | Handles timestamps and multiline |
| **Bash** | `~/.bash_history` | ✅ Full Support | Standard format parsing |
| **Fish** | `~/.local/share/fish/fish_history` | ✅ Full Support | YAML format support |

## 📈 Statistics & Analytics

Get detailed insights into your command usage:

```bash
$ history-menu --stats

📊 TERMINAL COMMAND MENU STATISTICS
==================================================
Total commands in history: 2,024
Unique commands: 814

📁 COMMAND CATEGORIES:
  Kubernetes: 313    (15.5%)
  System: 141        (7.0%)
  Docker: 38         (1.9%)
  Git: 6             (0.3%)
  Other: 1,526       (75.3%)

🔥 TOP 10 MOST USED COMMANDS:
   1. ssh root@10.210.9.131        (48 times)
   2. k get pods -A                (35 times)
   3. ll                           (30 times)
   4. docker ps                    (25 times)
   5. git status                   (20 times)
   ...

📱 APP USAGE:
Sessions started: 12
Commands executed via app: 45
```

## 🏗️ Project Structure

```
terminal-command-menu/
├── terminal_menu/           # Core package
│   ├── __init__.py
│   ├── main.py             # CLI entry point
│   ├── tui.py              # Terminal UI components
│   ├── history_parser.py   # Shell history parsing
│   ├── settings.py         # Configuration management
│   └── executor.py         # Command execution
├── history-menu            # Main executable
├── cmdmenu                 # Alternative executable
├── setup.sh                # Automated setup script (Unix/macOS)
├── setup.bat               # Automated setup script (Windows)
├── requirements.txt        # Python dependencies
├── setup.py               # Package configuration
├── .gitignore             # Git ignore patterns
├── LICENSE                # MIT License
├── README.md              # This file
├── INSTALL.md             # Detailed installation guide
└── PROJECT_SUMMARY.md     # Complete project overview
```

## 🔧 Technical Details

### Built With
- **[Textual](https://textual.textualize.io/)** - Modern Python TUI framework
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal formatting
- **[Click](https://click.palletsprojects.com/)** - Command-line interface framework
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation and settings

### Requirements
- **Python**: 3.8 or higher
- **Platforms**: macOS, Linux
- **Terminal**: Color support recommended

### Performance
- ⚡ **Sub-second startup** even with 2,000+ commands
- 🔍 **Real-time search** with fuzzy matching
- 💾 **Minimal memory footprint** with efficient data structures
- 🔄 **Lazy loading** for large history files

## 🤝 Contributing

This project was built from a comprehensive Product Requirements Document (PRD) to solve real developer productivity challenges. 

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/yourusername/terminal-command-menu.git
cd terminal-command-menu

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests
python -m pytest

# Check the implementation against PRD
cat PROJECT_SUMMARY.md
```

### Feature Requests

See `PROJECT_SUMMARY.md` for the complete feature roadmap and implementation status.

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built to solve the common developer pain point of managing complex terminal commands
- Inspired by tools like `fzf` and `telescope.nvim` but specifically designed for command history
- Special thanks to the Textual team for the amazing TUI framework

---

**Made with ❤️ for developers who live in the terminal**

*Transform your command-line workflow today!* 🚀
