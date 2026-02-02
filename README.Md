# Agent Tutorial

A learning project for building an AI coding agent with streaming capabilities and a terminal user interface.

## Overview

This project demonstrates how to build an AI-powered coding agent that interacts with users through a terminal interface. It features:

- **Streaming responses** for real-time AI interaction
- **Terminal User Interface (TUI)** built with Rich
- **Asynchronous architecture** using Python's asyncio
- **Context management** for maintaining conversation history
- **Event-driven design** for extensible agent behavior

## Installation

### Prerequisites

- Python 3.12 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone git@github.com:dymaaaj7/study-coding-agent.git
cd study-coding-agent
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package with development dependencies:
```bash
pip install -e .[dev,test]
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the agent with a prompt:

```bash
python main.py "Explain how async/await works in Python"
```

The agent will respond with streaming output in your terminal.

## Project Structure

```
agent_tutorial/
├── agent/
│   ├── __init__.py
│   ├── agent.py       # Main Agent class with event streaming
│   └── events.py       # Event definitions and types
├── client/
│   ├── __init__.py
│   ├── client.py      # LLM client for API communication
│   └── response.py    # Response parsing and streaming
├── context/
│   └── manager.py     # Conversation context management
├── prompts/
│   └── system.py      # System prompt configuration
├── ui/
│   ├── __init__.py
│   └── tui.py         # Terminal user interface
├── utils/
│   └── text.py        # Text processing utilities
├── main.py            # CLI entry point
├── pyproject.toml     # Project configuration
└── pytest.ini         # Test configuration
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
ruff check --fix .
```

### Type Checking

```bash
mypy .
```

### Pre-commit Hooks

The project uses pre-commit hooks to maintain code quality. They are automatically installed during setup. To run them manually:

```bash
pre-commit run --all-files
```

## Features

- **Streaming Communication**: Real-time streaming of AI responses
- **Context Awareness**: Maintains conversation history across interactions
- **Event System**: Extensible event-driven architecture
- **Rich TUI**: Beautiful terminal interface with formatted output
- **Type Safety**: Fully type-annotated codebase
- **Async/Await**: Modern Python async patterns throughout

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.Md](./CONTRIBUTING.Md) for detailed guidelines.

## License

See [LICENSE.txt](./LICENSE.txt).