<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="navwrapper">
      <nav>
        <RouterLink to="/" class="nav-sub-element">Accueil</RouterLink>
        <div class="nav-element">
          <RouterLink to="/admin-list-questions" class="nav-sub-element">Page Admin</RouterLink>
          <RouterLink to="/login" class="nav-sub-element">Connexion</RouterLink>
        </div>

      </nav>
    </div>
  </header>
  <RouterView />
</template>

<style scoped>

</style>
