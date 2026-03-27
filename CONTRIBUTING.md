# Contributing to evo-agents

First off, thank you for considering contributing to evo-agents! It's people like you that make evo-agents such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed and what behavior you expected**
* **Include screenshots if possible**
* **Include system information** (OS, OpenClaw version, Python version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Explain why this enhancement would be useful**
* **List some examples of how this enhancement would be used**

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include comments in your code where necessary
* Update documentation as needed
* Test your changes thoroughly

## Development Setup

### Prerequisites

* Python 3.10+
* OpenClaw installed
* Git

### Setting Up

```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/evo-agents.git
cd evo-agents

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if any)
pip3 install -r requirements.txt  # When we have requirements
```

### Testing

```bash
# Run tests (when we have tests)
python3 -m pytest tests/

# Test the scripts manually
./scripts/core/setup-multi-agent.sh test-agent
./scripts/core/add-agent.sh demo "Demo Agent" 🤖
```

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Styleguide

* Follow PEP 8
* Use 4 spaces for indentation
* Use double quotes for strings
* Keep lines under 100 characters

### Documentation Styleguide

* Use Markdown
* Reference methods and classes in backticks: \`method_name()\`
* Use code blocks for examples

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Documentation only changes
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed

## Thank You!

Your contributions to open source, large or small, make projects like this possible. Thank you for taking the time to contribute.
