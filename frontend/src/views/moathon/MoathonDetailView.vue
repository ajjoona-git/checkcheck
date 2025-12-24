<template>
  <div class="moathon-detail-container" v-if="moathon">

    <header class="detail-header">
      <div class="title-section">
        <h1 class="moathon-title">{{ moathon.title }}</h1>
        <span class="badge-purpose">{{ formatPurpose(moathon.purpose) }}</span>
      </div>

      <div class="owner-actions" v-if="isOwner">
        <button @click="handleEdit" class="btn-icon">수정</button>
        <button @click="handleDelete" class="btn-icon delete">삭제</button>
      </div>

      <div class="user-profile-card">
        <div class="profile-top">
          <img :src="getImageUrl(moathon.user_info.profile_image)" class="profile-img" alt="프로필" />
          <div class="user-info">
            <h2 class="nickname">
              {{ moathon.user_info.nickname }}
              <span v-if="isOwner" class="badge-owner">ME</span>
            </h2>
            <div class="user-stats">
              <span>팔로워 {{ moathon.user_info.follower_count }}</span>
              <span class="divider">|</span>
              <span>팔로잉 {{ moathon.user_info.following_count }}</span>
            </div>
            <BadgeLibrary 
              v-if="moathon.user_info.owner_badges"
              :badges="moathon.user_info.owner_badges" 
            />
          </div>
        </div>
      </div>
    </header>

    <section class="main-content">
      <div class="track-visual">
        <div class="track-bg">
          <div class="track-progress" :style="{ width: trackWidth }"></div>
          <div class="runner-icon" :style="{ left: trackWidth }">
            🏃
            <span class="progress-bubble">{{ moathon.progress_rate }}%</span>
          </div>
        </div>
        <div class="track-labels">
          <span>START</span>
          <span>GOAL</span>
        </div>
      </div>

      <div class="info-stats">
        <div class="stat-item">
          <span class="label">목표 금액</span>
          <span class="value accent">{{ Number(moathon.target_amount).toLocaleString() }}원</span>
        </div>
        <div class="stat-item">
          <span class="label">기간</span>
          <span class="value">{{ moathon.start_date }} ~ {{ moathon.end_date }}</span>
        </div>
        <div class="stat-item">
          <span class="label">D-Day</span>
          <span class="value">{{ dDay }}</span>
        </div>
      </div>

      <hr class="divider" />

      <div class="product-link-section" v-if="mappedProduct">
        <h3>사용 중인 금융 상품</h3>
        <ProductCard :product="mappedProduct" @click="goProductDetail" />
      </div>
    </section>

    <footer class="detail-footer">
      <div class="action-bar">
        <button class="btn-like" :class="{ active: moathon.likes.is_liked }" @click="handleLike">
          <span class="heart-icon">{{ moathon.likes.is_liked ? '❤️' : '🤍' }}</span>
          <span class="like-text">
            {{ moathon.likes.is_liked ? '응원 중입니다!' : '응원하기' }}
          </span>
          <span class="like-count">
            {{ moathon.likes.count || 0 }}
          </span>
        </button>
      </div>

      <div class="comment-section">
        <h3>응원 댓글 ({{ comments.length }})</h3>

        <div class="comment-input-area">
          <input v-model="newComment" type="text" placeholder="따뜻한 응원의 한마디를 남겨주세요!" @keyup.enter="submitComment" />
          <button @click="submitComment" :disabled="!newComment.trim()">등록</button>
        </div>

        <div class="comment-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">

            <div v-if="editingCommentId === comment.id" class="edit-mode">
              <input v-model="editCommentContent" type="text" class="edit-input"
                @keyup.enter="saveComment(comment.id)" />
              <div class="edit-actions">
                <button @click="saveComment(comment.id)" class="btn-save">저장</button>
                <button @click="cancelEdit" class="btn-cancel">취소</button>
              </div>
            </div>

            <div v-else>
              <div class="comment-header">
                <span class="comment-author">{{ comment.nickname }}</span>
                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              </div>
              <p class="comment-content">{{ comment.content }}</p>

              <div class="comment-actions" v-if="comment.is_owner">
                <button @click="startEdit(comment)">수정</button>
                <button @click="deleteComment(comment.id)">삭제</button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </footer>

  </div>
  <div v-else class="loading">
    로딩 중...
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoathonStore } from '@/stores/moathon'
import { useAccountStore } from '@/stores/accounts'
import ProductCard from '@/components/product/ProductCard.vue'
import BadgeLibrary from '@/components/common/BadgeLibrary.vue'

