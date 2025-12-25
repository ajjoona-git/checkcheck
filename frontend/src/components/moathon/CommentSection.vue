<template>
  <section class="comment-section mt-5">
    <div class="d-flex align-items-center mb-3 gap-2">
      <h3 class="fw-bold m-0" style="color: var(--text-primary);">응원하기</h3>
      <span class="badge bg-light text-dark rounded-pill border">{{ comments.length }}</span>
    </div>

    <div class="comment-action-row mb-5 p-2 bg-white shadow-sm border d-flex align-items-center">

      <button class="btn btn-like-circle rounded-circle ms-1" :class="{ active: likes?.is_liked }" @click="onLike"
        title="이 모아톤 응원하기">
        <i class="bi" :class="likes?.is_liked ? 'bi-heart-fill' : 'bi-heart'"></i>
      </button>

      <input v-model="newComment" type="text" class="form-control border-0 bg-transparent px-3"
        placeholder="따뜻한 응원의 한마디를 남겨주세요!" @keyup.enter="submitComment" />

      <button class="btn btn-primary-custom rounded-pill px-4 py-2 me-1" @click="submitComment"
        :disabled="!newComment.trim()">
        등록
      </button>
    </div>

    <div class="comment-list d-flex flex-column gap-3">
      <div v-for="comment in comments" :key="comment.id" class="comment-item p-4 bg-white border rounded-4">

        <div v-if="editingCommentId === comment.id" class="edit-mode d-flex gap-2">
          <input v-model="editCommentContent" type="text" class="form-control" @keyup.enter="saveComment(comment.id)" />
          <button @click="saveComment(comment.id)" class="btn btn-dark btn-sm text-nowrap rounded-3">저장</button>
          <button @click="cancelEdit" class="btn btn-light border btn-sm text-nowrap rounded-3">취소</button>
        </div>

        <div v-else>
          <div class="d-flex justify-content-between mb-2">
            <div class="d-flex align-items-center gap-2">
              <span class="fw-bold text-primary">{{ comment.nickname }}</span>
              <span class="text-muted small">• {{ formatDate(comment.created_at) }}</span>
            </div>

            <div class="comment-actions" v-if="comment.is_owner">
              <button @click="startEdit(comment)" class="action-btn me-2">수정</button>
              <button @click="deleteComment(comment.id)" class="action-btn">삭제</button>
            </div>
          </div>
          <p class="mb-0 text-dark comment-content">{{ comment.content }}</p>
        </div>
      </div>

      <div v-if="comments.length === 0" class="text-center py-5 text-muted">
        <p>아직 작성된 댓글이 없습니다. 첫 번째 응원을 남겨보세요!</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useMoathonStore } from '@/stores/moathon'

const props = defineProps({
  moathonId: { type: Number, required: true },
  comments: { type: Array, default: () => [] },
  likes: { type: Object, default: () => ({ is_liked: false, count: 0 }) },
  onLike: { type: Function, required: true }
})

const store = useMoathonStore()
const newComment = ref('')
const editingCommentId = ref(null)
const editCommentContent = ref('')

const formatDate = (dateStr) => dateStr ? dateStr.substring(0, 10) : ''

// 댓글 등록
const submitComment = async () => {
  if (!newComment.value.trim()) return
  await store.createComment(props.moathonId, newComment.value)
  newComment.value = ''
}

// 댓글 수정 모드 시작
const startEdit = (c) => {
  editingCommentId.value = c.id
  editCommentContent.value = c.content
}

// 댓글 수정 취소
const cancelEdit = () => {
  editingCommentId.value = null
  editCommentContent.value = ''
}

// 댓글 수정 저장
const saveComment = async (commentId) => {
  if (!editCommentContent.value.trim()) {
    alert('내용을 입력해주세요.')
    return
  }
  await store.updateComment(props.moathonId, commentId, editCommentContent.value)
  cancelEdit()
}

// 댓글 삭제
const deleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    await store.deleteComment(props.moathonId, commentId)
  }
}
</script>

<style scoped>
/* 입력창 Row 컨테이너 */
.comment-action-row {
  height: 64px;
  transition: all 0.2s ease;
  border: 1px solid #e0e0e0 !important;
  border-radius: 36px;
}

.comment-action-row:focus-within {
  box-shadow: 0 4px 12px rgba(27, 94, 32, 0.15) !important;
  border-color: var(--moathon-green) !important;
  transform: translateY(-1px);
}

.form-control:focus {
  box-shadow: none;
}

/* 좋아요(하트) 원형 버튼 */
.btn-like-circle {
  width: 48px;
  height: 48px;
  border: 1px solid #f0f0f0;
  background: #f8f9fa;
  color: #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  transition: all 0.2s;
  flex-shrink: 0;
}

.btn-like-circle:hover {
  background: #ffe3e3;
  color: #ff6b6b;
  border-color: #ffc9c9;
}

.btn-like-circle.active {
  background: #ff6b6b;
  color: white;
  border-color: #ff6b6b;
  box-shadow: 0 4px 10px rgba(255, 107, 107, 0.3);
}

/* 등록 버튼 */
.btn-primary-custom {
  background-color: var(--moathon-green);
  color: white;
  border: none;
  font-weight: 700;
  white-space: nowrap;
  transition: all 0.2s;
}

.btn-primary-custom:hover {
  background-color: #144a18;
  transform: translateY(-1px);
}

.btn-primary-custom:disabled {
  background-color: #e9ecef;
  color: #adb5bd;
  transform: none;
}

/* 댓글 아이템 */
.comment-item {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
  border-color: #f1f3f5 !important;
  transition: background-color 0.2s;
}

.comment-content {
  line-height: 1.6;
  white-space: pre-wrap;
  color: #495057;
}

.action-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-decoration: underline;
  cursor: pointer;
}

.action-btn:hover {
  color: var(--text-primary);
}
</style>