@echo off
title Sales Analysis Dashboard
echo ===================================================
echo       Starting Sales Analysis Dashboard...
echo ===================================================
echo.

python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Standard python command failed. Trying with direct Python path...
    C:\Python312\python.exe main.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred while launching the dashboard.
    pause
)
