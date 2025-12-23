import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useProductStore = defineStore('product', () => {
  const accountStore = useAccountStore()
  const API_URL = import.meta.env.VITE_API_URL

  const products = ref([])
  const productDetail = ref(null)
  const isLoading = ref(false)

  const getProducts = async () => {
    // 이미 데이터가 있다면 다시 부르지 않음 (SPA 네비게이션 시 효율성)
    if (products.value.length > 0) return

    isLoading.value = true
    let allResults = []
    let nextUrl = `${API_URL}/products/`

    try {
      while (nextUrl) {
        const response = await axios.get(nextUrl)
        const data = response.data
        allResults = [...allResults, ...data.results]
        nextUrl = data.next
      }
      products.value = allResults
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
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
      productDetail.value = response.data
    } catch (error) {
      console.error('상품 상세 조회 실패:', error)
    }
  }

  return { products, productDetail, getProducts, getProductDetail, isLoading }
})