<template>
  <h1>QuestionManager</h1>
  <QuestionDisplay :question="question" :nbQuestion="nbQuestion" @answer-selected="answerClickedHandler" />
</template>

<script>
import QuestionDisplay from '../components/QuestionDisplay.vue';
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";


export default {
  name: "QuestionManager",
  components: {
    QuestionDisplay
  },
  data() {
    return {
      question: {
        position: 1,
        title: "",
        image: "",
        text: "",
        possibleAnswers: []
      },
      nbQuestion: 0
    };
  },
  methods: {
    async loadQuestionByPosition() {
      var getQuestionApiResult = await quizApiService.getQuestion(this.question.position);
      this.question.title = getQuestionApiResult.data.title;
      this.question.image = getQuestionApiResult.data.image;
      this.question.text = getQuestionApiResult.data.text;
      this.question.possibleAnswers = getQuestionApiResult.data.possibleAnswers;
    },
    async answerClickedHandler(answerSelected) {
      // ### 1) stockage de la réponse utilisateur
      console.log("la question selectionnée est :", answerSelected);
      // Doit stocker la dernière réponse donnée (recupération de la liste getParticipationScore() 
      var participationScore = participationStorageService.getParticipationScore();
      // Conversion en Array d'Int pour poouvoir manipuler facilement l'objet
      var participationScoreArray = JSON.parse("[" + participationScore + "]");
      // Modification de la réponse à la position souhaitée
      participationScoreArray[this.question.position - 1] = answerSelected;
      // + ajout de la dernière position + saveParticipationScore(liste_updatée)) 
      participationStorageService.saveParticipationScore(participationScoreArray);
      // ### 2) passage à la question suivante si ce n'est pas la dernière
      if (this.question.position < this.nbQuestion) {
        this.question.position += 1;
        this.loadQuestionByPosition();
      }
      else this.endQuiz();
    },
    async endQuiz() {
      // Cette fonction doit
      this.$router.push('/your-score');
    }
  },
  async created() {
    console.log("Composant QuestionManager 'created'");
    //initialisation de la variable locale hasParticipated à false pour que le score soit pris en compte à la fin du questionnaire
    participationStorageService.saveHasParticipated(false);

    this.loadQuestionByPosition(this.question.position);
    //connaitre le nombre de questions du quiz :

    var quizInfoApiResult = await quizApiService.getQuizInfo();
    this.nbQuestion = quizInfoApiResult.data.size;
    console.log("nb questions", this.nbQuestion);

    // initialisons la variable locale participationScore qui contient la liste des réponses entrées par l'utilisateur
    var participationScore = new Array(this.nbQuestion).fill(0);
    participationStorageService.saveParticipationScore(participationScore);

  }
};
</script>