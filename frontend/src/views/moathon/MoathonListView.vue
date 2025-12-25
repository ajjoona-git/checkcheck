<template>
  <div class="page-wrapper">
    <div class="container py-5">
      <header class="page-header text-center mb-5 fade-in">
        <h1 class="header-title">모아톤 커뮤니티</h1>
        <p class="header-subtitle">
          지금 <span class="highlight">{{ store.count }}</span>개의 도전이 함께 달리고 있어요!
        </p>
      </header>

      <div v-if="store.moathons.length > 0" class="moathon-grid fade-in">
        <MoathonCard 
          v-for="moathon in store.moathons" 
          :key="moathon.id" 
          :moathon="moathon"
        />
      </div>
      
      <div v-else class="empty-state fade-in">
        <p class="empty-text">아직 등록된 모아톤이 없습니다.</p>
        <p class="empty-subtext">가장 먼저 챌린지를 시작해보세요!</p>
      </div>

      <div class="pagination-wrapper" v-if="store.count > 0">
        <Pagination
          :current-page="store.currentPage"
          :total-count="store.count"
          :items-per-page="24"
          :display-page-count="5"
          @change-page="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
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
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

.container {
  max-width: 1320px; 
  margin: 0 auto;
}

/* 헤더 스타일 */
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
  font-size: 1.2rem;
}

/* 그리드 레이아웃 */
.moathon-grid {
  display: grid;
  gap: 24px; 
  grid-template-columns: repeat(1, 1fr);
  margin-bottom: 60px;
}

@media (min-width: 640px) { .moathon-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 960px) { .moathon-grid { grid-template-columns: repeat(3, 1fr); } }
@media (min-width: 1280px) { .moathon-grid { grid-template-columns: repeat(4, 1fr); } }

/* 빈 상태 스타일 */
.empty-state {
  text-align: center;
  padding: 100px 0;
  background: white;
  border-radius: 32px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.03);
}

.empty-icon { font-size: 4rem; margin-bottom: 20px; opacity: 0.8; }
.empty-text { font-size: 1.2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; }
.empty-subtext { color: var(--text-secondary); }

.pagination-wrapper {
  margin-top: 40px;
  display: flex;
  justify-content: center;
}

.fade-in { animation: fadeIn 0.6s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>