import json
from sqliteFile import *

QUESTION_KEYS = ["title","text","image","position","possibleAnswers"]
POSSIBLE_ANSWERS_KEYS = ["text","isCorrect"]
NB_ANSWERS_MAX = 4 # Nombre max de réponses possibles par question (implémenté car les test postman laissent apparaitre des questions avec 3 réponses seulement)

class Question:
    # Choix de pas mettre id dans l'objet python : car on ne reçoit pas d'ID du python mais de la BDD
    def __init__(self, position:int, title:str, text:str, image:str, answer1:str, answer2:str, answer3:str, answer4:str, trueAnswer:int):
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.a1 = answer1
        self.a2 = answer2
        self.a3 = answer3
        self.a4 = answer4
        self.trueA = trueAnswer

def jsonTOpythonobject(jsonfile):
    pythonobject = json.loads(jsonfile)
    return pythonobject

def pythonobjectTOjson(pythonObject):
    jsonobject = json.dumps(pythonObject.__dict__)
    return jsonobject

def dictTOQuestion(dictPython):
    # On estime que le dictionnaire en entrée est déjà de la bonne forme car cette fonction sera utilisée seulement dans le cadre
    # de la fonction DefaultPostQuestion()
    # 1) Recherche de la bonne réponse parmis les 4 réponses possibles : 
    answers = dictPython["possibleAnswers"]
    trueA = 0
    for i in range (len(answers)):
        if answers[i]["isCorrect"]:
            trueA = i + 1
    # 2) Mapping des clés du dictionnaire avec les attributs de la classe Question :
    cond, lst_txt_answers = answersGoodSize(answers)
    if cond :
        returnedQuestion = Question(dictPython["position"], dictPython["title"], dictPython["text"], dictPython["image"], lst_txt_answers[0], lst_txt_answers[1], lst_txt_answers[2], lst_txt_answers[3],trueA)
    else :
        returnedQuestion = Question(dictPython["position"], dictPython["title"], dictPython["text"], dictPython["image"], answers[0]["text"], answers[1]["text"], answers[2]["text"], answers[3]["text"],trueA)
    return returnedQuestion

def answersGoodSize(answers):
    """
    L'objectif de cette méthode est de vérifier que le dictionnaire des réponses possibles à la
    question est bien de la bonne taille (NB_ANSWERS_MAX du Cahier des Charges)
    Cette fonction renvoie donc la liste de tous les text de reponse en complétant avec des string 
    vides si la taille initilale est plus petite que la taille voulue.
    """
    cond = False
    lst_txt_answers = []
    if len(answers) < NB_ANSWERS_MAX:
        cond = True
        # 1) On rempli la liste avec toutes les réponses déjà existantes
        for i in range (len(answers)):
            lst_txt_answers += [answers[i]["text"]]
        # 2) on complète la liste avec des réponse par défaut vides
        for j in range (NB_ANSWERS_MAX - len(answers)):
            lst_txt_answers += [""]
    return cond,lst_txt_answers
    

def DefaultPostQuestion(jsonQuestion):
    # (1) Vérifier la forme et le contenu du json en voyé en requete) <- à voir si on l'implémente...
    if not isJSONShapeOk(jsonQuestion) :
        return -1

    # 2) Vérifier l'unicité de la bonne réponse
    if not isUniquegoodAnswer(jsonQuestion) :
        return -1

    # 3) Vérifier la position de la question
    if not checkPosition(jsonQuestion):
        return -1                               # Cas de figure à traiter en fonction de l'implémentation voulue en FRONTEND

    # 4) Etapes pour ajouter à la base :
    # A) Transformer JSON en objet Question
    questionObject = dictTOQuestion(jsonQuestion)
    # B) Créer requete à partir de cet objet
    sqlInsert = createSQLRequestInsert(questionObject)
    # C) Inserer dans la BDD
    insertData(sqlInsert)
    # D) En finalité, la requete doit renvoyer l'ID de la question récement insérée :
    last_id = selectData(getlastID())[0][0]
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
    while condition and cnt < len(QUESTION_KEYS) :
        if QUESTION_KEYS[cnt] not in jsonQuestion:
            condition = False
        cnt += 1
    if not condition :
        return condition
    else :
        # Test sur les clés de niveau 2 :
        cnt2 = 0
        for answer in jsonQuestion["possibleAnswers"]:
            while condition and cnt2 < len(POSSIBLE_ANSWERS_KEYS):
                if POSSIBLE_ANSWERS_KEYS[cnt2] not in answer:
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
    elif current_pos <= len(positions) :
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
    if futur_pos > len(positions):
        return False
    # 2) ajuster toutes les pos supérieurs à l'ancienne position
    insertData(decIncrementPosition(old_pos))
    # 3) ajuster les pos qui vont passer après la futur_pos
    insertData(incrementPosition(futur_pos))
    return True

def DeleteAllQuestion():
    sqlRequest1, sqlRequest2 = truncateTable()
    insertData(sqlRequest1)
    insertData(sqlRequest2)
    return 1

def DeleteAQuestion(questionId):
    # Il faut vérifier que l'ID existe pour cette question
    sqlRequest = getQuestionByID(questionId)
    current_question = selectData(sqlRequest)
    # Lorsque la question récupérée est vide, on sait qu'il n'y a pas l'ID correspondant dans la base de donnée
    if len(current_question) == 0 :
        # Si la liste est vide, on retourne l'entier -1 qui sera traité dans notre ENDPOINT pour afficher l'erreur 404
        return -2
    # Sinon on traite la modification de la question
    # 1) On ajuste les valeurs des positions suppérieure à la position de la question que l'on va supprimer
    AjustPosition(questionId)
    # 2) Puis on supprime la question en fonction de l'ID selectionné
    sqlRequest = delete1Question(questionId)
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
    sqlRequest = getQuestionByID(questionId)
    current_question = selectData(sqlRequest)
    # Lorsque la question récupérée est vide, on sait qu'il n'y a pas l'ID correspondant dans la base de donnée
    if len(current_question) == 0 :
        # Si la liste est vide, on retourne l'entier -1 qui sera traité dans notre ENDPOINT pour afficher l'erreur 404
        return -2
    # Sinon on traite la modification de la question
    #   (A) Vérifier la forme et le contenu du json en voyé en requete) <- à voir si on l'implémente...
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
    return 1

