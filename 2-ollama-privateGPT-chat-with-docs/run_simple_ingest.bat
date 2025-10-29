@echo off
cd /d C:\Users\imowb\Projects\Ollama
call .venv\Scripts\activate.bat
cd 2-ollama-privateGPT-chat-with-docs
python simple_ingest.py
pause