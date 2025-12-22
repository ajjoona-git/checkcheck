import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMoathonStore = defineStore('moathon', () => {
  const API_URL = import.meta.env.VITE_API_URL

  const moathons = ref([])         // 화면에 보여줄 모아톤 리스트 (누적됨)
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

  return { 
    moathons, 
    count, 
    currentPage, 
    itemsPerPage,
    totalPages, 
    fetchMoathons,
   }
})
