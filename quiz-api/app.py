from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token


AUTH_PASSWORD = "flask2023"

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Hello world"

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

if __name__ == "__main__":
    app.run()