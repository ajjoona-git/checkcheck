<template>
  <div class="container">
    <header class="page-header">
      <h1>🏆 모아톤 챌린지</h1>
      <p>총 {{ store.count }}개의 도전이 진행 중입니다!</p>
      
      <RouterLink :to="{ name: 'moathonCreate' }" class="create-btn">
        + 내 모아톤 만들기
      </RouterLink>
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

    <div class="pagination" v-if="store.totalPages > 1">
      <button 
        :disabled="store.currentPage === 1" 
        @click="changePage(1)"
        class="page-btn nav-btn"
      >
        &lt;&lt;
      </button>

      <button 
        :disabled="store.currentPage === 1" 
        @click="changePage(store.currentPage - 1)"
        class="page-btn nav-btn"
      >
        &lt;
      </button>

      <button 
        v-for="page in visiblePages" 
        :key="page"
        @click="changePage(page)"
        class="page-btn number-btn"
        :class="{ active: page === store.currentPage }"
      >
        {{ page }}
      </button>

      <button 
        :disabled="store.currentPage === store.totalPages" 
        @click="changePage(store.currentPage + 1)"
        class="page-btn nav-btn"
      >
        &gt;
      </button>

      <button 
        :disabled="store.currentPage === store.totalPages" 
        @click="changePage(store.totalPages)"
        class="page-btn nav-btn"
      >
        &gt;&gt;
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useMoathonStore } from '@/stores/moathon'
import MoathonCard from '@/components/moathon/MoathonCard.vue'

const store = useMoathonStore()

// 페이지 변경 핸들러
const changePage = (page) => {
  if (page >= 1 && page <= store.totalPages) {
    store.fetchMoathons(page)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// 화면에 보여줄 페이지 번호 계산 (최대 5개씩 노출)
const visiblePages = computed(() => {
  const current = store.currentPage
  const total = store.totalPages
  const maxVisible = 5
  
  let start = current - Math.floor(maxVisible / 2)
  start = Math.max(start, 1)
  
  let end = start + maxVisible - 1
  end = Math.min(end, total)

  // 끝 부분 보정 (예: 총 10페이지인데 현재 9페이지면 6,7,8,9,10 보여줌)
  if (end - start + 1 < maxVisible) {
    start = Math.max(end - maxVisible + 1, 1)
  }

  const pages = []
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

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
}

/* 그리드 레이아웃 수정 */
.moathon-grid {
  display: grid;
  gap: 20px; /* 카드 간격 24px -> 20px로 조금 좁힘 */
  
  /* 기본(모바일): 1열 */
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

/* 데스크탑: 4열 (최대 4개) */
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

/* 페이지네이션 스타일 (기존 유지) */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 50px;
}

.page-btn {
  background: white;
  border: 1px solid #ddd;
  min-width: 36px; /* 버튼 크기 살짝 조정 */
  height: 36px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  color: #555;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-btn:hover:not(:disabled) {
  background-color: #f0f0f0;
  border-color: #bbb;
}

.page-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
  background-color: #f9f9f9;
}

.page-btn.active {
  background-color: #2c3e50;
  color: white;
  border-color: #2c3e50;
  font-weight: bold;
}

.nav-btn {
  font-weight: bold;
  color: #888;
}
</style>