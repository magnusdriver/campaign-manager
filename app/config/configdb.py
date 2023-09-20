from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
import yaml

def configLoader() -> dict:
    with open("./app/config/main_config.yaml", "r") as ymlfile: 
        return yaml.load(ymlfile, Loader=yaml.FullLoader) 

cfg = configLoader()

dbParams = cfg['postgresql-parameters']

dbUrl = URL.create(
    drivername="postgresql",
    username=dbParams['user'],
    host=dbParams['host'],
    database=dbParams['database'],
    password=dbParams['password']
)

db = SQLAlchemy()