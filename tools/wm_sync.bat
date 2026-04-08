@echo off
setlocal
REM === Ustaw ścieżkę do Pythona jeśli potrzeba ===
REM set PYTHON=C:\Program Files\Python313\python.exe

if not exist ".env" (
  echo Brak pliku .env w katalogu tools\. Skopiuj .env.example do .env i wstaw GITHUB_TOKEN.
)

REM Instalacja zależności (raz)
pip show requests >NUL 2>&1 || pip install requests
pip show python-dotenv >NUL 2>&1 || pip install python-dotenv

echo [wm_sync] Pobieram gałąź Rozwiniecie (read-only)...
python "%~dp0wm_sync.py" pull
if errorlevel 1 goto :eof

echo [wm_sync] Tworzę paczkę JSON...
python "%~dp0wm_sync.py" bundle
echo [wm_sync] Gotowe. Paczka: out\wm_bundle.json
pause
