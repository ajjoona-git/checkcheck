import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

// 금융 상품 및 은행 정보 상태 관리 (24시간 캐싱)
export const useProductStore = defineStore('product', () => {
  const API_URL = import.meta.env.VITE_API_URL
  
  const products = ref([])
  const productDetail = ref(null)
  const isLoading = ref(false)
  const banks = ref([])
  
  // 캐시 만료 시간: 24시간
  const CACHE_EXPIRY_MS = 24 * 60 * 60 * 1000
  const lastFetched = ref({
    products: 0,
    banks: 0
  })

  // 캐시된 데이터 유효성 검사 (24시간 기준)
  const isCacheValid = (type) => {
    const now = new Date().getTime()
    const fetchedTime = lastFetched.value[type] || 0
    // 현재 시간 - 저장된 시간 < 24시간 이면 유효
    return (now - fetchedTime < CACHE_EXPIRY_MS)
  }

  // 금융 상품 목록 조회 (캐시 활용)
  const getProducts = async (forceRefresh = false) => {
    // 캐시가 유효하고 강제 갱신이 아니면 저장된 데이터 사용
    if (!forceRefresh && products.value.length > 0 && isCacheValid('products')) {
      console.log('스토어: 저장된 상품 데이터 사용 (유효함)')
      return
    }

    isLoading.value = true
    let allResults = []
    let nextUrl = `${API_URL}/products/`

    try {
      console.log('스토어: 서버에서 상품 데이터 업데이트 중...')
      // 페이지네이션된 모든 상품 데이터 조회
      while (nextUrl) {
        const response = await axios.get(nextUrl)
        const data = response.data
        allResults = [...allResults, ...data.results]
        nextUrl = data.next
      }

      products.value = allResults
      lastFetched.value.products = new Date().getTime()

    } catch (err) {
      console.error('상품 로딩 실패:', err)
    } finally {
      isLoading.value = false
    }
  }

  // 특정 금융 상품의 상세 정보 조회
  const getProductDetail = async (id) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/products/${id}/`,
      })
      productDetail.value = response.data
    } catch (error) {
      console.error('상품 상세 조회 실패:', error)
      throw error
    }
  }

  // 은행 목록 조회 (캐시 활용)
  const getBanks = async (forceRefresh = false) => {
    // 캐시가 유효하고 강제 갱신이 아니면 저장된 데이터 사용
    if (!forceRefresh && banks.value.length > 0 && isCacheValid('banks')) {
      return
    }

    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/products/banklist/`,
      })
      banks.value = response.data
      // 조회 시간 갱신
      lastFetched.value.banks = new Date().getTime()
    } catch (error) {
      console.error('은행 목록 조회 실패:', error)
    }
  }

  return {
    products,
    productDetail,
    isLoading,
    banks,
    lastFetched,
    getProducts,
    getProductDetail,
    getBanks
  }
}, {
  persist: {
    paths: ['products', 'banks', 'lastFetched'],
  }
})