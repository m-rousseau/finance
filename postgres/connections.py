import psycopg2
from psycopg2 import sql
from . import config

def connect(sql_query, table_name):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config.config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        
    # create the SQL object
        sql_obj = sql.SQL(sql_query)
        # sql_obj = sql.SQL(sql_query).format(sql.Identifier(table_name))

        cur.execute(sql_obj)

        # commit the insert
        conn.commit()

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()