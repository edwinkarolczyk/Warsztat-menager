@echo off
setlocal enabledelayedexpansion

REM Ustaw katalog roboczy – jeśli potrzebne
cd /d "%~dp0"

REM Ustaw Python (jeśli masz wiele wersji, dopasuj)
set PYTHON=py -3

REM Uruchom Jarvisa
%PYTHON% jarvis_engine.py

pause
