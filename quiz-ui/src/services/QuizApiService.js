import axios from "axios";
import participationStorageService from "@/services/ParticipationStorageService";


const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error("error dans le quizapi : ", error.request.status);
        if (error.request.status == 401) {
          participationStorageService.saveLoginState(2);         // Connexion refusée error 401 --> on passe la variable locale a 2 (= "Veuillez vous reconnecter" affiché dans le HTML)
          window.location.href = "/login";
        }

      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    var urlBaseRequest = "questions?position=";
    var urlRequest = urlBaseRequest.concat('', position);
    return this.call("get", urlRequest);
  },
  getResult(playerName, answers) {
    var data = {
      playerName: playerName,
      answers: answers
    };
    return this.call("post", "participations", data);
  },
  getToken(password) {
    return this.call("post", "login", { password: password });
  },
  deleteQuestionById(questionId, token) {
    var urlBaseRequest = "questions/";
    var urlRequest = urlBaseRequest.concat('', questionId);
    return this.call("delete", urlRequest, questionId, token);
  },
  postAQuestion(payload, token) {
    return this.call('post', "questions", payload, token);
  },
  modifyQuestion(questionId, payload, token) {
    var urlBaseRequest = "questions/";
    var urlRequest = urlBaseRequest.concat('', questionId);
    return this.call('put', urlRequest, payload, token);
  },
  checkAdmin(token) {
    return this.call('post', 'check-admin', token, token);
  },
  deleteAllParticipation(token) {
    return this.call('delete', 'participations/all', token, token);
  },
};