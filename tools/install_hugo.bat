@echo off
echo Installing Hugo Extended for Windows...

REM Create Hugo directory
set HUGO_DIR=%USERPROFILE%\hugo
set HUGO_BIN=%HUGO_DIR%\bin

if not exist "%HUGO_BIN%" (
    mkdir "%HUGO_BIN%"
    echo Created Hugo directory: %HUGO_BIN%
)

REM Download Hugo using PowerShell
echo Downloading Hugo Extended...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/gohugoio/hugo/releases/download/v0.121.1/hugo_extended_0.121.1_windows-amd64.zip' -OutFile '%HUGO_DIR%\hugo.zip'"

if not exist "%HUGO_DIR%\hugo.zip" (
    echo Failed to download Hugo
    pause
    exit /b 1
)

REM Extract Hugo
echo Extracting Hugo...
powershell -Command "Expand-Archive -Path '%HUGO_DIR%\hugo.zip' -DestinationPath '%HUGO_BIN%' -Force"
del "%HUGO_DIR%\hugo.zip"

REM Test Hugo
echo Testing Hugo installation...
"%HUGO_BIN%\hugo.exe" version

if %ERRORLEVEL% EQU 0 (
    echo Hugo installed successfully!
    echo Location: %HUGO_BIN%\hugo.exe
    
    REM Add to PATH for current session
    set PATH=%PATH%;%HUGO_BIN%
    
    echo Hugo is ready to use!
) else (
    echo Hugo installation failed
    pause
    exit /b 1
)

pause
