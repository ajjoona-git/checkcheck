<template>
  <div class="update-view-container">
    <h1>모아톤 정보 수정</h1>
    
    <div v-if="loading" class="loading-text">데이터를 불러오는 중...</div>
    
    <MoathonCreateForm 
      v-else
      :is-submitting="submitting" 
      :is-edit="true"
      :initial-data="currentData"
      @submit="handleUpdate" 
    />

    <button class="btn-cancel" @click="goBack">취소</button>
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

const moathonId = route.params.id
const loading = ref(true)
const submitting = ref(false)
const currentData = ref(null)

// 1. 기존 데이터 불러오기
onMounted(async () => {
  try {
    // 상세 데이터가 스토어에 없다면 fetch
    if (!store.moathonDetail || store.moathonDetail.id != moathonId) {
      await store.fetchMoathonDetail(moathonId)
    }
    
    // 폼에 전달할 데이터 객체 생성
    const detail = store.moathonDetail
    if (detail) {
      currentData.value = {
        title: detail.title,
        target_amount: detail.target_amount,
        purpose: detail.purpose,
        // start_amount는 수정 대상이 아니라면 제외
      }
    }
  } catch (err) {
    console.error(err)
    alert('정보를 불러오지 못했습니다.')
    router.go(-1)
  } finally {
    loading.value = false
  }
})

// 2. 수정 요청 처리
const handleUpdate = async (formData) => {
  submitting.value = true
  try {
    // Store의 updateMoathon 액션 호출
    await store.updateMoathon(moathonId, formData)
    
    alert('수정이 완료되었습니다.')
    router.push({ name: 'moathonDetail', params: { id: moathonId } })
  } catch (err) {
    console.error(err)
    alert('수정에 실패했습니다.')
  } finally {
    submitting.value = false
  }
}

const goBack = () => {
  router.go(-1)
}
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