import json
from sqliteFile import *
from time import strftime
from datetime import datetime as dt

JSON_QUESTION_KEYS = ["title","text","image","position","possibleAnswers"]
JSON_POSSIBLE_ANSWERS_KEYS = ["text","isCorrect"]
JSON_PARTICIPATION_KEYS = ["playerName","answers"]
DB_COLUMNS_LST = ['Position', 'Titre', 'Image', 'Texte']

class Question:
    # Choix de pas mettre id dans l'objet python : car on ne reçoit pas d'ID du python mais de la BDD
    def __init__(self, position:int, title:str, text:str, image:str):
        self.position   = position
        self.title      = title
        self.text       = text
        self.image      = image

class Reponse:
    def __init__(self, text:str, isCorrect:int, questionId:int):
        self.text       = text
        self.isCorrect  = isCorrect
        self.questionId = questionId

def dictTOQuestion(dictPython):
    # On doit distinguer l'objet Question de l'objet Reponse car l'attribut ID_question dans la table Reponse est créé en fonction de la question choisie
    newQuestion = Question(dictPython["position"], dictPython["title"], dictPython["text"], dictPython["image"])
    return newQuestion

def dictToReponses(dictPython,idQuestion):
    answers = dictPython["possibleAnswers"]
    responses = []
    for answer in answers:
        text = answer[JSON_POSSIBLE_ANSWERS_KEYS[0]]
        isCorrect = answer[JSON_POSSIBLE_ANSWERS_KEYS[1]]
        newResponse = Reponse(text,isCorrect,idQuestion)
        responses += [newResponse]
    return responses

def tupleToQuestion(tuple_row):
    returned_question = Question(tuple_row[0],tuple_row[1],tuple_row[2],tuple_row[3])
    return returned_question

def tupleToReponse(tuple_row):
    returned_response = Reponse(tuple_row[1],tuple_row[2],tuple_row[3])
    reponseId = tuple_row[0]
    return reponseId,returned_response

def tuplesTOjsonObject(tuple_question,tuple_answers,questionId):
    json_returned = {}
    # (A) coté question :
    questionObject = tupleToQuestion(tuple_question)
    json_returned["id"]                  = questionId
    json_returned[JSON_QUESTION_KEYS[0]] = questionObject.title
    json_returned[JSON_QUESTION_KEYS[1]] = questionObject.text
    json_returned[JSON_QUESTION_KEYS[2]] = questionObject.image
    json_returned[JSON_QUESTION_KEYS[3]] = questionObject.position
    json_returned[JSON_QUESTION_KEYS[4]] = []
    # (B) coté reponses :
    for answer in tuple_answers:
        reponseId, responseObject = tupleToReponse(answer)
        # Ne pas oublier de convertir les entier 1/0 en boolean True/False
        isCorrect = False
        if responseObject.isCorrect == 1 :
            isCorrect = True
        json_returned[JSON_QUESTION_KEYS[4]] += [{
            JSON_POSSIBLE_ANSWERS_KEYS[0] : responseObject.text,
            JSON_POSSIBLE_ANSWERS_KEYS[1] : isCorrect,
            "id"                          : reponseId  
        }]
    return json.dumps(json_returned,ensure_ascii=False)

def DefaultPostQuestion(jsonQuestion):
    # (1) Vérifier la forme et le contenu du json en voyé en requete) <- à voir si on l'implémente...
    if not isJSONShapeOk(jsonQuestion) :
        return -1

    # 2) Vérifier l'unicité de la bonne réponse
    if not isUniquegoodAnswer(jsonQuestion) :
        print("test2")
        return -1

    # 3) Vérifier la position de la question
    if not checkPosition(jsonQuestion):        
        print("test3")
        return -1                               # Cas de figure à traiter en fonction de l'implémentation voulue en FRONTEND

    # 4) Etapes pour ajouter à la base :
    # A) Transformer JSON en objet Question
    questionObject = dictTOQuestion(jsonQuestion)
    # B) Créer la requête SQL pour l'insérer dans la Table Questions et l'insérer
    sqlInsert = insertINTOQuestion(questionObject)
    insertData(sqlInsert)
    # C) Récupérer l'ID de la question pour la renvoyer à la fin 
    last_id = selectData(getlastID())[0][0]
    # D) Utiliser l'ID récupérée pour transformer le JSON en liste de Reponses
    lstResponses = dictToReponses(jsonQuestion,last_id)
    # E) Création requete SQL pour insérer chaque réponse associée à la Question
    for response in lstResponses:
        sqlInsert = insertINTOResponse(response)
        insertData(sqlInsert)
    return last_id

