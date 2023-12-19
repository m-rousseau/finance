from sqlalchemy import create_engine, URL, text
from configparser import ConfigParser
import os


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


# executes SQL statements
# def execute():
#     with engine.connect() as connection:
#         connection.execute("<some statement>")
#         connection.commit()  # commits "some statement"

#         # new transaction starts
#         connection.execute("<some other statement>")
#         connection.rollback()  # rolls back "some other statement"

#         # new transaction starts
#         connection.execute("<a third statement>")
#         connection.commit()  # commits "a third statement"


# if __name__ == '__main__':
#     try:
#         # engine = get_connection()
#         with engine.connect() as connection:
#             result = connection.execute(
#                 text("select ticker from stocks")
#                 )
#             for row in result:
#                 print("ticker:", row.ticker)
#     except Exception as ex:
#         print("Sorry your connection is not created some interruption is occured please check and try it again \n", ex)