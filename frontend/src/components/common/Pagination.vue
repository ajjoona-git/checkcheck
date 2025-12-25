<template>
  <div class="pagination" v-if="totalPages > 0">
    <button 
      :disabled="currentPage <= 1" 
      @click="onPageChange(currentPage - 1)" 
      class="page-btn prev"
    >
      <i class="bi bi-chevron-left"></i>
    </button>

    <button 
      v-for="page in pageNumbers" 
      :key="page" 
      class="page-btn number"
      :class="{ active: currentPage === page }"
      @click="onPageChange(page)"
    >
      {{ page }}
    </button>

    <button 
      :disabled="currentPage >= totalPages" 
      @click="onPageChange(currentPage + 1)" 
      class="page-btn next"
    >
      <i class="bi bi-chevron-right"></i>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: { type: Number, required: true },
  totalCount: { type: Number, required: true },
  itemsPerPage: { type: Number, default: 24 }, // [중요] 그리드 개수와 일치 (12)
  displayPageCount: { type: Number, default: 5 }
})

const emit = defineEmits(['change-page'])

const totalPages = computed(() => {
  if (props.totalCount === 0) return 1
  return Math.ceil(props.totalCount / props.itemsPerPage)
})

// [핵심] 페이지 번호 계산 로직 (수정됨)
const pageNumbers = computed(() => {
  const total = totalPages.value
  const current = props.currentPage
  const displayCount = props.displayPageCount

  // 1. 전체 페이지가 보여줄 개수(5)보다 적으면 -> 그냥 1부터 끝까지 다 보여줌
  if (total <= displayCount) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  // 2. 현재 페이지를 기준으로 시작과 끝 계산 (중앙 정렬)
  let start = current - Math.floor(displayCount / 2)
  let end = start + displayCount - 1

  // 3. [보정 1] 시작점이 1보다 작으면 -> 1로 강제 고정하고, 끝점을 다시 계산
  if (start < 1) {
    start = 1
    end = Math.min(total, start + displayCount - 1)
  }

  // 4. [보정 2] 끝점이 전체 페이지를 넘으면 -> 전체 페이지로 강제 고정하고, 시작점을 역산
  if (end > total) {
    end = total
    start = Math.max(1, end - displayCount + 1)
  }

  // 5. 배열 생성
  const pages = []
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const onPageChange = (page) => {
  if (page < 1 || page > totalPages.value) return
  emit('change-page', page)
}
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  width: fit-content;
  margin: 0 auto;
}

.page-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 6px;
  border: none;
  background: transparent;
  border-radius: 50%;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
}

.page-btn:hover:not(:disabled) {
  background: var(--bg-secondary);
  color: var(--moathon-green);
  transform: translateY(-2px);
}

.page-btn.active {
  background: var(--moathon-green);
  color: white;
  box-shadow: 0 4px 10px rgba(27, 94, 32, 0.3);
}

.page-btn:disabled {
  color: #e0e0e0;
  cursor: not-allowed;
  background: transparent;
}
</style>