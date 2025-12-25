<template>
  <div class="chart-container">
    <div v-if="!isLoaded" class="loading-overlay">
      <div class="spinner-border text-success" role="status"></div>
      <p class="mt-2 text-muted small">차트 로딩 중...</p>
    </div>
    <div ref="chartRef" class="chart-div"></div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useGoogleCharts } from '@/composables/useGoogleCharts'

const props = defineProps({
  chartData: { type: Array, required: true, default: () => [] },
  type: { type: String, default: 'gold' }
})

const chartRef = ref(null)
const { isLoaded, loadCharts } = useGoogleCharts()
let chartInstance = null

const drawChart = (google) => {
  if (!chartRef.value || props.chartData.length === 0) return

  const dataHeader = ['Date', 'Low', 'Open', 'Close', 'High']
  const dataRows = props.chartData.map(item => [
    item.date,            
    item.low,             
    item.open,            
    item.close_last,      
    item.high             
  ])

  const data = google.visualization.arrayToDataTable([
    dataHeader,
    ...dataRows
  ], false) 

  const options = {
    legend: 'none',
    candlestick: {
      fallingColor: { strokeWidth: 0, fill: '#4c6ef5' },
      risingColor: { strokeWidth: 0, fill: '#fa5252' } 
    },
    colors: ['#222'],
    vAxis: { 
      format: 'short',
      textStyle: { color: '#888' },
      gridlines: { color: '#f1f3f5' }
    },
    hAxis: { 
      slantedText: true,       
      slantedTextAngle: 45,    
      showTextEvery: Math.ceil(props.chartData.length / 10),
      textStyle: { fontSize: 11, color: '#888' },
      gridlines: { color: 'transparent' }
    },
    chartArea: { width: '85%', height: '75%', top: 20 }, 
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
.chart-container {
  width: 100%;
  height: 500px;
  position: relative;
}

.chart-div { width: 100%; height: 100%; }

.loading-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(255,255,255,0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10;
}
</style>