#!/bin/bash
export DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py runserver 0.0.0.0:8000
