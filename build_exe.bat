@echo off
echo ========================================
echo Python App to EXE Converter
echo ========================================

echo.
echo [1/4] Activating Python virtual environment...
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo.
echo [2/4] Installing required packages (psutil and pyinstaller)...
pip install psutil pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install packages!
    pause
    exit /b 1
)

echo.
echo [3/4] Converting app.py to flowbit.exe...
pyinstaller --onefile --noconsole --name flowbit app.py
if errorlevel 1 (
    echo ERROR: Failed to create executable!
    pause
    exit /b 1
)

echo.
echo [4/4] Build completed successfully!
echo.
echo Executable created at: dist\flowbit.exe
echo.
echo You can find your executable in the 'dist' folder.
echo.

echo Press any key to continue...
pause >nul