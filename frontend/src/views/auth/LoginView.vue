<template>
  <div>
    <h1>로그인 페이지</h1>

    <form @submit.prevent="logIn">
      <label for="username">username: </label>
      <input type="text" id="username" v-model.trim="username" /> <br>

      <label for="password">password: </label>
      <input type="password" id="password" v-model.trim="password" /> <br>

      <input type="submit" value="LogIn" />
    </form>
  </div>
</template>

<script setup>
  import { ref } from 'vue';
  import { useAccountStore } from '@/stores/accounts';

  const username = ref(null)
  const password = ref(null)

  const accountStore = useAccountStore()

  const logIn = function () {
    const payload = {
      username: username.value,
      password: password.value,
    }
    accountStore.logIn(payload)
  }
</script>

<style scoped>

</style>