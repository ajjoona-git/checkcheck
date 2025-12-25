<template>
  <div class="options-list">
    <div v-for="option in options" :key="option.id" class="option-card">
      <div class="opt-content">
        <div class="badge-group">
          <span class="badge term">{{ option.save_trm }}개월</span>

          <span v-if="option.rsrv_type_nm" class="badge type">
            {{ option.rsrv_type_nm }}
          </span>

          <span v-if="option.intr_rate_type_nm" class="badge type">
            {{ option.intr_rate_type_nm }}
          </span>
        </div>

        <div class="rates-wrapper">
          <div class="rate-item">
            <span class="label">기본 금리</span>
            <span class="value basic">{{ option.intr_rate }}%</span>
          </div>
          <div class="rate-divider"></div>
          <div class="rate-item">
            <span class="label">최고 우대</span>
            <span class="value max">{{ option.intr_rate2 }}%</span>
          </div>
        </div>
      </div>

      <div class="opt-action">
        <button @click="$emit('select-option', option.id)" class="create-btn">
          이 옵션으로 시작하기 <i class="bi bi-arrow-right-circle ms-2"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  options: {
    type: Array,
    required: true,
    default: () => []
  }
})

defineEmits(['select-option'])
</script>

<style scoped>
.options-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.option-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 24px 32px;
  background: white;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.option-card:hover {
  border-color: #2c3e50;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

/* 좌측 콘텐츠 영역 */
.opt-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 뱃지 스타일 */
.badge-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.badge {
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge.term {
  background-color: #2c3e50;
  color: white;
}

.badge.type {
  background-color: #f1f3f5;
  color: #495057;
  border: 1px solid #dee2e6;
}

/* 금리 정보 스타일 */
.rates-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
}

.rate-item {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.rate-item .label {
  font-size: 0.9rem;
  color: #868e96;
}

.rate-item .value {
  font-size: 1.1rem;
  font-weight: 700;
  font-family: 'Roboto', sans-serif;
}

.value.basic {
  color: #343a40;
}

.value.max {
  color: #e74c3c;
  font-size: 1.25rem;
}

.rate-divider {
  width: 1px;
  height: 14px;
  background-color: #dee2e6;
}

/* 버튼 스타일 */
.create-btn {
  background: #2c3e50;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
  display: flex;
  align-items: center;
}

.create-btn:hover {
  background: #1a252f;
}

/* 모바일 대응 */
@media (max-width: 600px) {
  .option-card {
    flex-direction: column;
    align-items: stretch;
    gap: 20px;
    padding: 24px;
  }

  .opt-action {
    display: flex;
    justify-content: flex-end;
  }

  .create-btn {
    width: 100%;
    justify-content: space-between;
  }
}
</style>