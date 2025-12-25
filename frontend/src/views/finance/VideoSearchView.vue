<template>
  <div class="page-wrapper">
    <div class="container py-5 fade-in">

      <header class="page-header text-center mb-5">
        <h1 class="header-title">금융 튜브</h1>
        <p class="header-subtitle">
          관심 있는 <span class="highlight">금융 키워드</span>로 최신 영상을 찾아보세요.
        </p>

        <div class="search-bar-wrapper mt-4 mx-auto">
          <form @submit.prevent="getVideos" class="d-flex align-items-center w-100">
            <i class="bi bi-search text-secondary ms-3"></i>
            <input type="text" class="form-control border-0 bg-transparent shadow-none"
              placeholder="검색어를 입력하세요 (예: 재테크, 적금)" v-model.trim="query">
            <button type="submit" class="btn btn-search-icon">
              <i class="bi bi-arrow-right"></i>
            </button>
          </form>
        </div>
      </header>

      <div v-if="videoStore.videos && videoStore.videos.length > 0"
        class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4">
        <div v-for="video in videoStore.videos" :key="video.id.videoId" class="col">
          <VideoCard :video="video" @click="goDetail(video)" />
        </div>
      </div>

      <div v-else class="text-center py-5 text-muted">
        <p>검색 결과가 없습니다.<br>새로운 키워드로 검색해보세요!</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import VideoCard from '@/components/video/VideoCard.vue';
import { useVideoStore } from '@/stores/videos';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const query = ref(null)
const videoStore = useVideoStore()
const router = useRouter()

// 영상 검색 함수
const getVideos = function () {
  if (!query.value) return
  videoStore.getVideos(query.value)
}

// 영상 상세 페이지로 이동 함수
const goDetail = function (video) {
  router.push({ name: 'videoDetail', params: { id: video.id.videoId } })
}
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

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

/* Search Bar */
.search-bar-wrapper {
  max-width: 500px;
  background: white;
  border-radius: 50px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 4px;
  transition: all 0.3s ease;
}

.search-bar-wrapper:focus-within {
  box-shadow: 0 8px 20px rgba(27, 94, 32, 0.15);
  border-color: var(--moathon-green);
  transform: translateY(-2px);
}

.form-control {
  font-size: 1rem;
  padding: 12px;
}

.btn-search-icon {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background-color: var(--moathon-green);
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-search-icon:hover {
  background-color: #144a18;
  transform: scale(1.05);
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