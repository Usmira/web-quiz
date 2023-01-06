<template>
  <div class="main-container">
    <div class="main-element">
      <h1>Login as Admin</h1>
      <p>password</p>
      <input class="name-input" type="password" v-model="password" />
      <div>{{ message }}</div>
      <button class="start-btn" @click="loginAsAdmin">Log In</button>

    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "LoginPage",
  data() {
    return {
      password: '',
      message: '',
    };
  },
  methods: {
    async loginAsAdmin() {
      try {
        var token = await quizApiService.getToken(this.password);
        participationStorageService.saveToken(token.data.token);
        participationStorageService.saveLoginState(0);         // bon mot de passe --> on remet la variable locale a 0 (= pas de message affiché lors du prochain chargement de page)
        this.$router.push('/admin-list-questions');
      } catch {
        participationStorageService.saveLoginState(1);         // Mauvais mot de passe --> on passe la variable locale a 1 (= "Mauvais mot de passe" affiché dans le HTML)
      }
    }
  },
  async created() {
    var loginState = participationStorageService.getLoginState();
    if (loginState == 0) {
      this.message = ''
    } else if (loginState == 1) {
      this.message = "Mauvais mot de passe"
    } else if (loginState == 2) {
      this.message = "Session expirée, veuillez vous reconnecter"
    }
  }
};
</script>