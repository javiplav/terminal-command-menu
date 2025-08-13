#!/bin/bash
# Simple and reliable install script for Terminal Command Menu

set -e

INSTALL_DIR="$HOME/.local/bin"
SCRIPT_URL="https://raw.githubusercontent.com/javiplav/terminal-command-menu/main/terminal-menu-standalone"

echo "🚀 Installing Terminal Command Menu..."

# Create install directory
mkdir -p "$INSTALL_DIR"

# Download the script
echo "📥 Downloading standalone script..."
if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$SCRIPT_URL" -o "$INSTALL_DIR/terminal-menu"
elif command -v wget >/dev/null 2>&1; then
    wget -q "$SCRIPT_URL" -O "$INSTALL_DIR/terminal-menu"
else
    echo "❌ Error: Neither curl nor wget found."
    echo "Please install curl or wget, or download manually:"
    echo "  curl -fsSL $SCRIPT_URL -o ~/.local/bin/terminal-menu"
    exit 1
fi

# Make executable
chmod +x "$INSTALL_DIR/terminal-menu"

echo "✅ Installed to $INSTALL_DIR/terminal-menu"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  Adding ~/.local/bin to your PATH..."
    
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        echo "✅ Added to ~/.zshrc"
        echo "💡 Run: source ~/.zshrc (or restart your terminal)"
    elif [[ "$SHELL" == *"bash"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        echo "✅ Added to ~/.bashrc" 
        echo "💡 Run: source ~/.bashrc (or restart your terminal)"
    else
        echo "Please add this to your shell profile:"
        echo '  export PATH="$HOME/.local/bin:$PATH"'
    fi
else
    echo "✅ ~/.local/bin is already in your PATH"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  terminal-menu          # Launch interactive menu"
echo "  terminal-menu --stats  # Show statistics"
echo "  terminal-menu --help   # Show help"
echo ""
echo "No Python packages or virtual environments required!"