def isJSONShapeOk(jsonQuestion):
    """
    Cette Fonction permet de vérifier si la forme du json reçu en 
    paramètre est correcte. Cad est-ce qu'il contient les clés nécessaire pour 
    l'enregistrement dans la BDD.
    """
    condition = True
    cnt = 0
    # Test sur les clés de niveau 1 :
    while condition and cnt < len(JSON_QUESTION_KEYS) :
        if JSON_QUESTION_KEYS[cnt] not in jsonQuestion:
            condition = False
        cnt += 1
    if not condition :
        return condition
    else :
        # Test sur les clés de niveau 2 :
        cnt2 = 0
        for answer in jsonQuestion["possibleAnswers"]:
            while condition and cnt2 < len(JSON_POSSIBLE_ANSWERS_KEYS):
                if JSON_POSSIBLE_ANSWERS_KEYS[cnt2] not in answer:
                    condition = False
                cnt2 += 1
            cnt2=0
        return condition

def isUniquegoodAnswer(jsonQuestion):
    # On part du principe qu'on a déjà vérifié que le json avait le bon format
    cnt = 0
    for answer in jsonQuestion["possibleAnswers"]:
        if answer['isCorrect'] :
            cnt += 1
    if cnt == 1 :
        return True
    return False

def checkPosition(jsonQuestion): # add jsonQuestion
    current_pos = jsonQuestion["position"]
    # Cette fonction doit réaliser une query pour vérifier les positions des différentes questions existantes
    # Première chose à vérifier : la position est inférieur ou égale à la taille + 1 de la totalité des questions
    positions = selectData(getAllPositions("Questions"))
    if current_pos > len(positions) + 1:
        # Cas de figure ou la position dépasse le nombre de question après l'insertion de cette dernière
        # On traitera l'erreur plutot dans la fonction DefaultPostQuestion()
        return False
    elif current_pos < 1 :
        # Cas de figure où la position est strictement inférieur à 1 :
        return False
    elif 0 < current_pos <= len(positions) :
        # On est dans le cas où on doit modifier les positions avant d'insérer la question
        SQLRequest = incrementPosition(current_pos)
        insertData(SQLRequest)
    # Pour le dernier cas il ne se passe rien on fait juste un insert classique donc on laisse la fonction DefaultPostQuestion() s'en occuper
    return True

def checkModifiedPosition(questionId,jsonQuestion):
    futur_pos = jsonQuestion["position"]
    old_pos = selectData(get1Position(questionId))[0][0]
    positions = selectData(getAllPositions("Questions"))
    # 1) on doit vérifier que la nouvelle position respecte les règles des positions etablie dans le CDC
    if futur_pos > len(positions) or futur_pos < 1:
        return False
    # 2) ajuster toutes les pos supérieurs à l'ancienne position
    insertData(decIncrementPosition(old_pos))
    # 3) ajuster les pos qui vont passer après la futur_pos
    insertData(incrementPosition(futur_pos))
    return True

def DeleteAllQuestion():
    sqlRequest1, sqlRequest2 = truncateTable("Questions")
    sqlRequest3, sqlRequest4 = truncateTable("Reponses")
    insertData(sqlRequest1)
    insertData(sqlRequest2)
    insertData(sqlRequest3)
    insertData(sqlRequest4)
    return 1

