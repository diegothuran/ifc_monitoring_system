@echo off
echo ========================================
echo IFC Monitoring System - Streamlit App
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Streamlit application...
echo App will be available at: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

streamlit run main.py --server.port 8501 --server.address 0.0.0.0

pause
