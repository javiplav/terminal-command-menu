# Installation Guide

## Quick Setup

1. **Create and activate a virtual environment (RECOMMENDED):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install the package:**
   ```bash
   pip install -e .
   ```

3. **Run the application:**
   ```bash
   terminal-menu
   # or
   cmd-menu
   # or
   tcm
   ```

## Manual Installation

If you prefer to run without installing:

```bash
# Make scripts executable
chmod +x terminal-menu cmd-menu

# Add to your PATH or create aliases
export PATH="$PATH:/path/to/terminal-tool"

# Or create shell aliases
alias terminal-menu='/path/to/terminal-tool/terminal-menu'
alias cmd-menu='/path/to/terminal-tool/cmd-menu'
alias tcm='/path/to/terminal-tool/terminal-menu'
```

## Shell Integration

For the best experience, add an alias to your shell profile:

### Zsh (.zshrc)
```bash
alias tm='terminal-menu'
alias cm='cmd-menu'
alias tcm='terminal-menu'
```

### Bash (.bashrc or .bash_profile)
```bash
alias tm='terminal-menu'
alias cm='cmd-menu'
alias tcm='terminal-menu'
```

### Fish (config.fish)
```fish
alias tm='terminal-menu'
alias cm='cmd-menu'
alias tcm='terminal-menu'
```

## Usage Examples

```bash
# Basic usage
terminal-menu

# Show statistics only
terminal-menu --stats

# Skip confirmation prompts
terminal-menu --no-confirm

# Limit number of commands displayed
terminal-menu --max-commands 50

# Force specific shell type
terminal-menu --shell zsh

# Show configuration paths
terminal-menu --config
```

## Keyboard Shortcuts

- **Arrow Keys / j/k**: Navigate command list
- **Enter**: Execute selected command
- **/** or **Ctrl+F**: Focus search box
- **Escape**: Clear search or quit
- **Ctrl+R**: Refresh history
- **Ctrl+S**: Settings (not yet implemented)
- **Ctrl+C / Ctrl+Q**: Quit

## Configuration

The application stores its configuration in:
- **macOS/Linux**: `~/.config/terminal-command-menu/`

You can view the current configuration paths with:
```bash
terminal-menu --config
```

## Troubleshooting

### No commands shown
- Make sure you have command history in your shell
- Check that the correct shell type is detected with `--stats`
- Try forcing shell type with `--shell zsh/bash/fish`

### Permission errors
- Ensure the scripts are executable: `chmod +x history-menu cmdmenu`
- Check that your shell history files are readable

### Python version
- Requires Python 3.8 or higher
- Check with: `python3 --version`

### Virtual environment issues
- Always use a virtual environment to avoid conflicts
- If commands not found after installation, ensure venv is activated
- Deactivate with: `deactivate`, reactivate with: `source venv/bin/activate`
