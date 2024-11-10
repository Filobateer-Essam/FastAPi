import psycopg2
from psycopg2.extras import RealDictCursor

def Connection_DB():
    
    try:
        # Connect to database here
        conn = psycopg2.connect(host='localhost',
        database = 'fastapi', user = 'postgres' , password = 'sniper1',cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Connect To Database Successfully 😎😎") 
        return cursor
    except psycopg2.Error as e:
       return f"Unable to connect to the database {e.pgerror} , {e.diag.message_detail} "
        