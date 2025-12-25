<template>
  <div class="page-wrapper" v-if="product">
    <div class="container py-5 fade-in">

      <div class="header-section text-center mb-5">
        <h1 class="product-title">{{ product.fin_prdt_nm }}</h1>
        <div class="badges mb-3 d-flex justify-content-center gap-2">
          <span class="bank-badge">{{ product.bank_name }}</span>
          <span class="type-badge" :class="product.product_type">
            {{ product.product_type === 'DEPOSIT' ? '예금' : '적금' }}
          </span>
        </div>
      </div>

      <div class="info-grid mb-5">
        <div class="info-card">
          <h4 class="info-label">가입 대상</h4>
          <p class="info-value">{{ product.join_member || '실명의 개인' }}</p>
        </div>

        <div class="info-card">
          <h4 class="info-label">가입 방법</h4>
          <p class="info-value">{{ product.join_way || '영업점, 인터넷, 스마트폰' }}</p>
        </div>

        <div class="info-card full-width" v-if="product.etc_note">
          <div class="d-flex align-items-center gap-2 mb-2">
            <i class="bi bi-info-circle-fill text-secondary"></i>
            <h4 class="info-label m-0">유의 사항</h4>
          </div>
          <p class="info-value text-secondary">{{ product.etc_note }}</p>
        </div>
      </div>

      <hr class="divider my-5">

      <div class="options-section">
        <div class="text-center mb-4">
          <h2 class="section-title">금리 및 기간 옵션</h2>
          <p class="section-desc">원하는 조건을 선택하여 저축 챌린지를 시작해보세요.</p>
        </div>

        <ProductOptionList v-if="product.options && product.options.length > 0" :options="product.options"
          @select-option="goMoathonCreate" />

        <div v-else class="empty-state">
          <p>상세 옵션 정보가 없습니다.</p>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="loading-state">
    <div class="spinner-border text-primary" role="status"></div>
    <p class="mt-3">상품 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { computed, watch, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { useAccountStore } from '@/stores/accounts'
import ProductOptionList from '@/components/product/ProductOptionList.vue'

const store = useProductStore()
const accountStore = useAccountStore()
const route = useRoute()
const router = useRouter()

const isLoading = ref(true)
const product = computed(() => store.productDetail)

// 상품 정보 조회
const fetchProduct = async (productId) => {
  isLoading.value = true
  try {
    await store.getProductDetail(productId)
  } catch (err) {
    // 식품 정보 로드 실패
    throw err
  } finally {
    isLoading.value = false
  }
}

// 라우트 변경 감지 및 상품 정보 재조회
watch(
  () => route.params.id,
  (newId) => {
    if (newId) fetchProduct(newId)
  },
  { immediate: true }
)

// 모아톤 생성 페이지로 이동
const goMoathonCreate = (optionId) => {
  if (!accountStore.isAuthenticated) {
    const userConfirm = confirm('로그인이 필요한 서비스입니다.\n로그인 페이지로 이동하시겠습니까?')
    if (userConfirm) {
      router.push({ name: 'login' })
    }
    return
  }

  router.push({
    name: 'moathonCreate',
    query: { productId: optionId }
  })
}
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

.container {
  max-width: 1000px;
}

/* Header */
.product-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-top: 10px;
  line-height: 1.3;
}

.bank-badge {
  background: white;
  border: 1px solid #e0e0e0;
  color: var(--text-secondary);
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.type-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 700;
}

.type-badge.DEPOSIT {
  background-color: #e3f2fd;
  color: #1976d2;
}

.type-badge.SAVING {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

/* Info Grid */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.info-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  border: 1px solid rgba(0, 0, 0, 0.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.full-width {
  grid-column: 1 / -1;
}

.icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.bg-blue-light {
  background: #e3f2fd;
}

.bg-green-light {
  background: #e8f5e9;
}

.info-label {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.info-value {
  font-size: 1.1rem;
  color: #495057;
  line-height: 1.6;
  margin: 0;
  word-break: keep-all;
}

/* Options Section */
.section-title {
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.section-desc {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.divider {
  border-color: rgba(0, 0, 0, 0.05);
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  color: var(--text-secondary);
}

.empty-state {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 24px;
  color: var(--text-secondary);
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

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .product-title {
    font-size: 2rem;
  }
}
</style>