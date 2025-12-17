@echo off
CLS
echo Compilando...
g++ -std=c++17 main.cpp src/BST.cpp -o main

IF %ERRORLEVEL% EQU 0 (
    echo Compilacion exitosa. Ejecutando...
    echo -----------------------------------
    main.exe
) ELSE (
    echo Error de compilacion.
)
PAUSE