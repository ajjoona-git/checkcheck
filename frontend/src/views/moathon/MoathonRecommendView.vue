<template>
  <div class="page-wrapper">
    <div class="container fade-in">
      
      <div class="header text-center mb-5">
        <h1 class="page-title">모아톤 추천받기</h1>
        <p class="page-subtitle">저축 목표를 입력하고 <span class="highlight">AI 맞춤 상품</span>을 추천받아 보세요.</p>
      </div>

      <div class="recommend-container">
        
        <div v-if="!store.recommendationResult" class="form-section">
          <MoathonRecommendForm :is-loading="store.isRecommending" @submit="handleRecommend" />
        </div>

        <div v-else class="result-section fade-in">
          <MoathonRecommendCard 
            :detail="detail" 
            :warnings="warnings" 
            @create="createWithProduct"
            @retry="resetRecommendation" 
          />
        </div>

      </div>
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

const handleRecommend = async (formData) => {
  savedFormData.value = { ...formData }
  try {
    await store.recommendProduct(formData)
  } catch (error) {
    alert('추천 상품을 불러오지 못했습니다.')
  }
}

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

const resetRecommendation = () => {
  store.recommendationResult = null
  savedFormData.value = null
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.container {
  max-width: 680px;
  width: 100%;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.highlight {
  color: var(--moathon-green);
  font-weight: 700;
}

.recommend-container {
  width: 100%;
}

.bg-green-light { background-color: #e8f5e9; }

.fade-in { animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>