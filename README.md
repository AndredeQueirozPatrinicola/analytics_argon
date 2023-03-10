# FFLCH Analytics

Libraries instalation:

    python3 -m venv venv
    source venv/bin/activate 
    pip3 install -r requirements.txt

Mysql:

    sudo apt-get install python-dev default-libmysqlclient-dev

Exemplo .env:

    DEBUG=True

    SECRET_KEY=yoursecretkey

    DBNAME=analytics
    DBUSER=admin
    DBPASSWORD=admin
    DBHOST=localhost  
    DBPORT=3306

    ETL_DBNAME=etl
    ETL_DBUSER=admin
    ETL_DBPASSWORD=password
    ETL_DBHOST=localhost
    ETL_DBPORT=3306

Up django:

    python3 manage.py migrate
    python3 manage.py runserver

Scripts para popular db:

    python3 populadb.py 

Front-end:

    npm install

Dev server webpack bundle:

    npm run dev

