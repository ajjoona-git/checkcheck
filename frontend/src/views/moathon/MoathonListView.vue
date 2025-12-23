<template>
  <div class="container">
    <header class="page-header">
      <h1>모아톤 커뮤니티</h1>
      <p>총 {{ store.count }}개의 도전이 진행 중입니다!</p>
    </header>

    <div v-if="store.moathons.length > 0" class="moathon-grid">
      <MoathonCard 
        v-for="moathon in store.moathons" 
        :key="moathon.id" 
        :moathon="moathon"
      />
    </div>
    
    <div v-else class="empty-state">
      <p>등록된 모아톤이 없습니다.</p>
    </div>

    <div class="pagination-wrapper" v-if="store.count > 0">
      <Pagination
        :current-page="store.currentPage"
        :total-count="store.count"
        :items-per-page="12"
        :display-page-count="5"
        @change-page="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useMoathonStore } from '@/stores/moathon'
import MoathonCard from '@/components/moathon/MoathonCard.vue'
import Pagination from '@/components/common/Pagination.vue'

const store = useMoathonStore()

// 페이지 변경 핸들러
const handlePageChange = (page) => {
  store.fetchMoathons(page)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  store.fetchMoathons(1)
})
</script>

<style scoped>
.container {
  /* 4개를 배치하기 위해 최대 너비를 1200px -> 1320px 정도로 확장 */
  max-width: 1320px; 
  margin: 0 auto;
  padding: 40px 16px; 
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.create-btn {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 24px;
  background-color: #2c3e50;
  color: white;
  text-decoration: none;
  border-radius: 30px;
  font-weight: bold;
  transition: background-color 0.2s;
}

.create-btn:hover {
  background-color: #1a252f;
}

/* 그리드 레이아웃 */
.moathon-grid {
  display: grid;
  gap: 20px; 
  grid-template-columns: repeat(1, 1fr);
}

/* 태블릿 (작은 화면): 2열 */
@media (min-width: 640px) {
  .moathon-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 태블릿 (큰 화면) / 작은 노트북: 3열 */
@media (min-width: 960px) {
  .moathon-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* 데스크탑: 4열 */
@media (min-width: 1280px) {
  .moathon-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.empty-state {
  text-align: center;
  padding: 80px 0;
  color: #888;
}

.pagination-wrapper {
  margin-top: 50px;
  display: flex;
  justify-content: center;
}
</style>