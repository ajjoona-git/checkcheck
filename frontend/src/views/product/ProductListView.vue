<template>
  <div class="product-list-container">
    <div class="header">
      <h1>🏦 금융 상품 찾기</h1>
      <p>나에게 딱 맞는 예/적금 상품을 찾아보세요.</p>
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
        <option v-for="bank in bankList" :key="bank" :value="bank">
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

// 은행 목록 (하드코딩 예시)
// TODO: API 호출로 변경
const bankList = [
  '우리은행', '한국스탠다드차타드은행', '대구은행', '부산은행', 
  '광주은행', '제주은행', '전북은행', '경남은행', '중소기업은행', 
  '한국산업은행', '국민은행', '신한은행', '농협은행', '하나은행', 
  '케이뱅크', '수협은행', '카카오뱅크', '토스뱅크'
]

const filteredProducts = computed(() => {
  let results = store.products

  // 1. 탭 필터 (예금/적금)
  if (filters.type !== 'ALL') {
    results = results.filter(p => p.product_type === filters.type)
  }

  // 2. 은행 필터
  if (filters.bank) {
    results = results.filter(p => p.bank_name === filters.bank)
  }

  // 3. 기간 필터 (선택한 기간 옵션이 있는 상품만)
  if (filters.period) {
    results = results.filter(p => 
      p.options.some(opt => opt.save_trm === filters.period)
    )
  }

  // 4. 정렬 (최고 금리순)
  // 원본 보호를 위해 복사본([...]) 생성 후 정렬
  return [...results].sort((a, b) => {
    let rateA, rateB

    if (filters.period) {
      // 기간이 선택되었으면, 해당 기간의 우대금리(intr_rate2)를 찾아 비교
      const optA = a.options.find(o => o.save_trm === filters.period)
      const optB = b.options.find(o => o.save_trm === filters.period)
      // 해당 기간 옵션이 없으면 -1 (맨 뒤로 보냄)
      rateA = optA ? optA.intr_rate2 : -1
      rateB = optB ? optB.intr_rate2 : -1
    } else {
      // 기간 선택 없으면 상품 자체의 최고 우대 금리(max_rate) 사용
      rateA = a.max_rate
      rateB = b.max_rate
    }
    
    // 내림차순 정렬
    return rateB - rateA
  })
})

// [페이지네이션] 현재 페이지에 보여줄 데이터 슬라이싱
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

onMounted(() => {
  store.getProducts()
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