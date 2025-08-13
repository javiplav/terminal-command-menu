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
$ terminal-menu
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

### Option 1: One-Line Install (Recommended)
```bash
# Download and install standalone version (no Python packages needed!)
curl -fsSL https://raw.githubusercontent.com/javiplav/terminal-command-menu/main/install.sh | bash
```

Or manually:
```bash
# Download standalone script
mkdir -p ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/javiplav/terminal-command-menu/main/terminal-menu-standalone -o ~/.local/bin/terminal-menu
chmod +x ~/.local/bin/terminal-menu

# Add ~/.local/bin to PATH (add to ~/.zshrc or ~/.bashrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Option 2: Development Setup
```bash
# Clone the repository for development
git clone https://github.com/javiplav/terminal-command-menu.git
cd terminal-command-menu

# Run the automated setup script
./scripts/setup.sh
```

### Usage

```bash
# Launch the interactive menu (works immediately after install!)
terminal-menu

# ⚡ Fast mode - optimized performance (recommended!)
terminal-menu --fast

# 🚀 Maximum speed - fast mode + no confirmation
terminal-menu --fast --no-confirm

# View your command statistics
terminal-menu --stats

# Show help and all options
terminal-menu --help
```

**No virtual environments or package installation required with the standalone version!**

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
terminal-menu --help

# Fast mode for better performance
terminal-menu --fast

# Force specific shell type
terminal-menu --shell zsh

# Limit displayed commands
terminal-menu --max-commands 50

# Skip confirmation dialogs
terminal-menu --no-confirm

# View configuration paths
terminal-menu --config

# Refresh cached history
terminal-menu --refresh
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
$ terminal-menu --stats

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
terminal-command-menu/          # 📦 Clean, lightweight project (468K total)
├── terminal_menu/              # 🐍 Core Python package
│   ├── __init__.py
│   ├── main.py                # CLI entry point
│   ├── tui.py                 # Terminal UI components
│   ├── history_parser.py      # Shell history parsing
│   ├── settings.py            # Configuration management
│   └── executor.py            # Command execution
├── scripts/                   # 🔧 Development & setup scripts
│   ├── setup.sh              # Automated dev setup (Unix/macOS)
│   ├── setup.bat             # Automated dev setup (Windows)
│   └── install-global.sh     # Global wrapper installation
├── docs/                      # 📚 Documentation
│   └── PROJECT_SUMMARY.md    # Detailed project overview
├── terminal-menu-standalone   # ⭐ Main deliverable (single file)
├── install.sh                 # ⭐ One-line installer
├── requirements.txt           # Python dependencies
├── setup.py                  # Package configuration
├── .gitignore                # Git ignore (excludes venv/, .venv/, etc.)
├── LICENSE                   # MIT License
└── README.md                 # This file

# Note: venv/ directories are created locally for development but excluded from git
```

## 🔧 Technical Details

### Built With
- **[Textual](https://textual.textualize.io/)** - Modern Python TUI framework
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal formatting
- **[Click](https://click.palletsprojects.com/)** - Command-line interface framework
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation and settings

### Requirements

#### Standalone Version (Recommended)
- **Python**: 3.6+ (usually pre-installed)
- **Dependencies**: None (uses standard library + curses)
- **Installation**: Just download and run!

#### Development Version
- **Python**: 3.8 or higher  
- **Dependencies**: pip packages (textual, rich, click, pydantic)
- **Installation**: Virtual environment setup

#### Both Versions
- **Platforms**: macOS, Linux
- **Terminal**: Color support recommended

### Performance

#### Execution Speed
- 🚀 **Fast mode**: ~10-50ms command overhead
- 🐌 **Normal mode**: ~100-500ms overhead (alias preprocessing)
- ⚡ **Direct shell**: ~0ms (for comparison)

#### App Performance  
- ⚡ **Sub-second startup** even with 2,000+ commands
- 🔍 **Real-time search** with fuzzy matching
- 💾 **Minimal memory footprint** with efficient data structures
- 🔄 **Lazy loading** for large history files

#### Performance Tips
```bash
# Recommended for daily use
terminal-menu --fast --no-confirm

# Create an alias for maximum speed
echo "alias tcm='terminal-menu --fast --no-confirm'" >> ~/.zshrc
```

📖 **See [docs/PERFORMANCE.md](docs/PERFORMANCE.md) for detailed performance analysis and optimization guide.**

## 🤝 Contributing

This project was built from a comprehensive Product Requirements Document (PRD) to solve real developer productivity challenges. 

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/javiplav/terminal-command-menu.git
cd terminal-command-menu

# Option A: Use automated setup script (recommended)
./scripts/setup.sh

# Option B: Manual setup
python3 -m venv venv           # Create virtual environment
source venv/bin/activate       # Activate it (Windows: venv\Scripts\activate)
pip install --upgrade pip      # Upgrade pip
pip install -e .              # Install in development mode

# Verify installation
terminal-menu --help

# Check the implementation against PRD
cat docs/PROJECT_SUMMARY.md
```

### Development Notes

- **Virtual Environment**: Always use a virtual environment for development. The project .gitignore excludes `venv/`, `.venv/`, and other common venv directory names.
- **Dependencies**: Keep `requirements.txt` updated when adding new dependencies.
- **Testing**: Run the standalone version to test changes without package installation.

### Feature Requests

See `docs/PROJECT_SUMMARY.md` for the complete feature roadmap and implementation status.

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built to solve the common developer pain point of managing complex terminal commands
- Inspired by tools like `fzf` and `telescope.nvim` but specifically designed for command history
- Special thanks to the Textual team for the amazing TUI framework

---

**Made with ❤️ for developers who live in the terminal**

*Transform your command-line workflow today!* 🚀
