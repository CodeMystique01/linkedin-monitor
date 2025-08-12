@echo off
echo Starting LinkedIn Monitor in Development Mode...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy "config.env.example" ".env"
    echo.
    echo IMPORTANT: Please edit .env file with your API keys.
    notepad .env
    echo.
    pause
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
pip install -r backend\requirements.txt

REM Install Node.js dependencies
echo Installing Node.js dependencies...
cd frontend
call npm install
cd ..

echo.
echo ✅ Setup complete!
echo.
echo Starting backend server...
start /b cmd /c "cd backend && python app.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo Starting frontend development server...
cd frontend
start /b cmd /c "npm start"
cd ..

echo.
echo 🚀 Development servers starting...
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📊 API Docs: http://localhost:8000/docs
echo.
echo Press any key to open the frontend...
pause
start http://localhost:3000

pause
