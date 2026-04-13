@echo off
echo Starting UMMA AI Bot (using py launcher)...
echo.

REM Try using py launcher (works with Microsoft Store Python)
where py >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python launcher not found!
    echo.
    echo Please see INSTALL_PYTHON.md for installation instructions
    echo.
    pause
    exit /b 1
)

REM Show Python version
echo Checking Python version...
py --version
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    py -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create virtual environment
        echo Please see INSTALL_PYTHON.md for help
        pause
        exit /b 1
    )
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Run the bot
echo Starting bot...
echo Press Ctrl+C to stop the bot
echo.
python main.py

pause
