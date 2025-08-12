# Installation Guide

## Quick Setup

1. **Install the package:**
   ```bash
   pip install -e .
   ```

2. **Run the application:**
   ```bash
   history-menu
   # or
   cmdmenu
   ```

## Manual Installation

If you prefer to run without installing:

```bash
# Make scripts executable
chmod +x history-menu cmdmenu

# Add to your PATH or create aliases
export PATH="$PATH:/path/to/terminal-tool"

# Or create shell aliases
alias history-menu='/path/to/terminal-tool/history-menu'
alias cmdmenu='/path/to/terminal-tool/cmdmenu'
```

## Shell Integration

For the best experience, add an alias to your shell profile:

### Zsh (.zshrc)
```bash
alias hm='history-menu'
alias cm='cmdmenu'
```

### Bash (.bashrc or .bash_profile)
```bash
alias hm='history-menu'
alias cm='cmdmenu'
```

### Fish (config.fish)
```fish
alias hm='history-menu'
alias cm='cmdmenu'
```

## Usage Examples

```bash
# Basic usage
history-menu

# Show statistics only
history-menu --stats

# Skip confirmation prompts
history-menu --no-confirm

# Limit number of commands displayed
history-menu --max-commands 50

# Force specific shell type
history-menu --shell zsh

# Show configuration paths
history-menu --config
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
history-menu --config
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
