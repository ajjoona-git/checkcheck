<template>
  <div>
    <h1>로그인 페이지</h1>

    <form @submit.prevent="logIn">
      <label for="username">이름: </label>
      <input type="text" id="username" v-model.trim="username" /> <br>

      <label for="email">이메일: </label>
      <input type="email" id="email" v-model.trim="email" /> <br>

      <label for="password">비밀번호: </label>
      <input type="password" id="password" v-model.trim="password" /> <br>

      <input type="submit" value="LogIn" />
    </form>
  </div>
</template>

<script setup>
  import { ref } from 'vue';
  import { useAccountStore } from '@/stores/accounts';
  import { useRouter } from 'vue-router';

  const username = ref(null)
  const email = ref(null)
  const password = ref(null)

  const accountStore = useAccountStore()
  const router = useRouter()

  const logIn = function () {
    const payload = {
      username: username.value,
      email: email.value,
      password: password.value,
    }
    accountStore.logIn(payload)
    router.push({ name: 'home' })
  }
</script>

<style scoped>

</style>