<template>
  <div class="rate-chart card">
    <div class="card-body p-4">
      <div v-if="chartData.length > 0" class="chart-container">
        <div v-for="item in chartData" :key="item.id" class="chart-row">
          
          <div class="label-col">
            <span class="product-name text-truncate" :title="item.fin_prdt_nm">{{ item.product_name }}</span>
            <span class="bank-name text-muted">{{ item.bank }}</span>
          </div>
          
          <div class="bar-area">
            <div class="bar-group">
              <div class="bar basic" :style="{ width: item.rate1Width + '%' }">
                <span class="rate-text" v-if="item.rate1Width > 15">{{ item.intr_rate }}%</span>
              </div>
              <span class="legend" v-if="item.rate1Width <= 15">{{ item.intr_rate }}%</span>
              <span class="legend-label">기본</span>
            </div>
            
            <div class="bar-group">
              <div class="bar max" :style="{ width: item.rate2Width + '%' }">
                <span class="rate-text" v-if="item.rate2Width > 15">{{ item.intr_rate2 }}%</span>
              </div>
              <span class="legend" v-if="item.rate2Width <= 15">{{ item.intr_rate2 }}%</span>
              <span class="legend-label text-success fw-bold">최고</span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center py-5 text-muted">
        <i class="bi bi-bar-chart-line fs-1 mb-2 d-block opacity-50"></i>
        비교할 데이터가 없습니다.
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  moathons: {
    type: Array,
    default: () => []
  }
})

// 차트 데이터 가공
const chartData = computed(() => {
  if (!props.moathons || props.moathons.length === 0) return []
  
  // 기준점 계산 (최대 금리가 너무 작으면 5%를 기준으로 함)
  const maxRateValue = Math.max(
    ...props.moathons.map(m => Math.max(m.intr_rate || 0, m.intr_rate2 || 0)), 
    5
  )

  return props.moathons.map(m => ({
    ...m,
    // intr_rate가 없을 경우 0 처리
    rate1Width: ((m.intr_rate || 0) / maxRateValue) * 100,
    rate2Width: ((m.intr_rate2 || 0) / maxRateValue) * 100
  }))
})
</script>

<style scoped>
.rate-chart.card {
  border: 1px solid rgba(0,0,0,0.02);
  border-radius: 24px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.03);
  background: white;
  height: 100%; /* 부모 높이에 맞춤 */
}

.chart-title { color: var(--text-primary); }

.chart-row {
  display: flex;
  margin-bottom: 24px;
  align-items: center;
}

.label-col {
  width: 130px;
  display: flex;
  flex-direction: column;
  margin-right: 16px;
  flex-shrink: 0;
}

.product-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.bank-name {
  font-size: 0.8rem;
}

.bar-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-right: 10px; /* 텍스트 공간 확보 */
}

.bar-group {
  display: flex;
  align-items: center;
  height: 24px;
}

.bar {
  height: 100%;
  border-radius: 6px; /* 둥근 바 */
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 8px;
  font-size: 0.8rem;
  color: white;
  font-weight: 600;
  transition: width 1s cubic-bezier(0.2, 0.8, 0.2, 1);
  min-width: 4px;
}

/* 색상 변수 활용 */
.bar.basic { background-color: var(--moathon-deep); opacity: 0.7; }
.bar.max { background-color: var(--moathon-green); }

.rate-text {
  font-size: 0.75rem;
  white-space: nowrap;
}

.legend {
  font-size: 0.8rem;
  margin-left: 8px;
  color: var(--text-primary);
  font-weight: 600;
}

.legend-label {
  font-size: 0.7rem;
  color: var(--text-secondary);
  margin-left: auto;
  padding-left: 8px;
  min-width: 30px;
  text-align: right;
}
</style>