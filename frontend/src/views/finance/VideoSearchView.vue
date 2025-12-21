<template>
  <div>
    <h1>관심 종목 검색</h1>
    <form class="input-group mb-3" @submit.prevent="getVideos">
      <input type="text" class="form-control" placeholder="검색어를 입력하세요" v-model.trim="query">
      <button type="submit" class="btn btn-success" id="search">찾기</button>
    </form>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-5 g-4">
      <div v-for="video in videoStore.videos" :key="video.id.videoId" class="col">
        <VideoCard :video="video" @click="goDetail(video)" />
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

  const getVideos = function () {
    videoStore.getVideos(query.value)
  }
  const goDetail = function (video) {
    router.push({ name: 'videoDetail', params: { id: video.id.videoId } })
  }
</script>

<style scoped>

</style>