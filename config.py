import os
basedir = os.path.abspath(os.path.dirname(__file__))

# yaml är en textfil som ligger utanför "exefilen" 
# interpreterande
class Config:
    DEBUG = False


class ProductionConfig(Config):
    username = "SA"
    password = "Hejsan11!!"
    server = "mssqlserver1"
    port = 1433
    database = "Comments"
    odbc_driver = "ODBC Driver 17 for SQL Server"

    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver={odbc_driver.replace(' ', '+')}"

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    DEBUG = True