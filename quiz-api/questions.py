import json
from sqliteFile import *

QUESTION_KEYS = ["title","text","image","position","possibleAnswers"]
POSSIBLE_ANSWERS_KEYS = ["text","isCorrect"]

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
    returnedQuestion = Question(dictPython["position"], dictPython["title"], dictPython["text"], dictPython["image"], answers[0]["text"], answers[1]["text"], answers[2]["text"], answers[3]["text"],trueA)
    return returnedQuestion


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
    insertion_result = insertData(sqlInsert)
    # D) En finalité, la requete doit renvoyer l'ID de la question récement insérée :
    last_id = selectData(getID())[0][0]
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
    positions = selectData(getPositions("Questions"))
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