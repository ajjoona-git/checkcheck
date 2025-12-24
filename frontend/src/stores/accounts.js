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

  const logIn = async function (payload) { 
    const { username, email, password } = payload

    try {
      const res = await axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: { username, email, password }
      })
      console.log('로그인 성공, 토큰 저장 중...')

      const newToken = res.data.key
      token.value = newToken
      localStorage.setItem('token', newToken) 
      await getProfile()
    } catch (err) {
      console.error('로그인 에러:', err)
      throw err
    }
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

  const logOut = async function () {
    try {
      // 1. 백엔드에 로그아웃 요청 (토큰 블랙리스트 처리 등)
      // 토큰이 없다면 요청을 보낼 필요도 없음
      if (token.value) {
        await axios({
          method: 'post',
          url: `${API_URL}/accounts/logout/`,
          headers: {
            Authorization: `Token ${token.value}`
          }
        })
        console.log('백엔드 로그아웃 성공')
      }
    } catch (err) {
      // 2. 401 에러가 나더라도(이미 만료됨 등) 프론트에서는 무시하고 진행
      console.warn('백엔드 로그아웃 실패(무시하고 진행):', err)
    } finally {
      // 3. [핵심] 성공하든 실패하든 프론트엔드 정보는 무조건 삭제
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      console.log('프론트엔드 상태 초기화 완료')
    }
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

  const editProfile = async (payload) => {
    try {
      const res = await axios({
        method: 'patch',
        url: `${API_URL}/accounts/profile/update/`,
        data: payload,
        headers: {
          Authorization: `Token ${token.value}`,
          'Content-Type': 'multipart/form-data'
        }
      })

      console.log('프로필 수정 완료:', res.data)

      // 수정 후 최신 정보를 다시 불러와 state 갱신 (데이터 동기화)
      await getProfile()

      return res.data
    } catch (err) {
      console.error('프로필 수정 실패:', err)
      throw err
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
    editProfile,
    followUser,
  }
}, {
  persist: {
    paths: ['token', 'user']
  }
})