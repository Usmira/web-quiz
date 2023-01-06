<template>
  <div class="main-container">
    <div class="main-element">
      <h1>Démarrer le Quiz</h1>
      <p>Veuillez saisir votre pseudo</p>
      <input class="name-input" type="text" v-model="username" />
      <button class="start-btn" @click="launchNewQuiz">GO!</button>
    </div>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "NewQuizPage",
  data() {
    return {
      username: ''
    };
  },
  methods: {
    launchNewQuiz() {
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    },
  },
  async created() {
  }
};
</script>