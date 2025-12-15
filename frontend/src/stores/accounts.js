import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {
  const router = useRouter()
  const API_URL = import.meta.env.VITE_API_URL
  const token = ref(null)

  const signUp = function (payload) {
    const { username, email, password1, password2, nickname, birth } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, email, password1, password2, nickname, birth
      }
    })
      .then(res => {
        console.log('회원가입이 완료되었습니다.')
        const password = password1
        logIn({ username, email, password })
      })
      .catch(err => console.log(err))
  }

  const logIn = function (payload) {
    const { username, email, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, email, password
      }
    })
      .then(res => {
        console.log('로그인이 완료되었습니다.')
        token.value = res.data.key
        router.push({ name: 'home' })
      })
      .catch(err => console.log(err))
  }

  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log('로그아웃이 완료되었습니다.')
        token.value = null
        router.push({ name: 'login'})
      })
      .catch((err) => console.log(err))
  }

  return { 
    API_URL,
    token,
    signUp,
    logIn,
    logOut,
   }
})