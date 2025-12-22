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
  const recommendationResult = ref(null) // 추천된 상품 목록 저장
  const isRecommending = ref(false)   // 추천 로딩 상태

  const count = ref(0)             // 전체 개수
  const currentPage = ref(1)      // 현재 페이지 번호
  const itemsPerPage = 24         // 페이지당 개수 설정

  const totalPages = computed(() => {
    return Math.ceil(count.value / itemsPerPage)
  })

  const fetchMoathons = async (page = 1) => {
    try {
      const response = await axios.get(`${API_URL}/moathons/`, {
        params: {
          page: page,
          page_size: itemsPerPage 
        }
      })
      
      const { results, count: totalCount } = response.data

      moathons.value = results
      count.value = totalCount
      currentPage.value = page

    } catch (error) {
      console.error('모아톤 목록 조회 실패:', error)
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

  return { 
    moathons, 
    count, 
    currentPage, 
    itemsPerPage,
    totalPages, 
    recommendationResult,
    isRecommending,
    fetchMoathons,
    createMoathon,
    recommendProduct,
   }
})
