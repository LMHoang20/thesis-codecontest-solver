from database import get_db_conn

def get_editorials():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM editorials")
    editorials = cursor.fetchall()
    conn.close()
    return editorials

if __name__ == '__main__':
    editorials = get_editorials()
    print(editorials)