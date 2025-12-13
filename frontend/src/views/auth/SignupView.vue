<template>
  <div>
    <h1>회원가입 페이지</h1>

    <form @submit.prevent="signUp">
      <label for="username">username: </label>
      <input type="text" id="username" v-model.trim="username" /> <br>

      <label for="email">email: </label>
      <input type="email" id="email" v-model.trim="email" /> <br>
      
      <label for="password1">password: </label>
      <input type="password" id="password1" v-model.trim="password1" /> <br>
      
      <label for="password2">password confirmation: </label>
      <input type="password" id="password2" v-model.trim="password2" /> <br>
      
      <label for="nickname">nickname: </label>
      <input type="text" id="nickname" v-model.trim="nickname" /> <br>
      
      <label for="birth">birth: </label>
      <input type="date" id="birth" v-model.trim="birth" /> <br>
      
      <input type="submit" value="signup">
    </form>
  </div>
</template>

<script setup>
  import { useAccountStore } from '@/stores/accounts';
  import { ref } from 'vue';

  const username = ref(null)
  const email = ref(null)
  const password1 = ref(null)
  const password2 = ref(null)
  const nickname = ref(null)
  const birth = ref(null)

  const accountStore = useAccountStore()

  const signUp = function () {
    const payload = { 
      username: username.value, 
      email: email.value, 
      password1: password1.value, 
      password2: password2.value, 
      nickname: nickname.value, 
      birth: birth.value, 
    }
    accountStore.signUp(payload)
  }
</script>

<style scoped>

</style>