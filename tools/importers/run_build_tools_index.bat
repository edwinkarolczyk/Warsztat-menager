@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"

REM ── Znajdź Pythona
set "PYTHON_EXE="
for %%P in ("py -3.13" "py -3.12" "python") do (
  call %%~P -c "import sys;print(sys.version)" >nul 2>nul
  if !errorlevel! EQU 0 (
    set "PYTHON_EXE=%%~P"
    goto :found
  )
)
:found
if not defined PYTHON_EXE (
  echo [ERROR] Python nie znaleziony.
  pause
  exit /b 1
)

echo [INFO] Uzywam: %PYTHON_EXE%
cd /d "%~dp0\..\.."

REM ── Buduj indeks narzędzi
%PYTHON_EXE% tools\importers\build_tools_index.py
set ERR=%ERRORLEVEL%
echo.
if %ERR% NEQ 0 (
  echo [ERROR] Indeks nie zostal zbudowany (kod %ERR%).
) else (
  echo [OK] Indeks zbudowany: data\narzedzia\narzedzia.json oraz data\tools_index.json
)
echo.
pause
