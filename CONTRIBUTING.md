# Contributing to Unified Memory System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/luoboask/evo-agents.git
cd evo-agents

# Create your agent workspace
mkdir -p ~/.openclaw/workspace-dev
ln -s $(pwd) ~/.openclaw/workspace-dev/unified-memory

# Test your changes
python3 scripts/health_check.py --agent dev
```

## How to Contribute

1. **Fork the repository** on GitHub
2. **Create a branch** for your feature (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and test them
4. **Commit** with clear messages (`git commit -m 'feat: add amazing feature'`)
5. **Push** to your fork (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

## Commit Message Convention

We follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Code Style

- Python: PEP 8
- Shell: POSIX compliant
- Documentation: Clear and concise

## Testing

Before submitting:

```bash
python3 scripts/health_check.py --agent test
python3 scripts/test_features.py --agent test
```

## Questions?

Open an issue or join the discussion.
