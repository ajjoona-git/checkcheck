<template>
  <div class="pagination" v-if="totalPages > 0">
    <button 
      :disabled="currentPage <= 1" 
      @click="onPageChange(currentPage - 1)" 
      class="page-btn prev"
    >
      &lt;
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
      &gt;
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// 부모로부터 받아야 할 데이터
const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalCount: {
    type: Number,
    required: true
  },
  itemsPerPage: {
    type: Number,
    default: 10 // 기본값 10개
  },
  displayPageCount: {
    type: Number,
    default: 5 // 한 번에 보여줄 페이지 번호 개수 (예: 1 2 3 4 5)
  }
})

// 부모에게 알릴 이벤트
const emit = defineEmits(['change-page'])

// 전체 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(props.totalCount / props.itemsPerPage)
})

// 보여줄 페이지 번호 배열 계산 (예: [1, 2, 3, 4, 5])
const pageNumbers = computed(() => {
  const pages = []
  const half = Math.floor(props.displayPageCount / 2)
  
  // 현재 페이지를 중심으로 범위 계산
  let start = Math.max(1, props.currentPage - half)
  let end = Math.min(totalPages.value, start + props.displayPageCount - 1)

  // 끝부분이 모자라면 앞부분을 더 채움
  if (end - start + 1 < props.displayPageCount) {
    start = Math.max(1, end - props.displayPageCount + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

// 페이지 변경 요청
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
  margin-top: 30px;
}

.page-btn {
  min-width: 40px;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 8px;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-btn:hover:not(:disabled) {
  background: #f8f9fa;
  border-color: #bbb;
}

.page-btn.active {
  background: #2c3e50;
  color: white;
  border-color: #2c3e50;
}

.page-btn:disabled {
  background: #f5f5f5;
  color: #ccc;
  cursor: not-allowed;
  border-color: #eee;
}
</style>