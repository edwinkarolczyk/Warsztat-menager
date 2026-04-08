@echo off
setlocal enabledelayedexpansion

echo [WM-INSTALL] Instalator Warsztat-Menager

echo.
set "DEFAULT_PROG_DIR=C:\WM\Warsztat-Menager-Release"
set "DEFAULT_DATA_DIR=C:\WM\data"

set /p PROG_DIR=Podaj katalog instalacji programu (ENTER = !DEFAULT_PROG_DIR!): 
if "!PROG_DIR!"=="" set "PROG_DIR=!DEFAULT_PROG_DIR!"

set /p DATA_DIR=Podaj katalog danych (ENTER = !DEFAULT_DATA_DIR!): 
if "!DATA_DIR!"=="" set "DATA_DIR=!DEFAULT_DATA_DIR!"

echo.
echo [WM-INSTALL] Program: !PROG_DIR!
echo [WM-INSTALL] Dane   : !DATA_DIR!

echo.
if not exist "dist" (
  echo [WM-INSTALL][ERROR] Brak katalogu dist. Najpierw uruchom build_wm_exe.bat.
  pause
  exit /b 1
)

set "EXE_NAME=WarsztatMenager.exe"
if not exist "dist\!EXE_NAME!" (
  echo [WM-INSTALL][ERROR] Nie znaleziono pliku dist\!EXE_NAME!. Upewnij się, że wykonano build_wm_exe.bat.
  pause
  exit /b 1
)

mkdir "!PROG_DIR!" 2>nul
if errorlevel 1 (
  if not exist "!PROG_DIR!" (
    echo [WM-INSTALL][ERROR] Nie można utworzyć katalogu programu.
    pause
    exit /b 1
  )
)

mkdir "!DATA_DIR!" 2>nul
mkdir "!DATA_DIR!\logs" 2>nul
mkdir "!DATA_DIR!\backup" 2>nul
mkdir "!DATA_DIR!\jarvis" 2>nul

copy /Y "dist\!EXE_NAME!" "!PROG_DIR!\!EXE_NAME!" >nul
if errorlevel 1 (
  echo [WM-INSTALL][ERROR] Nie udało się skopiować pliku EXE.
  pause
  exit /b 1
)

if exist "INFO_URUCHOMIENIE.txt" copy /Y "INFO_URUCHOMIENIE.txt" "!PROG_DIR!\INFO_URUCHOMIENIE.txt" >nul

echo Program: !PROG_DIR!\!EXE_NAME!> "!PROG_DIR!\INSTALL_INFO.txt"
echo Dane   : !DATA_DIR!>> "!PROG_DIR!\INSTALL_INFO.txt"
echo.>> "!PROG_DIR!\INSTALL_INFO.txt"
echo Katalogi danych:>> "!PROG_DIR!\INSTALL_INFO.txt"
echo   logs   - !DATA_DIR!\logs>> "!PROG_DIR!\INSTALL_INFO.txt"
echo   backup - !DATA_DIR!\backup>> "!PROG_DIR!\INSTALL_INFO.txt"
echo   jarvis - !DATA_DIR!\jarvis>> "!PROG_DIR!\INSTALL_INFO.txt"
echo.>> "!PROG_DIR!\INSTALL_INFO.txt"
echo Opcjonalnie ustaw zmienną WM_CONFIG_FILE, aby wskazać inny plik config.json.>> "!PROG_DIR!\INSTALL_INFO.txt"

echo.
echo [WM-INSTALL] Instalacja zakonczona.
echo EXE: !PROG_DIR!\!EXE_NAME!
echo Dane domyslnie: !DATA_DIR!
echo.
echo Aby wymusic uzycie innego config.json ustaw zmienna srodowiskowa WM_CONFIG_FILE.
echo.
pause
endlocal
