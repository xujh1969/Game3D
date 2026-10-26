@echo off
setlocal
set "GODOT_EXE=C:\Program Files\Godot_v4.7.2-stable_win64\Godot_v4.7.2-stable_win64_console.exe"
if not exist "%GODOT_EXE%" (
  echo Godot 4.7.2 was not found. Edit GODOT_EXE in this script.
  exit /b 1
)
if not exist "%APPDATA%\Godot\export_templates\4.7.2.stable\windows_release_x86_64.exe" (
  echo Install Godot 4.7.2 export templates in Editor - Manage Export Templates.
  exit /b 1
)
pushd "%~dp0"
if not exist "builds\Windows" mkdir "builds\Windows"
"%GODOT_EXE%" --headless --editor --path . --import
if errorlevel 1 goto failed
"%GODOT_EXE%" --headless --path . --export-release "Windows Desktop" "builds/Windows/MountainCourtyard.exe"
if errorlevel 1 goto failed
copy /y "docs\WINDOWS_BUILD.md" "builds\Windows\README.md" >nul
echo Exported: %~dp0builds\Windows\MountainCourtyard.exe
echo Keep the EXE, PCK and any exported DLL files together.
popd
exit /b 0
:failed
popd
exit /b 1
