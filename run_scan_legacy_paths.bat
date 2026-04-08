@echo off
setlocal ENABLEDELAYEDEXPANSION
chcp 65001 >nul
set "REPO=%~dp0"
pushd "%REPO%"
echo [BAT] Running from: "%CD%"

set "PYEXE="
where py >nul 2>&1 && set "PYEXE=py -3"
if not defined PYEXE ( where python >nul 2>&1 && set "PYEXE=python" )
if not defined PYEXE (
  echo [ERR] Nie znaleziono Pythona (py/python). Dodaj do PATH.
  pause & exit /b 2
)

echo.
echo [SCAN] Legacy sciezki/klucze...
%PYEXE% "tools\scan_legacy_paths.py"
set "RC=%ERRORLEVEL%"

set "REPORT=%CD%\legacy_paths_report.txt"
echo [BAT] Raport powinien byc tutaj: "%REPORT%"
if exist "%REPORT%" (
  if %RC% NEQ 0 (
    echo [SCAN] Wykryto trafienia. Otwieram raport...
    start notepad "%REPORT%"
  ) else (
    echo [SCAN] OK — czysto. Otwieram raport dla pewnosci...
    start notepad "%REPORT%"
  )
) else (
  echo [ERR] Nie znaleziono raportu: "%REPORT%"
)
echo.
pause
popd
endlocal
