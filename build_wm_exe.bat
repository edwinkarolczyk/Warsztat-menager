@echo off
REM Build Warsztat-Menager into a standalone EXE using PyInstaller.
setlocal enabledelayedexpansion

pushd %~dp0

set "WM_BUILD_DIR=%CD%\build"
set "WM_DIST_DIR=%CD%\dist"

if not exist "%WM_BUILD_DIR%" mkdir "%WM_BUILD_DIR%"
if not exist "%WM_DIST_DIR%" mkdir "%WM_DIST_DIR%"

py -3.13 -m PyInstaller --noconfirm --clean ^
    --workpath "%WM_BUILD_DIR%\pyinstaller" ^
    --distpath "%WM_DIST_DIR%" ^
    "%CD%\wm.spec"

popd
endlocal
