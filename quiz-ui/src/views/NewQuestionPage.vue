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
      <div>Upload Image</div>
      <!-- <div>
        <input type="file" @change="uploadFile" ref="file">
        <button @click="submitFile">Upload!</button>
      </div> -->
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
      //images: null,

      answersForm: 0,
      correctAnswer: 0,
      newQuestion: {
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
      var returnedRequest = await quizApiService.postAQuestion(payload, token);
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
    async tryAdmin() {
      var token = participationStorageService.getToken();
      return await quizApiService.checkAdmin(token);
    },
    // //pour upload un fichier
    // uploadFile() {
    //   this.Images = this.$refs.file.files[0];
    // },
    // submitFile() {
    //   const formData = new FormData();
    //   formData.append('file', this.Images);
    //   const headers = { 'Content-Type': 'multipart/form-data' };
    //   axios.post('https://httpbin.org/post', formData, { headers }).then((res) => {
    //     res.data.files; // binary representation of the file
    //     res.status; // HTTP status
    //   });
    // }
  },
  async created() {
    this.tryAdmin();
  }
}
</script> 