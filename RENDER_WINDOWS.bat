@echo off
rem Renders every shot in render\shots.json with Blender 4.1 (resumes where it stopped). Double-click to run.
rem Optional: drag nothing; or run from a terminal with shot names / groups, e.g.  RENDER_WINDOWS.bat boards coldopen
set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.1\blender.exe"
if not exist "%BLENDER%" set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"
if not exist "%BLENDER%" set "BLENDER=%~dp0..\blender-4.1.1-windows-x64\blender.exe"
if not exist "%BLENDER%" (
  echo Could not find Blender 4.1. Open this file in Notepad and put the path to blender.exe on the "set BLENDER=" line.
  pause
  exit /b 1
)
cd /d "%~dp0"
"%BLENDER%" -b --python render\run_all.py -- %*
echo.
echo Finished. Now open GitHub Desktop, commit the new files in renders\ and push.
pause
