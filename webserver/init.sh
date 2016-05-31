#!/bin/bash

python manage.py migrate

if [ "$ROOT_PASSWORD" == "" ]; then
    echo "No root password set for web server"
    exit 1
else
    # Root password environment variable IS set; so, use it
    echo "import os; from django.contrib.auth.models import User; print 'Root user already exists' if User.objects.filter(username='root') else User.objects.create_superuser('root', 'robert.h.higgins@gmail.com', os.environ['ROOT_PASSWORD'])" | python manage.py shell
fi
