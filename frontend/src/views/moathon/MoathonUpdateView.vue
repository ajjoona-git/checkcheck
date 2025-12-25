<template>
  <div class="page-wrapper">
    <div class="container fade-in">
      
      <div class="header text-center mb-5">
        <h1 class="page-title">모아톤 수정하기</h1>
        <p class="page-subtitle">목표나 제목을 변경하여 새로운 마음으로 시작해보세요.</p>
      </div>

      <div class="update-card shadow-sm">
        
        <div v-if="loading" class="loading-state">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-3 text-muted">정보를 불러오는 중입니다...</p>
        </div>

        <div v-else>
          <MoathonCreateForm 
            :is-edit="true"
            :moathon-id="moathonId" 
            :initial-data="initialData"
          />
          
          <div class="mt-4 text-center border-top pt-4">
            <button @click="router.back()" class="btn btn-cancel">
              취소하고 돌아가기
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoathonStore } from '@/stores/moathon'
import MoathonCreateForm from '@/components/moathon/MoathonCreateForm.vue'

const route = useRoute()
const router = useRouter()
const store = useMoathonStore()

const loading = ref(true)
const initialData = ref({})

// 1. URL에서 ID 추출
const moathonId = Number(route.params.id)

onMounted(async () => {
  try {
    if (!store.moathonDetail || store.moathonDetail.id !== moathonId) {
      await store.fetchMoathonDetail(moathonId)
    }
    
    const detail = store.moathonDetail
    if (detail) {
      initialData.value = {
        title: detail.title,
        target_amount: detail.target_amount,
        purpose: detail.purpose,
        id: detail.id
      }
    } else {
      throw new Error('데이터가 존재하지 않습니다.')
    }

  } catch (err) {
    console.error(err)
    alert('정보를 불러오지 못했습니다.')
    router.back()
  } finally {
    loading.value = false
  }
})
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

.update-card {
  background: white;
  padding: 40px;
  border-radius: 32px;
  border: 1px solid rgba(0, 0, 0, 0.02);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
}

.loading-state {
  text-align: center;
  padding: 40px 0;
}

.btn-cancel {
  background: white;
  color: var(--text-secondary);
  border: 1px solid #e0e0e0;
  padding: 10px 24px;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #f8f9fa;
  color: var(--text-primary);
}

.fade-in { animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 576px) {
  .update-card { padding: 24px; }
}
</style>