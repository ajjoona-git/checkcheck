<template>
  <div class="create-view page-wrapper">
    <div class="container fade-in">
      
      <div class="header text-center mb-5">
        <h1 class="page-title">모아톤 시작하기</h1>
        <p class="page-subtitle">선택하신 금융 상품으로 새로운 도전을 시작합니다.</p>
      </div>

      <div class="create-card shadow-sm">
        
        <div v-if="productId" class="selected-product-info mb-4">
          <div class="d-flex align-items-center justify-content-center gap-2">
            <i class="bi bi-check-circle-fill text-success"></i>
            <span>선택된 상품 옵션 ID: <strong>{{ productId }}</strong></span>
          </div>
        </div>
        
        <div v-else class="alert alert-warning d-flex align-items-center justify-content-center gap-2 mb-4" role="alert">
          <i class="bi bi-exclamation-triangle-fill"></i>
          <div>주의: 상품 정보가 선택되지 않았습니다.</div>
        </div>

        <MoathonCreateForm 
          :is-edit="false" 
          :initial-data="{ product_option: Number(productId) }"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MoathonCreateForm from '@/components/moathon/MoathonCreateForm.vue'

const route = useRoute()
const productId = computed(() => route.query.productId)
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.container {
  max-width: 600px;
  width: 100%;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.create-card {
  background: white;
  padding: 40px;
  border-radius: 32px; /* 둥근 모서리 */
  border: 1px solid rgba(0, 0, 0, 0.02);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
}

.selected-product-info {
  background: #e8f5e9; /* 연한 초록 배경 */
  color: var(--moathon-green);
  padding: 16px;
  border-radius: 16px;
  text-align: center;
  font-weight: 500;
  border: 1px solid rgba(27, 94, 32, 0.1);
}

.alert-warning {
  border-radius: 16px;
  border: none;
  background-color: #fff3cd;
  color: #856404;
}

.fade-in { animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>