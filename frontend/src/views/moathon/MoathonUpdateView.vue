<template>
  <div class="update-view container py-5">
    <div class="card shadow-sm border-0 p-4" style="max-width: 600px; margin: 0 auto;">
      <h2 class="text-center mb-4 fw-bold">모아톤 수정하기</h2>
      
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>

      <MoathonCreateForm 
        v-else
        :is-edit="true"
        :moathon-id="moathonId" 
        :initial-data="initialData"
      />
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

// 1. URL에서 ID 추출 (숫자 변환)
const moathonId = Number(route.params.id)

onMounted(async () => {
  try {
    // 2. [원본 로직 유지] 스토어에 데이터가 없거나 ID가 다르면 새로 fetch
    // (주의: fetchMoathonDetail은 반환값이 없을 수 있으므로 호출 후 state를 참조)
    if (!store.moathonDetail || store.moathonDetail.id !== moathonId) {
      await store.fetchMoathonDetail(moathonId)
    }
    
    // 3. [데이터 매핑] 스토어의 상세 정보를 폼 데이터 형식에 맞게 변환
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
    router.back() // 뒤로 가기
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.update-view-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

.loading-text {
  text-align: center;
  padding: 40px;
  color: #888;
}

.btn-cancel {
  width: 100%;
  padding: 15px;
  background-color: white;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
}
.btn-cancel:hover {
  background-color: #f8f9fa;
}
</style>