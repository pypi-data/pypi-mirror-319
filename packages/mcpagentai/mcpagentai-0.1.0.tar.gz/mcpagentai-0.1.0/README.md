
# MCPAgentAI :rocket:

[![PyPI](https://img.shields.io/pypi/v/mcpagentai.svg)](https://pypi.org/project/mcpagentai/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mcpagentai.svg)](https://pypi.org/project/mcpagentai/)
[![License](https://img.shields.io/pypi/l/mcpagentai.svg)](https://github.com/mcpagentai/mcpagentai/blob/main/LICENSE)

**MCPAgentAI** is a standardized **tool wrapping framework** for implementing and managing diverse tools in a unified way. It is designed to help developers quickly integrate and launch tool-based use cases.

### Key Features
- :wrench: **Standardized Wrapping**: Provides an abstraction layer for building tools using the MCP protocol.
- :rocket: **Flexible Use Cases**: Easily add or remove tools to fit your specific requirements.
- :sparkles: **Out-of-the-Box Tools**: Includes pre-built tools for common scenarios:
  - :clock2: Time utilities
  - :cloud: Weather information
  - :book: Dictionary lookups
  - :abacus: Calculator for mathematical expressions

### Tech Stack :hammer_and_wrench:
- **Python**: Core programming language
- **[MCP](https://pypi.org/project/mcp/) Framework**: Communication protocol
- **Docker**: Containerization

#### 🤔 What is MCP?

The **Model Context Protocol ([MCP](https://modelcontextprotocol.io/introduction))** is a cutting-edge standard for **context sharing and management** across AI models and systems. Think of it as the **language** AI agents use to interact seamlessly. 🧠✨

Here’s why **MCP** matters:

- 🧩 **Standardization**: MCP defines how context can be shared across models, enabling **interoperability**.
- ⚡ **Scalability**: It’s built to handle large-scale AI systems with high throughput.
- 🔒 **Security**: Robust authentication and fine-grained access control.
- 🌐 **Flexibility**: Works across diverse systems and AI architectures.

![Alt text](image.png)

---

## Installation :package:

### Install via PyPI
```bash
pip install mcpagentai
```

---

## Usage :computer:

### Run Locally
```bash
mcpagentai --local-timezone "America/New_York"
```

### Run in Docker
1. Build the Docker image:
   ```bash
   docker build -t mcpagentai .
   ```

2. Run the container:
   ```bash
   docker run -i --rm mcpagentai
   ```

---

## Tutorial: Selecting Specific Tools

You can configure MCPAgentAI to run only certain tools by modifying the agent configuration in your server or by updating the `server.py` file to only load desired agents. For example:
```python
from mcpagentai.tools.time_agent import TimeAgent
from mcpagentai.tools.weather_agent import WeatherAgent
from mcpagentai.core.multi_tool_agent import MultiToolAgent

multi_tool_agent = MultiToolAgent([
    TimeAgent(),
    WeatherAgent()
])
```
This setup will only enable **Time** and **Weather** tools.

---

## Integration Example: Claude Desktop Configuration

You can integrate MCPAgentAI with Claude Desktop using the following configuration:

`claude_desktop_config.json`
```json
{
    "mcpServers": {
        "mcpagentai": {
            "command": "docker",
            "args": ["run", "-i", "--rm", "mcpagentai"]
        }
    }
}
```

---

## Development :hammer_and_wrench:

1. Clone this repository:
   ```bash
   git clone https://github.com/mcpagentai/mcpagentai.git
   cd mcpagentai
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Build the package:
   ```bash
   python -m build
   ```

5. Run tests:
   ```bash
   pytest
   ```

---

## Contributing :handshake:

We welcome contributions! Please open an [issue](https://github.com/mcpagentai/mcpagentai/issues) or [pull request](https://github.com/mcpagentai/mcpagentai/pulls).

---

**License**: MIT  
Enjoy! :tada:
