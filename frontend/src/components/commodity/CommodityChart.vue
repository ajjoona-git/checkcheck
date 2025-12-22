<template>
  <div class="chart-wrapper">
    <div v-if="!isLoaded" class="loading-state">
      <div class="spinner"></div>
      <p>차트 데이터를 불러오는 중입니다...</p>
    </div>
    <div ref="chartRef" class="chart-div"></div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useGoogleCharts } from '@/composables/useGoogleCharts'

const props = defineProps({
  chartData: {
    type: Array,
    required: true,
    default: () => []
  },
  type: {
    type: String, 
    default: 'gold'
  }
})

const chartRef = ref(null)
const { isLoaded, loadCharts } = useGoogleCharts()
let chartInstance = null

const drawChart = (google) => {
  if (!chartRef.value || props.chartData.length === 0) return

  // 1. 데이터 포맷 변환
  const dataHeader = ['Date', 'Low', 'Open', 'Close', 'High']

  const dataRows = props.chartData.map(item => {
    return [
      item.date,            
      item.low,             
      item.open,            
      item.close_last,      
      item.high             
    ]
  })

  const data = google.visualization.arrayToDataTable([
    dataHeader,
    ...dataRows
  ], false) 

  // 2. [수정] 차트 옵션 설정
  const options = {
    legend: 'none',
    candlestick: {
      fallingColor: { strokeWidth: 0, fill: '#4c6ef5' }, 
      risingColor: { strokeWidth: 0, fill: '#fa5252' }   
    },
    colors: ['#222'],
    vAxis: { 
      format: 'short',
      title: '가격 (USD/KRW)'
    },
    // [추가] X축 스타일링 옵션
    hAxis: { 
      slantedText: true,       // 텍스트를 기울임
      slantedTextAngle: 45,    // 45도 회전
      showTextEvery: 1,        // 모든 라벨을 강제로 표시 (생략 방지)
      textStyle: {
        fontSize: 11           // 글자가 많을 경우를 대비해 크기 조정
      }
    },
    // [수정] 차트 영역 조정 (라벨 공간 확보를 위해 height를 80% -> 70%로 축소)
    chartArea: { width: '85%', height: '70%' }, 
    animation: {
      startup: true,
      duration: 1000,
      easing: 'out'
    },
    backgroundColor: 'transparent'
  }

  chartInstance = new google.visualization.CandlestickChart(chartRef.value)
  chartInstance.draw(data, options)
}

onMounted(async () => {
  const google = await loadCharts()
  drawChart(google)
})

watch(() => props.chartData, () => {
  if (isLoaded.value && window.google) {
    drawChart(window.google)
  }
}, { deep: true })
</script>

<style scoped>
/* 기존 스타일 유지 */
.chart-wrapper {
  width: 100%;
  height: 500px;
  position: relative;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  padding: 20px;
}
.chart-div { width: 100%; height: 100%; }
.loading-state {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #888;
}
.spinner {
  width: 40px; height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2c3e50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>