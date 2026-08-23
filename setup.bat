@echo off
REM LuxuryShoppers Bot Setup Script for Windows
REM This script automates the setup process for the Telegram Amazon Affiliate Bot

echo.
echo 🚀 LuxuryShoppers Bot Setup
echo ==============================
echo.

REM Check if Python is installed
echo ✓ Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo ✓ Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ✓ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo ✓ Installing dependencies...
pip install -r requirements.txt

echo.
echo ✓ Checking dependencies...
pip list | find "python-telegram-bot"
pip list | find "requests"
pip list | find "python-dotenv"
pip list | find "aiohttp"

echo.
echo ==============================
echo ✅ Setup Complete!
echo ==============================
echo.
echo Next steps:
echo 1. Copy .env.example to .env: copy .env.example .env
echo 2. Edit .env with your credentials:
echo    - TELEGRAM_BOT_TOKEN (from @BotFather^)
echo    - AMAZON_ACCESS_KEY
echo    - AMAZON_SECRET_KEY
echo    - AMAZON_ASSOCIATE_TAG
echo.
echo 3. Run the bot: python telegram_bot.py
echo.
echo 🎉 Happy Shopping!
echo.
pause
