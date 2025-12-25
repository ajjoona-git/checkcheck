<template>
  <div class="page-wrapper">
    <div class="container py-5 fade-in">

      <header class="page-header text-center mb-5">
        <h1 class="header-title">금/은 시세 조회</h1>
        <p class="header-subtitle">
          원하는 기간의 <span class="highlight">시세 변동</span>을 한눈에 확인해보세요.
        </p>
      </header>

      <div class="control-panel mb-4">

        <div class="tabs-group">
          <button v-for="type in ['gold', 'silver']" :key="type" @click="changeAssetType(type)"
            :class="['tab-btn', { active: selectedAsset === type }]">
            {{ type === 'gold' ? '금 (Gold)' : '은 (Silver)' }}
          </button>
        </div>

        <div class="filter-group">
          <div class="date-inputs">
            <input type="date" v-model="startDate" class="form-control date-input" />
            <span class="tilde">~</span>
            <input type="date" v-model="endDate" class="form-control date-input" />
          </div>
          <button @click="fetchMarketPrices(selectedAsset)" class="btn-search">
            <i class="bi bi-search me-1"></i> 조회
          </button>
        </div>
      </div>

      <div class="chart-card shadow-sm mb-5">
        <div class="card-header-custom mb-3">
          <h5 class="chart-title">
            <i class="bi bi-graph-up-arrow me-2 text-success"></i>
            {{ selectedAsset === 'gold' ? '금' : '은' }} 시세 차트
          </h5>
        </div>

        <div class="chart-body">
          <CommodityChart v-if="marketData.length > 0" :chartData="marketData" :type="selectedAsset" />
          <div v-else-if="!isLoading" class="empty-state">
            <i class="bi bi-calendar-x fs-1 mb-2 opacity-50"></i>
            <p>선택한 기간에 데이터가 없습니다.</p>
          </div>
          <div v-else class="loading-state">
            <div class="spinner-border text-success" role="status"></div>
          </div>
        </div>
      </div>

      <div class="table-card shadow-sm" v-if="marketData.length > 0">
        <div class="card-header-custom mb-3">
          <h5 class="table-title">상세 시세표</h5>
        </div>
        <div class="table-responsive">
          <table class="table custom-table">
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
                <td>{{ Number(item.open).toLocaleString() }}</td>
                <td class="text-danger">{{ Number(item.high).toLocaleString() }}</td>
                <td class="text-primary">{{ Number(item.low).toLocaleString() }}</td>
                <td :class="getPriceColor(item)">
                  {{ Number(item.close_last).toLocaleString() }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

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
const startDate = ref('2023-01-01')
const endDate = ref(today)

// 종가 색상 반환 함수
const getPriceColor = (item) => {
  if (item.close_last > item.open) return 'text-danger fw-bold'
  if (item.close_last < item.open) return 'text-primary fw-bold'
  return ''
}

// 시세 데이터 조회 함수
const fetchMarketPrices = async (assetType) => {
  if (startDate.value > endDate.value) {
    alert('종료일이 시작일보다 빠를 수 없습니다.')
    return
  }

  isLoading.value = true
  marketData.value = []

  try {
    const response = await axios.get(`${accountStore.API_URL}/visualizations/commodities/prices`, {
      params: {
        asset: assetType,
        start: startDate.value,
        end: endDate.value
      }
    })

    if (response.data && response.data.data) {
      marketData.value = response.data.data
    }
  } catch (error) {
    console.error('시세 조회 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// 선택된 자산 타입 변경
const changeAssetType = (type) => {
  selectedAsset.value = type
  fetchMarketPrices(type)
}

// 컴포넌트 마운트 시 시세 데이터 조회
onMounted(() => {
  fetchMarketPrices(selectedAsset.value)
})
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

/* Header Styles */
.header-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 12px;
  background: linear-gradient(135deg, var(--moathon-green) 0%, var(--moathon-deep) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.header-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.highlight {
  color: var(--moathon-green);
  font-weight: 800;
}

/* Control Panel */
.control-panel {
  padding: 20px;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

@media (min-width: 768px) {
  .control-panel {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
  }
}

/* Tabs */
.tabs-group {
  display: flex;
  gap: 8px;
  background: #f8f9fa;
  padding: 4px;
  border-radius: 50px;
  width: fit-content;
}

.tab-btn {
  padding: 8px 24px;
  border-radius: 50px;
  border: none;
  background: transparent;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.2s ease;
  font-size: 0.95rem;
}

.tab-btn.active {
  background: white;
  color: var(--moathon-green);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  font-weight: 700;
}

/* Filters */
.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8f9fa;
  padding: 8px 12px;
  border-radius: 16px;
  border: 1px solid #e0e0e0;
}

.date-input {
  border: none;
  background: transparent;
  font-size: 0.9rem;
  color: var(--text-primary);
  padding: 4px;
  width: auto;
}

.date-input:focus {
  box-shadow: none;
}

.tilde {
  color: var(--text-secondary);
}

.btn-search {
  padding: 10px 24px;
  background-color: var(--moathon-green);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-search:hover {
  background-color: #144a18;
  transform: translateY(-1px);
}

/* Charts & Table Cards */
.chart-card,
.table-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  border: 1px solid rgba(0, 0, 0, 0.02);
}

.chart-title,
.table-title {
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.empty-state,
.loading-state {
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

/* Table Custom */
.custom-table th {
  background-color: #f8f9fa;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.9rem;
  border-bottom: 1px solid #eee;
  padding: 16px;
  text-align: center;
}

.custom-table td {
  padding: 16px;
  vertical-align: middle;
  font-size: 0.95rem;
  border-bottom: 1px solid #f1f3f5;
  text-align: center;
}

.custom-table tr:last-child td {
  border-bottom: none;
}

/* Responsive */
@media (max-width: 768px) {
  .filter-group {
    flex-direction: column;
    width: 100%;
  }

  .date-inputs {
    width: 100%;
    justify-content: space-between;
  }

  .btn-search {
    width: 100%;
  }

  .tabs-group {
    width: 100%;
  }

  .tab-btn {
    flex: 1;
  }
}

.fade-in {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>