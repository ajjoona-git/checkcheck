import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

// 사용자 계정 인증 및 프로필 관리 상태 저장소
export const useAccountStore = defineStore('account', () => {
  const router = useRouter()
  const API_URL = import.meta.env.VITE_API_URL

  const user = ref(null)
  const token = ref(null)

  // 회원가입 처리 및 자동 로그인
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
        // 회원가입 완료, 자동 로그인 시작
        const password = password1
        logIn({ username, email, password })
        router.push({ name: 'onboarding' })
      })
      .catch(err => {
        // 회원가입 실패 처리
        throw err
      })
  }

  // 사용자 로그인 및 토큰 저장
  const logIn = async function (payload) { 
    const { username, email, password } = payload

    try {
      const res = await axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: { username, email, password }
      })
      // 로그인 성공, 토큰 저장 중
      const newToken = res.data.key
      token.value = newToken
      localStorage.setItem('token', newToken) 
      await getProfile()
    } catch (err) {
      // 로그인 실패 처리
      throw err
    }
  }

  // 로그인한 사용자의 프로필 정보 조회
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
      // 유저 정보 로드 완료
      return response.data
    } catch (error) {
      // 유저 정보 로드 실패 처리
      throw error
    }
  }

  // 사용자 로그아웃 및 토큰 초기화
  const logOut = async function () {
    try {
      // 1. 백엔드에 로그아웃 요청
      // 토큰이 없다면 요청을 보낼 필요도 없음
      if (token.value) {
        await axios({
          method: 'post',
          url: `${API_URL}/accounts/logout/`,
          headers: {
            Authorization: `Token ${token.value}`
          }
        })
      }
    } catch (err) {
      // 2. 401 에러가 나더라도(이미 만료됨 등) 프론트에서는 무시하고 진행
    } finally {
      // 3. 성공하든 실패하든 프론트엔드 정보는 무조건 삭제
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      // 프론트엔드 상태 초기화 완료
    }
  }

  // 현재 로그인 상태 확인
  const isAuthenticated = computed(() => {
    return token.value ? true : false
  })

  // 온보딩 단계에서 사용자 추가 정보 입력
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

      await getProfile()
      return response.data
    } catch (error) {
      // 온보딩 저장 실패 처리
      throw error
    }
  }

  // 기존 프로필 정보 수정 (이미지, 닉네임 등)
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
      // 프로필 수정 완료
      await getProfile()
      return res.data
    } catch (err) {
      // 프로필 수정 실패 처리
      throw err
    }
  }

  // 다른 사용자 팔로우 처리
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
      // 팔로우 요청 실패 처리
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