import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {
  const router = useRouter()
  const API_URL = import.meta.env.VITE_API_URL

  const user = ref(null)
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
        router.push({ name: 'onboarding' })
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
      .then(async res => {
        console.log('로그인이 완료되었습니다.')
        token.value = res.data.key
        await getProfile()
      })
      .catch(err => console.log(err))
  }

  const getProfile = async () => {
    if (!token.value) return

    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      
      user.value = response.data
      console.log('유저 정보 로드 완료:', user.value)
      return response.data
    } catch (error) {
      console.error('유저 정보 로드 실패:', error)
      throw error
    }
  }

  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: { Authorization: `Token ${token.value}` }
    })
      .then((res) => {
        console.log('로그아웃이 완료되었습니다.')
        token.value = null
        user.value = null
        router.push({ name: 'login'})
      })
      .catch((err) => console.log(err))
  }

  const isAuthenticated = computed(() => {
    return token.value ? true : false
  })

  const updateProfile = async (payload) => {
    try {
      const response = await axios({
        method: 'put',
        url: `${API_URL}/accounts/onboarding/`,
        data: payload,
        headers: {
          Authorization: `Token ${token.value}`,
          'Content-Type': 'multipart/form-data'
        }
      })

      console.log('온보딩 정보 저장 완료:', response.data)
      await getProfile()

      return response.data
    } catch (error) {
      console.error('온보딩 저장 실패:', error)
      throw error
    }
  }

  const followUser = async (targetId) => {
    try {
      const res = await axios({
        method: 'post',
        url: `${API_URL}/accounts/${targetId}/follow/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      return res.data
    } catch (err) {
      console.error('팔로우 요청 실패:', err)
      alert('팔로우 요청 중 오류가 발생했습니다.')
      throw err
    }
  }

  return { 
    API_URL,
    token,
    user,
    signUp,
    logIn,
    logOut,
    getProfile,
    isAuthenticated,
    updateProfile,
    followUser,
   }
}, {
  persist: {
    paths: ['token', 'user']
  }
})