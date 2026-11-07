@echo off
echo ========================================================
echo  Starting ClimateTrend AI - Weather Warehouse Dashboard
echo ========================================================
echo.

IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment 'venv' not found!
    echo Please ensure Python is installed and run: python -m venv venv
    pause
    exit /b
)

call venv\Scripts\activate.bat
echo [INFO] Virtual environment activated.
echo [INFO] Launching Streamlit application...
echo.
streamlit run app.py
pause
