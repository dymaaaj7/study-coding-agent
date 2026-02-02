# Contributing to Agent Tutorial

Thank you for your interest in contributing to this project! This guide will help you get started with setting up your development environment and understanding the contribution workflow.

## Initial Setup

These steps should be executed when cloning the repository for the first time.

### Cloning the Repository

First, ensure you have SSH keys set up for GitHub. If not, follow [GitHub's SSH key guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

Create a directory and clone the repository:

```bash
mkdir -p ~/source/study-coding-agent
cd ~/source/study-coding-agent
git clone git@github.com:dymaaaj7/study-coding-agent.git
cd study-coding-agent
```

### Configure Git

If you haven't already configured git globally, set your identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Or configure locally for this repository only:

```bash
git config --local user.name "Your Name"
git config --local user.email "your.email@example.com"
```

### Creating the Virtual Environment

Ensure you have Python virtual environment support installed:

```bash
sudo apt update
sudo apt install python3-virtualenv
```

Create and activate the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

Install the project in development mode with all dependencies:

```bash
pip install -e .[dev,test]
```

### Set Up Pre-commit Hooks

Install pre-commit hooks to automatically run code quality checks:

```bash
pre-commit install
pre-commit install-hooks
```

### Environment Variables

Create a `.env` file in the project root with your OpenAI API key:

```bash
OPENAI_API_KEY=your-api-key-here
```

Make sure to add `.env` to `.gitignore` if it's not already there (it should be by default).

## Development Workflow

### Keeping Your Branch Updated

Before starting work, ensure your local repository is up to date:

```bash
git pull --all
git fetch --all
```

If `pyproject.toml` has changed, reinstall dependencies:

```bash
pip install -e .[dev,test]
```

### Running Tests

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=. --cov-report=html
```

Run specific test files:

```bash
pytest tests/test_agent.py
```

### Code Quality

#### Formatting

Format code with Black:

```bash
black .
```

#### Linting

Check and fix issues with Ruff:

```bash
ruff check --fix .
```

#### Type Checking

Run mypy for type checking:

```bash
mypy .
```

### Pre-commit Hooks

Pre-commit hooks run automatically on `git commit`. To run them manually:

```bash
pre-commit run --all-files
```

If hooks fail, fix the reported issues and commit again. To bypass hooks (not recommended):

```bash
git commit --no-verify -m "Your commit message"
```

## Project Structure

Understanding the project architecture:

```
agent_tutorial/
├── agent/
│   ├── agent.py       # Core Agent class with event streaming
│   ├── events.py      # Event types and definitions
│   └── __init__.py
├── client/
│   ├── client.py      # OpenAI API client wrapper
│   ├── response.py    # Stream response parsing
│   └── __init__.py
├── context/
│   ├── manager.py     # Conversation context management
│   └── __init__.py
├── prompts/
│   ├── system.py      # System prompt templates
│   └── __init__.py
├── ui/
│   ├── tui.py         # Terminal interface (Rich-based)
│   └── __init__.py
├── utils/
│   ├── text.py        # Text processing utilities
│   └── __init__.py
├── main.py            # CLI entry point using Click
├── pyproject.toml     # Project metadata and tool config
├── pytest.ini         # pytest configuration
└── .gitignore         # Git ignore patterns
```

### Key Components

- **Agent**: Main orchestrator that manages the conversation loop and emits events
- **Client**: Handles communication with the OpenAI API
- **Context Manager**: Maintains conversation history and message formatting
- **TUI**: Provides a rich terminal interface for displaying agent responses
- **Event System**: Publishes events for text deltas, completions, and errors

## Coding Standards

This project follows:

- **PEP 8**: Python style guide
- **Type Hints**: All functions should have type annotations
- **Async/Await**: Use async patterns for I/O operations
- **Event-Driven**: Emit events for state changes and responses
- **Docstrings**: Follow Google style for docstrings

### Code Formatting

- Line length: 80 characters
- Use Black for automatic formatting
- Use Ruff for linting and import sorting
- Use mypy for type checking

## Creating a Pull Request

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards

3. Test thoroughly:
   ```bash
   pytest
   ruff check .
   mypy .
   black --check .
   ```

4. Commit your changes with a descriptive message:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. Push to your fork or branch:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a pull request on GitHub

## Troubleshooting

### Pre-commit Hooks Fail

If pre-commit hooks fail:
1. Read the error message carefully
2. Run the specific tool manually to see full output
3. Fix the reported issues
4. Run `pre-commit run --all-files` to verify fixes

### Import Errors

If you encounter import errors:
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -e .[dev,test]`
3. Check you're in the project root directory

### API Key Issues

If the agent can't connect to OpenAI:
1. Verify your `.env` file exists and contains `OPENAI_API_KEY`
2. Ensure the API key is valid and has credits
3. Check your internet connection

## Resources

- [Python Documentation](https://docs.python.org/3/)
- [Rich Library](https://rich.readthedocs.io/)
- [Click Documentation](https://click.palletsprojects.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)

## Questions?

If you have questions about contributing, please open an issue on GitHub with the "question" label.