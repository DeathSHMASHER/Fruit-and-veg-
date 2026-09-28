@echo off
echo ========================================================
echo  🥝 Starting ProduceVision AI (Fruit & Vegetable Detector)
echo ========================================================
echo.

py -3.13 app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying fallback python launcher...
    python app.py
)
pause
