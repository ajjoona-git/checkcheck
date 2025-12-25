<template>
  <div class="form-container">
    <form @submit.prevent="submitForm">
      
      <div class="form-group mb-4">
        <label for="purpose" class="form-label">저축 목적</label>
        <div class="select-wrapper">
          <select id="purpose" v-model="formData.purpose" class="form-select custom-select" required>
            <option value="" disabled>목적을 선택해주세요</option>
            <option value="GOAL">목돈 만들기</option>
            <option value="SHORT">단기 여유자금</option>
            <option value="SAFE">안정적 자산 보관</option>
            <option value="YIELD">이자 극대화</option>
            <option value="HABIT">저축 습관 형성</option>
          </select>
        </div>
      </div>

      <div class="form-group mb-4">
        <label for="target_amount" class="form-label">목표 금액 (원)</label>
        <input 
          type="number" 
          id="target_amount" 
          v-model.number="formData.target_amount" 
          class="form-control custom-input"
          placeholder="예: 10000000"
          required 
        />
      </div>

      <div class="form-group mb-4">
        <label for="start_amount" class="form-label">시작 금액 (원)</label>
        <input 
          type="number" 
          id="start_amount" 
          v-model.number="formData.start_amount" 
          class="form-control custom-input"
          placeholder="예: 2000000"
          required 
        />
      </div>

      <div class="form-group mb-5">
        <label for="term_months" class="form-label">저축 기간 (개월)</label>
        <input 
          type="number" 
          id="term_months" 
          v-model.number="formData.term_months" 
          class="form-control custom-input"
          placeholder="예: 12" 
          required 
        />
      </div>

      <button type="submit" class="submit-btn" :disabled="isLoading">
        <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        {{ isLoading ? 'AI 분석 중...' : '맞춤 상품 추천받기' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  isLoading: Boolean
})

const emit = defineEmits(['submit'])

const formData = reactive({
  purpose: 'GOAL',
  target_amount: null,
  start_amount: null,
  term_months: 12
})

const submitForm = () => {
  emit('submit', { ...formData })
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

.custom-input, .custom-select {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  font-size: 1rem;
  background-color: #fcfcfc;
  transition: all 0.2s ease;
  box-shadow: none;
}

.custom-input:focus, .custom-select:focus {
  border-color: var(--moathon-green);
  background-color: white;
  box-shadow: 0 0 0 4px rgba(27, 94, 32, 0.1);
}

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