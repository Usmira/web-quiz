import sqlite3

DB_COLUMNS = "(Position, Titre, Image, Texte, Rep_1, Rep_2, Rep_3, Rep_4, Good_Rep)"

def insertData(sqlRequest):
    db_connection = sqlite3.connect("questions.db") # Connexion à la BDD
    db_connection.isolation_level = None
    cur = db_connection.cursor()
    cur.execute("begin")                            # start transaction
    insertion_result = cur.execute(sqlRequest)      # save the question to db
    cur.execute("commit")                           # send the request
    return insertion_result

def selectData(sqlRequest):
    db_connection = sqlite3.connect("questions.db")
    db_connection.isolation_level = None
    cur = db_connection.cursor()
    cur.execute("begin")
    cur.execute(sqlRequest)
    rows = cur.fetchall()
    cur.execute("commit")
    return rows

def createSQLRequestInsert(pythonobject):
    sqlRequest = 'INSERT INTO Questions ' + DB_COLUMNS + ' VALUES (' + str(pythonobject.position) + ',"' + pythonobject.title + '","' + pythonobject.text + '","' + pythonobject.image + '","' + pythonobject.a1 + '","' + pythonobject.a2 + '","' + pythonobject.a3 + '","' + pythonobject.a4 + '",' + str(pythonobject.trueA) + ');'
    return sqlRequest

def getPositions(tableName):
    sqlRequest = "SELECT Position FROM " + tableName + ";"  
    return sqlRequest

def incrementPosition(current_pos):
    sqlRequest = "UPDATE Questions SET Position = Position + 1 WHERE Position >= " + str(current_pos)
    return sqlRequest

def getID():
    sqlRequest = "SELECT ID FROM Questions ORDER BY ID DESC LIMIT 1"
    return sqlRequest

def truncateTable():
    sqlRequest1 = "DELETE FROM Questions;"
    sqlRequest2 = "DELETE FROM sqlite_sequence WHERE name = 'Questions';"
    return sqlRequest1,sqlRequest2