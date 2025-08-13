#!/bin/bash
# Quick install script for Terminal Command Menu
# Downloads and sets up the standalone version

set -e

INSTALL_DIR="$HOME/.local/bin"
REPO_URL="https://raw.githubusercontent.com/javiplav/terminal-command-menu/main/terminal-menu-standalone"

echo "🚀 Installing Terminal Command Menu (standalone version)..."

# Create install directory
mkdir -p "$INSTALL_DIR"

# Download the standalone script
echo "📥 Downloading standalone script..."
if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$REPO_URL" -o "$INSTALL_DIR/terminal-menu"
elif command -v wget >/dev/null 2>&1; then
    wget -q "$REPO_URL" -O "$INSTALL_DIR/terminal-menu"
else
    echo "❌ Error: Neither curl nor wget found. Please install one of them."
    exit 1
fi

# Make executable
chmod +x "$INSTALL_DIR/terminal-menu"

# Create aliases
ln -sf "$INSTALL_DIR/terminal-menu" "$INSTALL_DIR/cmd-menu" 2>/dev/null || true
ln -sf "$INSTALL_DIR/terminal-menu" "$INSTALL_DIR/tcm" 2>/dev/null || true

echo "✅ Downloaded and installed to $INSTALL_DIR/terminal-menu"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  Add ~/.local/bin to your PATH:"
    echo ""
    echo "For zsh (add to ~/.zshrc):"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "For bash (add to ~/.bashrc):"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then restart your shell or run: source ~/.zshrc"
else
    echo "✅ ~/.local/bin is already in your PATH"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  terminal-menu       # Launch interactive menu"
echo "  terminal-menu --stats  # Show statistics"
echo "  cmd-menu           # Alternative command"
echo "  tcm                # Short alias"
echo ""
echo "No Python packages or virtual environments required!"
echo "The script uses only Python standard library + curses."
