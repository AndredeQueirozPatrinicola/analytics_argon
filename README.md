# FFLCH Analytics

Libraries instalation:

    python -m venv venv
    source venv/Scripts/activate (linux: source venv/bin/activate)
    pip install -r requirements.txt

Up django:

    python manage.py runserver

Participantes:

    - Thiago
    - Teste
    - André


Scripts para popular db:

    python manage.py shell

    from apps.home.utils import Api

    api = Api()

    # Popula dados de departamentos:
    api.pega_dados_departamentos()

    # Popula dados docentes:
    api.pega_dados_docente ()


