# Contributing to ContentForge AI

Thank you for your interest in contributing to ContentForge AI! This document provides guidelines and instructions for contributing.

## 🤝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors

## 🐛 Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title** - Summarize the issue in the title
2. **Description** - Detailed description of the bug
3. **Steps to reproduce** - Clear steps to reproduce the issue
4. **Expected behavior** - What you expected to happen
5. **Actual behavior** - What actually happened
6. **Environment** - Python version, OS, etc.
7. **Logs/Screenshots** - If applicable

## 💡 Suggesting Features

Feature requests are welcome! Please include:

1. **Use case** - Why is this feature needed?
2. **Proposed solution** - How should it work?
3. **Alternatives** - Other approaches you've considered
4. **Additional context** - Any other relevant information

## 🔧 Pull Requests

### Before Starting

1. **Check existing issues** - Make sure someone isn't already working on it
2. **Create an issue** - Discuss your approach before implementing
3. **Fork the repository** - Create your own fork to work on

### Development Process

```bash
# 1. Fork and clone
git clone https://github.com/yourusername/contentforge-ai.git
cd contentforge-ai/multi-agent-content

# 2. Create a branch
git checkout -b feature/your-feature-name

# 3. Set up environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Make your changes
# - Write clear, commented code
# - Follow existing code style
# - Add tests if applicable

# 5. Test your changes
python main.py --sample

# 6. Commit your changes
git add .
git commit -m "Add: brief description of changes"

# 7. Push to your fork
git push origin feature/your-feature-name

# 8. Create a Pull Request
```

### PR Guidelines

- **Clear title** - Use prefixes: `Add:`, `Fix:`, `Update:`, `Refactor:`
- **Description** - Explain what and why, not just how
- **Link issues** - Reference related issues with `Closes #123`
- **Small PRs** - Keep changes focused and manageable
- **Tests** - Include tests for new features
- **Documentation** - Update README if needed

### Code Style

- Follow **PEP 8** for Python code
- Use **type hints** where applicable
- Write **docstrings** for functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

Example:
```python
def extract_key_points(content: str, min_points: int = 4) -> List[KeyPoint]:
    """
    Extract semantic key points from content.
    
    Args:
        content: Raw text content to analyze
        min_points: Minimum number of points to extract
        
    Returns:
        List of KeyPoint objects with concept, claim, and implication
    """
    # Implementation here
    pass
```

## 📁 Project Structure

When adding files, follow the existing structure:

```
agents/     - AI agent implementations
schemas/    - Pydantic models
pipeline/   - Orchestration logic
config/     - Configuration files
utils/      - Utility functions
ui/         - Streamlit interface
react-ui/   - React frontend
```

## 🧪 Testing

Currently, testing is manual. Future contributions for automated tests are welcome!

Manual testing checklist:
- [ ] CLI works with all input methods (file, URL, text)
- [ ] Streamlit UI displays correctly
- [ ] All agents produce valid output
- [ ] Pipeline completes without errors
- [ ] Output files are created correctly

## 📝 Documentation

When adding features, update:
- **README.md** - If user-facing
- **Docstrings** - For all new functions/classes
- **Comments** - For complex logic
- **CHANGELOG.md** - Document your changes

## 🎯 Priority Areas

We especially welcome contributions in:

- **Testing** - Unit tests, integration tests
- **Documentation** - Tutorials, examples, guides
- **Features** - New platforms, agents, capabilities
- **Bug fixes** - Any issues you discover
- **Performance** - Optimization improvements
- **UI/UX** - Interface improvements

## ❓ Questions?

- **Create an issue** - For general questions
- **Discussions** - For open-ended discussions
- **Email** - For private matters

## 🙏 Thank You!

Every contribution, no matter how small, is valuable and appreciated. Thank you for helping make ContentForge AI better!