def DeleteAQuestion(questionId):
    # Il faut vérifier que l'ID existe pour cette question
    sqlRequest       = getQuestionByID(questionId)
    current_question = selectData(sqlRequest)
    # Lorsque la question récupérée est vide, on sait qu'il n'y a pas l'ID correspondant dans la base de donnée
    if len(current_question) == 0 :
        # Si la liste est vide, on retourne l'entier -2 qui sera traité dans notre ENDPOINT pour afficher l'erreur 404
        return -2
    # Sinon on traite la modification de la question
    # 1) On ajuste les valeurs des positions suppérieure à la position de la question que l'on va supprimer
    AjustPosition(questionId)
    # 2) Puis on supprime la question en fonction de l'ID selectionné
    sqlRequest = delete1Question(questionId)
    insertData(sqlRequest)
    # 3) on supprime également les réponses associées à cette question dans la table des Reponses
    sqlRequest = deleteResponses(questionId)
    insertData(sqlRequest)
    return 1

def AjustPosition(questionId):
    # 1) On récupère la position de la question que l'on souhaite supprimer
    current_pos = selectData(get1Position(questionId))[0][0]
    # 2) On vérifie s'il existe des questions avec un position supérieur à celle que l'on supprime 
    # Si oui, on ajuste leur position : pos = pos - 1
    sqlRequest = decIncrementPosition(current_pos)
    insertData(sqlRequest)
    return 1

def ModifyAQuestion(questionId,jsonQuestion):
    # Il faut vérifier que l'ID existe pour cette question
    sqlRequest       = getQuestionByID(questionId)
    current_question = selectData(sqlRequest)
    # Lorsque la question récupérée est vide, on sait qu'il n'y a pas l'ID correspondant dans la base de donnée
    if len(current_question) == 0 :
        # Si la liste est vide, on retourne l'entier -2 qui sera traité dans notre ENDPOINT pour afficher l'erreur 404
        return -2
    # Sinon on traite la modification de la question
    #   (A) Vérifier la forme et le contenu du json envoyé en requete) <- à voir si on l'implémente...
    if not isJSONShapeOk(jsonQuestion) :
        return -1
    #   (B) Vérifier l'unicité de la bonne réponse
    if not isUniquegoodAnswer(jsonQuestion) :
        return -1
    #   (C) Vérifier et modifier les valeurs des positions alentours
    if not checkModifiedPosition(questionId,jsonQuestion):
        return -1  
    #   (D) Transformer JSON en objet Question
    questionObject = dictTOQuestion(jsonQuestion)
    #   (E) Update de la question correspondant à l'ID recherché
    sqlRequest = updateQuestionByID(questionId,questionObject)
    insertData(sqlRequest)
    #   (F) Transformer JSON en listes d'objets Reponses
    lstResponses = dictToReponses(jsonQuestion,questionId)
    #   (G) Update des reponses correspondantes à l'ID recherché (on va simplement supprimer les auciennes et ajouter les nouvelles car le changement d'id de la reponse n'a pas d'impact sur le fonctionnement de l'application)
    sqlRequest = deleteResponses(questionId)
    insertData(sqlRequest)
    for response in lstResponses:
        sqlInsert = insertINTOResponse(response)
        insertData(sqlInsert)
    return 1

def getAQuestion(questionId):
    # (1) Récupération de la ligne qui correspond à la question dans la BDD
    sqlRequest       = getQuestionByIDwithoutID(questionId)
    current_question = selectData(sqlRequest)  
    # Lorsque la question récupérée est vide, on sait qu'il n'y a pas l'ID correspondant dans la base de donnée
    if len(current_question) == 0 :
        # Si la liste est vide, on retourne l'entier -2 qui sera traité dans notre ENDPOINT pour afficher l'erreur 404
        return -2
    # (2) Maintenant qu'on est sûr que l'ID existe, il faut transformer les lignes des tables Questions et Reponses en JSON bien formaté
    sqlRequest      = getResponseByQuestionID(questionId)
    current_answers = selectData(sqlRequest)
    jsonObject      = tuplesTOjsonObject(current_question[0],current_answers,questionId)
    return jsonObject

