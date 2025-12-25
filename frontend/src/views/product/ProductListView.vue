<template>
  <div class="page-wrapper">
    <div class="container py-5 fade-in">

      <header class="page-header text-center mb-5">
        <h1 class="header-title">예·적금 조회</h1>
        <p class="header-subtitle">
          나에게 딱 맞는 <span class="highlight">금융 상품</span>을 찾아보세요.
        </p>
      </header>

      <div class="control-bar d-flex flex-column flex-lg-row justify-content-between align-items-center mb-4 gap-3">

        <ul class="nav nav-pills custom-pills">
          <li class="nav-item">
            <a class="nav-link" :class="{ active: filters.type === 'ALL' }" @click.prevent="filters.type = 'ALL'"
              href="#">전체</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: filters.type === 'DEPOSIT' }"
              @click.prevent="filters.type = 'DEPOSIT'" href="#">정기예금</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: filters.type === 'SAVING' }" @click.prevent="filters.type = 'SAVING'"
              href="#">정기적금</a>
          </li>
        </ul>

        <div class="d-flex align-items-center gap-2 filter-group">

          <select v-model="filters.bank" class="form-select custom-select compact">
            <option value="">전체 은행</option>
            <option v-for="bank in store.banks" :key="bank" :value="bank">
              {{ bank }}
            </option>
          </select>

          <select v-model="filters.period" class="form-select custom-select compact">
            <option value="">전체 기간</option>
            <option value="6">6개월</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>

          <button @click="refreshData" class="btn btn-refresh compact" :disabled="store.isLoading" title="최신 데이터 불러오기">
            <i class="bi bi-arrow-clockwise" :class="{ 'spin-icon': store.isLoading }"></i>
          </button>
        </div>
      </div>

      <div v-if="store.isLoading" class="loading-state">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-3 text-muted fw-medium">최신 금리 정보를 불러오는 중입니다...</p>
      </div>

      <div v-else>
        <div class="d-flex justify-content-end mb-3 px-1">
          <span class="sort-info text-muted small">
            총 <b class="text-dark">{{ filteredProducts.length }}</b>개 ·
            {{ filters.period ? `${filters.period}개월 금리순` : '최고 우대금리순' }}
          </span>
        </div>

        <div v-if="filteredProducts.length > 0">
          <div class="product-grid">
            <ProductCard v-for="product in paginatedProducts" :key="product.id" :product="product"
              @click="goDetail(product.id)" />
          </div>

          <div class="mt-5 d-flex justify-content-center">
            <Pagination :current-page="currentPage" :total-count="filteredProducts.length"
              :items-per-page="itemsPerPage" @change-page="handlePageChange" />
          </div>
        </div>

        <div v-else class="empty-state">
          <p>조건에 맞는 상품을 찾지 못했습니다.</p>
          <button class="btn btn-outline-primary btn-sm mt-2 rounded-pill px-3"
            @click="filters.bank = ''; filters.period = ''">
            필터 초기화
          </button>
        </div>
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
  type: 'ALL',
  bank: '',
  period: ''
})

const currentPage = ref(1)
const itemsPerPage = 24

const CACHE_KEY = 'moathon_products_data'
const CACHE_EXPIRY_MS = 24 * 60 * 60 * 1000

// 필터링 및 정렬된 상품 목록
const filteredProducts = computed(() => {
  if (!store.products) return []

  // 필터링
  let results = store.products
  if (filters.type !== 'ALL') {
    results = results.filter(p => p.product_type === filters.type)
  }
  if (filters.bank) {
    results = results.filter(p => p.bank_name === filters.bank)
  }
  if (filters.period) {
    results = results.filter(p =>
      p.options.some(opt => opt.save_trm === filters.period)
    )
  }

  // 정렬
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

// 현재 페이지에 해당하는 상품 목록
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredProducts.value.slice(start, end)
})

// 필터 변경 시 페이지 초기화
watch(filters, () => {
  currentPage.value = 1
})

// 페이지 변경 처리
const handlePageChange = (page) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 상품 상세 페이지로 이동
const goDetail = (id) => {
  router.push({ name: 'productDetail', params: { id } })
}

// 데이터 로드 (캐시 활용)
const loadData = async (forceRefresh = false) => {
  const cachedData = localStorage.getItem(CACHE_KEY)
  const now = new Date().getTime()

  // 캐시 유효기간 내 데이터가 있으면 로드
  if (!forceRefresh && cachedData) {
    const parsed = JSON.parse(cachedData)
    if (now - parsed.timestamp < CACHE_EXPIRY_MS) {
      store.products = parsed.products
      store.banks = parsed.banks
      store.isLoading = false
      return
    }
  }

  await store.getProducts()
  await store.getBanks()

  const dataToSave = {
    timestamp: now,
    products: store.products,
    banks: store.banks
  }
  localStorage.setItem(CACHE_KEY, JSON.stringify(dataToSave))
}

// 최신 데이터 불러오기
const refreshData = () => {
  if (confirm('최신 금리 정보를 다시 불러오시겠습니까?')) {
    loadData(true)
  }
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

/* Header */
.header-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 12px;
  background: linear-gradient(135deg, var(--moathon-green) 0%, var(--moathon-deep) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.header-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.highlight {
  color: var(--moathon-green);
  font-weight: 800;
}

/* 탭 스타일 */
.custom-pills {
  background: white;
  padding: 4px;
  border-radius: 50px;
  display: inline-flex;
}

.custom-pills .nav-link {
  color: var(--text-secondary);
  border-radius: 50px;
  padding: 6px 20px;
  font-weight: 700;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.custom-pills .nav-link.active {
  background-color: var(--moathon-green);
  color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

/* 필터 그룹 */
.custom-select.compact {
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  padding: 6px 32px 6px 12px;
  font-size: 0.9rem;
  color: var(--text-primary);
  cursor: pointer;
  min-width: 120px;
  height: 38px;
  background-position: right 10px center;
}

.custom-select:focus {
  border-color: var(--moathon-green);
  box-shadow: 0 0 0 3px rgba(27, 94, 32, 0.1);
}

/* 새로고침 버튼 */
.btn-refresh.compact {
  border: 1px solid #e0e0e0;
  background: white;
  color: var(--text-secondary);
  border-radius: 12px;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.2s;
}

.btn-refresh:hover:not(:disabled) {
  background: #f8f9fa;
  color: var(--moathon-green);
  border-color: var(--moathon-green);
}

.spin-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

/* 그리드 */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* 상태 표시 */
.loading-state,
.empty-state {
  text-align: center;
  padding: 100px 0;
  color: var(--text-secondary);
}

.empty-state {
  background: white;
  border-radius: 24px;
  border: 2px dashed #e0e0e0;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.fade-in {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 991px) {
  .control-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    justify-content: space-between;
  }

  .custom-select.compact {
    flex: 1;
  }
}
</style>