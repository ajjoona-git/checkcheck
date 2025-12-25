<template>
  <div class="badge-library card" ref="containerRef">
    <div class="card-body p-4">
      <div class="badge-grid" :style="{ '--grid-cols': columns }">
        <div 
          v-for="badge in paginatedBadges" 
          :key="badge.id" 
          class="badge-item"
        >
          <div class="badge-icon-wrapper mb-2" :title="badge.description">
            <img 
              :src="resolveImagePath(badge.url)" 
              :alt="badge.name"
              class="badge-img"
              :class="{ 'is-inactive': badge.quantity === 0 }"
            />
            
            <span 
              v-if="badge.quantity >= 2" 
              class="badge-count"
            >
              x{{ badge.quantity }}
            </span>
          </div>

          <p class="badge-name text-center mb-0">
            {{ badge.name }}
          </p>
        </div>
        
        <div 
          v-for="n in emptySlots" 
          :key="`empty-${n}`" 
          class="badge-item empty"
        ></div>
      </div>
    </div>

    <div class="card-footer bg-white border-0 d-flex justify-content-center pb-4" v-if="totalPages > 1">
      <div class="pagination-controls">
        <button 
          class="nav-btn" 
          @click="prevPage" 
          :disabled="currentPage === 0"
        >
          <i class="bi bi-chevron-left"></i>
        </button>
        
        <span class="page-indicator">{{ currentPage + 1 }} / {{ totalPages }}</span>
        
        <button 
          class="nav-btn" 
          @click="nextPage" 
          :disabled="currentPage >= totalPages - 1"
        >
          <i class="bi bi-chevron-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  badges: { type: Array, required: true, default: () => [] }
})

const containerRef = ref(null)
const currentPage = ref(0)
const columns = ref(4)
const itemsPerPage = computed(() => columns.value * 2) // 항상 2줄

let resizeObserver = null

const handleResize = (entries) => {
  for (const entry of entries) {
    const width = entry.contentRect.width
    // 너비에 따라 컬럼 수 조정 (뱃지 하나당 약 100px~120px 확보)
    if (width < 300) {
      columns.value = 2
    } else if (width < 400) {
      columns.value = 3
    } else if (width < 600) {
      columns.value = 4
    } else if (width < 800) {
      columns.value = 5
    } else if (width < 1000) {
      columns.value = 6
    } else {
      columns.value = 8
    }
    
    // 페이지 리셋 (범위 초과 방지)
    if (currentPage.value >= totalPages.value) {
      currentPage.value = Math.max(0, totalPages.value - 1)
    }
  }
}

onMounted(() => {
  if (containerRef.value) {
    resizeObserver = new ResizeObserver(handleResize)
    resizeObserver.observe(containerRef.value)
  }
})

onUnmounted(() => {
  if (resizeObserver) resizeObserver.disconnect()
})

const totalPages = computed(() => {
  if (!props.badges || props.badges.length === 0) return 1
  return Math.ceil(props.badges.length / itemsPerPage.value)
})

const paginatedBadges = computed(() => {
  const start = currentPage.value * itemsPerPage.value
  const end = start + itemsPerPage.value
  return props.badges.slice(start, end)
})

const emptySlots = computed(() => {
  const currentCount = paginatedBadges.value.length
  // 마지막 페이지 등에서 빈 자리가 생기면 채워줌 (높이 유지)
  return Math.max(0, itemsPerPage.value - currentCount)
})

const prevPage = () => { if (currentPage.value > 0) currentPage.value-- }
const nextPage = () => { if (currentPage.value < totalPages.value - 1) currentPage.value++ }

const resolveImagePath = (path) => {
  if (!path) return '/assets/badges/default.png'
  if (path.startsWith('frontend/')) {
    return '/' + path.substring('frontend/'.length)
  }
  return path
}
</script>

<style scoped>
.badge-library {
  border: 1px solid rgba(0,0,0,0.02);
  border-radius: 24px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.03);
  background: white;
  transition: transform 0.2s ease;
  width: 100%; /* 부모 요소에 꽉 차게 */
}

.badge-grid {
  display: grid;
  gap: 16px;
  justify-items: center;
  /* CSS 변수를 통해 동적으로 컬럼 수 설정 */
  grid-template-columns: repeat(var(--grid-cols, 4), 1fr);
  min-height: 240px; /* 2줄 높이 확보 */
}

.badge-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.badge-item.empty { visibility: hidden; }

.badge-icon-wrapper {
  position: relative;
  /* 아이콘 크기: 반응형으로 조정 가능하지만 고정값도 무난함 */
  width: 72px; 
  height: 72px;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 뱃지 배경색을 없애거나 아주 연하게 (이미지가 돋보이도록) */
  background: transparent; 
  transition: transform 0.2s;
}

.badge-item:hover .badge-icon-wrapper {
  transform: scale(1.1);
}

.badge-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  /* 드롭 섀도우로 뱃지 입체감 살리기 */
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
}

.badge-img.is-inactive {
  filter: grayscale(100%) opacity(0.3);
}

.badge-count {
  position: absolute;
  bottom: 0;
  right: -4px;
  background-color: #ff5252;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  border: 2px solid white;
}

.badge-name {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-top: 8px;
  font-weight: 600;
  max-width: 80px; /* 이름 길면 말줄임 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 페이지네이션 컨트롤 */
.pagination-controls {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--bg-secondary);
  padding: 6px 16px;
  border-radius: 30px;
}

.nav-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.nav-btn:disabled { color: #d0d0d0; cursor: not-allowed; }
.nav-btn:hover:not(:disabled) { color: var(--moathon-green); }

.page-indicator {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-primary);
  min-width: 40px;
  text-align: center;
}
</style>