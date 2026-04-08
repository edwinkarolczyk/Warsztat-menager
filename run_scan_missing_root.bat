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
echo [SCAN] Szukam uzyc repo-relative (bez <root>)...
%PYEXE% "tools\scan_missing_root.py"
set "RC=%ERRORLEVEL%"

set "REPORT=%CD%\missing_root_report.txt"
echo [BAT] Raport: "%REPORT%"
if exist "%REPORT%" (
  if %RC% NEQ 0 (
    echo [SCAN] Wykryto podejrzane wpisy. Otwieram raport...
    start notepad "%REPORT%"
  ) else (
    echo [SCAN] OK — raport otwieram dla pewnosci...
    start notepad "%REPORT%"
  )
) else (
  echo [ERR] Nie znaleziono raportu: "%REPORT%"
)
echo.
pause
popd
endlocal
