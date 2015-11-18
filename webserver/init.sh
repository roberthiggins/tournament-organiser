python manage.py syncdb --noinput

if [ "$ROOT_PASSWORD" == "" ]; then
    # Root password environment variable is not set; so, load it from config.ini
    echo "from ConfigParser import SafeConfigParser; parser = SafeConfigParser(); parser.read('/webapp/config.ini'); from django.contrib.auth.models import User; print 'Root user already exists' if User.objects.filter(username='root') else User.objects.create_superuser('higgins', 'robert.h.higgins@gmail.com.com', parser.get('general', 'ROOT_PASSWORD'))" | python manage.py shell
else
    # Root password environment variable IS set; so, use it
    echo "import os; from django.contrib.auth.models import User; print 'Root user already exists' if User.objects.filter(username='root') else User.objects.create_superuser('higgins', 'robert.h.higgins@gmail.com.com', os.environ['ROOT_PASSWORD'])" | python manage.py shell
fi
