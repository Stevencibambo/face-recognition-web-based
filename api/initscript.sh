#!/bin/bash
python manage.py db init && python manage.py db migrate --message 'initialize database' && python manage.py db upgrade && python manage.py proc && python manage.py train
