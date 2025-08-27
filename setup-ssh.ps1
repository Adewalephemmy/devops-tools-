# setup-ssh.ps1

$sshDir = "$env:USERPROFILE\.ssh"
$pubKey = "$sshDir\id_ed25519.pub"
$authKeys = "$sshDir\authorized_keys"
$knownHosts = "$sshDir\known_hosts"

# 1. Make sure .ssh exists
if (-not (Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir
}

# 2. Ensure authorized_keys contains your public key
if (Test-Path $pubKey) {
    $keyContent = Get-Content $pubKey
    if (-not (Select-String -Path $authKeys -Pattern [regex]::Escape($keyContent) -Quiet)) {
        Add-Content -Path $authKeys -Value $keyContent
        Write-Output "✅ Public key added to authorized_keys"
    } else {
        Write-Output "ℹ️  Key already in authorized_keys"
    }
} else {
    Write-Output "❌ No id_ed25519.pub found. Generate one with: ssh-keygen -t ed25519"
    exit 1
}

# 3. Fix known_hosts file
if (-not (Test-Path $knownHosts)) {
    New-Item -ItemType File -Path $knownHosts -Force | Out-Null
}
icacls $knownHosts /inheritance:r /grant:r "$env:USERNAME:(R,W)" | Out-Null
Write-Output "✅ Permissions fixed for known_hosts"

# 4. Restart sshd service
Restart-Service sshd
Write-Output "🔄 sshd service restarted"

# 5. Add localhost to known_hosts automatically
ssh-keyscan -t ed25519 localhost >> $knownHosts
Write-Output "✅ Localhost fingerprint added"

Write-Output "🎉 SSH setup complete. You can now run:"
Write-Output "ssh -i $sshDir\id_ed25519 localhost"
