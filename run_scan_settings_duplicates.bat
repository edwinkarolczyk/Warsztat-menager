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
echo [SCAN] Duplikaty/niespojnosci ustawien...
%PYEXE% "tools\scan_settings_duplicates.py"
set "RC=%ERRORLEVEL%"

set "REPORT=%CD%\settings_duplicates_report.txt"
echo [BAT] Raport powinien byc tutaj: "%REPORT%"
if exist "%REPORT%" (
  if %RC% NEQ 0 (
    echo [SCAN] Wykryto problemy. Otwieram raport...
    start notepad "%REPORT%"
  ) else (
    echo [SCAN] OK — dobrze. Otwieram raport dla pewnosci...
    start notepad "%REPORT%"
  )
) else (
  echo [ERR] Nie znaleziono raportu: "%REPORT%"
)
echo.
pause
popd
endlocal
