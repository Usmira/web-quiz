export default {
  clear() {
    window.localStorage.clear();
  },
  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem("playerName");
  },
  saveParticipationScore(participationScore) {
    window.localStorage.setItem("participationScore", participationScore);
  },
  getParticipationScore() {
    return window.localStorage.getItem("participationScore");
  },
  saveHasParticipated(hasParticipated) {
    window.localStorage.setItem("hasParticipated", hasParticipated);
  },
  getHasParticipated() {
    return window.localStorage.getItem("hasParticipated");
  },
  saveLastScore(lastScore) {
    window.localStorage.setItem("lastScore", lastScore);
  },
  getLastScore() {
    return window.localStorage.getItem("lastScore");
  },
  saveToken(token) {
    window.localStorage.setItem("token", token);
  },
  getToken() {
    return window.localStorage.getItem("token");
  },
  saveCurrentQuestionPosition(currentPosition) {
    window.localStorage.setItem("currentPosition", currentPosition);
  },
  getCurrentQuestionPosition() {
    return window.localStorage.getItem("currentPosition");
  },
  saveLoginState(loginState) {
    window.localStorage.setItem("loginState", loginState);
  },
  getLoginState() {
    return window.localStorage.getItem("loginState");
  },
};