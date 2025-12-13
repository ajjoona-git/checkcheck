<template>
  <div>
    <h1>Moathon</h1>
    <nav>
      <RouterLink :to="{ name: 'home' }">HOME</RouterLink> | 
      <RouterLink :to="{ name: 'explore' }">EXPLORE</RouterLink> | 
      <RouterLink :to="{ name: 'create' }">CREATE</RouterLink> | 
      <RouterLink :to="{ name: 'mypage' }">MY PAGE</RouterLink> | 
      <RouterLink :to="{ name: 'login' }">LOGIN</RouterLink> | 
      <RouterLink :to="{ name: 'signup' }">SIGNUP</RouterLink>
    </nav>
    <RouterView />
  </div>
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router';
</script>

<style scoped>

</style>