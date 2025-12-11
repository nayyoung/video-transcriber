# Contributing to Video Transcriber

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/video-transcriber.git
   cd video-transcriber
   ```

2. **Create a virtual environment**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install dev dependencies
   ```

## Project Structure

```
video-transcriber/
├── src/video_transcriber/    # Main package
│   ├── __init__.py           # Package exports
│   ├── __main__.py           # CLI entry point
│   ├── config.py             # Configuration management
│   ├── downloader.py         # Video downloading
│   ├── audio.py              # Audio extraction
│   ├── transcriber.py        # Transcription
│   ├── processor.py          # Main orchestration
│   ├── utils.py              # Utility functions
│   └── exceptions.py         # Custom exceptions
├── tests/                    # Test suite (to be added)
├── run.py                    # Convenience entry point
├── transcribe.py             # Backward compatibility (deprecated)
└── pyproject.toml            # Project configuration
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Write descriptive docstrings for modules, classes, and functions
- Keep functions focused and single-purpose
- Use meaningful variable names

### Code Formatting

We recommend using `black` for code formatting:

```bash
black src/
```

### Linting

Use `flake8` to check for code issues:

```bash
flake8 src/
```

### Type Checking

Use `mypy` for static type checking:

```bash
mypy src/
```

## Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise commit messages
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests (when available)
   pytest
   
   # Test the CLI
   python -m video_transcriber --help
   python run.py --urls test_urls.txt --debug
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add feature: description"
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Wait for code review

## Adding New Features

When adding new features:

1. **Consider the module structure** - Does this fit into an existing module or need a new one?
2. **Add proper error handling** - Use custom exceptions from `exceptions.py`
3. **Add logging** - Use the `logging` module for informative messages
4. **Update configuration** - Add new settings to `config.py` if needed
5. **Update CLI** - Add command-line arguments in `__main__.py` if applicable
6. **Update documentation** - Update README.md and docstrings

## Bug Reports

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs. actual behavior
- Error messages and logs (use `--debug` flag)

## Feature Requests

Feature requests are welcome! Please:

- Check if the feature already exists
- Describe the use case
- Explain why it would be useful to others
- Consider if it fits the project scope

## Questions?

- Open an issue with the "question" label
- Check existing issues and documentation first

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow

Thank you for contributing!
