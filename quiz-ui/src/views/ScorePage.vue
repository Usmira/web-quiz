<template>
  <div class="main-container">
    <div class="main-element">
      <h1>Scores</h1>
      <div>
        <p>Pseudo : {{ playerName }}</p>
      </div>
      <div>
        <p>Résultat du quiz : {{ score }} </p>
      </div>
      <button class="start-btn" @click="returnHome">Home</button>
      <div>
        <p>Classement général</p>
        <div class="score-container">
          <div class="score-line-titre">
            <div class="position-titre">
              Position
            </div>
            <div class="player-name-tire">
              Pseudo
            </div>
            <div class="player-score-titre">
              Score
            </div>
          </div>
          <div class="score-line" v-for="(scoreEntry, index) in registeredScores" v-bind:key="scoreEntry.date">
            <div class="position">
              {{ index + 1 }}e
            </div>
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
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";


export default {
  name: "ScorePage",
  data() {
    return {
      playerName: "",
      score: 0,
      registeredScores: []
    }
  },
  methods: {
    returnHome() {
      // route to home
      this.$router.push('/');
    },
    async getScores() {
      var quizInfoApiResult = await quizApiService.getQuizInfo();
      this.registeredScores = quizInfoApiResult.data.scores;
    }
  },
  async created() {
    // ATTENTION !!!  si on laisse ainsi, à chaque actualisation de page on sauvegarde un nouveau score identique
    //calcul du score du joueur :
    // on récupère la liste des réponses et le nom du joueur stockés en variables locales
    var playerName = participationStorageService.getPlayerName();
    var participationScore = participationStorageService.getParticipationScore();
    // Conversion en Array d'Int
    var participationScoreArray = JSON.parse("[" + participationScore + "]");

    //Test du booléen hasParticipated : si false => on enregistre le score, et on l'affiche; si true => on affiche seulement le score
    var hasParticipated = participationStorageService.getHasParticipated();
    if (hasParticipated == "false") {
      // envoie de la requete à l'API :
      var endParticipation = await quizApiService.getResult(playerName, participationScoreArray);
      this.playerName = endParticipation.data.playerName;
      this.score = endParticipation.data.score;
      participationStorageService.saveLastScore(this.score);
    } else {
      this.playerName = participationStorageService.getPlayerName();
      this.score = participationStorageService.getLastScore();
    };
    //supprimer les scores du joueurs : il faut repasser par la question 1 pour effectuer le quiz et avoir un résultat
    participationStorageService.saveHasParticipated(true);
    this.getScores();

  }
};
</script>