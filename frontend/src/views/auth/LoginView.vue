<template>
  <div>
    <h1>로그인 페이지</h1>

    <form @submit.prevent="handleLogin">
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

  // const logIn = function () {
  //   const payload = {
  //     username: username.value,
  //     email: email.value,
  //     password: password.value,
  //   }
  //   accountStore.logIn(payload)
  //   router.push({ name: 'home' })
  // }

  const handleLogin = async () => {
  try {
    const payload = {
      username: username.value,
      email: email.value,
      password: password.value,
    }
    // 1. 로그인이 끝날 때까지 기다립니다.
    await accountStore.logIn(payload) 
    
    // 2. 다 끝나면 이동합니다.
    router.push({ name: 'home' })
    
  } catch (err) {
    alert('로그인에 실패했습니다.')
  }
}
</script>

<style scoped>

</style>