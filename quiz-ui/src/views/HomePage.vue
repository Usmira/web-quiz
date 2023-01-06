<template>
  <div class="main-container">
    <div class="main-element">
      <h1>Bienvenue sur Quiz F1</h1>
      <RouterLink to="/start-new-quiz-page" class="start-btn">Démarrer le quiz !</RouterLink>
      <div class="score-container">
        <div class="score-line" v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
          <div class="player-name">
            {{ scoreEntry.playerName }}
          </div>
          <div class="player-score">
            {{ scoreEntry.score }}
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: []
    };
  },
  async created() {
    var quizInfoApiResult = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfoApiResult.data.scores;
  }
};
</script>

<style>

</style>


