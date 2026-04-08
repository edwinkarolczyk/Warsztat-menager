@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ── KATALOG ROBOCZY = folder skryptu
cd /d "%~dp0"

REM ── Znajdź Pythona (prefer wbudowany, potem systemowy)
set "PY_EMB=%~dp0..\..\Files\Python313\python.exe"
set "PYTHON_EXE="
if exist "%PY_EMB%" (
  set "PYTHON_EXE=%PY_EMB%"
) else (
  for %%P in ("py -3.13" "py -3.12" "py -3.11" "python" "python3") do (
    call %%~P -c "import sys;print(sys.version)" >nul 2>nul
    if !errorlevel! EQU 0 (
      set "PYTHON_EXE=%%~P"
      goto :found_py
    )
  )
)

:found_py
if not defined PYTHON_EXE (
  echo [ERROR] Nie znaleziono Pythona.
  pause
  exit /b 1
)

set "PYTHON_CMD=%PYTHON_EXE%"
if exist "%PYTHON_CMD%" (
  set "PYTHON_CMD="%PYTHON_CMD%""
)

echo [INFO] Python: %PYTHON_EXE%
echo [INFO] Katalog : "%cd%"

REM ── USTAW: nazwa pliku Excela i arkusza
set "XLS=Spis narzedzi.xlsx"
set "SHEET=Arkusz1"

REM ── AUTO: wykryte w pliku → numer=Kolumna1, nazwa=Kolumna3
%PYTHON_CMD% tools_from_excel.py ^
  --input "%XLS%" ^
  --sheet "%SHEET%" ^
  --data-root "..\..\data" ^
  --out-subdir "narzedzia" ^
  --col-numer "Kolumna1" ^
  --col-nazwa "Kolumna3" ^
  --pad 3 ^
  --typ-default "Wykrawające" ^
  --status-default "sprawne" ^
  --pracownik-default "edwin" ^
  --mode skip

set ERR=%ERRORLEVEL%
echo.
if %ERR% NEQ 0 (
  echo [ERROR] Skrypt zakonczyl sie kodem %ERR%
) else (
  echo [DONE] Gotowe.
)
echo.
pause
