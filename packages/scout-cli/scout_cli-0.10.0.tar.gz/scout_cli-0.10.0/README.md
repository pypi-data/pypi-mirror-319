# scout-cli

A modern, beautiful alternative to the traditional `ls` and `cd` commands, with smart AI-powered directory prediction.

## Features

- 🎨 Beautiful, colorful output
- 📊 Modern table-based layout
- 🔄 Multiple sorting options
- 👁 Show/hide hidden files
- 📌 Directory bookmarks
- 🧠 Smart AI-powered navigation
- 🔍 Fuzzy directory matching
- 💻 Cross-platform support

## Installation

### Option 1: Using pip (recommended)
```bash
# Install globally on your system
pip install scout-cli

# Or if you don't have root access
pip install --user scout-cli
```

### Option 2: From source
```bash
# Clone the repository
git clone <repository-url>
cd scout-cli

# Install
make install
```

## Usage

### List Files (replaces `ls`)
```bash
# Basic usage
scout

# Show all files (including hidden)
scout -a

# Sort by different criteria
scout --sort size      # Sort by file size
scout --sort modified  # Sort by modification time
scout --sort name      # Sort by name (default)

# List specific directory
scout /path/to/directory
```

### Smart Directory Navigation (replaces `cd`)
```bash
# Basic usage - just type part of the directory name!
scout jump projects    # Will find and suggest matching directories
scout jump docs       # Will match Documents, docs, etc.
scout jump down      # Will match Downloads, etc.

# No need to type the exact path - scout will find it for you!
scout jump src    # Matches any 'src' directory in current or parent dirs
scout jump web    # Matches 'website', 'webproject', etc.

# Traditional navigation still works
scout jump ../parent/dir
scout jump ~/Documents

# Go back to previous directory
scout jump -

# Create directory if it doesn't exist
scout jump --create new_directory

# Bookmark management
scout jump --save --name work  # Save current directory as 'work'
scout jump --save              # Save with directory name
scout jump --bookmarks        # List all bookmarks
scout jump work              # Jump to bookmarked 'work' directory
```

### Smart Directory Matching

Scout makes directory navigation easier with:
- 🧠 AI-powered suggestions: Learns from your navigation patterns
- 🕒 Time-aware predictions: Suggests directories based on your daily routine
- 📊 Usage-based ranking: Frequently used directories are prioritized
- 🔍 Fuzzy matching: Type approximate names
- 📈 Smart ranking: Best matches shown first
- 🎯 Common directory search: Automatically checks Documents, Downloads, etc.
- 💡 Interactive selection: Choose from matching directories
- ⭐️ Favorites indication: Frequently used directories are marked with a star
- ↩️ Easy backtracking: Use `scout jump -` to go back

### AI Features

Scout includes a lightweight machine learning system that:
- 📚 Learns from your navigation patterns
- 🕒 Considers time of day and day of week
- 🎯 Adapts to your common destinations
- 💾 Stores data locally for privacy
- 🚀 Uses minimal resources
- 🔄 Continuously improves as you use it

The AI system helps by:
1. Ranking directories based on your usage patterns
2. Prioritizing directories you use at specific times
3. Marking frequently used directories with a star (★)
4. Adapting suggestions to your daily routine

## Tips for VPS Usage

1. **Global Installation**: If you have root access, install globally:
   ```bash
   sudo pip install scout-cli
   ```

2. **User Installation**: If you don't have root access:
   ```bash
   pip install --user scout-cli
   ```
   Make sure `~/.local/bin` is in your PATH:
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Alias Setup** (optional): Add to your `.bashrc` or `.zshrc`:
   ```bash
   alias ls='scout'
   alias cd='scout jump'
   ```

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   make install
   ```

3. Run tests:
   ```bash
   make test
   ```

4. Build the package:
   ```bash
   make build
   ```

## License

MIT 