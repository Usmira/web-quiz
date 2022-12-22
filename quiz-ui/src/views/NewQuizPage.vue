<template>
  <h1>New Quiz Page</h1>
  <p>Saisissez votre nom</p>
  <input type="text" v-model="username" />
  <button @click="launchNewQuiz">GO!</button>
</template>

<script>
// import quizApiService from "@/services/QuizApiService";
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
      console.log("Launch new quiz with", this.username);
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    },
  },
  async created() {
    console.log("Composant NewQuizPage 'created'");
  }
};
</script>