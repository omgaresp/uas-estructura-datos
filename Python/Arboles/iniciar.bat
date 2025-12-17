@echo off
TITLE Simulador de Sistema de Archivos - Demo
CLS

ECHO ==========================================
ECHO   INICIANDO SISTEMA DE ARCHIVOS
ECHO   Limpiando datos de sesiones anteriores...
ECHO ==========================================

:: Elimina los JSON si existen para iniciar una demo limpia
IF EXIST sistema_arbol.json DEL sistema_arbol.json
IF EXIST papelera.json DEL papelera.json

ECHO.
ECHO Datos limpiados. Iniciando aplicacion...
ECHO.

:: Intenta ejecutar con diferentes comandos comunes de Python
python main.py
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO 'python' no encontrado, intentando con 'py'...
    py main.py
)

ECHO.
ECHO ==========================================
ECHO   FIN DE LA SESION
ECHO ==========================================
PAUSE