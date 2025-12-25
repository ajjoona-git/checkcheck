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
  const recommendationResult = ref(null) // 추천된 상품 목록 저장
  const isRecommending = ref(false)   // 추천 로딩 상태

  const count = ref(0)             // 전체 개수
  const currentPage = ref(1)      // 현재 페이지 번호
  const itemsPerPage = 24         // 페이지당 개수 설정

  const totalPages = computed(() => {
    return Math.ceil(count.value / itemsPerPage)
  })

  const moathonDetail = ref(null)
  const clearMoathonDetail = () => {
    moathonDetail.value = null
  }

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
      console.error('모아톤 목록 조회 실패:', error)
    }
  }

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
      console.error('모아톤 상세 조회 실패:', error)
      throw error
    }
  }

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
      console.error('댓글 조회 실패:', error)
    }
  }

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
      console.error('모아톤 생성 실패:', error)
      throw error
    }
  }

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
      console.error('모아톤 수정 실패:', error)
      throw error
    }
  }

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
      console.error('모아톤 삭제 실패:', err)
      throw err
    }
  }

  const likeMoathon = async (moathonId) => {
    try {
      const response = await axios.post(
        `${API_URL}/moathons/${moathonId}/like/`,
        {},
        { headers: { Authorization: `Token ${accountStore.token}` } }
      )

      if (moathonDetail.value && response.data) {
        if (!moathonDetail.value.likes) {
          moathonDetail.value.likes = { count: 0, is_liked: false }
        }
        if (response.data.hasOwnProperty('liked')) {
          moathonDetail.value.likes.is_liked = response.data.liked
        }
        if (response.data.hasOwnProperty('like_count')) {
          moathonDetail.value.likes.count = response.data.like_count
        }
      }

    } catch (err) {
      console.error('응원하기 실패:', err)
      if (err.response?.status === 401) {
        alert('로그인이 필요합니다.')
      }
    }
  }

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
      console.error('댓글 작성 실패:', error)
    }
  }

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
      console.error('댓글 수정 실패:', error)
      throw error
    }
  }

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
      console.error('댓글 삭제 실패:', err)
    }
  }

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
      console.error('추천 요청 실패:', error)
      throw error
    } finally {
      isRecommending.value = false
    }
  }

  const getFollowingMoathons = async () => {
    try {
      const token = accountStore.token
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
      console.log('팔로잉 모아톤 로드 성공:', res.data)

    } catch (err) {
      console.error('팔로잉 모아톤 로드 실패:', err)
      followingMoathons.value = []
    }
  }

  const resetState = () => {
    moathons.value = []
    followingMoathons.value = []
    moathonDetail.value = null
    console.log('Moathon Store 초기화 완료')
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
