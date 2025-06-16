@echo off
:: Este script agrega Python y sus Scripts al PATH del sistema

:: 1. Encontrar la ruta de Python automáticamente
for /f "tokens=*" %%a in ('python -c "import sys; print(sys.executable)"') do (
    set "python_path=%%~dpa"
)

:: 2. Agregar las rutas al PATH del usuario permanentemente
setx PATH "%PATH%;%python_path%;%python_path%Scripts\"

:: 3. Mensaje de confirmación
echo.
echo ✔ Se agregaron las siguientes rutas al PATH:
echo %python_path%
echo %python_path%Scripts\
echo.
echo Reinicie la consola y pruebe con: pyinstaller --version
pause