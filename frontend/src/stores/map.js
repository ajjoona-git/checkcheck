import { ref } from 'vue'
import { defineStore } from 'pinia'

// Kakao 지도 API 로드 및 상태 관리
export const useMapStore = defineStore('map', () => {
  const isScriptLoaded = ref(false)

  // Kakao 지도 API 스크립트 동적 로드
  const loadKakaoMapScript = () => {
    return new Promise((resolve, reject) => {
      if (window.kakao && window.kakao.maps) {
        isScriptLoaded.value = true
        resolve()
        return
      }

      const script = document.createElement('script')
      const API_KEY = import.meta.env.VITE_KAKAO_API_KEY
      
      if (!API_KEY) {
        reject(new Error('Kakao API Key가 없습니다. .env.local을 확인해주세요.'))
        return
      }

      script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&libraries=services&autoload=false`
      script.async = true

      script.onload = () => {
        isScriptLoaded.value = true
        window.kakao.maps.load(() => {
          resolve()
        })
      }

      script.onerror = (error) => {
        reject(error)
      }

      document.head.appendChild(script)
    })
  }

  return { isScriptLoaded, loadKakaoMapScript }
})