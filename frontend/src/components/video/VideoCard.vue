<template>
  <div>
    <div class="card h-100" style="width: 18rem;">
      <img 
        :src="video.snippet.thumbnails.medium.url" 
        class="card-img-top"
        :alt="video.snippet.title"
      >
      <div class="card-body">
        <h5 class="card-title">{{ decodeHtml(video.snippet.title) }}</h5>
      </div>
    </div>
  </div>
</template>

<script setup>
  defineProps({
    video: Object,
  })

  const decodeHtml = (raw) => {
    const parser = new DOMParser()
    const doc = parser.parseFromString(raw, 'text/html')
    return doc.body.textContent || ""
  }
</script>

<style scoped>

</style>