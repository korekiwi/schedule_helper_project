from dotenv import load_dotenv
import os

load_dotenv()

dialect = os.getenv('DIALECT')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
dbname = os.getenv('DBNAME')


def get_mysql_url():
    return f'{dialect}+{database}://{user}:{password}@{host}/{dbname}'
