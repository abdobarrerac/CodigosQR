@echo off
echo Creando el ejecutable del Generador de Códigos QR...
pyinstaller --name "Generador QR Geacco" --onefile --windowed --icon=logo_geacco.png main.py
echo Ejecutable creado exitosamente!
pause