const route = useRoute()
const router = useRouter()
const store = useMoathonStore()
const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_API_URL

const moathon = computed(() => store.moathonDetail)
const comments = computed(() => moathon.value?.comments || [])
const newComment = ref('')
const editingCommentId = ref(null)
const editCommentContent = ref('')

// [수정] 본인 확인 로직 (user_info 접근)
const isOwner = computed(() => {
  return moathon.value?.user_info?.nickname === accountStore.user?.nickname
})

const getImageUrl = (path) => {
  if (!path) {
    return '/default-profile.png' 
  }
  if (path.startsWith('http')) {
    return path
  }
  return `${API_URL}/media${path}`
}

// [수정] 좋아요 핸들러 (Store 액션 호출 후 로직은 Store에서 처리 가정)
const handleLike = async () => {
  const moathonId = route.params.id

  // 데이터 로딩 전이거나 ID가 없으면 중단
  if (!moathonId || !moathon.value) return

  if (!accountStore.isAuthenticated) {
    if (confirm('로그인이 필요한 서비스입니다. 로그인 하시겠습니까?')) {
      router.push({ name: 'login' })
    }
    return
  }
  await store.likeMoathon(moathonId)
}

// mappedProduct 등 나머지 로직은 기존 구조(product_option)가 유지되므로 동일
const mappedProduct = computed(() => {
  if (!moathon.value?.product_option) return null
  const opt = moathon.value.product_option
  return {
    id: opt.product_id,
    fin_prdt_nm: opt.product_name,
    bank_name: opt.bank_name,
    product_type: opt.product_type,
    max_rate: null,
    options: []
  }
})

// --- Methods (기존과 동일) ---
const trackWidth = computed(() => {
  const rate = parseFloat(moathon.value?.progress_rate || 0)
  return `${Math.min(rate, 100)}%`
})

const dDay = computed(() => {
  if (!moathon.value) return ''
  const end = new Date(moathon.value.end_date)
  const today = new Date()
  const diffTime = end - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays >= 0 ? `D-${diffDays}` : `D+${Math.abs(diffDays)}`
})

const formatPurpose = (code) => {
  const map = {
    'GOAL': '목돈 만들기',
    'SHORT': '단기 여유자금',
    'SAFE': '안정적 자산 보관',
    'YIELD': '이자 극대화',
    'HABIT': '저축 습관 형성',
  }
  return map[code] || code
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.substring(0, 10)
}

const goProductDetail = () => {
  if (mappedProduct.value?.id) {
    router.push({ name: 'productDetail', params: { id: mappedProduct.value.id } })
  }
}

const startEdit = (comment) => {
  editingCommentId.value = comment.id
  editCommentContent.value = comment.content
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

  try {
    const moathonId = route.params.id
    if (!moathonId) return
    await store.updateComment(moathonId, commentId, editCommentContent.value)
    cancelEdit()
  } catch (err) {
    console.error(err)
    alert('댓글 수정에 실패했습니다.')
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  await store.createComment(moathon.value.id, newComment.value)
  newComment.value = ''
  store.fetchMoathonDetail(moathon.value.id)
}

const deleteComment = async (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    await store.deleteComment(moathon.value.id, commentId)
    store.fetchMoathonDetail(moathon.value.id)
  }
}

const handleEdit = () => {
  router.push({ name: 'moathonUpdate', params: { id: moathon.value.id } })
}

const handleDelete = async () => {
  if (!confirm('정말로 모아톤을 삭제하시겠습니까? 복구할 수 없습니다.')) return

  try {
    await store.deleteMoathon(moathon.value.id)
    alert('모아톤이 삭제되었습니다.')
    router.push({ name: 'community' }) 
  } catch (err) {
    console.error(err)
    alert('삭제에 실패했습니다.')
  }
}

