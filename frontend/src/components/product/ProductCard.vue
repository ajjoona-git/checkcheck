<template>
  <div class="product-card" @click="handleClick">
    <div class="card-top">
      <span class="bank-name">{{ product.bank_name }}</span>
      <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>
      
      <div class="rate-info" v-if="product.max_rate">
        <span class="label">최고 연</span>
        <span class="rate">{{ product.max_rate }}%</span>
      </div>
    </div>

    <div class="card-bottom">
      <span class="type-badge" :class="product.product_type">
        {{ product.product_type === 'DEPOSIT' ? '예금' : '적금' }}
      </span>
      <span class="join-way">{{ parseJoinWay(product.join_way) }}</span>
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

const handleClick = () => {
  emit('click')
}

const parseJoinWay = (way) => {
  if (!way) return ''
  return way.split(',')[0] + (way.includes(',') ? ' 등' : '')
}
</script>

<style scoped>
.product-card {
  background: white;
  border: 1px solid #eee;
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 180px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  border-color: #2c3e50;
}

.card-top { margin-bottom: 20px; }

.bank-name { font-size: 0.9rem; color: #666; margin-bottom: 8px; display: block; font-weight: 500; }
.product-name { font-size: 1.25rem; font-weight: bold; color: #333; margin: 0 0 12px 0; line-height: 1.4; }

.rate-info { display: flex; align-items: baseline; gap: 4px; margin-top: 5px; }
.rate-info .label { font-size: 0.85rem; color: #666; }
.rate-info .rate { font-size: 1.4rem; font-weight: 800; color: #e74c3c; }

.card-bottom { display: flex; justify-content: space-between; align-items: center; margin-top: 15px; }

.type-badge { 
  display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
}
.type-badge.DEPOSIT { background-color: #e3f2fd; color: #1565c0; }
.type-badge.SAVING { background-color: #f3e5f5; color: #7b1fa2; }

.join-way { font-size: 0.8rem; color: #999; }
</style>