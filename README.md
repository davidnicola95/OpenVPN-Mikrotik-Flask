# OpenVPN MikroTik Flask Web Interface

## Overview
This project integrates **OpenVPN** on MikroTik routers with a **Debian-based VPN server** and provides a user-friendly **Flask web interface** for managing VPN profiles. The solution is designed to simplify VPN management tasks such as creating users, exporting certificates, and generating `.ovpn` configuration files.

## Features
- **MikroTik OpenVPN Server Integration**: Leverages MikroTik RouterOS to serve as the OpenVPN server.
- **Debian VPN Management**: Hosts the Flask application and handles certificate generation and file export.
- **Flask-Based Web Interface**: Simplifies user interaction by providing an accessible web platform for creating and managing VPN profiles.
- **Certificate Management**: Automatically generates and exports the necessary certificates and keys for each VPN client.
- **OVPN File Generation**: Creates fully configured `.ovpn` files for easy client-side setup.

## Requirements
### Hardware
- A MikroTik router with OpenVPN support.
- A Debian-based server or VM to host the Flask application.

### Software
- Python 3.x with the following libraries:
  - `Flask`
  - `paramiko`
  - `librouteros`
- MikroTik RouterOS properly configured to support OpenVPN.
- OpenVPN client software for end users.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/davidnicola95/OpenVPN-MikroTik-Flask.git
   cd OpenVPN-MikroTik-Flask
