<template>
  <div class="commodity-chart-container">
    <h1>금/은 현물 시세 차트</h1>
    <div v-if="loading" class="loading">차트 데이터를 불러오는 중...</div>
    <div v-else-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
    <div v-else-if="chartData && chartData.length > 0" class="chart-wrapper">
      <vue-google-charts :data="chartData" :options="chartOptions"></vue-google-charts>
    </div>
    <div v-else class="no-data">
      데이터가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import VueGoogleCharts from 'vue-google-charts';
import { useAccountStore } from '@/stores/accounts';

const loading = ref(true);
const chartData = ref(null);
const errorMessage = ref('');
const chartOptions = ref({
  title: '금/은 현물 시세 차트',
  legend: { position: 'top' },
  hAxis: { title: '날짜' },
  vAxis: { title: '가격' },
  candlestick: {
    fallingColor: { strokeWidth: 0, fill: '#a52714' }, // 빨간색
    risingColor: { strokeWidth: 0, fill: '#0f9d58' }, // 초록색
  },
  chartArea: { width: '80%', height: '70%' },
  animation: {
    startup: true,
    duration: 1000,
    easing: 'inAndOut',
  },
});

const accountStore = useAccountStore()

const fetchCommodityPrices = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/visualizations/commodities/prices', {
      headers: {
        Authorization: `Token ${accountStore.token}`, // 인증 토큰을 Authorization 헤더에 추가
      },
      params: {
        asset: 'gold',
        start: '2023-01-01',
        end: '2023-12-31',
      }
    });

    if (response.data && response.data.data && response.data.data.length > 0) {
      chartData.value = [
        ['Date', 'Low', 'Open', 'Close', 'High'], // Column headers
        ...response.data.data.map(item => [
          item.date, // 날짜
          item.low,  // 저가
          item.open, // 시가
          item.close_last, // 종가
          item.high, // 고가
        ]),
      ];
      loading.value = false;
    } else {
      errorMessage.value = '해당 기간에 데이터가 없습니다.';
      loading.value = false;
    }
  } catch (error) {
    console.error('Error fetching data', error);
    errorMessage.value = '데이터를 가져오는 중 오류가 발생했습니다.';
    loading.value = false;
  }
};

onMounted(() => {
  fetchCommodityPrices();
});
</script>

<style scoped>
.commodity-chart-container {
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  padding: 20px;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 4px;
  color: #c33;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #999;
}

.chart-wrapper {
  margin-top: 20px;
  max-width: 1200px;
}
</style>
