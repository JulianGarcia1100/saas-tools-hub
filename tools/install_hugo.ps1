# Hugo Installation Script for Windows
# Downloads and installs Hugo Extended

Write-Host "🔧 Installing Hugo Extended for Windows..." -ForegroundColor Green

# Create Hugo directory
$hugoDir = "$env:USERPROFILE\hugo"
$hugoBin = "$hugoDir\bin"

if (!(Test-Path $hugoBin)) {
    New-Item -ItemType Directory -Path $hugoBin -Force | Out-Null
    Write-Host "✅ Created Hugo directory: $hugoBin" -ForegroundColor Green
}

# Download Hugo Extended
$hugoVersion = "0.121.1"
$hugoUrl = "https://github.com/gohugoio/hugo/releases/download/v$hugoVersion/hugo_extended_${hugoVersion}_windows-amd64.zip"
$zipFile = "$hugoDir\hugo.zip"

Write-Host "📥 Downloading Hugo Extended v$hugoVersion..." -ForegroundColor Yellow

try {
    Invoke-WebRequest -Uri $hugoUrl -OutFile $zipFile
    Write-Host "✅ Downloaded Hugo successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to download Hugo: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Extract Hugo
Write-Host "📦 Extracting Hugo..." -ForegroundColor Yellow

try {
    Expand-Archive -Path $zipFile -DestinationPath $hugoBin -Force
    Remove-Item $zipFile
    Write-Host "✅ Hugo extracted successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to extract Hugo: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Add to PATH for current session
$env:PATH += ";$hugoBin"

# Check if Hugo is working
Write-Host "🧪 Testing Hugo installation..." -ForegroundColor Yellow

try {
    $hugoVersionOutput = & "$hugoBin\hugo.exe" version
    Write-Host "✅ Hugo installed successfully!" -ForegroundColor Green
    Write-Host "   Version: $hugoVersionOutput" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Hugo installation failed" -ForegroundColor Red
    exit 1
}

# Add to permanent PATH
Write-Host "🔧 Adding Hugo to system PATH..." -ForegroundColor Yellow

$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$hugoBin*") {
    [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$hugoBin", "User")
    Write-Host "✅ Hugo added to system PATH" -ForegroundColor Green
    Write-Host "   You may need to restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
} else {
    Write-Host "✅ Hugo already in system PATH" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Hugo installation completed!" -ForegroundColor Green
Write-Host "   Hugo location: $hugoBin\hugo.exe" -ForegroundColor Cyan
Write-Host "   You can now run: hugo version" -ForegroundColor Cyan
