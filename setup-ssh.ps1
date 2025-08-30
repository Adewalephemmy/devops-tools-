# Ensure OpenSSH services are running
Write-Host "Starting sshd and ssh-agent..."
Start-Service sshd -ErrorAction SilentlyContinue
Start-Service ssh-agent -ErrorAction SilentlyContinue

# Path to SSH key
$sshKey = "$env:USERPROFILE\.ssh\id_ed25519"

# Load key into ssh-agent (only if not already loaded)
Write-Host "Adding SSH key to agent..."
ssh-add -l | Select-String $sshKey -Quiet
if ($LASTEXITCODE -ne 0) {
    ssh-add $sshKey
}

# Ensure known_hosts exists
$sshDir = "$env:USERPROFILE\.ssh"
$knownHosts = "$sshDir\known_hosts"
if (!(Test-Path $knownHosts)) {
    New-Item -ItemType File -Path $knownHosts -Force | Out-Null
}

# Add localhost host key if missing
Write-Host "Adding localhost to known_hosts..."
ssh-keyscan -t ed25519 localhost | Out-File -Append -Encoding ascii $knownHosts

# Test connection (should not ask for password now)
Write-Host "Testing SSH connection..."
ssh -o StrictHostKeyChecking=no localhost hostname
