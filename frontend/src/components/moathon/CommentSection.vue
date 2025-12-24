<template>
  <section class="comment-section mt-5 pt-5 border-top">
    <h3 class="fw-bold mb-4">응원 댓글 <span class="text-primary">{{ comments.length }}</span></h3>

    <div class="comment-input-wrapper mb-5">
      <div class="input-group input-group-lg shadow-sm">
        <input 
          v-model="newComment" 
          type="text" 
          class="form-control border-0 bg-light"
          placeholder="따뜻한 응원의 한마디를 남겨주세요! (Enter로 등록)" 
          @keyup.enter="submitComment" 
        />
        <button 
          class="btn btn-primary px-4 fw-bold" 
          @click="submitComment" 
          :disabled="!newComment.trim()"
        >
          등록
        </button>
      </div>
    </div>

    <div class="comment-list d-flex flex-column gap-3">
      <div v-for="comment in comments" :key="comment.id" class="comment-item p-4 bg-white border rounded-3">

        <div v-if="editingCommentId === comment.id" class="edit-mode d-flex gap-2">
          <input 
            v-model="editCommentContent" 
            type="text" 
            class="form-control"
            @keyup.enter="saveComment(comment.id)" 
          />
          <button @click="saveComment(comment.id)" class="btn btn-dark text-nowrap">저장</button>
          <button @click="cancelEdit" class="btn btn-light border text-nowrap">취소</button>
        </div>

        <div v-else>
          <div class="d-flex justify-content-between mb-2">
            <div class="d-flex align-items-center gap-2">
              <span class="fw-bold">{{ comment.nickname }}</span>
              <span class="text-muted small">{{ formatDate(comment.created_at) }}</span>
            </div>
            <div class="comment-actions" v-if="comment.is_owner">
              <button 
                @click="startEdit(comment)"
                class="btn btn-link p-0 text-muted small text-decoration-none me-2"
              >
                수정
              </button>
              <button 
                @click="deleteComment(comment.id)"
                class="btn btn-link p-0 text-muted small text-decoration-none"
              >
                삭제
              </button>
            </div>
          </div>
          <p class="mb-0 text-dark" style="white-space: pre-wrap;">{{ comment.content }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useMoathonStore } from '@/stores/moathon'

const props = defineProps({
  moathonId: {
    type: Number,
    required: true
  },
  comments: {
    type: Array,
    default: () => []
  }
})

const store = useMoathonStore()

// Local State
const newComment = ref('')
const editingCommentId = ref(null)
const editCommentContent = ref('')

// Helpers
const formatDate = (dateStr) => dateStr ? dateStr.substring(0, 10) : ''

// Actions
const submitComment = async () => {
  if (!newComment.value.trim()) return
  await store.createComment(props.moathonId, newComment.value)
  newComment.value = ''
}

const startEdit = (c) => { 
  editingCommentId.value = c.id
  editCommentContent.value = c.content 
}

const cancelEdit = () => { 
  editingCommentId.value = null
  editCommentContent.value = '' 
}

const saveComment = async (commentId) => {
  if (!editCommentContent.value.trim()) {
    alert('내용을 입력해주세요.')
    return
  }
  await store.updateComment(props.moathonId, commentId, editCommentContent.value)
  cancelEdit()
}

const deleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    await store.deleteComment(props.moathonId, commentId)
  }
}
</script>

<style scoped>
/* 댓글 관련 CSS만 이동 */
.comment-section h3 {
  font-size: 1.1rem;
}

.comment-input-wrapper input:focus {
  box-shadow: none;
  background-color: #fff !important;
}

.comment-item {
  transition: background-color 0.2s;
}
</style>