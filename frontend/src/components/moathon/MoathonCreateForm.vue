<template>
  <div class="form-container">
    <form @submit.prevent="submitForm">

      <div class="form-group mb-4">
        <label for="title" class="form-label">모아톤 이름</label>
        <input 
          type="text" 
          id="title" 
          v-model="formData.title" 
          class="form-control custom-input"
          placeholder="예: 유럽 여행 가자!" 
          required 
        />
      </div>

      <div class="form-group mb-4">
        <label for="target_amount" class="form-label">목표 금액 (원)</label>
        <input 
          type="number" 
          id="target_amount" 
          v-model.number="formData.target_amount" 
          class="form-control custom-input"
          placeholder="목표 금액을 입력하세요"
          required 
          min="0" 
        />
      </div>

      <div class="form-group mb-4" v-if="!isEdit">
        <label for="start_amount" class="form-label">시작 금액 (원)</label>
        <input 
          type="number" 
          id="start_amount" 
          v-model.number="formData.start_amount" 
          class="form-control custom-input"
          placeholder="처음 입금할 금액을 입력하세요"
          required 
          min="0" 
        />
      </div>

      <div class="form-group mb-5">
        <label for="purpose" class="form-label">목표</label>
        <div class="select-wrapper">
          <select id="purpose" v-model="formData.purpose" class="form-select custom-select" required>
            <option value="" disabled>목표를 선택해주세요</option>
            <option value="GOAL">목돈 만들기</option>
            <option value="SHORT">단기 여유자금</option>
            <option value="SAFE">안정적 자산 보관</option>
            <option value="YIELD">이자 극대화</option>
            <option value="HABIT">저축 습관 형성</option>
          </select>
        </div>
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

watch(
  () => props.initialData,
  (newData) => {
    if (newData) {
      if (newData.title) formData.title = newData.title
      if (newData.purpose) formData.purpose = newData.purpose
      if (newData.target_amount) formData.target_amount = newData.target_amount
    }
  },
  { immediate: true }
)

const submitForm = async () => {
  try {
    const payload = {
      ...props.initialData,
      ...formData
    }

    if (props.isEdit) {
      await moathonStore.updateMoathon(props.initialData.id, payload)
      alert('모아톤이 성공적으로 수정되었습니다!')
      router.push({ name: 'moathonDetail', params: { id: props.initialData.id } })

    } else {
      await moathonStore.createMoathon(payload)
      await accountStore.getProfile()
      router.push({ name: 'home' })
    }
    
    emit('submit', payload)
  } catch (err) {
    console.error(err)
    if (err.response && err.response.status === 400) {
        alert('입력 정보를 확인해주세요.')
    } else {
        const msg = props.isEdit ? '수정에 실패했습니다.' : '생성에 실패했습니다.'
        alert(msg)
    }
  }
}
</script>

<style scoped>
.form-container { width: 100%; }

.form-label {
  display: block;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  font-size: 0.95rem;
}

/* 입력 필드 공통 스타일 */
.custom-input, .custom-select {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 16px; /* 둥근 모서리 */
  font-size: 1rem;
  background-color: #fcfcfc;
  transition: all 0.2s ease;
  box-shadow: none; /* 부트스트랩 기본 쉐도우 제거 */
}

.custom-input:focus, .custom-select:focus {
  border-color: var(--moathon-green);
  background-color: white;
  box-shadow: 0 0 0 4px rgba(27, 94, 32, 0.1); /* 초록색 포커스 링 */
}

/* placeholder 색상 */
.custom-input::placeholder { color: #adb5bd; }

/* 버튼 스타일 */
.submit-btn {
  width: 100%;
  padding: 16px;
  background-color: var(--moathon-green);
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 1.1rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(27, 94, 32, 0.2);
}

.submit-btn:hover:not(:disabled) {
  background-color: #144a18;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(27, 94, 32, 0.3);
}

.submit-btn:disabled {
  background-color: #e0e0e0;
  color: #adb5bd;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}
</style>