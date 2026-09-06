@echo off
cd /d "%~dp0"
set "PYTHONPATH=%~dp0src"
python -m bobw fixtures\example_note.md --output output\demo --config config\intake.example.json
if errorlevel 1 echo Demo failed. Check that Python 3.10 or newer is installed.
pause
