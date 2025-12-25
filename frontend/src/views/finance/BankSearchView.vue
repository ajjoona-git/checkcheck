<template>
  <div class="page-wrapper">
    <div class="container py-5 fade-in">
      
      <header class="page-header text-center mb-5">
        <h1 class="header-title">내 주변 은행 찾기</h1>
        <p class="header-subtitle">
          원하는 지역의 <span class="highlight">은행 위치</span>를 쉽고 빠르게 찾아보세요.
        </p>
      </header>

      <div class="content-wrapper shadow-lg">
        
        <div class="search-panel">
          <div class="panel-header mb-4">
            <h5 class="fw-bold m-0"><i class="bi bi-geo-alt-fill text-success me-2"></i>지역 선택</h5>
          </div>

          <div class="form-group mb-3">
            <label class="form-label">광역시 / 도</label>
            <div class="select-wrapper">
              <select v-model="selectedProvince" @change="onProvinceChange" class="form-select custom-select">
                <option value="">지역을 선택하세요</option>
                <option 
                  v-for="area in jsonData.mapInfo" 
                  :key="area.name" 
                  :value="area.name"
                >
                  {{ area.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group mb-3">
            <label class="form-label">시 / 군 / 구</label>
            <div class="select-wrapper">
              <select v-model="selectedCity" class="form-select custom-select" :disabled="!selectedProvince">
                <option value="">세부 지역을 선택하세요</option>
                <option v-for="city in availableCities" :key="city" :value="city">
                  {{ city }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group mb-4">
            <label class="form-label">은행 선택</label>
            <div class="select-wrapper">
              <select v-model="selectedBank" class="form-select custom-select">
                <option value="">은행을 선택하세요</option>
                <option v-for="bank in jsonData.bankInfo" :key="bank" :value="bank">
                  {{ bank }}
                </option>
              </select>
            </div>
          </div>

          <button @click="searchPlaces" class="btn-search">
            <i class="bi bi-search me-2"></i>검색하기
          </button>
        </div>

        <div id="map" class="map-area"></div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMapStore } from '@/stores/map'
import jsonData from '@/assets/data.json'

const mapStore = useMapStore()

const map = ref(null)
const markers = ref([]) 
const infowindow = ref(null) 

const selectedProvince = ref("")
const selectedCity = ref("")
const selectedBank = ref("")

const availableCities = computed(() => {
  if (!selectedProvince.value) return []
  const targetArea = jsonData.mapInfo.find(area => area.name === selectedProvince.value)
  return targetArea ? targetArea.countries : []
})

const onProvinceChange = () => {
  selectedCity.value = ""
}

onMounted(async () => {
  if (!mapStore.isScriptLoaded) {
    await mapStore.loadKakaoMapScript()
  }
  initMap()
})

const initMap = () => {
  const container = document.getElementById('map')
  const options = {
    center: new kakao.maps.LatLng(37.566826, 126.9786567),
    level: 3
  }
  map.value = new kakao.maps.Map(container, options)
  infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 })
}

const searchPlaces = () => {
  if (!selectedProvince.value || !selectedCity.value || !selectedBank.value) {
    alert("지역과 은행을 모두 선택해주세요.")
    return
  }

  removeMarker()

  const keyword = `${selectedProvince.value} ${selectedCity.value} ${selectedBank.value}`
  const ps = new kakao.maps.services.Places()
  ps.keywordSearch(keyword, placesSearchCB)
}

const placesSearchCB = (data, status, pagination) => {
  if (status === kakao.maps.services.Status.OK) {
    const bounds = new kakao.maps.LatLngBounds()

    for (let i = 0; i < data.length; i++) {
      displayMarker(data[i])
      bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x))
    }
    map.value.setBounds(bounds)
  } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
    alert('검색 결과가 존재하지 않습니다.')
  } else if (status === kakao.maps.services.Status.ERROR) {
    alert('검색 결과 중 오류가 발생했습니다.')
  }
}

const displayMarker = (place) => {
  const marker = new kakao.maps.Marker({
    map: map.value,
    position: new kakao.maps.LatLng(place.y, place.x)
  })

  markers.value.push(marker)

  kakao.maps.event.addListener(marker, 'click', function() {
    const content = `
      <div style="padding:16px;width:240px;background:white;border-radius:8px;">
        <h5 style="margin:0 0 4px;font-size:14px;font-weight:bold;color:#1b5e20;">${place.place_name}</h5>
        <p style="margin:0 0 8px;font-size:12px;color:#666;">${place.road_address_name || place.address_name}</p>
        <a href="${place.place_url}" target="_blank" style="display:inline-block;padding:4px 8px;background:#e8f5e9;color:#1b5e20;text-decoration:none;font-size:11px;border-radius:4px;font-weight:bold;">상세보기 <span style="font-size:10px;">></span></a>
      </div>
    `
    infowindow.value.setContent(content)
    infowindow.value.open(map.value, marker)
  })
}

const removeMarker = () => {
  if (infowindow.value) {
    infowindow.value.close()
  }
  for (let i = 0; i < markers.value.length; i++) {
    markers.value[i].setMap(null)
  }
  markers.value = []
}
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

/* Header Styles (Unified) */
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

/* Content Styles */
.content-wrapper {
  display: flex;
  height: 600px;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.02);
}

.search-panel {
  width: 320px;
  padding: 32px 24px;
  background-color: #ffffff;
  border-right: 1px solid #f1f3f5;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  z-index: 2;
}

.form-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.custom-select {
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  font-size: 0.95rem;
  background-color: #fcfcfc;
  cursor: pointer;
}
.custom-select:focus {
  border-color: var(--moathon-green);
  box-shadow: 0 0 0 4px rgba(27, 94, 32, 0.1);
}

.btn-search {
  margin-top: auto;
  padding: 14px;
  background-color: var(--moathon-green);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
}
.btn-search:hover {
  background-color: #144a18;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(27, 94, 32, 0.2);
}

.map-area {
  flex-grow: 1;
  background-color: #f1f3f5;
}

@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
    height: auto;
  }
  .search-panel {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #f1f3f5;
  }
  .map-area {
    height: 400px;
  }
}

.fade-in { animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>