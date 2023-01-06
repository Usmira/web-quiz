<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="navwrapper">
      <nav>
        <RouterLink to="/" class="nav-element">Home</RouterLink>
        <RouterLink to="/login" class="nav-element">Login</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>

</style>
