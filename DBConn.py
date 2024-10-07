import mysql.connector as db
def getConn():
    conn=db.connect(host="localhost",username="root",password="",database="project")
    return conn
def execteQuery(sql):
    conn=getConn()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def fetchData(sql):
    conn=getConn()
    cursor=conn.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def fetchOne(sql):
    conn=getConn()
    cursor=conn.cursor()
    cursor.execute(sql)
    data=cursor.fetchone()
    conn.commit()
    conn.close()
    return data