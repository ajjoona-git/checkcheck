<template>
  <div>
    <h1>Moathon</h1>
    <Navbar />

    <RouterView />
  </div>
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router';
  import Navbar from './components/common/Navbar.vue';
</script>

<style scoped>

</style>