@echo off
set DJANGO_SETTINGS_MODULE=my_project.settings
set PYTHONPATH=C:\Users\Rafael\Documents\IA-Chat-PDF\my_project
gunicorn my_project.wsgi:application --bind 127.0.0.1:8000
