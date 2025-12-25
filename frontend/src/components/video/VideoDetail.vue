<template>
  <div class="page-wrapper">
    <div class="container py-5 fade-in">
      
      <div class="header-section mb-4">
        <button @click="router.back()" class="btn-back mb-3">
          <i class="bi bi-arrow-left me-2"></i>목록으로
        </button>
      </div>

      <div v-if="video" class="video-detail-card shadow-lg">
        
        <div class="video-wrapper">
          <iframe
            :src="`https://www.youtube.com/embed/${video.id}`" 
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen
          ></iframe>
        </div>

        <div class="card-body p-4 p-md-5">
          <div class="d-flex flex-column gap-3">
            <h1 class="video-title">{{ decodeHtml(video.snippet.title) }}</h1>
            
            <div class="video-meta d-flex align-items-center gap-3 text-secondary">
              <span class="d-flex align-items-center gap-1">
                <i class="bi bi-calendar-event"></i>
                {{ video.snippet.publishedAtFormatted }}
              </span>
              <div class="vertical-divider"></div>
              <span class="d-flex align-items-center gap-1">
                <i class="bi bi-youtube text-danger"></i>
                {{ video.snippet.channelTitle }}
              </span>
            </div>

            <div class="description-box mt-3">
              <h5 class="desc-label mb-3">영상 설명</h5>
              <p class="description">{{ video.snippet.description }}</p>
            </div>
          </div>
        </div>

      </div>
      
      <div v-else class="loading-state">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-3 text-muted">영상을 불러오는 중입니다...</p>
      </div>

    </div>
  </div>
</template>

<script setup>
  import { useRoute, useRouter } from 'vue-router';
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useVideoStore } from '@/stores/videos';

  const route = useRoute()
  const router = useRouter()
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
        alert('영상을 불러올 수 없습니다.')
        router.back()
      })
  }

  onMounted(() => {
    getVideo()
  })
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

.container {
  max-width: 960px;
}

/* Back Button */
.btn-back {
  background: white;
  border: 1px solid rgba(0,0,0,0.1);
  padding: 8px 16px;
  border-radius: 50px;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s;
  display: inline-flex; align-items: center;
}
.btn-back:hover {
  background: #f8f9fa;
  color: var(--text-primary);
  transform: translateX(-4px);
}

/* Card Container */
.video-detail-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.02);
}

/* 16:9 Responsive Video Wrapper */
.video-wrapper {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;
  height: 0;
  background-color: #000;
}

.video-wrapper iframe {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
}

/* Content Styles */
.video-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.3;
  margin: 0;
}

.video-meta {
  font-size: 0.95rem;
}

.vertical-divider {
  width: 1px; height: 14px;
  background-color: #ddd;
}

.divider { border-color: rgba(0,0,0,0.05); }

/* Description Box */
.description-box {
  background-color: #f8f9fa;
  padding: 24px;
  border-radius: 16px;
}

.desc-label {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-secondary);
}

.description {
  white-space: pre-wrap;
  font-size: 1rem;
  line-height: 1.7;
  color: #495057;
  margin: 0;
  word-break: break-word;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 100px 0;
  color: var(--text-secondary);
}

.fade-in { animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .video-title { font-size: 1.4rem; }
  .card-body { padding: 20px; }
}
</style>