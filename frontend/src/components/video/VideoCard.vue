<template>
  <div class="video-card h-100" @click="$emit('click')">
    <div class="thumbnail-wrapper">
      <img :src="video.snippet.thumbnails.medium.url" class="card-img-top" :alt="video.snippet.title" loading="lazy">
      <div class="play-overlay">
        <i class="bi bi-play-fill"></i>
      </div>
    </div>

    <div class="card-body p-3">
      <h6 class="video-title mb-1" :title="decodeHtml(video.snippet.title)">
        {{ decodeHtml(video.snippet.title) }}
      </h6>
      <p class="channel-title text-muted small mb-0">
        {{ video.snippet.channelTitle }}
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  video: Object,
})

// HTML 엔티티 디코딩 함수
const decodeHtml = (raw) => {
  const parser = new DOMParser()
  const doc = parser.parseFromString(raw, 'text/html')
  return doc.body.textContent || ""
}
</script>

<style scoped>
.video-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(0, 0, 0, 0.02);
}

.video-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.thumbnail-wrapper {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  overflow: hidden;
}

.card-img-top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.video-card:hover .card-img-top {
  transform: scale(1.05);
}

/* 재생 아이콘 오버레이 (호버 시 등장) */
.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.video-card:hover .play-overlay {
  opacity: 1;
}

.play-overlay i {
  font-size: 3rem;
  color: white;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.video-title {
  font-size: 0.95rem;
  font-weight: 700;
  line-height: 1.4;
  color: var(--text-primary);

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.channel-title {
  font-size: 0.8rem;
}
</style>