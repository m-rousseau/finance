from sqlalchemy import create_engine, URL, text, Table, Column, Integer, String, MetaData
from configparser import ConfigParser
import init_tables
import os


# configuration for postgres connection
def config(filename='creds.ini', section='postgresql'):
    
    # get relative path
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, filename)
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


# connects to the postgres databse
def get_connection():

    engine = None
    params = config()

    dialect = params['dialectdriver']
    user = params['user']
    password = params['password']
    host = params['host']
    port = params['port']
    database = params['database']

    return create_engine(
        url="{0}://{1}:{2}@{3}:{4}/{5}".format(
            dialect, user, password, host, port, database
        # use these for debugging if needed
        # , echo=True
        # , echo_pool="debug"
        )
    )


# create all required data tables
def initialize_tables():

    # connect to database
    db_connection = get_connection()
    # create metadata object. this contains all table objects
    meta = init_tables.create_tables()
    # create any table that is currently not in the database
    meta.create_all(db_connection)

