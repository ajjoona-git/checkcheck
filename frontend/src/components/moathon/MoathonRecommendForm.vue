<template>
  <div class="form-container">
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="purpose">저축 목적</label>
        <select id="purpose" v-model="formData.purpose" required>
          <option value="" disabled>목적을 선택해주세요</option>
          <option value="GOAL">목돈 만들기</option>
          <option value="SHORT">단기 여유자금</option>
          <option value="SAFE">안정적 자산 보관</option>
          <option value="YIELD">이자 극대화</option>
          <option value="HABIT">저축 습관 형성</option>
        </select>
      </div>

      <div class="form-group">
        <label for="target_amount">목표 금액 (원)</label>
        <input type="number" id="target_amount" v-model.number="formData.target_amount" placeholder="예: 10000000"
          required />
      </div>

      <div class="form-group">
        <label for="start_amount">시작 금액 (원)</label>
        <input type="number" id="start_amount" v-model.number="formData.start_amount" placeholder="예: 2000000"
          required />
      </div>

      <div class="form-group">
        <label for="term_months">저축 기간 (개월)</label>
        <input type="number" id="term_months" v-model.number="formData.term_months" placeholder="예: 12" required />
      </div>

      <button type="submit" class="submit-btn" :disabled="isLoading">
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
.form-container {
  width: 100%;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

input,
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.submit-btn {
  width: 100%;
  padding: 15px;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.submit-btn:disabled {
  background: #95a5a6;
}
</style>