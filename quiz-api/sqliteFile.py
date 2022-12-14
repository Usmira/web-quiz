import sqlite3

DB_COLUMNS_STG = "Position, Titre, Image, Texte, Rep_1, Rep_2, Rep_3, Rep_4, Good_Rep"
DB_COLUMNS_LST = ['Position', 'Titre', 'Image', 'Texte', 'Rep_1', 'Rep_2', 'Rep_3', 'Rep_4', 'Good_Rep']
DB_QUESTIONS_COLUMNS_STG = "Position, Titre, Image, Texte"
DB_QUESTIONS_COLUMNS_LST = ['Position', 'Titre', 'Image', 'Texte']
DB_REPONSES_COLUMNS_STG = "Texte , isCorrect, Question_ID"
DB_REPONSES_COLUMNS_LST = ["Texte" , "isCorrect", "Question_ID"]
DB_NAME = "questions.db"

def insertData(sqlRequest):
    db_connection = sqlite3.connect(DB_NAME) # Connexion à la BDD
    db_connection.isolation_level = None
    cur = db_connection.cursor()
    cur.execute("begin")                            # start transaction
    insertion_result = cur.execute(sqlRequest)      # save the question to db
    cur.execute("commit")                           # send the request
    return insertion_result

def selectData(sqlRequest):
    db_connection = sqlite3.connect(DB_NAME)
    db_connection.isolation_level = None
    cur = db_connection.cursor()
    cur.execute("begin")
    cur.execute(sqlRequest)
    rows = cur.fetchall()
    cur.execute("commit")
    return rows

def insertINTOQuestion(pythonobject):
    sqlRequest = 'INSERT INTO Questions (' + DB_QUESTIONS_COLUMNS_STG + ') VALUES (' + str(pythonobject.position) + ',"' + pythonobject.title + '","' + pythonobject.text + '","' + pythonobject.image + '");'
    return sqlRequest

def insertINTOResponse(pythonobject):
    sqlRequest = 'INSERT INTO Reponses (' + DB_REPONSES_COLUMNS_STG + ') VALUES ("' + pythonobject.text + '",' + str(pythonobject.isCorrect) + ',' + str(pythonobject.questionId) + ');'
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

def truncateTable(tablename):
    sqlRequest1 = "DELETE FROM " + tablename + ";"
    sqlRequest2 = "DELETE FROM sqlite_sequence WHERE name = '" + tablename + "';"
    return sqlRequest1,sqlRequest2

def delete1Question(questionId):
    sqlRequest = "DELETE FROM Questions WHERE ID = " + str(questionId) + ";"
    return sqlRequest

def deleteResponses(questionId):
    sqlRequest = "DELETE FROM Reponses WHERE Question_ID = " + str(questionId) + ";"
    return sqlRequest

def getQuestionByID(questionId):
    sqlRequest = "SELECT * FROM Questions WHERE ID = " + str(questionId) + ";"
    return sqlRequest

def getQuestionByIDwithoutID(questionId):
    sqlRequest = "SELECT " + DB_QUESTIONS_COLUMNS_STG + " FROM Questions WHERE ID = " + str(questionId) + ";"
    return sqlRequest

def getResponseByQuestionIDwithoutID(questionId):
    sqlRequest = "SELECT " + DB_REPONSES_COLUMNS_STG + " FROM Reponses WHERE Question_ID = " + str(questionId) + ";"
    return sqlRequest

def getResponseByQuestionID(questionId):
    sqlRequest = "SELECT * FROM Reponses WHERE Question_ID = " + str(questionId) + ";"
    return sqlRequest

def updateQuestionByID(questionId,pythonobject):
    sqlRequest = 'UPDATE Questions SET ' + DB_QUESTIONS_COLUMNS_LST[0] + ' = ' + str(pythonobject.position) + ', ' + DB_QUESTIONS_COLUMNS_LST[1] + ' = "' + str(pythonobject.title) + '", ' + DB_QUESTIONS_COLUMNS_LST[2] + ' = "' + pythonobject.text + '", ' + DB_QUESTIONS_COLUMNS_LST[3] + ' = "' + pythonobject.image + '" WHERE ID = ' + str(questionId) + ';'
    return sqlRequest

def getIDwithPosition(questionPosition):
    sqlRequest = "SELECT ID FROM Questions WHERE Position = " + str(questionPosition) + ";"
    return sqlRequest

def addAParticipation(playerName,score,date):
    sqlRequest = 'INSERT INTO Participations (PlayerName,Score,Date) VALUES ("' + playerName + '",' + str(score) + ',"' + date + '");' 
    return sqlRequest

def getAllScoresSorted():
    sqlRequest = "SELECT PlayerName,Score,Date FROM Participations ORDER BY Score DESC;"
    return sqlRequest