// 데이터 로딩
watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      store.clearMoathonDetail()
      store.fetchMoathonDetail(newId)
    }
  },
  { immediate: true }
)

onUnmounted(() => {
  store.clearMoathonDetail()
})
</script>

<style scoped>
/* 스타일은 기존 유지 (템플릿 구조 변화가 크지 않음) */
.moathon-detail-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background: #fff;
}

/* ... (나머지 스타일 코드 생략, 기존 코드 사용) ... */
.detail-header {
  margin-bottom: 30px;
  text-align: center;
}

.user-profile-card {
  background: #f8f9fa;
  border-radius: 20px;
  padding: 24px;
}

.profile-top {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  position: relative;
}

.profile-img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-info {
  text-align: left;
}

.nickname {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0 0 4px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.badge-owner {
  font-size: 0.7rem;
  background: #2c3e50;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
}

.user-stats {
  font-size: 0.9rem;
  color: #666;
}

.divider {
  margin: 0 8px;
  color: #ddd;
}

.owner-actions {
  margin-left: auto;
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px;
}

.title-section {
  text-align: left;
}

.badge-purpose {
  display: inline-block;
  background: #e3f2fd;
  color: #1565c0;
  font-size: 0.8rem;
  padding: 4px 10px;
  border-radius: 12px;
  margin-bottom: 8px;
  font-weight: bold;
}

.moathon-title {
  font-size: 1.5rem;
  margin: 0;
  color: #333;
}

.track-visual {
  margin: 40px 0;
  padding: 0 10px;
}

.track-bg {
  height: 12px;
  background: #e9ecef;
  border-radius: 6px;
  position: relative;
}

.track-progress {
  height: 100%;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 6px;
  transition: width 1s ease-in-out;
}

.runner-icon {
  position: absolute;
  top: -24px;
  transform: translateX(-50%);
  font-size: 1.5rem;
  transition: left 1s ease-in-out;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.progress-bubble {
  font-size: 0.7rem;
  background: #333;
  color: white;
  padding: 2px 6px;
  border-radius: 10px;
  margin-top: 2px;
}

.track-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 0.8rem;
  color: #888;
  font-weight: bold;
}

.info-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  text-align: center;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-item .label {
  font-size: 0.85rem;
  color: #888;
}

.stat-item .value {
  font-weight: bold;
  font-size: 1rem;
  color: #333;
}

.stat-item .value.accent {
  color: #2c3e50;
  font-size: 1.1rem;
}

.btn-like {
  width: 100%;
  padding: 16px;
  background: #fff;
  color: #888;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.btn-like:hover {
  background: #f8f9fa;
}

.btn-like.active {
  background: #fff0f3;
  color: #e0245e;
  border-color: #ffdce0;
}

.like-count {
  background-color: #f1f3f5;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.9rem;
  color: #555;
  font-weight: bold;
}

.btn-like.active .like-count {
  background-color: #ffe3e8;
  color: #e0245e;
}

.comment-section h3 {
  font-size: 1.1rem;
  margin-bottom: 16px;
}

.comment-input-area {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.comment-input-area input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
}

.comment-input-area button {
  padding: 0 20px;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.comment-input-area button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

.comment-author {
  font-weight: bold;
}

.comment-date {
  color: #aaa;
  font-size: 0.8rem;
}

.comment-content {
  margin: 0;
  color: #555;
  line-height: 1.5;
}

.comment-actions {
  text-align: right;
  margin-top: 8px;
}

.comment-actions button {
  background: none;
  border: none;
  color: #aaa;
  font-size: 0.8rem;
  cursor: pointer;
}

.comment-actions button:hover {
  color: #ff6b6b;
  text-decoration: underline;
}

.loading {
  text-align: center;
  padding: 50px;
  color: #888;
}

.edit-mode {
  display: flex;
  gap: 8px;
  align-items: center;
  width: 100%;
}

.edit-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #2c3e50;
  border-radius: 8px;
  font-size: 0.95rem;
}

.edit-actions {
  display: flex;
  gap: 4px;
}

.btn-save {
  background: #2c3e50;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
}

.btn-cancel {
  background: #f1f3f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
}
</style>