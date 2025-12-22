<template>
  <div class="container">
    <h1 class="page-title">은행 찾기</h1>
    
    <div class="content-wrapper">
      <div class="search-panel">
        
        <div class="form-group">
          <label>광역시 / 도</label>
          <select v-model="selectedProvince" @change="onProvinceChange">
            <option value="">선택하세요</option>
            <option 
              v-for="area in jsonData.mapInfo" 
              :key="area.name" 
              :value="area.name"
            >
              {{ area.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>시 / 군 / 구</label>
          <select v-model="selectedCity">
            <option value="">선택하세요</option>
            <option v-for="city in availableCities" :key="city" :value="city">
              {{ city }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>은행</label>
          <select v-model="selectedBank">
            <option value="">은행을 선택하세요</option>
            <option v-for="bank in jsonData.bankInfo" :key="bank" :value="bank">
              {{ bank }}
            </option>
          </select>
        </div>

        <button @click="searchPlaces" class="search-btn">찾기</button>
      </div>

      <div id="map" class="map-area"></div>
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

const selectedProvince = ref("") // 선택된 광역시/도 (예: 서울특별시)
const selectedCity = ref("")     // 선택된 시/군/구 (예: 강남구)
const selectedBank = ref("")     // 선택된 은행 (예: 국민은행)

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
    center: new kakao.maps.LatLng(37.566826, 126.9786567), // 서울 시청 중심
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
      <div style="padding:10px;font-size:12px;width:200px;">
        <strong style="display:block;margin-bottom:5px;">${place.place_name}</strong>
        <span style="color:gray;">${place.road_address_name || place.address_name}</span>
        <br>
        <a href="${place.place_url}" target="_blank" style="color:blue;">상세보기</a>
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
.container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  border-bottom: 2px solid #ddd;
  padding-bottom: 10px;
}

.content-wrapper {
  display: flex;
  gap: 20px;
  height: 600px;
}

.search-panel {
  width: 300px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-weight: bold;
  font-size: 14px;
}

select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-btn {
  margin-top: auto;
  padding: 15px;
  background-color: #E86A33;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.search-btn:hover {
  background-color: #d55a26;
}

.map-area {
  flex-grow: 1;
  border-radius: 8px;
  border: 1px solid #ddd;
}
</style>