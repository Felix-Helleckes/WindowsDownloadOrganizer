@echo off
@echo off
REM Minimaler Starter: ruft das Python-Skript im selben Ordner auf.
py -3 "%~dp0sort.py" %*
if %ERRORLEVEL% NEQ 0 pause

