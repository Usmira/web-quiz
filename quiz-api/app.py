from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token,decode_token
from questions import quizInfo, DefaultPostQuestion, DeleteAllQuestion,DeleteAQuestion,ModifyAQuestion, getAQuestion, getIdbyPosition, defaultPostParticipation, DeleteAllParticipation
from rebuild import rebuildBDD

AUTH_PASSWORD = "flask2023"

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    result = "hello world"
    return {"result":result}

@app.route('/rebuild-db', methods=['POST'])
def rebuildDB():
    # 1) Try/except sur la récupération et le décodage du token :
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      # Le token possède un préfixe qu'il faut supprimer pour pouvoir le décoder
        decode_token(token)                        
    except:
        # 2) Connexion refusée par le serveur
        return 'Unauthorized', 401
    rebuildBDD()
    return 'Ok', 200

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    payload_returned = quizInfo()
    return payload_returned, 200

@app.route('/check-admin',methods=["POST"])
def checkAdmin():
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      
        decode_token(token)   
        return 'Ok', 200               
    except:
        return 'Unauthorized', 401

@app.route('/login', methods=["POST"])
def PostPassword():
    payload = request.get_json()
    if payload["password"] == AUTH_PASSWORD: #On teste ici si le password est celui voulu (voir password test de postman)
        # Il faut générer un token ici grâce à la librairie importée sur blackboard
        token = build_token()
        return {"token": token},200
    else:
        return 'Unauthorized', 401

@app.route('/questions',methods=['POST'])
def PostQuestion():
    # 1) Try/except sur la récupération et le décodage du token :
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      # Le token possède un préfixe qu'il faut supprimer pour pouvoir le décoder
        decode_token(token)                  
    except:
        # 2) Connexion refusée par le serveur
        return 'Unauthorized', 401
    # 2) Poster nouvelle question dans la BDD et récupérer ID
    question = request.get_json()
    quest_id = DefaultPostQuestion(question)
    return {"id":quest_id}, 200                             # pas oublier de gérer le cas position trop grande par rapport au nombre de questions

    
@app.route('/questions/all',methods=['DELETE'])
def DeleteAllQuestions():
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      # Le token possède un préfixe qu'il faut supprimer pour pouvoir le décoder
        decode_token(token)  
    except:
        return 'Unauthorized', 401
    DeleteAllQuestion()
    return {} ,204

@app.route('/questions/<questionId>',methods = ['DELETE'])
def DeleteQuestionByID(questionId):
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      # Le token possède un préfixe qu'il faut supprimer pour pouvoir le décoder
        decode_token(token) 
    except:
        return 'Unauthorized', 401
    result = DeleteAQuestion(questionId)
    if result == -2 :                                       # pas oublier de gérer le cas position trop grande par rapport au nombre de questions
        return 'Not Found', 404
    return {}, 204

@app.route('/questions/<questionId>',methods=["PUT"])
def ModifyQuestionByID(questionId):
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      # Le token possède un préfixe qu'il faut supprimer pour pouvoir le décoder
        decode_token(token) 
    except:
        return 'Unauthorized', 401
    question = request.get_json()
    result = ModifyAQuestion(questionId,question)
    if result == -2 :                                       # pas oublier de gérer le cas position trop grande par rapport au nombre de questions
        return 'Not Found', 404
    return {}, 204

@app.route('/questions/<questionId>', methods=['GET'])
def getQuestionByID(questionId):
    jsonQuestion = getAQuestion(questionId)
    if jsonQuestion == -2 :                                       # pas oublier de gérer le cas position trop grande par rapport au nombre de questions
        return 'Not Found', 404
    return jsonQuestion, 200

@app.route('/questions', methods=['GET'])
def getQuestionByPosition():
    position = request.args.get('position')
    questionId = getIdbyPosition(position)
    if len(questionId) == 0 :
        return 'Not Found' , 404
    jsonQuestion = getAQuestion(questionId[0][0])
    return jsonQuestion, 200

@app.route('/participations', methods=['POST'])
def postParticipation():
    participation = request.get_json()
    payload_retour = defaultPostParticipation(participation)
    if payload_retour == -2 :
        return 'Bad request', 400
    return payload_retour ,200

@app.route('/participations/all', methods=['DELETE'])
def deleteAllParticipations():
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      # Le token possède un préfixe qu'il faut supprimer pour pouvoir le décoder
        decode_token(token)  
    except:
        return 'Unauthorized', 401   
    DeleteAllParticipation()
    return {}, 204

if __name__ == "__main__":
    app.run()