<template>
  <div class="detail-container" v-if="product">
    <div class="product-info-section">
      <span class="bank-badge">{{ product.bank_name }}</span>
      <span class="type-badge" :class="product.product_type">
        {{ product.product_type === 'DEPOSIT' ? '예금' : '적금' }}
      </span>
      <h1 class="title">{{ product.fin_prdt_nm }}</h1>

      <div class="info-grid">
        <div class="info-item">
          <h4>가입 방법</h4>
          <p>{{ product.join_way || '영업점, 인터넷, 스마트폰' }}</p>
        </div>
        <div class="info-item">
          <h4>가입 대상</h4>
          <p>{{ product.join_member || '실명의 개인' }}</p>
        </div>
        <div class="info-item full-width" v-if="product.etc_note">
          <h4>유의 사항</h4>
          <p>{{ product.etc_note }}</p>
        </div>
      </div>
    </div>

    <hr class="divider" />

    <div class="options-section">
      <h2>금리 및 기간 옵션</h2>
      <p class="desc">원하는 조건을 선택하여 저축 챌린지를 시작해보세요.</p>

      <ProductOptionList v-if="product.options && product.options.length > 0" :options="product.options"
        @select-option="goMoathonCreate" />

      <div v-else class="empty-options">
        <p>상세 옵션 정보가 없습니다.</p>
      </div>
    </div>
  </div>

  <div v-else class="loading">
    <p>상품 정보를 불러오는 중입니다...</p>
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

const fetchProduct = async (productId) => {
  isLoading.value = true
  try {
    await store.getProductDetail(productId)
  } catch (err) {
    console.error('상품 정보 로딩 실패:', err)
  } finally {
    isLoading.value = false
  }
}

watch(
  () => route.params.id,
  (newId) => {
    if (newId) fetchProduct(newId)
  },
  { immediate: true }
)

const goMoathonCreate = (optionId) => {
  if (!accountStore.isLogin) {
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
.detail-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.loading {
  text-align: center;
  padding: 50px;
  color: #888;
}

.product-info-section {
  text-align: center;
  margin-bottom: 30px;
}

.bank-badge {
  background: #e3f2fd;
  color: #1565c0;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.type-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.type-badge.DEPOSIT {
  background-color: #e3f2fd;
  color: #1565c0;
}

.type-badge.SAVING {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.title {
  font-size: 2rem;
  margin: 16px 0 30px;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  background: #f8f9fa;
  padding: 24px;
  border-radius: 16px;
  text-align: left;
}

.info-item h4 {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 8px;
}

.info-item p {
  font-size: 1rem;
  color: #333;
  line-height: 1.5;
}

.full-width {
  grid-column: 1 / -1;
}

.divider {
  border: 0;
  height: 1px;
  background: #eee;
  margin: 40px 0;
}

.options-section h2 {
  margin-bottom: 8px;
  color: #2c3e50;
}

.desc {
  color: #666;
  margin-bottom: 24px;
}

.empty-options {
  color: #888;
  text-align: center;
  padding: 20px;
}
</style>