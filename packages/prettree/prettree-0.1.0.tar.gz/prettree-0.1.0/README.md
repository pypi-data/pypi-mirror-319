# PreTree 🌳

[![PyPI version](https://badge.fury.io/py/prettree.svg)](https://badge.fury.io/py/prettree)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A cross-platform Python package for visualizing directory structures in a tree-like format.

## Features

- 🖥️ Cross-platform compatibility
- 🌲 Tree-like visualization
- 📊 Configurable depth
- 🔍 Advanced filtering options
- ⚡ Both CLI and library usage
- 📂 Sorted output (directories first)
- 📏 Size-based filtering
- 🎯 Pattern matching

## Installation

```bash
pip install prettree
```

## Usage

### Basic Usage
```bash
# List current directory
prettree

# List specific directory
prettree /path/to/directory
```

### Advanced Options
```bash
# Show hidden files
prettree -a

# Limit depth to 2 levels
prettree -d 2

# Show only files (no directories)
prettree -f

# Show only directories
prettree -D

# Exclude empty directories
prettree -e

# Show only PDF files
prettree -p "*.pdf"

# Exclude configuration files
prettree -x "*.config"

# Show files larger than 1MB
prettree --min-size 1048576

# Show files between 100KB and 1MB
prettree --min-size 102400 --max-size 1048576
```

### As a Python Library
```python
from prettytree import list_directory

# Basic usage
for item in list_directory():
    print(item)

# Advanced usage
for item in list_directory(
    "/path/to/directory",
    max_depth=2,
    show_hidden=True,
    only_files=True,
    file_pattern="*.pdf",
    min_size=1048576
):
    print(item)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.   
