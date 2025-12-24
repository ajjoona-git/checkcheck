<template>
  <div class="form-container">
    <form @submit.prevent="submitForm">

      <div class="form-group">
        <label for="title">모아톤 이름</label>
        <input type="text" id="title" v-model="formData.title" placeholder="예: 유럽 여행 가자!" required />
      </div>

      <div class="form-group">
        <label for="target_amount">목표 금액 (원)</label>
        <input type="number" id="target_amount" v-model.number="formData.target_amount" placeholder="목표 금액을 입력하세요"
          required min="0" />
      </div>

      <div class="form-group" v-if="!isEdit">
        <label for="start_amount">시작 금액 (원)</label>
        <input type="number" id="start_amount" v-model.number="formData.start_amount" placeholder="처음 입금할 금액을 입력하세요"
          required min="0" />
      </div>

      <div class="form-group">
        <label for="purpose">목표</label>
        <select id="purpose" v-model="formData.purpose" required>
          <option value="" disabled>목표를 선택해주세요</option>
          <option value="GOAL">목돈 만들기</option>
          <option value="SHORT">단기 여유자금</option>
          <option value="SAFE">안정적 자산 보관</option>
          <option value="YIELD">이자 극대화</option>
          <option value="HABIT">저축 습관 형성</option>
        </select>
      </div>

      <button type="submit" class="submit-btn" :disabled="isSubmitting">
        {{ isSubmitting ? '처리 중...' : (isEdit ? '수정 완료' : '모아톤 시작하기') }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useMoathonStore } from '@/stores/moathon'
import { useRouter } from 'vue-router'

const moathonStore = useMoathonStore()
const accountStore = useAccountStore()
const router = useRouter()

const props = defineProps({
  isSubmitting: Boolean,
  initialData: {
    type: Object,
    default: () => ({})
  },
  isEdit: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit'])

const formData = reactive({
  title: '',
  purpose: 'GOAL',
  target_amount: null,
  start_amount: null
})

// [수정] 데이터 매핑 로직 강화
watch(
  () => props.initialData,
  (newData) => {
    if (newData) {
      // 수정 모드이거나, 해당 필드에 값이 있을 때만 매핑 (undefined 방지)
      if (newData.title) formData.title = newData.title
      if (newData.purpose) formData.purpose = newData.purpose
      if (newData.target_amount) formData.target_amount = newData.target_amount
      // start_amount는 보통 수정 불가하므로 초기화 로직에서 제외하거나 필요시 추가
    }
  },
  { immediate: true }
)

const submitForm = async () => {
  try {
    const payload = {
      ...props.initialData, // 예: { product_option: 1 }
      ...formData           // 예: { title: '...', purpose: '...', ... }
    }

    if (props.isEdit) {
      await moathonStore.updateMoathon(props.initialData.id, payload)
      alert('모아톤이 성공적으로 수정되었습니다!')
      router.push({ name: 'moathonDetail', params: { id: props.initialData.id } })

    } else {
      // 생성 (POST)
      await moathonStore.createMoathon(payload)
      await accountStore.getProfile() // 프로필 갱신 (진행 중인 모아톤 목록 업데이트)
      router.push({ name: 'home' })
    }
    
    emit('submit', payload)
  } catch (err) {
    console.error(err)
    if (err.response && err.response.status === 400) {
        alert('입력 정보를 확인해주세요. (필수 항목 누락 등)')
    } else {
        const msg = props.isEdit ? '수정에 실패했습니다.' : '생성에 실패했습니다.'
        alert(msg)
    }
  }
}
</script>

<style scoped>
.form-container { width: 100%; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-weight: 600; margin-bottom: 8px; color: #333; }
input, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
input:focus, select:focus { border-color: #2c3e50; outline: none; }
.submit-btn { width: 100%; padding: 15px; background-color: #2c3e50; color: white; border: none; border-radius: 12px; font-size: 1.1rem; font-weight: bold; cursor: pointer; transition: background-color 0.2s; margin-top: 10px; }
.submit-btn:disabled { background-color: #95a5a6; cursor: not-allowed; }
.submit-btn:hover:not(:disabled) { background-color: #34495e; }
</style>