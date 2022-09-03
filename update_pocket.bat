@echo off

set launcherver=1

set mypath=%cd%
echo %mypath%
python updater.py %launcherver% %mypath%

pause