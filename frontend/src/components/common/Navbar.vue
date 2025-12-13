<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="{ name: 'home' }">모아톤</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <RouterLink class="nav-link" :to="{ name: 'home' }">HOME</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'explore' }">EXPLORE</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'mypage' }">MY PAGE</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'create' }">CREATE</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'login' }">LOGIN</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'signup' }">SIGNUP</RouterLink>
          <form @submit.prevent="logOut">
            <input type="submit" class="nav-link" value="LOGOUT">
          </form>
        </div>
      </div>
    </div>
  </nav>
</template> 

<script setup>
  import { RouterLink } from 'vue-router';
  import { useAccountStore } from '@/stores/accounts';

  const accountStore = useAccountStore()
  const logOut = function () {
    accountStore.logOut()
  }
</script>

<style scoped>

</style>