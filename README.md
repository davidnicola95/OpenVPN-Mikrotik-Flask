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
   sudo apt install -y python3 python3-pip python3-venv
   ```

2. **Install Dependencies**:
   Use `pip` to install the necessary Python libraries:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install Flask paramiko librouteros
   python3 app.py
   ```

3. **Configure Environment Variables**:
   Modify these values within app.py:
   ```plaintext
   ROUTER_IP=X.X>X.X
   SSH_USERNAME=USERNAME
   SSH_PRIVATE_KEY=/path/to/private_key
   remote_host = "X.X.X.X"
   remote_port = "1194"
   ```

4. **Run the Flask App**:
   Start the Flask application:
   ```bash
   python3 app.py
   ```

5. **Access the Web Interface**:
   Open a browser and navigate to:
   ```
   http://<server_ip>:4444
   ```

## Usage
1. Navigate to the web interface.
2. Use the provided form to create a new VPN user.
3. Download the `.ovpn` configuration file for the created user.
4. Import the `.ovpn` file into your OpenVPN client to connect to the VPN.

## Security Notes
- Ensure that the private key and sensitive configuration files are not exposed in the repository or logs.
- Use HTTPS for accessing the Flask web interface in a production environment.

## Contributions
Contributions to improve or expand this project are welcome. Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer
This project is intended for educational and personal use. Ensure compliance with local laws and IT policies when using VPNs.

