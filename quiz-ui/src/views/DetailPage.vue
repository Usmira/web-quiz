<template>
  <div class="main-container">
    <div class="main-element">
      <h1>
        Affichage de la Question n°{{ position }}
      </h1>
      <div class="titre-container">
        <div class="titre-cadre"></div>
        <div class="titre">{{ question.title }}</div>
        <div class="titre-cadre"></div>
      </div>
      <div class="text">{{ question.text }} {{ question.id }} </div>
      <div class="response-edition-container" v-for="(reponse, index) in question.possibleAnswers"
        v-bind:key="reponse.id">
        <div v-if="reponse.isCorrect" class="response-edition-true-item">{{ reponse.text }}</div>
        <div v-else class="response-edition-false-item">{{ reponse.text }}</div>
      </div>
      <div>
        <button class="start-btn" @click="modifyQuestion">Éditer</button>
        <button class="start-btn" @click="deleteQuestion">Supprimer</button>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "DetailPage",
  data() {
    return {
      position: 0,
      question: {
        id: 0,
        title: "",
        text: "",
        possibleAnswers: []
      },
    }
  },
  methods: {
    modifyQuestion() {
      this.$router.push('/edit-question');
    },
    async deleteQuestion() {
      //recupértion du token local:
      var token = participationStorageService.getToken();
      var returnedAPIRequest = await quizApiService.deleteQuestionById(this.question.id, token);

      this.$router.push('/admin-list-questions');
    },
    async tryAdmin() {
      var token = participationStorageService.getToken();
      return await quizApiService.checkAdmin(token);
    },
  },
  async created() {
    this.tryAdmin();

    this.position = participationStorageService.getCurrentQuestionPosition();
    //await loadQuestionByPosition(this.position);
    var questionAPIResult = await quizApiService.getQuestion(this.position);
    this.question.id = questionAPIResult.data.id;
    this.question.title = questionAPIResult.data.title;
    this.question.text = questionAPIResult.data.text;
    this.question.possibleAnswers = questionAPIResult.data.possibleAnswers;

  }
}
</script>