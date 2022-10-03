# FFLCH Analytics

Libraries instalation:

    python3 -m venv venv
    source venv/bin/activate 
    pip install -r requirements.txt

Mysql:

    sudo apt-get install python-dev default-libmysqlclient-dev

Exemplo mysql core/settings.py:

    DEBUG=True

    SECRET_KEY=yoursecretkey

    DBNAME=analytics
    DBUSER=admin
    DBPASSWORD=admin
    DBHOST=localhost  # Or an IP Address that your DB is hosted on
    DBPORT=3306

Up django:

    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver

Scripts para popular db:

    python3 populadb.py 

