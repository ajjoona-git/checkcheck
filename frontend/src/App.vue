<template>
  <div>
    <Navbar />

    <RouterView class="content" />

    <Footer />
  </div>
</template>

<script setup>
// 앱의 전체 레이아웃 구성 (네비게이션, 라우터, 푸터)
import { RouterView } from 'vue-router';
import Navbar from '@/components/common/Navbar.vue';
import Footer from '@/components/common/Footer.vue';
</script>

<style scoped>
.content {
  min-height: calc(100vh - 240px);
}
</style>