@echo off
title Iniciando Sistema Django
echo =======================================
echo     Iniciando la aplicacion...
echo =======================================

:: 1. Comprobar si Python esta instalado en el sistema
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Python no esta instalado o no fue agregado al PATH.
    echo Por favor, descarga e instala Python desde www.python.org
    echo IMPORTANTE: Marca la casilla "Add Python to PATH" al instalar.
    echo.
    pause
    exit /b
)

:: 2. Crear un entorno virtual si es la primera vez que se ejecuta
IF NOT EXIST "entorno_local" (
    echo [INFO] Primera ejecucion detectada.
    echo [INFO] Creando entorno virtual (esto puede tomar un minuto)...
    python -m venv entorno_local
)

:: 3. Activar el entorno virtual
call entorno_local\Scripts\activate

:: 4. Instalar o verificar dependencias
echo [INFO] Verificando e instalando dependencias (requirements.txt)...
pip install -r requirements.txt --disable-pip-version-check

:: 5. Aplicar migraciones por si hay cambios en la base de datos
echo [INFO] Verificando base de datos...
python manage.py migrate

:: 6. Abrir automaticamente el navegador web
echo [INFO] Abriendo la aplicacion en tu navegador...
start http://127.0.0.1:8000

:: 7. Iniciar el servidor web
echo.
echo ========================================================
echo EL SISTEMA ESTA CORRIENDO. NO CIERRES ESTA VENTANA NEGRA.
echo Para apagar el sistema, presiona CTRL+C o cierra la ventana.
echo ========================================================
python manage.py runserver
pause