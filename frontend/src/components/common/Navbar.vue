<template>
  <nav class="navbar navbar-expand-md bg-body-tertiary">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" :to="{ name: 'home' }">
        <img :src="logo" alt="Moathon Logo" class="logo" />
      </RouterLink>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <RouterLink v-if="accountStore.isAuthenticated" class="nav-link" :to="{ name: 'moathonRecommend' }">모아톤 추천받기</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'community' }">모아톤 커뮤니티</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'products' }">예·적금 조회</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'bank' }">은행 위치</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'commodity' }">시세 확인</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'videoSearch' }">유튜브 검색</RouterLink>
        </div>

        <div class="navbar-nav ms-auto">
          <template v-if="!accountStore.isAuthenticated">
            <RouterLink class="nav-link" :to="{ name: 'login' }">로그인</RouterLink>
            <RouterLink class="nav-link" :to="{ name: 'signup' }">회원가입</RouterLink>
          </template>

          <template v-else>
            <RouterLink class="nav-link" :to="{ name: 'mypage' }">프로필</RouterLink>
            <form @submit.prevent="logOut">
              <input type="submit" class="nav-link" value="로그아웃">
            </form>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
  import { RouterLink } from 'vue-router';
  import { useAccountStore } from '@/stores/accounts';
  import logo from '@/assets/logo.svg'

  const accountStore = useAccountStore()
  const logOut = function () {
    accountStore.logOut()
  }
</script>

<style scoped>

</style>