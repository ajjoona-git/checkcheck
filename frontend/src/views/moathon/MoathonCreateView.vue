<template>
  <div class="create-view">
    <div class="header">
      <h1>모아톤 시작하기</h1>
      <p>선택하신 금융 상품으로 모아톤을 시작합니다.</p>
    </div>

    <div class="card">
      <div v-if="productId" class="selected-product-info">
        <p>선택된 상품 ID: <strong>{{ productId }}</strong></p>
        </div>
      <div v-else class="alert alert-warning text-center">
        주의: 상품 정보가 선택되지 않았습니다.
      </div>

      <MoathonCreateForm 
        :is-edit="false" 
        :initial-data="{ product_option: Number(productId) }"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
// Store 호출 제거 (MoathonCreateForm 내부에서 처리함)
import MoathonCreateForm from '@/components/moathon/MoathonCreateForm.vue'

const route = useRoute()
const productId = computed(() => route.query.productId)

// handleCreate 로직 제거 -> MoathonCreateForm 내부의 submitForm에서 처리됨
</script>

<style scoped>
.create-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.card {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.selected-product-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
  color: #666;
}
</style>