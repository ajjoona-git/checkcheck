<template>
  <div class="rate-chart card p-4 mb-4">
    <h3 class="mb-3">📊 나의 상품 금리 비교</h3>
    <div class="chart-container">
      <div v-for="item in chartData" :key="item.id" class="chart-row">
        <div class="label-col">
          <span class="product-name">{{ item.product_name }}</span>
          <span class="bank-name">{{ item.bank }}</span>
        </div>
        <div class="bar-area">
          <div class="bar-group">
            <div class="bar basic" :style="{ width: item.rate1Width + '%' }">
              <span class="rate-text">{{ item.intr_rate }}%</span>
            </div>
            <span class="legend">기본</span>
          </div>
          <div class="bar-group">
            <div class="bar max" :style="{ width: item.rate2Width + '%' }">
              <span class="rate-text">{{ item.intr_rate2 }}%</span>
            </div>
            <span class="legend">최고</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  moathons: Array
})

// 차트 데이터 가공: 최대 금리를 100%로 잡고 너비 계산
const chartData = computed(() => {
  if (!props.moathons || props.moathons.length === 0) return []
  
  // 전체 데이터 중 가장 높은 금리 찾기 (너비 기준점)
  const maxRate = Math.max(
    ...props.moathons.map(m => Math.max(m.intr_rate, m.intr_rate2))
  , 5) // 최소 5% 기준

  return props.moathons.map(m => ({
    ...m,
    rate1Width: (m.intr_rate / maxRate) * 100,
    rate2Width: (m.intr_rate2 / maxRate) * 100
  }))
})
</script>

<style scoped>
.chart-row {
  display: flex;
  margin-bottom: 20px;
  align-items: center;
}
.label-col {
  width: 120px;
  display: flex;
  flex-direction: column;
  font-size: 0.9rem;
  margin-right: 15px;
}
.bank-name { font-size: 0.8rem; color: #666; }
.bar-area { flex: 1; }
.bar-group { display: flex; align-items: center; margin-bottom: 4px; }
.bar {
  height: 20px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 5px;
  font-size: 0.75rem;
  color: white;
  transition: width 1s ease-in-out;
}
.bar.basic { background-color: #a5d6a7; } /* 연한 초록 */
.bar.max { background-color: #4caf50; }   /* 진한 초록 */
.legend { font-size: 0.7rem; margin-left: 5px; color: #888; }
</style>