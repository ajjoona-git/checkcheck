<template>
  <div class="container py-5" v-if="moathon">

    <header class="detail-header mb-5">
      <div class="d-flex justify-content-between align-items-end border-bottom pb-3">
        <div class="title-section">
          <span class="badge-purpose mb-2">{{ formatPurpose(moathon.purpose) }}</span>
          <h1 class="moathon-title fw-bold">{{ moathon.title }}</h1>
        </div>
        <div class="owner-actions" v-if="isOwner">
          <button @click="handleEdit" class="btn btn-outline-secondary btn-sm me-2">수정</button>
          <button @click="handleDelete" class="btn btn-outline-danger btn-sm">삭제</button>
        </div>
      </div>
    </header>

    <div class="row g-5">
      <div class="col-lg-4">
        <div class="sticky-top" style="top: 2rem; z-index: 10;">
          <div class="user-profile-card shadow-sm border">
            <div class="profile-header d-flex flex-column align-items-center text-center pb-4 border-bottom">
              <img :src="getImageUrl(moathon.user_info.profile_image)" class="profile-img-lg mb-3" alt="프로필" />
              <h4 class="nickname fw-bold mb-1">{{ moathon.user_info.nickname }}</h4>

              <div class="mt-3">
                <span v-if="isOwner" class="badge bg-secondary rounded-pill px-3 py-2">나의 모아톤</span>
                <button v-else @click="handleFollow" :class="['btn-follow', { 'following': isFollowing }]">
                  {{ isFollowing ? '팔로잉' : '팔로우' }}
                </button>
              </div>

              <div class="user-metrics mt-3 d-flex gap-3 text-secondary small">
                <span>팔로워 <b class="text-dark">{{ moathon.user_info.follower_count }}</b></span>
                <span>팔로잉 <b class="text-dark">{{ moathon.user_info.following_count }}</b></span>
              </div>
            </div>

            <div class="badges-section pt-4">
              <BadgeLibrary v-if="moathon.user_info.owner_badges" :badges="moathon.user_info.owner_badges" />
              <p v-else class="text-muted small text-center py-3">아직 획득한 뱃지가 없습니다.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-8">
        <section class="track-section mb-5 p-4">
          <div class="track-wrapper">
            <MoathonTrack :percent="currentProgress" :profile-image="userProfileImage" />
          </div>
        </section>

        <section class="info-stats-grid mb-5">
          <div class="stat-card">
            <span class="label">목표 금액</span>
            <span class="value text-primary">{{ Number(moathon.target_amount).toLocaleString() }}원</span>
          </div>
          <div class="stat-card">
            <span class="label">기간</span>
            <span class="value">{{ moathon.start_date }} ~ {{ moathon.end_date }}</span>
          </div>
          <div class="stat-card">
            <span class="label">D-Day</span>
            <span class="value">{{ dDay }}</span>
          </div>
        </section>

        <section class="product-section mb-5" v-if="mappedProduct">
          <h5 class="fw-bold mb-3">사용 중인 금융 상품</h5>
          <ProductCard :product="mappedProduct" @click="goProductDetail" />
        </section>

        <section class="action-section mb-5">
          <button class="btn-like-large" :class="{ active: moathon.likes.is_liked }" @click="handleLike">
            <span class="heart-icon">{{ moathon.likes.is_liked ? '❤️' : '🤍' }}</span>
            <span class="like-text ms-2">
              {{ moathon.likes.is_liked ? '이미 응원하셨습니다!' : '이 모아톤 응원하기' }}
            </span>
            <span class="like-badge ms-2">{{ moathon.likes.count || 0 }}</span>
          </button>
        </section>

        <hr class="d-lg-none my-5">
      </div>
    </div>

    <section class="comment-section mt-5 pt-5 border-top">
      <h3 class="fw-bold mb-4">응원 댓글 <span class="text-primary">{{ comments.length }}</span></h3>

      <div class="comment-input-wrapper mb-5">
        <div class="input-group input-group-lg shadow-sm">
          <input v-model="newComment" type="text" class="form-control border-0 bg-light"
            placeholder="따뜻한 응원의 한마디를 남겨주세요! (Enter로 등록)" @keyup.enter="submitComment" />
          <button class="btn btn-primary px-4 fw-bold" @click="submitComment" :disabled="!newComment.trim()">
            등록
          </button>
        </div>
      </div>

      <div class="comment-list d-flex flex-column gap-3">
        <div v-for="comment in comments" :key="comment.id" class="comment-item p-4 bg-white border rounded-3">

          <div v-if="editingCommentId === comment.id" class="edit-mode d-flex gap-2">
            <input v-model="editCommentContent" type="text" class="form-control"
              @keyup.enter="saveComment(comment.id)" />
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
                <button @click="startEdit(comment)"
                  class="btn btn-link p-0 text-muted small text-decoration-none me-2">수정</button>
                <button @click="deleteComment(comment.id)"
                  class="btn btn-link p-0 text-muted small text-decoration-none">삭제</button>
              </div>
            </div>
            <p class="mb-0 text-dark" style="white-space: pre-wrap;">{{ comment.content }}</p>
          </div>
        </div>
      </div>
    </section>

  </div>
  <div v-else class="loading-container d-flex justify-content-center align-items-center vh-100">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoathonStore } from '@/stores/moathon'
import { useAccountStore } from '@/stores/accounts'
import ProductCard from '@/components/product/ProductCard.vue'
import BadgeLibrary from '@/components/common/BadgeLibrary.vue'
import MoathonTrack from '@/components/moathon/MoathonTrack.vue';
import defaultProfile from '/default-profile.png'; // [수정] 경로 수정

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
const currentProgress = ref(0)

