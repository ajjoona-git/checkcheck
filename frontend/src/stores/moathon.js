import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

export const useMoathonStore = defineStore('moathon', () => {
  const accountStore = useAccountStore()
  const router = useRouter()
  const API_URL = import.meta.env.VITE_API_URL

  const moathons = ref([])
  const followingMoathons = ref([])
  const recommendationResult = ref(null)
  const isRecommending = ref(false)

  const count = ref(0)
  const currentPage = ref(1)
  const itemsPerPage = 24

  const totalPages = computed(() => {
    return Math.ceil(count.value / itemsPerPage)
  })

  const moathonDetail = ref(null)

  // 모아톤 상세 정보 초기화
  const clearMoathonDetail = () => {
    moathonDetail.value = null
  }

  // 모아톤 목록 조회 (페이지네이션)
  const fetchMoathons = async (page = 1) => {
    try {
      const config = {
         method: 'get',
         url: `${API_URL}/moathons/`,
         params: {
           page: page,
           page_size: itemsPerPage 
         },
         headers: {}
      }
      
      if (accountStore.token) {
        config.headers.Authorization = `Token ${accountStore.token}`
      }
      
      const response = await axios(config)
      const { results, count: totalCount } = response.data

      moathons.value = results
      count.value = totalCount
      currentPage.value = page

    } catch (error) {
      // 모아톤 목록 조회 실패 처리
      throw error
    }
  }

  // 특정 모아톤의 상세 정보 조회
  const fetchMoathonDetail = async (id) => {
    try {
      const config = {
        method: 'get',
        url: `${API_URL}/moathons/${id}/`,
        headers: {}
      }

      if (accountStore.token) {
        config.headers.Authorization = `Token ${accountStore.token}`
      }

      const response = await axios(config)
      moathonDetail.value = response.data
    } catch (error) {
      // 모아톤 상세 조회 실패 처리
      throw error
    }
  }

  // 모아톤의 댓글 목록 조회
  const fetchComments = async (moathonId) => {
    try {
      const config = {
        method: 'get',
        url: `${API_URL}/moathons/${moathonId}/comments/`,
        headers: {}
      }

      if (accountStore.token) {
        config.headers.Authorization = `Token ${accountStore.token}`
      }

      const response = await axios(config)
      const commentList = response.data.results ? response.data.results : response.data

      if (moathonDetail.value) {
        moathonDetail.value.comments = commentList
      }
    } catch (error) {
      // 댓글 목록 조회 실패 처리
      throw error
    }
  }

  // 모아톤 생성
  const createMoathon = async (payload) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/moathons/create/`,
        data: payload,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        }
      })
      router.push({ name: 'moathonDetail', params: { id: response.data.id } })
      return response.data
    } catch (error) {
      // 모아톤 생성 실패 처리
      throw error
    }
  }

  // 모아톤 수정
  const updateMoathon = async (id, payload) => {
    try {
      const response = await axios({
        method: 'patch',
        url: `${API_URL}/moathons/${id}/`,
        data: payload,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        }
      })
      moathonDetail.value = response.data
    } catch (error) {
      // 모아톤 수정 실패 처리
      throw error
    }
  }

  // 모아톤 삭제
  const deleteMoathon = async (id) => {
    try {
      await axios({
        method: 'delete',
        url: `${API_URL}/moathons/${id}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        }
      })
    } catch (err) {
      // 모아톤 삭제 실패 처리
      throw err
    }
  }

  // 모아톤 응원하기 (좋아요)
  const likeMoathon = async (moathonId) => {
    try {
      const response = await axios.post(
        `${API_URL}/moathons/${moathonId}/like/`,
        {},
        { headers: { Authorization: `Token ${accountStore.token}` } }
      )
      if (moathonDetail.value && response.data) {
        // 좋아요 정보가 없으면 초기화
        if (!moathonDetail.value.likes) {
          moathonDetail.value.likes = { count: 0, is_liked: false }
        }
        // 응답에 따라 좋아요 상태 및 카운트 갱신
        if (response.data.hasOwnProperty('liked')) {
          moathonDetail.value.likes.is_liked = response.data.liked
        }
        // 카운트 정보가 있으면 갱신
        if (response.data.hasOwnProperty('like_count')) {
          moathonDetail.value.likes.count = response.data.like_count
        }
      }

    } catch (err) {
      // 모아톤 좋아요 실패 처리
      if (err.response?.status === 401) {
        alert('로그인이 필요합니다.')
      }
    }
  }

  // 댓글 작성
  const createComment = async (moathonId, content) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/moathons/${moathonId}/comments/`,
        data: { content },
        headers: {
          Authorization: `Token ${accountStore.token}`,
        }
      })
      await fetchComments(moathonId)
    } catch (error) {
      // 댓글 작성 실패 처리
      throw error
    }
  }

  // 댓글 수정
  const updateComment = async (moathonId, commentId, content) => {
    try {
      const response = await axios({
        method: 'patch',
        url: `${API_URL}/moathons/${moathonId}/comments/${commentId}/`,
        data: { content },
        headers: {
          Authorization: `Token ${accountStore.token}`,
        }
      })
      await fetchComments(moathonId)
    } catch (error) {
      // 댓글 수정 실패 처리
      throw error
    }
  }

  // 댓글 삭제
  const deleteComment = async (moathonId, commentId) => {
    try {
      await axios({
        method: 'delete',
        url: `${API_URL}/moathons/${moathonId}/comments/${commentId}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        }
      })
      await fetchComments(moathonId)
    } catch (err) {
      // 댓글 삭제 실패 처리
      throw err
    }
  }

  // 상품 추천 요청
  const recommendProduct = async (payload) => {
    isRecommending.value = true
    recommendationResult.value = null
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/recommendations/recommend_product/`,
        data: payload,
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
      recommendationResult.value = response.data
      return response.data
    } catch (error) {
      // 추천 요청 실패 처리
      throw error
    } finally {
      isRecommending.value = false
    }
  }

  // 팔로잉 모아톤 목록 조회
  const getFollowingMoathons = async () => {
    try {
      const token = accountStore.token

      // 로그인 상태 확인
      if (!token) {
        console.log('로그인 상태가 아니므로 팔로잉 목록을 불러오지 않습니다.')
        return
      }

      const res = await axios({
        method: 'get',
        url: `${API_URL}/moathons/following/`,
        headers: {
          Authorization: `Token ${token}`
        }
      })

      followingMoathons.value = res.data
    } catch (err) {
      // 팔로잉 모아톤 로드 실패 처리
      followingMoathons.value = []
    }
  }

  // 스토어 상태 초기화
  const resetState = () => {
    moathons.value = []
    followingMoathons.value = []
    moathonDetail.value = null
  }

  return {
    moathons,
    recommendationResult,
    isRecommending,
    count,
    currentPage,
    itemsPerPage,
    totalPages,
    moathonDetail,
    followingMoathons,
    clearMoathonDetail,
    fetchMoathons,
    fetchMoathonDetail,
    fetchComments,
    createMoathon,
    updateMoathon,
    deleteMoathon,
    likeMoathon,
    createComment,
    updateComment,
    deleteComment,
    recommendProduct,
    getFollowingMoathons,
    resetState,
  }
})
