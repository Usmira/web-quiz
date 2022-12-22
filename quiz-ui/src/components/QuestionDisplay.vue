<template>
  <h1>Question n° {{ question.position }}/{{ nbQuestion }}</h1>
  <p>Titre : {{ question.title }}</p>
  <img v-if="question.image" :src="question.image" />
  <p>Texte : {{ question.text }} </p>
  <p>Réponses :</p>
  <div v-for="(reponse, index) in question.possibleAnswers" v-bind:key="reponse.id">
    <a @click="$emit('answer-selected', index + 1)"> {{ index + 1 }}) {{ reponse.text }}</a>
  </div>
</template>

<script>

export default {
  name: "QuestionDisplay",
  emits: ["answer-selected"],
  props: {
    question: {
      type: Object
    },
    nbQuestion: {
      type: Number
    }
  },
  async created() {
    console.log("Composant QuestionDisplay 'created'");
  }
};
</script>

