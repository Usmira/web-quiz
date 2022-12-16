from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token,decode_token
from questions import DefaultPostQuestion

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
    # 1) Récupération et décodage du token :
    # token = request.headers.get('Authorization')
    ### !!!!! ATTENTION : Comment décoder le token ?? car la fonction decode du jwt ne fonctionne pas...

    # 2) Poster nouvelle question dans la BDD et récupérer ID
    question = request.get_json()
    quest_id = DefaultPostQuestion(question)
    return {"id":quest_id}, 200

if __name__ == "__main__":
    app.run()