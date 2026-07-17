#!/bin/bash

echo "======================================="
echo "       Iniciando la aplicación..."
echo "======================================="

# 1. Comprobar si Python3 está instalado
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python3 no está instalado en este equipo."
    echo "Por favor, instálalo desde python.org o usando brew/apt."
    exit
fi

# 2. Crear entorno virtual si no existe
if [ ! -d "entorno_local" ]; then
    echo "[INFO] Primera ejecución. Creando entorno virtual..."
    python3 -m venv entorno_local
fi

# 3. Activar el entorno
source entorno_local/bin/activate

# 4. Instalar dependencias
echo "[INFO] Instalando dependencias de requirements.txt..."
pip install -r requirements.txt --disable-pip-version-check

# 5. Aplicar migraciones
echo "[INFO] Configurando la base de datos..."
python manage.py migrate

# 6. Abrir el navegador según el Sistema Operativo
echo "[INFO] Abriendo el navegador..."
if command -v open &> /dev/null; then
    open http://127.0.0.1:8000  # Comando para Mac
elif command -v xdg-open &> /dev/null; then
    xdg-open http://127.0.0.1:8000  # Comando para Linux
fi

# 7. Iniciar el servidor
echo ""
echo "========================================================="
echo "EL SISTEMA ESTÁ CORRIENDO. NO CIERRES ESTA TERMINAL."
echo "Para apagar el sistema, presiona CTRL+C."
echo "========================================================="
python manage.py runserver