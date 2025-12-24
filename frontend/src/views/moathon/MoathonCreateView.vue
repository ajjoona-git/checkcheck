<template>
  <div class="create-view">
    <div class="header">
      <h1>모아톤 시작하기</h1>
      <p>선택하신 금융 상품으로 모아톤을 시작합니다.</p>
    </div>

    <div class="card">
      <div class="selected-product-info">
        <p>선택된 상품 ID: <strong>{{ productId }}</strong></p>
      </div>

      <MoathonCreateForm :is-submitting="isSubmitting" @submit="handleCreate" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useMoathonStore } from '@/stores/moathon'
import MoathonCreateForm from '@/components/moathon/MoathonCreateForm.vue'

const route = useRoute()
const store = useMoathonStore()

const isSubmitting = ref(false)
const productId = computed(() => route.query.productId)

const handleCreate = async (formData) => {
  if (!productId.value) {
    alert('잘못된 접근입니다. 상품 정보가 없습니다.')
    return
  }

  isSubmitting.value = true
  try {
    // 폼 데이터 + 쿼리 파라미터의 상품 ID 결합
    const payload = {
      ...formData,
      product_option: Number(productId.value)
    }
    await store.createMoathon(payload)
  } catch (error) {
    alert('모아톤 생성에 실패했습니다.')
  } finally {
    isSubmitting.value = false
  }
}
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