<template>
  <div>
    <Navbar />

    <RouterView class="content" />

    <Footer />
  </div>
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router';
  import Navbar from '@/components/common/Navbar.vue';
  import Footer from '@/components/common/Footer.vue';
</script>

<style scoped>
.content {
  min-height: calc(100vh - 240px); /* Navbar + Footer 높이 제외 */
}
</style>