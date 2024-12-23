from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import paramiko
from librouteros import connect
from librouteros.exceptions import TrapError

app = Flask(__name__)

# MikroTik credentials
ROUTER_IP = "192.168.100.1"
SSH_USERNAME = "admin"
SSH_PRIVATE_KEY = "/home/ngvpn/.ssh/id_rsa"  # Adjust this to the correct path of your private key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/error')
def error_page():
    return render_template('error.html')

def generate_certificate_and_key(username, private_key_password):
    # File paths on the MikroTik router
    ca_crt = "cert_export_ca-template.crt"
    client_crt = "cert_export_client-template.crt"
    client_key = "cert_export_client-template.key"

    # Re-export the client certificate with a user-specified password
    os.system(f'ssh -i {SSH_PRIVATE_KEY} {SSH_USERNAME}@{ROUTER_IP} "/certificate export-certificate client-template export-passphrase=\"{private_key_password}\""')

    # Use SCP to copy the files from the MikroTik router to the local system
    os.system(f'scp -o StrictHostKeyChecking=no -i {SSH_PRIVATE_KEY} {SSH_USERNAME}@{ROUTER_IP}:/cert_export_ca-template.crt /tmp/{username}-ca.crt')
    os.system(f'scp -o StrictHostKeyChecking=no -i {SSH_PRIVATE_KEY} {SSH_USERNAME}@{ROUTER_IP}:/cert_export_client-template.crt /tmp/{username}-cert.crt')
    os.system(f'scp -o StrictHostKeyChecking=no -i {SSH_PRIVATE_KEY} {SSH_USERNAME}@{ROUTER_IP}:/cert_export_client-template.key /tmp/{username}-cert.key')

    return f'{username}-ca.crt', f'{username}-cert.crt', f'{username}-cert.key'

@app.route('/create_vpn', methods=['POST'])
def create_vpn():
    username = request.form['username']
    password = request.form['password']
    private_key_password = request.form['private_key_password']

    try:
        # Establish SSH connection to MikroTik
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(SSH_PRIVATE_KEY)
        ssh.connect(ROUTER_IP, username=SSH_USERNAME, pkey=private_key)

        # Check if the username already exists
        check_user_command = f"/ppp secret print where name={username}"
        stdin, stdout, stderr = ssh.exec_command(check_user_command)
        output = stdout.read().decode().strip()
        
        if username in output:
            ssh.close()
            return redirect(url_for('error_page', error_message=f"Error: Username '{username}' already exists."))

        # Create the VPN profile (PPP secret)
        create_secret_command = f"/ppp secret add name={username} password={password} service=ovpn profile=default"
        stdin, stdout, stderr = ssh.exec_command(create_secret_command)
        error = stderr.read().decode().strip()
        if error:
            return redirect(url_for('error_page', error_message=f"An error occurred: {error}"))

        # Close SSH connection
        ssh.close()

        # Generate the certificates and keys
        ca_crt, client_crt, client_key = generate_certificate_and_key(username, private_key_password)

        # Load the certificates and keys
        with open(f'/tmp/{ca_crt}', 'r') as ca_file:
            ca_certificate = ca_file.read()

        with open(f'/tmp/{client_crt}', 'r') as cert_file:
            client_certificate = cert_file.read()

        with open(f'/tmp/{client_key}', 'r') as key_file:
            client_key_content = key_file.read()

        # Define the remote host and other parameters
        remote_host = "YOUR IP"
        remote_port = "1194"
        protocol = "tcp"

        # Create the OVPN file content
        ovpn_content = f"""
client
dev tun
proto tcp-client
remote {remote_host} {remote_port}
resolv-retry infinite
nobind
redirect-gateway def1
persist-key
persist-tun
remote-cert-tls server
cipher AES-128-CBC
auth SHA1
auth-user-pass

<ca>
{ca_certificate.strip()}
</ca>

<cert>
{client_certificate.strip()}
</cert>

<key>
{client_key_content.strip()}
</key>
"""

        # Write the content to the OVPN file
        ovpn_file_path = f'/tmp/{username}.ovpn'
        with open(ovpn_file_path, 'w') as ovpn_file:
            ovpn_file.write(ovpn_content.strip())

        # Provide the download link
        return send_file(ovpn_file_path, as_attachment=True)

    except TrapError as e:
        return redirect(url_for('error_page', error_message=f"An error occurred: {str(e)}"))
    except paramiko.AuthenticationException as e:
        return redirect(url_for('error_page', error_message=f"Authentication failed: {str(e)}"))
    except Exception as e:
        return redirect(url_for('error_page', error_message=f"An unexpected error occurred: {str(e)}"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444)