const isOwner = computed(() => moathon.value?.user_info?.nickname === accountStore.user?.nickname)
const isFollowing = computed(() => moathon.value?.user_info?.is_following)

const getImageUrl = (path) => {
  if (!path) return defaultProfile
  if (path.startsWith('http')) return path
  return `${API_URL}${path}`
}

const userProfileImage = computed(() => {
  if (moathon.value?.user_info?.profile_image) {
    return getImageUrl(moathon.value.user_info.profile_image)
  }
  return defaultProfile;
});

const handleLike = async () => {
  if (!accountStore.isAuthenticated) {
    if (confirm('로그인이 필요한 서비스입니다. 로그인 하시겠습니까?')) router.push({ name: 'login' })
    return
  }
  await store.likeMoathon(route.params.id)
}

const handleFollow = async () => {
  if (!accountStore.isAuthenticated) {
    if (confirm('로그인이 필요한 서비스입니다. 로그인 하시겠습니까?')) router.push({ name: 'login' })
    return
  }
  if (!moathon.value?.user_info) return;
  const result = await accountStore.followUser(moathon.value.user_info.id)
  if (result) {
    await store.fetchMoathonDetail(moathon.value.id)
    await accountStore.getProfile()
  }
}

const mappedProduct = computed(() => {
  if (!moathon.value?.product_option) return null
  const opt = moathon.value.product_option
  return {
    id: opt.product_id,
    fin_prdt_nm: opt.product_name,
    bank_name: opt.bank_name,
    product_type: opt.product_type,
    options: []
  }
})

// --- Utils ---
const dDay = computed(() => {
  if (!moathon.value) return ''
  const end = new Date(moathon.value.end_date)
  const today = new Date()
  const diffDays = Math.ceil((end - today) / (1000 * 60 * 60 * 24))
  return diffDays >= 0 ? `D-${diffDays}` : `D+${Math.abs(diffDays)}`
})

const formatPurpose = (code) => {
  const map = { 'GOAL': '목돈 만들기', 'SHORT': '단기 여유자금', 'SAFE': '안정적 자산 보관', 'YIELD': '이자 극대화', 'HABIT': '저축 습관 형성' }
  return map[code] || code
}
const formatDate = (dateStr) => dateStr ? dateStr.substring(0, 10) : ''

const goProductDetail = () => {
  if (mappedProduct.value?.id) router.push({ name: 'productDetail', params: { id: mappedProduct.value.id } })
}

// --- Comment Actions ---
const startEdit = (c) => { editingCommentId.value = c.id; editCommentContent.value = c.content }
const cancelEdit = () => { editingCommentId.value = null; editCommentContent.value = '' }
const submitComment = async () => {
  if (!newComment.value.trim()) return
  await store.createComment(moathon.value.id, newComment.value)
  newComment.value = ''
}
const saveComment = async (cid) => {
  if (!editCommentContent.value.trim()) return alert('내용 입력')
  await store.updateComment(route.params.id, cid, editCommentContent.value)
  cancelEdit()
}
const deleteComment = async (cid) => {
  if (confirm('삭제하시겠습니까?')) await store.deleteComment(moathon.value.id, cid)
}
const handleEdit = () => router.push({ name: 'moathonUpdate', params: { id: moathon.value.id } })
const handleDelete = async () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await store.deleteMoathon(moathon.value.id)
    router.push({ name: 'home' })
  }
}

// --- Watchers ---
watch(() => route.params.id, async (newId) => {
  if (newId) {
    store.clearMoathonDetail()
    await store.fetchMoathonDetail(newId)
  }
}, { immediate: true })

watch(moathon, (newData) => {
  if (newData?.progress_rate) currentProgress.value = newData.progress_rate
}, { immediate: true })

onUnmounted(() => store.clearMoathonDetail())
</script>

<style scoped>
/* 타이틀 & 뱃지 */
.badge-purpose {
  background-color: #e3f2fd;
  color: #0d6efd;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 700;
}

.moathon-title {
  color: #333;
  margin-top: 0.5rem;
}

/* 정보 그리드 (Stats) */
.info-stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.stat-card .label {
  font-size: 0.85rem;
  color: #888;
  font-weight: 600;
}

.stat-card .value {
  font-size: 1.1rem;
  font-weight: 800;
  color: #333;
}

/* 좋아요 버튼 (Large) */
.btn-like-large {
  width: 100%;
  padding: 18px;
  background: white;
  border: 2px solid #eee;
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-like-large:hover {
  background: #f8f9fa;
  border-color: #ddd;
}

.btn-like-large.active {
  background: #fff0f3;
  border-color: #ffc9db;
  color: #e0245e;
}

.like-badge {
  background: #f1f3f5;
  padding: 2px 10px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.btn-like-large.active .like-badge {
  background: #ffe3e8;
  color: #e0245e;
}

/* 우측 프로필 카드 */
.user-profile-card {
  background: #fff;
  border-radius: 20px;
  padding: 30px 20px;
}

.profile-img-lg {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #f8f9fa;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.btn-follow {
  padding: 8px 24px;
  border-radius: 50px;
  border: none;
  font-weight: bold;
  background: #0d6efd;
  color: white;
  transition: all 0.2s;
}

.btn-follow:hover {
  background: #0b5ed7;
}

.btn-follow.following {
  background: #e9ecef;
  color: #495057;
  border: 1px solid #ced4da;
}

.btn-follow.following:hover {
  color: #dc3545;
  background: #ffeea1;
  border-color: #ffeea1;
}

/* 반응형 모바일 대응 */
@media (max-width: 991px) {
  .info-stats-grid {
    grid-template-columns: 1fr;
  }

  /* 모바일에서 통계 세로 정렬 */
  .sticky-top {
    position: static !important;
  }

  /* 모바일에서 sticky 해제 */
}
</style>