# Viyu XMPP Server

## Overview
Viyu XMPP Server is a Python-based server built on `slixmpp` to handle custom XMPP events. It provides an easy way to manage GET and POST stanzas with customizable handlers for real-time communication applications.

## Features
- Handles XMPP sessions and events.
- Provides custom GET and POST handlers.
- Secure connection with SSL support (with optional certificate verification).
- Easy-to-extend for additional XMPP stanzas.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/viyu-package.git
   cd viyu-package
   ```

2. Install the package:
   ```bash
   pip install .
   ```

## Usage

### Running the XMPP Server
Create an instance of `ViyuXmppServer` with your JID and password, and start the server:

```python
from viyu_xmpp.server import ViyuXmppServer

xmpp = ViyuXmppServer("user@domain", "password")
xmpp.connect()
xmpp.process()
```

### Adding Custom Handlers
Define and register custom event handlers for GET and POST stanzas:

```python
# Add a GET handler
xmpp.add_get("event_name", lambda: {"status": "success", "data": "Hello, GET!"})

# Add a POST handler
xmpp.add_post("event_name", lambda: {"status": "success", "message": "Hello, POST!"})
```

### Sample Configuration
You can extend the server's functionality by modifying the event handlers and plugins as required.

## Dependencies
- Python >= 3.6
- `slixmpp`
- `cryptography`

## Contributing
Contributions are welcome! Please submit a pull request or create an issue for any bugs or feature requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or support, contact TRIYOM SOFTWARES PVT LTD at [admin@triyom.in](mailto:admin@triyom.in).

## Project Links
- **Source Code**: [GitHub Repository](https://github.com/yourusername/viyu-package)
- **Bug Tracker**: [Issues](https://github.com/yourusername/viyu-package/issues)
