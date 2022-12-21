from sqliteFile import insertData, truncateTable
import sqlite3

DB_NAME = "questions.db"

def rebuildBDD():
    """
    Fonction permettant de générer une base vide avec l'initialisation des tables nécessaires
    """
    #   (1) On verifie que le fichier de base de donnée existe, sinon on le crée
    createDatabase(DB_NAME)
    #   (2) On vérifie que les tables Questions, Reponses et Participations sont bien implémentées dans la base de donnée
    insertData(checkQuestionsTable())
    insertData(checkReponsesTable())
    insertData(checkParticipationsTable())
    #   (3) On vide les 3 tables
    qR1, qR2 = truncateTable("Questions")
    qR3, qR4 = truncateTable("Reponses")
    qR5, qR6 = truncateTable("Participations")
    insertData(qR1)
    insertData(qR2)
    insertData(qR3)
    insertData(qR4)
    insertData(qR5)
    insertData(qR6)
    return 1

def createDatabase(dbName):
    try:
        conn = sqlite3.connect(dbName)
        cur = conn.cursor()
        cur.close()
        conn.close()
        etat = "Connexion/Création de la base " + dbName + " effectuée."
        return {"Etat": etat}
    except sqlite3.Error as error:
        return {"Erreur lors de la connexion à SQLite": error}

def checkReponsesTable():
    sqlRequest = "CREATE TABLE IF NOT EXISTS Reponses (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Texte TEXT, isCorrect INTEGER, QUESTION_ID INTEGER)"
    return sqlRequest

def checkQuestionsTable():
    sqlRequest = "CREATE TABLE IF NOT EXISTS Questions (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Position INTEGER NOT NULL, Titre TEXT, Image TEXT, Texte TEXT)"
    return sqlRequest

def checkParticipationsTable():
    sqlRequest = "CREATE TABLE IF NOT EXISTS Participations (ID INTEGER PRIMARY KEY AUTOINCREMENT, PlayerName TEXT, Score INTEGER, Date DATETIME)"
    return sqlRequest