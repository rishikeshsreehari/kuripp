@echo off
call venv\Scripts\activate
pip freeze > requirements.txt
