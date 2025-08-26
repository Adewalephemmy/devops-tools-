import paramiko
import os

def ssh_command(host, user, password, command):
    """Execute a command on a remote server via SSH"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"🔗 Connecting to {host}...")
        client.connect(hostname=host, username=user, password=password, timeout=10)

        stdin, stdout, stderr = client.exec_command(command)

        print("✅ Command Output:")
        for line in stdout:
            print(line.strip())

        error = stderr.read().decode()
        if error:
            print("❌ Error:", error)

    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        client.close()


def sftp_transfer(host, user, password, local_file, remote_file, action="upload"):
    """Upload or download files via SFTP"""
    try:
        print(f"🔗 Connecting to {host} via SFTP...")
        transport = paramiko.Transport((host, 22))
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        if action == "upload":
            print(f"⬆️ Uploading {local_file} → {remote_file}")
            sftp.put(local_file, remote_file)
        elif action == "download":
            print(f"⬇️ Downloading {remote_file} → {local_file}")
            sftp.get(remote_file, local_file)

        print("✅ Transfer complete.")
        sftp.close()
        transport.close()

    except Exception as e:
        print(f"❌ SFTP transfer failed: {e}")


if __name__ == "__main__":
    # SSH Credentials (use env vars for safety)
    host = os.getenv("SSH_HOST", "127.0.0.1")
    user = os.getenv("SSH_USER", "testuser")
    password = os.getenv("SSH_PASS", "password123")

    # Run remote command
    ssh_command(host, user, password, "uname -a")

    # Upload example
    sftp_transfer(host, user, password,
                  local_file="README.md",
                  remote_file="/tmp/readme_copy.md",
                  action="upload")

    # Download example
    sftp_transfer(host, user, password,
                  local_file="downloaded_log.txt",
                  remote_file="/var/log/syslog",
                  action="download")