def getIdbyPosition(questionPosition):
    sqlRequest = getIDwithPosition(questionPosition)
    questionId = selectData(sqlRequest)
    return questionId

def defaultPostParticipation(participation):
    #   (1) Vérifier la forme et le contenu du json envoyé en requete)
    if not isJsonParticipationShapeOK(participation):
        return -1
    #   (2) Vérifier la taille de la valeurs associée à la clé answers de la participation (il faut récup le nombre de question dans la table question)
    answers = participation["answers"]
    sqlRequest = getAllPositions("Questions")
    nb_questions = len(selectData(sqlRequest))
    if len(answers) != nb_questions :
        # Si la liste n'est pas de meme taille, on retourne l'entier -2 qui sera traité dans notre ENDPOINT pour afficher l'erreur 404
        return -2
    #   (3) Préparer le résumé des bonnes réponses
    score = 0
    answersSummaries = []
    for Q_pos in range (len(answers)):
        iRep_pos = answers[Q_pos]
        trueRep_pos = whereIsTrueRep(Q_pos + 1)
        wasCorrect = False
        if iRep_pos == trueRep_pos :
            score += 1
            wasCorrect = True
        answersSummaries.append({
            "correctAnswerPosition" : trueRep_pos, 
            "wasCorrect"            : wasCorrect
        })
    playerName = participation["playerName"]
    returned_payload = {"answersSummaries":answersSummaries,"playerName":playerName,"score":score}
    # Calcul de la date à laquelle on poste la réponse :
    date = calcultimenow()
    # On n'oublie pas d'ajouter la participation dans la table Participations
    sqlRequest = addAParticipation(playerName,score,date)
    insertData(sqlRequest)
    return returned_payload

def isJsonParticipationShapeOK(jsonObject):
    condition = True
    cnt = 0
    # Test sur les clés de niveau 1 :
    while condition and cnt < len(JSON_PARTICIPATION_KEYS) :
        if JSON_PARTICIPATION_KEYS[cnt] not in jsonObject:
            condition = False
        cnt += 1
    return condition

def whereIsTrueRep(questionPosition):
    # Pour une question donnée on veut savoir quelle est la position de la réponse dans l'ordre des réponses
    questionId = getIdbyPosition(questionPosition)
    sqlRequest = getResponseByQuestionIDwithoutID(questionId[0][0])
    responses  = selectData(sqlRequest)
    cnt = 0
    condition = True
    responsePosition = 0 # j'initialise la position de la reponse à 0 dans le cas de figure où une question ne comporterait pas de bonne réponse (impossible car on a bien fait attention à ce cas de figure lorsque l'admin poste une nouvelle question)
    while cnt < len(responses) and condition :
        if responses[cnt][1] == 1:
            condition = False
            responsePosition = cnt + 1
        cnt += 1
    return responsePosition

def calcultimenow():
    date =  dt.now()
    return date.strftime("%d/%m/%Y %H-%M-%S")

def DeleteAllParticipation():
    sqlRequest1, sqlRequest2 = truncateTable("Participations")
    insertData(sqlRequest1)
    insertData(sqlRequest2)
    return 1

def quizInfo():
    # On récupère d'abord le nombre de question du quiz
    sqlRequest = getAllPositions("Questions")
    nb_questions = len(selectData(sqlRequest))
    # On forme ensuite le tableau des scores :
    sqlRequest = getAllScoresSorted()
    participations_sorted = selectData(sqlRequest)
    scores = []
    for participation in participations_sorted:
        scores.append({
            "playerName" : participation[0],
            "score"      : participation[1],
            "date"       : participation[2]   
        })
    return {"size":nb_questions,"scores":scores}
