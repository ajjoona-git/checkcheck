<template>
  <div class="product-card" @click="handleClick">

    <div class="card-header-section">
      <span class="bank-name">{{ product.bank_name }}</span>
      <h3 class="product-name text-truncate-2">{{ product.fin_prdt_nm }}</h3>
    </div>

    <div class="card-rate-section">
      <div class="rate-box" v-if="product.max_rate">
        <span class="rate-label">최고 연</span>
        <span class="rate-value">{{ product.max_rate }}%</span>
      </div>
      <div class="rate-box empty" v-else>
        <span class="rate-label">금리 정보 없음</span>
      </div>
    </div>

    <div class="card-footer-section">
      <div class="badges">
        <span class="type-badge" :class="product.product_type">
          {{ product.product_type === 'DEPOSIT' ? '예금' : '적금' }}
        </span>
      </div>
      <span class="join-way text-truncate">{{ parseJoinWay(product.join_way) }}</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click'])

// 카드 클릭 시 이벤트
const handleClick = () => {
  emit('click')
}

// 가입 방법 파싱 함수
const parseJoinWay = (way) => {
  if (!way) return ''
  const ways = way.split(',')
  return ways[0] + (ways.length > 1 ? ` 외 ${ways.length - 1}건` : '')
}
</script>

<style scoped>
.product-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.04);
  border-radius: 24px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 220px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
  position: relative;
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  border-color: rgba(27, 94, 32, 0.2);
}

.card-header-section {
  margin-bottom: 16px;
}

.bank-name {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 600;
  margin-bottom: 6px;
  display: block;
}

.product-name {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.4;
}

/* 말줄임 처리 (2줄) */
.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Rate Section */
.card-rate-section {
  margin-bottom: 20px;
}

.rate-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--moathon-green);
  line-height: 1;
  letter-spacing: -1px;
}

.rate-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-right: 4px;
  font-weight: 500;
}

/* Footer Section */
.card-footer-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-top: 1px solid #f5f5f7;
  padding-top: 16px;
}

.type-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 700;
}

.type-badge.DEPOSIT {
  background-color: #e3f2fd;
  color: #1976d2;
}

.type-badge.SAVING {
  background-color: #f3e5f5;
  color: #8e24aa;
}

.join-way {
  font-size: 0.8rem;
  color: #adb5bd;
  max-width: 50%;
  text-align: right;
}
</style>