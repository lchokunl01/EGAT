import paramiko

# Windows machine (equipment) SSH server details
windows_server_ip = "10.157.39.203"
ssh_username = "admin"
ssh_password = "admin"

# Remote SFTP directory path on the Windows equipment
remote_directory = "C:/RelayData/AY1_AT1_R230803_074008.csv"  # Replace with the actual remote directory path

# Local file path on the Raspberry Pi
local_file_path = "/home/pi/LFL/AY1_AT1_R230803_074008.csv"  # Replace with the local file path you want to upload

# Create an SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the Windows equipment via SSH
ssh.connect(windows_server_ip, username=ssh_username, password=ssh_password)

# Create an SFTP client session
sftp = ssh.open_sftp()

# Change the remote directory (if needed)
sftp.chdir(remote_directory)

# Upload the file from Raspberry Pi to the Windows equipment
sftp.put(local_file_path, remote_directory)

# Close the SFTP session
sftp.close()

# Close the SSH connection
ssh.close()
