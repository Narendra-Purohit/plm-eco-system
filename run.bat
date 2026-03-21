@echo off
echo Starting Backend Django Server...
start cmd /k "cd backend && call .\env\Scripts\activate && python manage.py runserver"

echo Starting Frontend Server...
start cmd /k "cd frontend && python -m http.server 8080"

echo Project services are starting up!
