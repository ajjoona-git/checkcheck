<template>
  <div class="moathon-card" @click="goDetail" :class="{ 'highlight': isHighlight }">
    <div class="card-header-custom">
      <div class="d-flex justify-content-between align-items-start w-100">
        <h3 class="title text-truncate">{{ moathon.title }}</h3>
        <span class="bank-badge">{{ moathon.bank }}</span>
      </div>
    </div>

    <div class="card-body-custom">
      <div class="info-row">
        <span class="label">Challenger</span>
        <span class="value">{{ moathon.nickname }}</span>
      </div>
      <div class="info-row">
        <span class="label">상품</span>
        <span class="value text-truncate">{{ moathon.product_name }}</span>
      </div>

      <div class="progress-section">
        <div class="progress-bg">
          <div class="progress-fill" :style="{ width: `${moathon.progress_rate}%` }"></div>
        </div>
        <div class="progress-text">
          <span class="label">달성률</span>
          <span class="percent">{{ moathon.progress_rate }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  moathon: {
    type: Object,
    required: true
  },
  isHighlight: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()

// 모아톤 상세 페이지로 이동
const goDetail = () => {
  if (props.moathon.id) {
    router.push({ name: 'moathonDetail', params: { id: props.moathon.id } })
  }
}
</script>

<style scoped>
.moathon-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  position: relative;
  overflow: hidden;
}

/* 하이라이트 모드 (메인 페이지 등에서 강조용) */
.moathon-card.highlight {
  border: 1px solid var(--moathon-green);
  background-color: #f1f8e9;
}

.moathon-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.card-header-custom {
  margin-bottom: 16px;
}

.title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.3;
  max-width: 70%;
}

.bank-badge {
  font-size: 0.75rem;
  background-color: rgba(27, 94, 32, 0.08);
  color: var(--moathon-green);
  padding: 6px 10px;
  border-radius: 20px;
  font-weight: 700;
  white-space: nowrap;
}

.card-body-custom {
  margin-top: auto;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
  margin-bottom: 8px;
}

.info-row .label {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.info-row .value {
  font-weight: 600;
  color: var(--text-primary);
  max-width: 60%;
  text-align: right;
}

.progress-section {
  margin-top: 20px;
}

.progress-bg {
  width: 100%;
  height: 10px;
  background-color: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--moathon-deep) 0%, var(--moathon-green) 100%);
  border-radius: 10px;
  transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.progress-text {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 0.85rem;
}

.progress-text .percent {
  color: var(--moathon-green);
  font-weight: 800;
}
</style>