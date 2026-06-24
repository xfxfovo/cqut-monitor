@echo off
chcp 65001 >nul
cd /d "%~dp0"
python src\main.py >> run.log 2>&1
