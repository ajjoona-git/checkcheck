<template>
  <div class="badge-library card">
    <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center pt-3 px-3">
      <h6 class="m-0 fw-bold">뱃지 도감</h6>
      <span class="page-indicator text-muted small">{{ currentPage + 1 }} / {{ totalPages }}</span>
    </div>

    <div class="card-body p-3">
      <div class="row g-3" style="min-height: 280px;"> <div 
          v-for="badge in paginatedBadges" 
          :key="badge.id" 
          class="col-4 d-flex flex-column align-items-center justify-content-start"
        >
          <div class="badge-icon-wrapper mb-2" :title="badge.description">
            <img 
              :src="resolveImagePath(badge.url)" 
              :alt="badge.name"
              class="badge-img"
              :class="{ 'is-inactive': badge.quantity === 0 }"
            >
            
            <span 
              v-if="badge.quantity >= 2" 
              class="badge-count badge rounded-pill bg-danger"
            >
              x{{ badge.quantity }}
            </span>
          </div>

          <p class="badge-name text-center mb-0 fw-semibold text-truncate w-100">
            {{ badge.name }}
          </p>
        </div>
      </div>
    </div>

    <div class="card-footer bg-white border-0 d-flex justify-content-between pb-3 px-3" v-if="totalPages > 1">
      <button 
        class="btn btn-sm btn-outline-secondary custom-nav-btn" 
        @click="prevPage" 
        :disabled="currentPage === 0"
      >
        <i class="bi bi-chevron-left"></i> 이전
      </button>
      <button 
        class="btn btn-sm btn-outline-secondary custom-nav-btn" 
        @click="nextPage" 
        :disabled="currentPage >= totalPages - 1"
      >
        다음 <i class="bi bi-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  badges: {
    type: Array,
    required: true,
    default: () => []
  }
})

// 페이지네이션 설정
const itemsPerPage = 9 // 3x3 그리드
const currentPage = ref(0)

// 전체 페이지 수 계산
const totalPages = computed(() => {
  if (!props.badges || props.badges.length === 0) return 1
  return Math.ceil(props.badges.length / itemsPerPage)
})

// 현재 페이지에 해당하는 뱃지들 추출
const paginatedBadges = computed(() => {
  const start = currentPage.value * itemsPerPage
  const end = start + itemsPerPage
  return props.badges.slice(start, end)
})

// 페이지 이동 함수
const prevPage = () => {
  if (currentPage.value > 0) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < totalPages.value - 1) currentPage.value++
}

// 이미지 경로 처리 함수
const resolveImagePath = (path) => {
  if (!path) return '/assets/badges/default.png' // fallback 이미지
  
  // 서버에서 'frontend/src/assets/...' 형태로 넘어오는 경우 처리
  // Vite 개발 환경에서는 '/src/assets/...' 경로로 접근 가능
  if (path.startsWith('frontend/')) {
    return '/' + path.substring('frontend/'.length)
  }
  return path
}
</script>

<style scoped>
.badge-library {
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  overflow: hidden;
}

.badge-icon-wrapper {
  position: relative;
  width: 64px;
  height: 64px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.badge-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: all 0.3s ease;
}

/* 획득하지 못한 뱃지: 흑백 + 투명도 처리 */
.badge-img.is-inactive {
  filter: grayscale(100%);
  opacity: 0.3;
}

/* 수량 뱃지 (우측 하단) */
.badge-count {
  position: absolute;
  bottom: -2px;
  right: -6px;
  font-size: 0.7rem;
  padding: 0.25em 0.6em;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  z-index: 10;
}

.badge-name {
  font-size: 0.75rem;
  color: #555;
  letter-spacing: -0.5px;
}

.page-indicator {
  font-family: monospace;
}

.custom-nav-btn {
  width: 80px;
  border-radius: 20px;
  font-size: 0.8rem;
}
</style>