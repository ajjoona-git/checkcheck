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

const props = defineProps({
  isSubmitting: Boolean,
  // [NEW] 수정을 위한 초기 데이터
  initialData: {
    type: Object,
    default: null
  },
  // [NEW] 수정 모드 여부
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

// [NEW] 초기 데이터가 들어오면 폼에 적용 (Immediate: true로 초기 로딩 대응)
watch(
  () => props.initialData,
  (newData) => {
    if (newData) {
      formData.title = newData.title
      formData.purpose = newData.purpose
      formData.target_amount = newData.target_amount
      // start_amount는 수정 시 보통 제외하지만, 필요하다면 매핑
    }
  },
  { immediate: true }
)

const submitForm = () => {
  emit('submit', { ...formData })
}
</script>

<style scoped>
/* 기존 스타일 그대로 유지 */
.form-container { width: 100%; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-weight: 600; margin-bottom: 8px; color: #333; }
input, select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
input:focus, select:focus { border-color: #2c3e50; outline: none; }
.submit-btn { width: 100%; padding: 15px; background-color: #2c3e50; color: white; border: none; border-radius: 12px; font-size: 1.1rem; font-weight: bold; cursor: pointer; transition: background-color 0.2s; margin-top: 10px; }
.submit-btn:disabled { background-color: #95a5a6; cursor: not-allowed; }
.submit-btn:hover:not(:disabled) { background-color: #34495e; }
</style>