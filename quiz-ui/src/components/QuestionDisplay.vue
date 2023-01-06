<template>
  <h1>Question n° {{ question.position }}/{{ nbQuestion }}</h1>
  <div class="titre-container">
    <div class="titre-cadre"></div>
    <div class="titre">{{ question.title }}</div>
    <div class="titre-cadre"></div>
  </div>
  <img v-if="question.image" :src="question.image" />
  <div class="text">{{ question.text }} </div>
  <div class="response-container" v-for="(reponse, index) in question.possibleAnswers" v-bind:key="reponse.id">
    <a class="response-link" @click="$emit('answer-selected', index + 1)">{{ reponse.text }}</a>
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
  }
};
</script>

