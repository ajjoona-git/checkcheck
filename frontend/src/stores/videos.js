import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

// YouTube 동영상 검색 상태 관리
export const useVideoStore = defineStore('video', () => {
  const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
  const YOUTUBE_API_URL = import.meta.env.VITE_YOUTUBE_API_URL
  const videos = ref([])

  // YouTube API를 통한 금융 관련 동영상 검색
  const getVideos = function (query) {
    axios({
      method: 'get',
      url: `${YOUTUBE_API_URL}/search`,
      params: {
        key: YOUTUBE_API_KEY,
        part: 'snippet',
        q: query,
        type: 'video',
        maxResults: 16,
      }
    })
      .then(res => {
        videos.value = res.data.items
      })
      .catch(err =>{
        // 동영상 검색 실패 처리
        throw err
      })
  }

  return { 
    YOUTUBE_API_KEY, YOUTUBE_API_URL, 
    videos,
    getVideos,
  }
})
