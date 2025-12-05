@echo off
echo Starting Medical QA System Web Version...

echo Starting Backend Server...
start "Medical QA Backend" cmd /k "python server.py"

echo Starting Frontend Interface...
cd web_ui
start "Medical QA Frontend" cmd /k "npm run dev"

echo System started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
