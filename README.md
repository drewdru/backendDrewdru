# Backend for drewdru.com
Backend for personal website and fun

## Microservices
Frontend repository: https://github.com/drewdru/sitedrewdru

## Dependencies
1. Python >= 3.8.0
2. [requiremets.txt](requiremets.txt)

## Local deployment
### Configure project
Create and configure .env file

    cp .env.dev .env

### Build dependencies

    virtualenv env -p python3
    source env/bin/activate
    pip install -r requiremets.txt

### Run dev server

  ./run.sh dev

## Production deployment
### Configure project
Create and configure .env file

    cp .env.dev .env.prod

Create and configure settings_prod.py

    cp backendDrewdru/settings_dev.py backendDrewdru/settings_prod.py

### Build dependencies

    virtualenv env -p python3
    source env/bin/activate
    pip install -r requiremets.txt

### Run with gunicorn

  ./run.sh prod

### Run as daemon
You could use this command for run app on system startup
 
    start-stop-daemon --start --name backendDrewdru --exec /home/drewdru/develop/python/backendDrewdru/run.sh prod
