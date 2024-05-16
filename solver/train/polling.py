import time

from constants import *
from database.mongodb import MongoDB
from database import get_db_conn


def create_table_generated_editorial():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_editorials (
            id SERIAL PRIMARY KEY,
            name INT NOT NULL,
            generated TEXT NOT NULL,
            config JSONB NOT NULL,
            priority INT NOT NULL
        )
    """)

def insert_generated_editorial(problem: dict):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute()
    cursor.execute("""
        INSERT INTO generated_editorials (name, generated, config, priority)
        VALUES (%s, %s, %s, %s)
    """, (problem['name'], problem['generated'], problem['config'], problem['priority']))
    conn.commit()

if __name__ == "__main__":
    # create a MongoDB object
    create_table_generated_editorial()
    mongodb = MongoDB(MONGO_USER, MONGO_PASSWORD)
    # create a connection to the database
    client = mongodb.get_db_conn()
    # create a database
    db = client['codecontest']
    # create a collection
    collection = db['problems']
    while True:
        # get all documents
        problems = collection.find()
        for problem in problems:
            # insert a document
            problem = {
                "name": problem['name'],
                "prefix": problem['prefix'],
                "generated": problem['generated'],
            }
            insert_generated_editorial(problem)    
        time.sleep(10)
    # close the connection
    client.close()