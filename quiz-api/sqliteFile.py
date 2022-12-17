import sqlite3

DB_COLUMNS_STG = "(Position, Titre, Image, Texte, Rep_1, Rep_2, Rep_3, Rep_4, Good_Rep)"
DB_COLUMNS_LST = ['Position', 'Titre', 'Image', 'Texte', 'Rep_1', 'Rep_2', 'Rep_3', 'Rep_4', 'Good_Rep']

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
    sqlRequest = 'INSERT INTO Questions ' + DB_COLUMNS_STG + ' VALUES (' + str(pythonobject.position) + ',"' + pythonobject.title + '","' + pythonobject.text + '","' + pythonobject.image + '","' + pythonobject.a1 + '","' + pythonobject.a2 + '","' + pythonobject.a3 + '","' + pythonobject.a4 + '",' + str(pythonobject.trueA) + ');'
    return sqlRequest

def getAllPositions(tableName):
    sqlRequest = "SELECT Position FROM " + tableName + ";"  
    return sqlRequest

def get1Position(questionId):
    sqlRequest = "SELECT Position FROM Questions WHERE ID = " + str(questionId) + ";"
    return sqlRequest

def incrementPosition(current_pos):
    sqlRequest = "UPDATE Questions SET Position = Position + 1 WHERE Position >= " + str(current_pos)
    return sqlRequest

def decIncrementPosition(current_pos):
    sqlRequest = "UPDATE Questions SET Position = Position - 1 WHERE Position > " + str(current_pos)
    return sqlRequest

def getlastID():
    sqlRequest = "SELECT ID FROM Questions ORDER BY ID DESC LIMIT 1"
    return sqlRequest

def truncateTable():
    sqlRequest1 = "DELETE FROM Questions;"
    sqlRequest2 = "DELETE FROM sqlite_sequence WHERE name = 'Questions';"
    return sqlRequest1,sqlRequest2

def delete1Question(questionId):
    sqlRequest = "DELETE FROM Questions WHERE ID = " + str(questionId) + ";"
    return sqlRequest

def getQuestionByID(questionId):
    sqlRequest = "SELECT * FROM Questions WHERE ID = " + str(questionId) + ";"
    return sqlRequest

def updateQuestionByID(questionId,pythonobject):
    sqlRequest = 'UPDATE Questions SET ' + DB_COLUMNS_LST[0] + ' = ' + str(pythonobject.position) + ', ' + DB_COLUMNS_LST[1] + ' = "' + str(pythonobject.title) + '", ' + DB_COLUMNS_LST[2] + ' = "' + pythonobject.text + '", ' + DB_COLUMNS_LST[3] + ' = "' + pythonobject.image + '", ' + DB_COLUMNS_LST[4] + ' = "' + pythonobject.a1 + '", ' + DB_COLUMNS_LST[5] + ' = "' + pythonobject.a2 + '", ' + DB_COLUMNS_LST[6] + ' = "' + pythonobject.a3 + '", ' + DB_COLUMNS_LST[7] + ' = "' + pythonobject.a4 + '", ' + DB_COLUMNS_LST[8] + ' = ' + str(pythonobject.trueA) + ' WHERE ID = ' + str(questionId) + ';'
    return sqlRequest
