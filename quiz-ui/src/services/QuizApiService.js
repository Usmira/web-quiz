import axios from "axios";

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
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    var urlBaseRequest = "questions?position="
    var urlRequest = urlBaseRequest.concat('', position);
    return this.call("get", urlRequest);
  },
  getResult(playerName, answers) {
    var data = {
      playerName: playerName,
      answers: answers
    };
    return this.call("post", "participations", data);
  }
};