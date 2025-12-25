<template>
  <div class="product-list-container">
    <div class="header">
      <h1>금융 상품 찾기</h1>
      <p>나에게 딱 맞는 예/적금 상품을 찾아보세요.</p>
    </div>

    <div class="text-end mb-2">
      <button 
        @click="refreshData" 
        class="btn btn-sm btn-outline-secondary"
        :disabled="store.isLoading"
      >
        <i class="bi bi-arrow-clockwise"></i> 최신 데이터로 새로고침
      </button>
    </div>

    <div class="tabs-wrapper mb-4">
      <ul class="nav nav-pills justify-content-center">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: filters.type === 'ALL' }" @click.prevent="filters.type = 'ALL'" href="#">전체</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: filters.type === 'DEPOSIT' }" @click.prevent="filters.type = 'DEPOSIT'" href="#">정기예금</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: filters.type === 'SAVING' }" @click.prevent="filters.type = 'SAVING'" href="#">정기적금</a>
        </li>
      </ul>
    </div>

    <div class="filter-bar">
      <select v-model="filters.bank" class="form-select bank-select">
        <option value="">전체 은행</option>
        <option v-for="bank in store.banks" :key="bank" :value="bank">
          {{ bank }}
        </option>
      </select>

      <select v-model="filters.period" class="form-select period-select">
        <option value="">전체 기간</option>
        <option value="6">6개월</option>
        <option value="12">12개월</option>
        <option value="24">24개월</option>
        <option value="36">36개월</option>
      </select>
    </div>

    <div v-if="store.isLoading" class="loading-state">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2">모든 상품 정보를 불러오는 중입니다...</p>
    </div>

    <div v-else>
      <div class="header-info mb-3">
        <span class="badge bg-secondary">{{ filteredProducts.length }}개의 상품</span>
        <span v-if="filters.period" class="ms-2 text-primary small">
          * {{ filters.period }}개월 금리 기준 정렬됨
        </span>
        <span v-else class="ms-2 text-primary small">
          * 최고 우대 금리 기준 정렬됨
        </span>
      </div>

      <div v-if="filteredProducts.length > 0">
        <div class="product-grid">
          <ProductCard
            v-for="product in paginatedProducts" 
            :key="product.id" 
            :product="product"
            @click="goDetail(product.id)"
          />
        </div>

        <Pagination
          :current-page="currentPage"
          :total-count="filteredProducts.length"
          :items-per-page="itemsPerPage"
          @change-page="handlePageChange"
        />
      </div>

      <div v-else class="empty-state">
        <p>조건에 맞는 상품이 없습니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import ProductCard from '@/components/product/ProductCard.vue'
import Pagination from '@/components/common/Pagination.vue'

const store = useProductStore()
const router = useRouter()

const filters = reactive({
  type: 'ALL',      // ALL, DEPOSIT, SAVING
  bank: '',         // 은행명
  period: ''        // 저장 기간 (문자열 '6', '12' 등)
})

const currentPage = ref(1)
const itemsPerPage = 12

// [캐싱 설정] 
const CACHE_KEY = 'moathon_products_data'
const CACHE_EXPIRY_MS = 24 * 60 * 60 * 1000 // 24시간 (하루)

const filteredProducts = computed(() => {
  // store.products가 없으면 빈 배열 반환 (에러 방지)
  if (!store.products) return []
  
  let results = store.products

  // 1. 탭 필터
  if (filters.type !== 'ALL') {
    results = results.filter(p => p.product_type === filters.type)
  }

  // 2. 은행 필터
  if (filters.bank) {
    results = results.filter(p => p.bank_name === filters.bank)
  }

  // 3. 기간 필터
  if (filters.period) {
    results = results.filter(p => 
      p.options.some(opt => opt.save_trm === filters.period)
    )
  }

  // 4. 정렬
  return [...results].sort((a, b) => {
    let rateA, rateB

    if (filters.period) {
      const optA = a.options.find(o => o.save_trm === filters.period)
      const optB = b.options.find(o => o.save_trm === filters.period)
      rateA = optA ? optA.intr_rate2 : -1
      rateB = optB ? optB.intr_rate2 : -1
    } else {
      rateA = a.max_rate
      rateB = b.max_rate
    }
    
    return rateB - rateA
  })
})

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredProducts.value.slice(start, end)
})

watch(filters, () => {
  currentPage.value = 1
})

const handlePageChange = (page) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const goDetail = (id) => {
  router.push({ name: 'productDetail', params: { id } })
}

// [핵심 로직] 데이터 로드 함수 (캐시 우선)
const loadData = async (forceRefresh = false) => {
  // 1. 로컬 스토리지 확인
  const cachedData = localStorage.getItem(CACHE_KEY)
  const now = new Date().getTime()

  // 2. 캐시가 있고, 강제 새로고침이 아니며, 유효 기간 내인 경우
  if (!forceRefresh && cachedData) {
    const parsed = JSON.parse(cachedData)
    
    // 유효기간 체크 (현재 시간 - 저장 시간 < 설정 시간)
    if (now - parsed.timestamp < CACHE_EXPIRY_MS) {
      console.log('LocalStorage에서 상품 데이터를 불러왔습니다.')
      
      // Pinia Store에 직접 데이터 주입
      // (Store에 setProducts 같은 액션이 없다면 직접 할당 가능하지만, 
      // Pinia는 $patch나 직접 할당 모두 반응성을 지원합니다)
      store.products = parsed.products
      store.banks = parsed.banks
      store.isLoading = false
      return
    }
  }

  // 3. 캐시가 없거나 만료되었으면 API 호출
  console.log('서버에서 최신 상품 데이터를 불러옵니다...')
  await store.getProducts()
  await store.getBanks()

  // 4. 받아온 데이터를 로컬 스토리지에 저장
  const dataToSave = {
    timestamp: now,
    products: store.products,
    banks: store.banks
  }
  localStorage.setItem(CACHE_KEY, JSON.stringify(dataToSave))
}

// 강제 새로고침 버튼용
const refreshData = () => {
  if (confirm('최신 금리 정보를 다시 불러오시겠습니까?')) {
    loadData(true)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.product-list-container { max-width: 1200px; margin: 0 auto; padding: 40px 16px; }
.header { text-align: center; margin-bottom: 30px; }

/* 탭 스타일 */
.nav-pills .nav-link {
  color: #666;
  border-radius: 20px;
  padding: 8px 24px;
  margin: 0 4px;
  font-weight: 600;
}
.nav-pills .nav-link.active {
  background-color: #2c3e50;
  color: #fff;
}

/* 필터 바 */
.filter-bar {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-bottom: 20px;
}
.form-select {
  width: auto;
  min-width: 120px;
  border-radius: 8px;
  border-color: #ddd;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 80px 0;
  color: #888;
}

.header-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>