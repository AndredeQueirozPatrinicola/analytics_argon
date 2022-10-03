# FFLCH Analytics

Libraries instalation:

    python3 -m venv venv
    source venv/bin/activate 
    pip install -r requirements.txt

Mysql:

    sudo apt-get install python-dev default-libmysqlclient-dev

Exemplo mysql core/settings.py:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'analytics',
            'USER': 'admin',
            'PASSWORD': 'admin',
            'HOST': 'localhost',   # Ou IP onde o seu BD esta sendo hosteado
            'PORT': '3306',
        }
    }

Up django:

    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver

Scripts para popular db:

    python3 populadb.py 

