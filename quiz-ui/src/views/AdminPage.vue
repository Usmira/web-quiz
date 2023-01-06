<template>
  <div class="main-container">
    <div class="main-element">
      <h1>Gestionnaire de questions</h1>
      <button class="start-btn" @click="deleteAllParticipation">Supprimer participations</button>
      <div @click="detailQuestion(index + 1)" class="score-line" v-for="(question, index) in questions"
        v-bind:key="question.id">
        {{ question.position }} - {{ question.title }}
      </div>
      <button class="start-btn" @click="createNewQuestion">Créer une question</button>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "AdminPage",
  data() {
    return {
      nbQuestion: 0,
      questions: []
    }
  },
  methods: {
    async loadQuestionByPosition(position) {
      var getQuestionApiResult = await quizApiService.getQuestion(position);

      var question = {
        id: getQuestionApiResult.data.id,
        title: getQuestionApiResult.data.title,
        position: getQuestionApiResult.data.position
      };
      return question;
    },
    async detailQuestion(position) {
      //on enregistre la position dans une variable locale (car je galère avec les emits):
      participationStorageService.saveCurrentQuestionPosition(position)
      this.$router.push('/admin-detail-question');
    },
    createNewQuestion() {
      this.$router.push('/create-new-question');
    },
    async deleteAllParticipation() {
      var token = participationStorageService.getToken();
      return await quizApiService.deleteAllParticipation(token);
    },
    async tryAdmin() {
      var token = participationStorageService.getToken();
      return await quizApiService.checkAdmin(token);
    }
  },
  async created() {
    this.tryAdmin();

    var quizInfoApiResult = await quizApiService.getQuizInfo();
    this.nbQuestion = quizInfoApiResult.data.size;

    // on veut charger les questions dans notre variable question
    this.questions = new Array(this.nbQuestion).fill(0)
    for (let step = 0; step < this.nbQuestion; step++) {
      this.questions[step] = await this.loadQuestionByPosition(step + 1);
    };


  }
}
</script>