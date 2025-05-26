@echo off
title SEO Affiliate Content Site - Quick Launcher
color 0A

echo.
echo ========================================
echo   🎯 SEO Affiliate Content Site
echo   Automated Content Generation System
echo ========================================
echo.

cd /d "%~dp0"

echo 🔧 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.9+ first.
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

echo 📦 Installing/updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo 🚀 Starting Quick Start Setup...
echo.

python quick_start.py

echo.
echo 📋 Quick Actions:
echo.
echo 1. Generate 5 keywords and 2 content pieces
echo 2. Deploy site to Netlify
echo 3. Track performance
echo 4. Start automation
echo 5. Open documentation
echo 6. Exit
echo.

:menu
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo 🎯 Generating content...
    python main.py full-run --keywords 5 --content 2
    echo.
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo 🚀 Deploying site...
    python main.py deploy
    echo.
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo 📊 Tracking performance...
    python main.py track
    echo.
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo 🤖 Starting automation...
    python main.py automate
    echo.
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo 📚 Opening documentation...
    start docs\README.md
    goto menu
)

if "%choice%"=="6" (
    echo.
    echo 👋 Goodbye!
    exit /b 0
)

echo Invalid choice. Please try again.
goto menu
