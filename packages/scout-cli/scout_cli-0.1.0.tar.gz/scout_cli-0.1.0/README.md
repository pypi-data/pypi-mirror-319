# scout-cli

A modern, beautiful alternative to the traditional `ls` command.

## Features

- 🎨 Beautiful, colorful output
- 📊 Modern table-based layout
- 🔄 Multiple sorting options
- 👁 Show/hide hidden files
- 💻 Cross-platform support

## Installation

```bash
pip install scout-cli
```

## Usage

Basic usage:
```bash
scout
```

Show all files (including hidden):
```bash
scout -a
```

Sort by different criteria:
```bash
scout --sort size    # Sort by file size
scout --sort modified  # Sort by modification time
scout --sort name    # Sort by name (default)
```

Specify a different directory:
```bash
scout /path/to/directory
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