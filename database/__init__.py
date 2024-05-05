import psycopg2

def get_db_conn():
    return psycopg2.connect(database="thesis", user='postgres', password='1234', host='127.0.0.1', port= '5432'
)

