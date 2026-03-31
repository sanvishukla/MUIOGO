@echo off
REM smoke.bat - Windows wrapper for the minimal stdlib unittest smoke harness.
echo Running MUIOGO Smoke Tests...
python "%~dp0..\tests\smoke_test.py"
pause
