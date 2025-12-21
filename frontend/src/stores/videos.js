import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useVideoStore = defineStore('video', () => {
  const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
  const YOUTUBE_API_URL = import.meta.env.VITE_YOUTUBE_API_URL
  const videos = ref([])

  const getVideos = function (query) {
    axios({
      method: 'get',
      url: `${YOUTUBE_API_URL}/search`,
      params: {
        key: YOUTUBE_API_KEY,  // 필수: 발급받은 API Key
        part: 'snippet',       // 필수: 제목, 썸네일 등을 받기 위해 설정
        q: query,              // 필수: 검색어
        type: 'video',         // 선택: 동영상만 검색하도록 필터링
        maxResults: 10,        // 선택: 가져올 동영상 개수
      }
    })
      .then(res => {
        console.log('검색 성공:', res.data.items)
        videos.value = res.data.items
      })
      .catch(err =>{
        console.log(err)
      })
  }

  return { 
    YOUTUBE_API_KEY, YOUTUBE_API_URL, 
    videos,
    getVideos,
  }
}, { persist: true })
