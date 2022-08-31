# FFLCH Analytics

Mysql:

    sudo apt-get install python-dev default-libmysqlclient-dev

Libraries instalation:

    python -m venv venv
    source venv/Scripts/activate (linux: source venv/bin/activate)
    pip install -r requirements.txt

Up django:

    python3 manage.py migrate
    python3 manage.py runserver

Exemplo mysql core/settings.py:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'analytics',
            'USER': 'admin',
            'PASSWORD': 'admin',
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }

Scripts para popular db:

    python manage.py shell

    from apps.home.utils import Api

    api = Api()

    # Popula dados de departamentos:
    api.pega_dados_departamentos()

    # Popula dados docentes:
    api.pega_dados_docente ()


