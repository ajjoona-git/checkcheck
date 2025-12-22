<template>
  <div class="detail-card">
    <div class="card-header">
      <span class="bank-badge">{{ detail.bank_name }}</span>
      <h3 class="product-title">{{ detail.product_name }}</h3>
      <div class="rate-highlight">
        <span class="label">최고 금리</span>
        <span class="value">{{ detail.intr_rate2 }}%</span>
      </div>
    </div>

    <hr class="divider" />

    <div class="options-grid">
      <div class="option-item">
        <span class="opt-label">기본 금리</span>
        <span class="opt-value">{{ detail.intr_rate }}%</span>
      </div>
      <div class="option-item">
        <span class="opt-label">저축 기간</span>
        <span class="opt-value">{{ detail.save_trm }}개월</span>
      </div>
      <div class="option-item">
        <span class="opt-label">적립 방식</span>
        <span class="opt-value">{{ detail.rsrv_type_nm }}</span>
      </div>
      <div class="option-item">
        <span class="opt-label">이자 계산</span>
        <span class="opt-value">{{ detail.intr_rate_type_nm }}</span>
      </div>
    </div>

    <div class="detail-text-section">
      <div class="text-group" v-if="detail.spcl_cnd">
        <h4>우대 조건</h4>
        <p>{{ detail.spcl_cnd }}</p>
      </div>

      <div class="text-group" v-if="detail.etc_note">
        <h4>기타 설명</h4>
        <p>{{ detail.etc_note }}</p>
      </div>

      <div class="text-group" v-if="detail.mtrt_int">
        <h4>만기 후 이자율</h4>
        <p>{{ detail.mtrt_int }}</p>
      </div>

      <div class="warning-box" v-if="warnings && warnings.length > 0">
        <h4>가입 전 유의사항</h4>
        <ul>
          <li v-for="(warn, idx) in warnings" :key="idx">
            {{ warn }}
          </li>
        </ul>
      </div>
    </div>

    <div class="action-buttons">
      <button @click="$emit('create')" class="start-btn">
        이 상품으로 시작하기
      </button>
      <button @click="$emit('retry')" class="retry-btn">
        다시 추천 받기
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  detail: {
    type: Object,
    required: true
  },
  warnings: {
    type: Array,
    default: () => []
  }
})

defineEmits(['create', 'retry'])
</script>

<style scoped>
.detail-card {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #eee;
}

.card-header {
  text-align: center;
  margin-bottom: 20px;
}

.bank-badge {
  background: #e3f2fd;
  color: #1976d2;
  font-size: 0.85rem;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 600;
}

.product-title {
  font-size: 1.6rem;
  margin: 12px 0;
  color: #333;
}

.rate-highlight {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #fff5f5;
  color: #e74c3c;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
}

.rate-highlight .value {
  font-size: 1.4rem;
}

.divider {
  border: 0;
  height: 1px;
  background: #eee;
  margin: 24px 0;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.option-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 12px;
}

.opt-label {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 4px;
}

.opt-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.detail-text-section {
  margin-bottom: 30px;
}

.text-group {
  margin-bottom: 20px;
}

.text-group h4 {
  font-size: 1rem;
  color: #2c3e50;
  margin-bottom: 8px;
  font-weight: 700;
}

.text-group p {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.6;
  white-space: pre-line;
  background: #fff;
  padding: 0;
}

.warning-box {
  background-color: #fff8e1;
  border: 1px solid #ffe0b2;
  color: #bf360c;
  padding: 20px;
  border-radius: 12px;
  margin-top: 25px;
}

.warning-box h4 {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.warning-box ul {
  list-style-type: disc;
  padding-left: 20px;
  margin: 0;
}

.warning-box li {
  margin-bottom: 6px;
  font-size: 0.95rem;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.start-btn {
  width: 100%;
  padding: 16px;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.start-btn:hover {
  background: #34495e;
}

.retry-btn {
  width: 100%;
  padding: 14px;
  background: white;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn:hover {
  background: #f1f3f5;
}
</style>