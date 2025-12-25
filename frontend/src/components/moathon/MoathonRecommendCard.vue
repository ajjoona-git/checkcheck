<template>
  <div class="detail-card">
    
    <div class="card-header-section text-center mb-4">
      <span class="bank-badge">{{ detail.bank_name }}</span>
      <h3 class="product-title text-truncate">{{ detail.product_name }}</h3>
      
      <div class="rate-highlight mt-3">
        <span class="label">최고 금리</span>
        <span class="value">{{ detail.intr_rate2 }}%</span>
      </div>
    </div>

    <hr class="divider opacity-10" />

    <div class="options-grid mb-4">
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

    <div class="detail-text-section mb-4">
      <div class="info-group" v-if="detail.spcl_cnd">
        <h6 class="info-title">우대 조건</h6>
        <p class="info-desc">{{ detail.spcl_cnd }}</p>
      </div>

      <div class="info-group" v-if="detail.etc_note">
        <h6 class="info-title">기타 설명</h6>
        <p class="info-desc">{{ detail.etc_note }}</p>
      </div>

      <div class="warning-box mt-4" v-if="warnings && warnings.length > 0">
        <h6 class="warning-title"><i class="bi bi-exclamation-triangle-fill me-2"></i>가입 전 유의사항</h6>
        <ul class="warning-list">
          <li v-for="(warn, idx) in warnings" :key="idx">{{ warn }}</li>
        </ul>
      </div>
    </div>

    <div class="action-buttons d-flex flex-column gap-3">
      <button @click="$emit('create')" class="btn-action start">
        이 상품으로 시작하기 <i class="bi bi-arrow-right-circle ms-2"></i>
      </button>
      <button @click="$emit('retry')" class="btn-action retry">
        다시 추천 받기
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  detail: { type: Object, required: true },
  warnings: { type: Array, default: () => [] }
})

defineEmits(['create', 'retry'])
</script>

<style scoped>
.detail-card {
  width: 100%;
}

/* Header */
.bank-badge {
  background-color: rgba(0,0,0,0.05);
  color: var(--text-secondary);
  font-size: 0.85rem;
  padding: 4px 12px;
  border-radius: 50px;
  font-weight: 600;
}

.product-title {
  font-size: 1.8rem;
  font-weight: 800;
  margin-top: 10px;
  color: var(--text-primary);
  line-height: 1.3;
}

.rate-highlight {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #e8f5e9;
  color: var(--moathon-green);
  padding: 8px 20px;
  border-radius: 99px;
}
.rate-highlight .label { font-size: 0.9rem; font-weight: 600; }
.rate-highlight .value { font-size: 1.6rem; font-weight: 800; line-height: 1; }

/* Grid */
.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.option-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8f9fa;
  padding: 16px;
  border-radius: 16px;
}

.opt-label { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 4px; }
.opt-value { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); }

/* Text Section */
.info-group { margin-bottom: 20px; }
.info-title { font-size: 0.95rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; display: flex; align-items: center; }
.info-desc { font-size: 0.95rem; color: #555; line-height: 1.6; margin: 0; background: #fff; }

.warning-box {
  background-color: #fff8e1;
  border: 1px solid #ffe0b2;
  color: #bf360c;
  padding: 20px;
  border-radius: 16px;
}
.warning-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 10px; display: flex; align-items: center; }
.warning-list { margin: 0; padding-left: 20px; font-size: 0.9rem; line-height: 1.5; }

/* Buttons */
.btn-action {
  width: 100%;
  padding: 16px;
  border-radius: 16px;
  font-size: 1.05rem;
  font-weight: 700;
  transition: all 0.2s;
  border: none;
}

.btn-action.start {
  background: var(--moathon-green);
  color: white;
  box-shadow: 0 4px 12px rgba(27, 94, 32, 0.2);
}
.btn-action.start:hover {
  background: #144a18;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(27, 94, 32, 0.3);
}

.btn-action.retry {
  background: white;
  color: var(--text-secondary);
  border: 1px solid #e0e0e0;
}
.btn-action.retry:hover {
  background: #f8f9fa;
  color: var(--text-primary);
}
</style>