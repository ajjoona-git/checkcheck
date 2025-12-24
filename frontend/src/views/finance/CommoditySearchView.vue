<template>
  <div class="market-container">
    <div class="header-section">
      <h1>금/은 시세 조회</h1>
      <p>원하는 기간의 시세 변동을 확인해보세요.</p>
    </div>

    <div class="filter-controls">
      <div class="date-group">
        <label>기간:</label>
        <input type="date" v-model="startDate" class="date-input" />
        <span>~</span>
        <input type="date" v-model="endDate" class="date-input" />
      </div>
      <button @click="fetchMarketPrices(selectedAsset)" class="search-btn">
        조회
      </button>
    </div>

    <div class="tabs">
      <button 
        v-for="type in ['gold', 'silver']" 
        :key="type"
        @click="changeAssetType(type)"
        :class="['tab-btn', { active: selectedAsset === type }]"
      >
        {{ type === 'gold' ? '금 (Gold)' : '은 (Silver)' }}
      </button>
    </div>

    <div class="chart-section">
      <CommodityChart 
        v-if="marketData.length > 0" 
        :chartData="marketData" 
        :type="selectedAsset" 
      />
      <div v-else-if="!isLoading" class="no-data">
        선택한 기간에 데이터가 없습니다.
      </div>
      <div v-else class="loading-indicator">로딩중...</div>
    </div>

    <div class="table-section" v-if="marketData.length > 0">
      <h3>상세 시세표</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th>날짜</th>
            <th>시가</th>
            <th>고가</th>
            <th>저가</th>
            <th>종가</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in [...marketData].reverse()" :key="item.date">
            <td>{{ item.date }}</td>
            <td>{{ item.open.toLocaleString() }}</td>
            <td class="high">{{ item.high.toLocaleString() }}</td>
            <td class="low">{{ item.low.toLocaleString() }}</td>
            <td :class="getPriceColor(item)">
              {{ item.close_last.toLocaleString() }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import CommodityChart from '@/components/commodity/CommodityChart.vue'

const accountStore = useAccountStore()
const marketData = ref([])
const selectedAsset = ref('gold')
const isLoading = ref(false)

const today = new Date().toISOString().split('T')[0]
const oneMonthAgo = new Date()
oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1)
const lastMonth = oneMonthAgo.toISOString().split('T')[0]

const startDate = ref(lastMonth)
const endDate = ref(today)

// 상승/하락 색상 결정
const getPriceColor = (item) => {
  if (item.close_last > item.open) return 'rising'
  if (item.close_last < item.open) return 'falling'
  return ''
}

// 데이터 조회 함수
const fetchMarketPrices = async (assetType) => {
  if (startDate.value > endDate.value) {
    alert('종료일이 시작일보다 빠를 수 없습니다.')
    return
  }

  isLoading.value = true
  marketData.value = [] // 탭 전환 시 데이터 초기화 (깜빡임 방지)
  
  try {
    // 백엔드 API 호출
    const response = await axios.get(`${accountStore.API_URL}/visualizations/commodities/prices`, {
      params: { 
        asset: assetType,
        start: startDate.value,
        end: endDate.value
      }
    })
    
    // 응답 예시: { asset: "gold", data: [ ... ] }
    // 실제 차트에 필요한 데이터 배열만 추출
    if (response.data && response.data.data) {
      marketData.value = response.data.data
    }
  } catch (error) {
    console.error('시세 조회 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// 탭 변경 핸들러
const changeAssetType = (type) => {
  selectedAsset.value = type
  fetchMarketPrices(type)
}

onMounted(() => {
  fetchMarketPrices(selectedAsset.value)
})
</script>

<style scoped>
.market-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
}
.header-section { text-align: center; margin-bottom: 30px; }
.filter-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 12px;
}

.date-group {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  color: #555;
}

.date-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: inherit;
}
.date-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: inherit;
}

.search-btn {
  padding: 8px 20px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}

.search-btn:hover {
  background-color: #3e5871;
}

.tabs {
  display: flex; justify-content: center; gap: 12px; margin-bottom: 20px;
}
.tab-btn {
  padding: 10px 24px; border-radius: 50px; border: 1px solid #ddd;
  background: white; cursor: pointer; font-weight: 600; text-transform: capitalize;
  transition: all 0.2s;
}
.tab-btn.active {
  background: #2c3e50; color: white; border-color: #2c3e50;
}
.chart-section { margin-bottom: 50px; min-height: 500px; }
.no-data { text-align: center; padding: 50px; color: #888; }
.table-section {
  background: white; padding: 24px; border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.data-table {
  width: 100%; border-collapse: collapse; text-align: center;
}
.data-table th {
  background: #f8f9fa; padding: 12px; font-weight: bold; color: #495057;
}
.data-table td { padding: 12px; border-bottom: 1px solid #eee; }
.high { color: #fa5252; }
.low { color: #4c6ef5; }
.rising { color: #fa5252; font-weight: bold; }
.falling { color: #4c6ef5; font-weight: bold; }
</style>