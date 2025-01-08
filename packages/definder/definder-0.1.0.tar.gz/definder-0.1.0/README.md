# depfinder 🔍

A fast Python dependency analyzer that automatically discovers and extracts third-party imports from your Python projects. It uses parallel processing to quickly scan your codebase and identify all external dependencies.

## Features ✨

- Fast parallel file processing using `ProcessPoolExecutor`
- Intelligent package name mapping (e.g., `PIL` → `pillow`, `cv2` → `opencv-python`)
- Excludes standard library imports automatically
- Generates `requirements.txt` file
- Support for both single files and directories
- Smart handling of local module imports

## Installation 📦

```bash
pip install depfinder
```

## Usage 🚀

Basic usage to analyze a directory and generate requirements.txt:
```bash
python -m definder src/
```

Analyze multiple paths:
```bash
python -m definder src/ tests/ scripts/
```

Options:
```bash
python -m definder src/ --no-save     # Don't generate requirements file
python -m definder src/ --workers 4   # Specify number of parallel workers
```

## How it Works 🛠️

1. Recursively scans all Python files in specified directories
2. Uses AST parsing to safely extract imports
3. Filters out standard library and local module imports
4. Maps import names to correct PyPI package names
5. Generates a clean requirements file

## Output 📝

The tool will:
1. Show all scanned files
2. List discovered third-party dependencies
3. Generate a `requirements.txt` file (or `requirements-definder.txt` if the former exists)

## License 📄

[License information here]

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.