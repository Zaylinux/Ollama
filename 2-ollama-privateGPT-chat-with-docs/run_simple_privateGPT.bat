@echo off
cd /d C:\Users\imowb\Projects\Ollama
call .venv\Scripts\activate.bat
cd 2-ollama-privateGPT-chat-with-docs
echo Starting Simple PrivateGPT...
python simple_privateGPT.py