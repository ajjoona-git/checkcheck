<template>
  <div class="moathon-card" @click="goDetail">
    <div class="card-header">
      <h3 class="title">{{ moathon.title }}</h3>
      <span class="bank-badge">{{ moathon.bank }}</span>
    </div>

    <div class="card-body">
      <div class="info-row">
        <span class="label">Challenger</span>
        <span class="value">{{ moathon.nickname }}</span>
      </div>
      <div class="info-row">
        <span class="label">상품</span>
        <span class="value">{{ moathon.product_name }}</span>
      </div>
      
      <div class="progress-section">
        <div class="progress-bg">
          <div 
            class="progress-fill" 
            :style="{ width: `${moathon.progress_rate}%` }"
          ></div>
        </div>
        <div class="progress-text">
          <span>달성률</span>
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
  }
})

const router = useRouter()

const goDetail = () => {
  router.push({ name: 'moathonDetail', params: { id: props.moathon.id } })
}
</script>

<style scoped>
.moathon-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.moathon-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin: 0;
  word-break: keep-all;
  line-height: 1.4;
}

.bank-badge {
  font-size: 0.75rem;
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 6px;
  white-space: nowrap;
  margin-left: 8px;
  flex-shrink: 0;
}

.card-body {
  margin-top: auto;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  margin-bottom: 6px;
  color: #666;
}

.info-row .value {
  font-weight: 600;
  color: #444;
}

.progress-section {
  margin-top: 16px;
}

.progress-bg {
  width: 100%;
  height: 8px;
  background-color: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #4caf50;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.progress-text {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
  font-size: 0.8rem;
  color: #888;
}

.progress-text .percent {
  color: #4caf50;
  font-weight: 700;
}
</style>