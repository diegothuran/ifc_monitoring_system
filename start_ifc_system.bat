@echo off
echo ========================================
echo    IFC Monitoring System - Startup
echo ========================================
echo.

echo [1/3] Verificando dependencias...
C:\Users\diego\AppData\Local\Programs\Python\Python313\python.exe -c "import fastapi, uvicorn, streamlit; print('Dependencias OK')" 2>nul
if errorlevel 1 (
    echo ERRO: Dependencias nao encontradas!
    echo Execute: pip install fastapi uvicorn streamlit
    pause
    exit /b 1
)

echo [2/3] Iniciando Backend (porta 8000)...
start "IFC Backend" cmd /k "cd /d %~dp0 && C:\Users\diego\AppData\Local\Programs\Python\Python313\python.exe main.py"

echo Aguardando backend inicializar...
timeout /t 5 /nobreak >nul

echo [3/3] Iniciando Frontend Streamlit (porta 8501)...
start "IFC Streamlit" cmd /k "cd /d %~dp0 && C:\Users\diego\AppData\Local\Programs\Python\Python313\python.exe -m streamlit run streamlit_app/main.py --server.port 8501"

echo.
echo ========================================
echo    Sistema iniciado com sucesso!
echo ========================================
echo.
echo URLs:
echo   Frontend: http://localhost:8501
echo   Backend:  http://localhost:8000
echo   Docs:     http://localhost:8000/docs
echo.
echo Credenciais:
echo   Usuario: admin
echo   Senha:   admin123
echo.
echo Pressione qualquer tecla para fechar...
pause >nul

