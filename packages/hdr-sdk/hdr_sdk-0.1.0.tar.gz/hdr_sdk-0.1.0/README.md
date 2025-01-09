# HDR SDK

[![PyPI version](https://badge.fury.io/py/hdr-sdk.svg)](https://badge.fury.io/py/hdr-sdk)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Coverage](https://codecov.io/gh/basin-dev/hdr-sdk/branch/main/graph/badge.svg)](https://codecov.io/gh/basin-dev/hdr-sdk)

A powerful Python SDK for programmatic computer control and automation through HDR's services. This SDK enables seamless interaction with remote computers, providing precise control over mouse movements, keyboard inputs, and screen operations.

## 🚀 Key Features

- **Mouse Control**: Precise cursor movement, clicks, drags, and position tracking
- **Keyboard Automation**: Key press simulation and text input
- **Screen Operations**: High-quality screenshot capture
- **Real-time Communication**: WebSocket-based connection with automatic management
- **Built-in Logging**: Comprehensive activity tracking and debugging support
- **Type Safety**: Full type hints for enhanced IDE support and code reliability

## 📋 Requirements

- Python 3.10+
- Active HDR API key
- Stable internet connection

## ⚡ Quick Install

```bash
pip install hdr-sdk
```

## 🔧 Configuration

Configure the SDK using either environment variables or programmatic initialization:

### Environment Variables

```bash
export HDR_API_KEY=your_api_key
```

### Programmatic Configuration

```python
from hdr_sdk.config import HDRConfig

config = HDRConfig(
    api_key="your_api_key",
    base_url="wss://api.hdr.is/compute/ws"  # Optional, defaults to this value
)
```

## 💻 Basic Usage

```python
import asyncio
import os
from hdr_sdk import Computer

async def main():
    # Initialize the computer
    computer = Computer({
        "api_key": os.getenv("HDR_API_KEY"),
        "base_url": "wss://api.hdr.is/compute/ephemeral"  # Optional
    })

    # Connect to the computer
    await computer.connect()

    try:
        # Execute natural language commands
        await computer.do("Tell me the weather in Tokyo")

        # Or use specific commands
        await computer.do("Take a screenshot of the current window")

    finally:
        # Close the connection
        await computer.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🎯 Example Use Cases

### General Computer Control

```python
# Weather information
await computer.do("Tell me the weather in Tokyo")

# System commands
await computer.do("Tell me the weather in Tokyo using only bash")

# Web automation
await computer.do("Go to https://example.com and click the first link")
```

### Web Development

```python
# Create a web server with specific styling
await computer.do(
    "Create a python web server that serves a simple html page with " +
    "the text 'Hello World' in a modern style"
)

# Interact with web elements
await computer.do("Fill out the login form and submit it")
```

### Custom Actions

```python
# Take screenshots
await computer.screenshot()

# Mouse control
await computer.move_mouse(x=100, y=200)
await computer.click()

# Keyboard input
await computer.type_text("Hello, World!")
```

## 🛠️ Advanced Features

### Mouse Operations

```python
# Move mouse to specific coordinates
await computer.move_mouse(x=100, y=200)

# Perform click actions
await computer.click()
await computer.right_click()
await computer.double_click()

# Click and drag
await computer.click_and_drag(start_x=100, start_y=200, end_x=300, end_y=400)
```

### Keyboard Operations

```python
# Type text
await computer.type_text("Hello, World!")

# Press specific keys
await computer.press_key("enter")
await computer.press_keys(["ctrl", "c"])
```

## 📝 Logging

The SDK automatically maintains detailed logs in the `computer_logs/` directory:

- Command execution logs
- Screenshots
- Session information in JSONL format

Each session's logs are stored in a timestamped directory for easy reference.

## ⚠️ Error Handling

The SDK provides specialized exception classes for robust error handling:

```python
from hdr_sdk.exceptions import ComputerError, ComputerToolError, HDRConfigError

try:
    await computer.execute_command(...)
except ComputerError as e:
    print(f"General computer error: {e}")
except ComputerToolError as e:
    print(f"Tool-specific error: {e}")
except HDRConfigError as e:
    print(f"Configuration error: {e}")
```

## 🔒 WebSocket Connection Details

The SDK maintains a secure WebSocket connection with:

- Automatic SSL/WSS encryption
- 20-second ping/pong keep-alive mechanism
- Graceful connection cleanup
- API key-based authentication

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code style and standards
- Pull request process
- Development setup
- Testing requirements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/basin-dev/hdr-sdk/issues)
- **Email**: support@hdr.is
- **Discord**: [Join our community](https://discord.gg/mBN8xEsTuU)

## 🏗️ Built With

- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Websockets](https://websockets.readthedocs.io/) - WebSocket client
- [Python 3.10+](https://www.python.org/) - Modern Python features
