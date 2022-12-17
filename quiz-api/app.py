from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token,decode_token
from questions import DefaultPostQuestion, DeleteAllQuestion, DeleteAQuestion

AUTH_PASSWORD = "flask2023"

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    result = "hello world"
    return {"result":result}

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200

@app.route('/login', methods=["POST"])
def PostPassword():
    payload = request.get_json()
    if payload["password"] == AUTH_PASSWORD: #On teste ici si le password est celui voulu (voir password test de postman)
        # Il faut générer un token ici grâce à la librairie importée sur blackboard
        token = build_token()
        return {"token": token}
    else:
        return 'Unauthorized', 401

@app.route('/questions',methods=['POST'])
def PostQuestion():
    # 1) Try/except sur la récupération et le décodage du token :
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      # Le token possède un préfixe qu'il faut supprimer pour pouvoir le décoder
        decode_token(token)                        
        # 2) Poster nouvelle question dans la BDD et récupérer ID
        question = request.get_json()
        quest_id = DefaultPostQuestion(question)
        return {"id":quest_id}, 200
    except:
        # 2) Connexion refusée par le serveur
        return 'Unauthorized', 401
    
@app.route('/questions/all',methods=['DELETE'])
def DeleteAllQuestions():
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      # Le token possède un préfixe qu'il faut supprimer pour pouvoir le décoder
        decode_token(token)  
        DeleteAllQuestion()
        return {} ,204
    except:
        return 'Unauthorized', 401

@app.route('/questions/<questionId>',methods = ['DELETE'])
def DeleteQuestionByID(questionId):
    try:
        beared_token = request.headers.get('Authorization')
        token = beared_token.split(" ")[1]                      # Le token possède un préfixe qu'il faut supprimer pour pouvoir le décoder
        decode_token(token) 
        DeleteAQuestion(questionId)
        return {}, 204
    except:
        return 'Unauthorized', 401

if __name__ == "__main__":
    app.run()