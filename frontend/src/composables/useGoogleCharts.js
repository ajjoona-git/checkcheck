import { ref } from 'vue'

// 전역 상태로 관리하여 앱 어디서든 한 번만 로드되도록 함
const isLoaded = ref(false)
const isLoading = ref(false)

export const useGoogleCharts = () => {
  const loadCharts = () => {
    return new Promise((resolve, reject) => {
      // 1. 이미 로드가 완료된 경우 즉시 반환
      if (window.google && window.google.charts && isLoaded.value) {
        resolve(window.google)
        return
      }

      // 2. 다른 컴포넌트에서 이미 로딩을 시작한 경우 (폴링으로 대기)
      if (isLoading.value) {
        const checkInterval = setInterval(() => {
          if (isLoaded.value && window.google) {
            clearInterval(checkInterval)
            resolve(window.google)
          }
        }, 100)
        return
      }

      // 3. 최초 로딩 시작
      isLoading.value = true
      
      const script = document.createElement('script')
      script.src = 'https://www.gstatic.com/charts/loader.js'
      script.async = true
      script.defer = true
      
      script.onload = () => {
        if (!window.google) {
          reject(new Error('Google Charts loader failed to load'))
          return
        }

        // 'corechart' 패키지에는 LineChart, BarChart, CandlestickChart 등이 포함됨
        window.google.charts.load('current', { packages: ['corechart'] })
        
        window.google.charts.setOnLoadCallback(() => {
          isLoaded.value = true
          isLoading.value = false
          resolve(window.google)
        })
      }
      
      script.onerror = (err) => {
        isLoading.value = false
        reject(err)
      }
      
      document.head.appendChild(script)
    })
  }

  return { isLoaded, loadCharts }
}