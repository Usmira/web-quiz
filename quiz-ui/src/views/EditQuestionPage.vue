<template>
  <div class="main-container">
    <div class="main-element">
      <h1>Création d'une nouvelle question</h1>
      <div class="form-item">
        <div>Position : </div>
        <input class="position-input" type="number" v-model="newQuestion.position" />
      </div>
      <div class="form-item">
        <div>Titre : </div>
        <input class="title-input" type="text" v-model="newQuestion.title" />
      </div>
      <div class="form-item">
        <div>Intitulé de la question : </div>
        <textarea class="text-input" type="text" v-model="newQuestion.text"></textarea>
      </div>

      <div class="upload-image-container">
        <input type="file" id="file" accept="image/jpeg, image/png, image/jpg" @click="newImage">
        <img id="image" :src="newQuestion.image">
      </div>

      <div>Réponses possibles :</div>
      <div class="create-a-response-container" v-for="(reponse, index) in answersForm">
        <div class="answer-form-item">
          <button v-if="correctAnswer == index" class="checkbox-btn-true" @click="checkboxFunction(index)">V</button>
          <button v-else="" class="checkbox-btn-false" @click="checkboxFunction(index)">F</button>
          <input class="answer-input" type="text" v-model="newQuestion.possibleAnswers[index]" />
          <button v-if="index == answersForm - 1" class="delete-btn" @click="deleteResponse">-</button>
        </div>
      </div>
      <button class="add-btn" @click="addResponse">Ajouter une réponse</button>
      <div>
        <button class="start-btn" @click="saveQuestion">Sauvegarder</button>
        <button class="start-btn" @click="cancel">Annuler</button>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "NewQuestionPage",
  data() {
    return {
      answersForm: 0,
      correctAnswer: 0,
      newQuestion: {
        id: null,
        position: null,
        title: null,
        text: null,
        image: "",
        possibleAnswers: []
      },
      answersBoolean: []
    }
  },
  methods: {
    async saveQuestion() {
      //fonction qui doit post la nouvelle question
      //on prépare d'abord la data :
      var possibleAnswers = []
      for (var i = 0; i < this.answersBoolean.length; i++) {
        possibleAnswers.push({
          text: this.newQuestion.possibleAnswers[i],
          isCorrect: this.answersBoolean[i]
        })
      }
      var payload = {
        title: this.newQuestion.title,
        text: this.newQuestion.text,
        image: this.newQuestion.image,
        position: this.newQuestion.position,
        possibleAnswers: possibleAnswers
      }
      //on appelle la méthode correspondante dans l'API
      var token = participationStorageService.getToken();
      var returnedRequest = await quizApiService.modifyQuestion(this.newQuestion.id, payload, token);
      //on redirige l'admin sur la page qui liste les questions
      this.$router.push('/admin-list-questions');
    },
    cancel() {
      this.$router.push('/admin-list-questions');
    },
    addResponse() {
      this.answersForm += 1;
      this.resetAnswersBoolean(this.correctAnswer);
    },
    deleteResponse() {
      this.answersForm -= 1;
      if (this.correctAnswer >= this.answersForm) {
        this.correctAnswer = 0;
      }
      this.resetAnswersBoolean(this.correctAnswer)
      if (this.newQuestion.possibleAnswers.length > this.answersForm) {
        this.newQuestion.possibleAnswers.pop()
      }
    },
    checkboxFunction(index) {
      this.correctAnswer = index;
      this.resetAnswersBoolean(index);
    },
    resetAnswersBoolean(index) {
      this.answersBoolean = []
      for (var i = 0; i < this.answersForm; i++) {
        this.answersBoolean.push(false);
      }
      this.answersBoolean[index] = true;
    },
    newImage() {
      //fonction pour venir récupérer l'image uploadé et l'afficher sur la page html
      const file = document.querySelector("#file")
      file.addEventListener("change", () => {
        const reader = new FileReader()

        reader.addEventListener("load", () => {  // Utilisation d'une arrow function pour hériter de this de ma composante
          // Vérifions si reader.result est défini et valide
          if (reader.result) {
            this.newQuestion.image = reader.result
            document.querySelector("#image").src = this.newQuestion.image
          }
        });
        reader.readAsDataURL(file.files[0])
      });
    },
    async tryAdmin() {
      var token = participationStorageService.getToken();
      return await quizApiService.checkAdmin(token);
    },
  },
  async created() {
    this.tryAdmin();

    //recupération des infos de la questions
    var position = await participationStorageService.getCurrentQuestionPosition()
    var requestAPIresult = await quizApiService.getQuestion(position);
    this.newQuestion.id = requestAPIresult.data.id;
    this.newQuestion.position = requestAPIresult.data.position;
    this.newQuestion.title = requestAPIresult.data.title;
    this.newQuestion.text = requestAPIresult.data.text;
    this.newQuestion.image = requestAPIresult.data.image;
    //gestion des answers :
    // d'abord connaitre le nombre de reponse pour créer les espaces sur le front
    var nbAnswers = requestAPIresult.data.possibleAnswers.length;
    this.answersForm = nbAnswers;
    //remplir les deux listes qui correspondent au bon affichage des réponses :

    for (var i = 0; i < this.answersForm; i++) {
      this.newQuestion.possibleAnswers.push(requestAPIresult.data.possibleAnswers[i].text);
      if (requestAPIresult.data.possibleAnswers[i].isCorrect) {
        this.answersBoolean.push(true);
        this.correctAnswer = i
      } else {
        this.answersBoolean.push(false);
      }
    }
  }
}
</script> 