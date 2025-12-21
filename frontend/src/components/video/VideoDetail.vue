<template>
  <div v-if="video">
    <h1>{{ decodeHtml(video.snippet.title) }}</h1>
    <p>업로드 날짜: {{ video.snippet.publishedAtFormatted }}</p>

    <iframe
      width="560"
      height="315" 
      :src="`https://www.youtube.com/embed/${video.id}`" 
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
      allowfullscreen
    ></iframe>

    <p class="description">{{ video.snippet.description }}</p>
  </div>
  
  <div v-else>
    로딩 중...
  </div>
</template>

<script setup>
  import { useRoute } from 'vue-router';
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useVideoStore } from '@/stores/videos';

  const route = useRoute()
  const video = ref(null)
  const videoStore = useVideoStore()

  const decodeHtml = (raw) => {
    const parser = new DOMParser()
    const doc = parser.parseFromString(raw, 'text/html')
    return doc.body.textContent || ""
  }

  const getVideo = () => {
    const videoId = route.params.id
    axios({
      method: 'get',
      url: `${videoStore.YOUTUBE_API_URL}/videos`,
      params: {
        key: videoStore.YOUTUBE_API_KEY,
        part: 'snippet',
        id: videoId, 
      }
    })
      .then(res => {
        const item = res.data.items[0]
        if (item?.snippet?.publishedAt) {
           item.snippet.publishedAtFormatted = item.snippet.publishedAt.split('T')[0]
        }

        console.log('상세 정보 조회 성공:', item)
        video.value = item
      })
      .catch(err =>{
        console.log(err)
      })
  }

  onMounted(() => {
    getVideo()
  })
</script>

<style scoped>
.description {
  white-space: pre-wrap; /* 설명의 줄바꿈을 유지해서 보여줍니다 */
  margin-top: 20px;
}
</style>