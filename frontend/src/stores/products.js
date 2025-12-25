import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('product', () => {
  const API_URL = import.meta.env.VITE_API_URL
  const CACHE_EXPIRY_MS = 24 * 60 * 60 * 1000

  const products = ref([])
  const productDetail = ref(null)
  const isLoading = ref(false)
  const banks = ref([])

  const lastFetched = ref({
    products: 0,
    banks: 0
  })

  const isCacheValid = (type) => {
    const now = new Date().getTime()
    const fetchedTime = lastFetched.value[type] || 0
    // 현재 시간 - 저장된 시간 < 24시간 이면 유효
    return (now - fetchedTime < CACHE_EXPIRY_MS)
  }

  const getProducts = async (forceRefresh = false) => {
    if (!forceRefresh && products.value.length > 0 && isCacheValid('products')) {
      console.log('스토어: 저장된 상품 데이터 사용 (유효함)')
      return
    }

    isLoading.value = true
    let allResults = []
    let nextUrl = `${API_URL}/products/`

    try {
      console.log('스토어: 서버에서 상품 데이터 업데이트 중...')
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

  const getBanks = async (forceRefresh = false) => {
    if (!forceRefresh && banks.value.length > 0 && isCacheValid('banks')) {
      return
    }

    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/products/banklist/`,
      })
      banks.value = response.data
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