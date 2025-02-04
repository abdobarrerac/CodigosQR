# Generador de Códigos QR - Geacco

Esta aplicación permite generar códigos QR personalizados con logo para todos los empleados listados en un archivo Excel.

## Para Usuarios

### Instalación
1. Descargue el archivo `Generador QR Geacco.exe` de la carpeta `dist`
2. Copie el ejecutable a la ubicación que prefiera en su computadora

### Uso de la Aplicación
1. Haga doble clic en `Generador QR Geacco.exe`
2. En la interfaz gráfica:
   - Haga clic en "Buscar Excel" para seleccionar su archivo Excel
   - Haga clic en "Buscar Logo" para seleccionar el logo de la empresa
   - Haga clic en "Seleccionar Carpeta" para elegir dónde guardar los códigos QR
   - Haga clic en "Generar Códigos QR" para iniciar el proceso

### Formato del Archivo Excel
El archivo Excel debe contener:
- Una columna llamada "Nombre" con los nombres de los empleados
- Una columna llamada "URL" con los enlaces personales de cada empleado

## Para Desarrolladores

### Requisitos Previos
1. Python 3.8 o superior
2. Git (opcional, para clonar el repositorio)

### Configuración del Entorno de Desarrollo
1. Clone o descargue este repositorio
2. Abra una terminal en la carpeta del proyecto
3. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```

### Ejecutar en Modo Desarrollo
```
python main.py
```

### Crear el Ejecutable
1. Instale PyInstaller (si no está instalado):
   ```
   pip install pyinstaller
   ```
2. Ejecute el archivo `build.bat` haciendo doble clic en él
3. El ejecutable se creará en la carpeta `dist`

## Solución de Problemas

Si encuentra algún error:
1. Asegúrese de que el archivo Excel tiene el formato correcto
2. Verifique que el logo está en formato PNG o JPG
3. Asegúrese de tener permisos de escritura en la carpeta de salida

## Soporte

Si necesita ayuda adicional, contacte al equipo de soporte técnico.
