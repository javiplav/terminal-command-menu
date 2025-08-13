# ⚡ Performance Guide

## Why Commands Execute Slower Through the App

You may notice that commands take longer to execute when run through Terminal Command Menu compared to typing them directly in your shell. This document explains why and how to optimize performance.

## 🐌 Performance Bottlenecks

### 1. **Alias Loading (BIGGEST IMPACT: 100-500ms)**
**What happens:** Every time you execute a command, the app runs:
```bash
zsh -i -c 'source ~/.zshrc 2>/dev/null; alias'
```

**Why it's slow:** 
- Spawns a new interactive shell process
- Sources your entire `.zshrc` configuration
- Loads all plugins, themes, and customizations
- Extracts and parses all aliases

**Impact:** This is the single biggest performance bottleneck.

### 2. **App Startup Overhead (100-300ms)**
- Loading Python modules (textual, rich, click, pydantic)
- Initializing the TUI framework
- Parsing shell history files

### 3. **History Processing (50-200ms)**
- Reading and parsing thousands of history entries
- Categorizing commands by type
- Computing frequency statistics

### 4. **Additional Processing (10-50ms)**
- Safety checks for dangerous commands
- Command preparation and validation
- Statistics recording

## ⚡ Performance Solutions

### **Option 1: Fast Mode (RECOMMENDED)**
Use the `--fast` flag to bypass alias preprocessing:

```bash
terminal-menu --fast
```

**Benefits:**
- ✅ **10-50ms overhead** (vs 100-500ms normal)
- ✅ **Still supports aliases** (shell handles them directly)
- ✅ **Maximum performance** while maintaining functionality

**How it works:**
```bash
# Normal mode (slower)
zsh -i -c 'source ~/.zshrc; alias'  # Load aliases
kubectl get pods                    # Expand k→kubectl in Python

# Fast mode (faster)  
zsh -i -c 'k get pods'              # Let shell handle aliases directly
```

### **Option 2: Skip Confirmation**
Combine with `--no-confirm` for even faster execution:

```bash
terminal-menu --fast --no-confirm
```

**Benefits:**
- ✅ **No confirmation dialog**
- ✅ **Immediate execution**
- ✅ **Fastest possible workflow**

### **Option 3: Direct Execution (FOR REFERENCE)**
For comparison, direct shell execution:
```bash
k get pods  # ~0-10ms (immediate)
```

## 📊 Performance Comparison

| Execution Method | Startup | Alias Processing | Total Overhead |
|------------------|---------|------------------|----------------|
| **Direct Shell** | 0ms | 0ms | **~0ms** |
| **App --fast** | 100-300ms* | 0ms | **~10-50ms per command** |
| **App Normal** | 100-300ms* | 100-500ms | **~100-500ms per command** |

*Startup overhead only applies once per session

## 🎯 Performance Recommendations

### **For Maximum Speed:**
```bash
# Create an alias for fast mode
echo "alias tcm='terminal-menu --fast --no-confirm'" >> ~/.zshrc
source ~/.zshrc

# Usage
tcm  # Launch in fast mode
```

### **For Heavy Users:**
If you use Terminal Command Menu frequently:
1. Use `--fast` mode by default
2. Create shell aliases for common flags
3. Consider using the app for command discovery, direct execution for routine commands

### **For Complex Alias Users:**
If you have complex aliases that don't work in fast mode:
1. Use normal mode when needed
2. Test your aliases in fast mode first
3. Report any alias compatibility issues

## 🔧 Technical Details

### **Alias Loading Process:**
```python
# Normal mode - our preprocessing
def _load_shell_aliases(self):
    result = subprocess.run(['zsh', '-i', '-c', 'alias'], ...)
    return parse_aliases(result.stdout)

# Fast mode - shell handles it
def execute_fast_mode(command):
    subprocess.run(f'zsh -i -c "{command}"', shell=True)
```

### **Why This Works:**
- **Normal mode:** We load aliases into Python, then expand them
- **Fast mode:** We let the shell expand aliases naturally
- **Result:** Fast mode is much faster while maintaining full alias support

## 🚀 Future Optimizations

Planned improvements:
- [ ] **Alias caching** - Cache aliases between sessions
- [ ] **Lazy history loading** - Load history in background
- [ ] **Command prediction** - Pre-load likely next commands
- [ ] **Shell integration** - Direct shell hooks for zero overhead

## 📈 Measuring Performance

To measure performance in your environment:

```bash
# Test normal mode
time terminal-menu --stats

# Test fast mode  
time terminal-menu --fast --stats

# Compare with direct execution
time kubectl get pods
```

## 💡 Best Practices

1. **Use fast mode by default** unless you have issues
2. **Combine with --no-confirm** for maximum speed
3. **Create aliases** for your preferred flags
4. **Test your setup** to find the best configuration
5. **Report performance issues** to help improve the app

---

**Remember:** The app is designed for **command discovery and reuse**, not to replace direct shell execution for every command. Use it when you need to find and reuse commands from your history!
