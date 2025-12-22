<template>
  <div class="recommend-view">
    <div class="header">
      <h1>모아톤 추천받기</h1>
      <p>저축 목표를 입력하고 맞춤 상품을 추천받아 보세요.</p>
    </div>

    <div v-if="!store.recommendationResult" class="card fade-in">
      <MoathonRecommendForm :is-loading="store.isRecommending" @submit="handleRecommend" />
    </div>

    <div v-else class="result-section fade-in">
      <MoathonRecommendCard :detail="detail" :warnings="warnings" @create="createWithProduct"
        @retry="resetRecommendation" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMoathonStore } from '@/stores/moathon'
import { useAccountStore } from '@/stores/accounts'
import MoathonRecommendForm from '@/components/moathon/MoathonRecommendForm.vue'
import MoathonRecommendCard from '@/components/moathon/MoathonRecommendCard.vue'

const router = useRouter()
const store = useMoathonStore()
const accountStore = useAccountStore()

const savedFormData = ref(null)

const detail = computed(() => {
  return store.recommendationResult?.final_recommendation?.option_detail || {}
})

const warnings = computed(() => {
  return store.recommendationResult?.final_recommendation?.warnings || []
})

// 1. 프로필 정보 확인 (onMounted)
onMounted(async () => {
  if (!accountStore.user) {
    try { await accountStore.getProfile() } catch (e) { }
  }
  const user = accountStore.user
  if (!user || !user.salary || !user.assets || !user.tender) {
    alert('정확한 상품 추천을 위해 프로필 정보를 먼저 설정해주세요.')
    router.replace({ name: 'mypage' })
  }
})

// 2. 추천 요청 핸들러
const handleRecommend = async (formData) => {
  savedFormData.value = { ...formData }
  try {
    await store.recommendProduct(formData)
  } catch (error) {
    alert('추천 상품을 불러오지 못했습니다.')
  }
}

// 3. '이걸로 시작' 핸들러 (바로 생성)
const createWithProduct = async () => {
  if (!detail.value || !detail.value.product_name) {
    alert('상품 정보가 올바르지 않습니다. 다시 시도해주세요.')
    return
  }

  if (!confirm(`[${detail.value.product_name}] 상품으로 모아톤을 시작하시겠습니까?`)) return

  if (!savedFormData.value) {
    alert('입력 정보가 만료되었습니다. 다시 추천을 받아주세요.')
    resetRecommendation()
    return
  }

  try {
    const payload = {
      // title: savedFormData.value.title,
      purpose: savedFormData.value.purpose,
      target_amount: savedFormData.value.target_amount,
      start_amount: savedFormData.value.start_amount,
      product_option: detail.value.option_id 
    }

    await store.createMoathon(payload)
    resetRecommendation()
  } catch (error) {
    alert('모아톤 생성 중 오류가 발생했습니다.')
  }
}

// 4. '다시 추천 받기' 핸들러 (초기화)
const resetRecommendation = () => {
  store.recommendationResult = null
  savedFormData.value = null
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
/* View는 레이아웃과 컨테이너 스타일만 유지 */
.recommend-view {
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
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.result-header {
  text-align: center;
  margin-bottom: 20px;
}

.result-header h2 {
  font-size: 1.4rem;
  color: #2c3e50;
  margin-bottom: 8px;
}

/* 애니메이션 */
.fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>