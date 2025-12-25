<template>
  <div class="page-wrapper" v-if="!isLoading && moathon && moathon.user_info">
    <div class="container py-5 fade-in">

      <header class="detail-header mb-4">
        <div class="d-flex flex-column flex-lg-row justify-content-between align-items-lg-end gap-3 border-bottom pb-4">
          <div class="title-section">
            <h1 class="moathon-title fw-bold m-0">
              {{ moathon.title }}
              <span class="badge-purpose ms-2">{{ formatPurpose(moathon.purpose) }}</span>
            </h1>
          </div>

          <div class="d-flex align-items-center gap-3">
            <div class="owner-actions d-flex gap-2" v-if="isOwner">
              <button @click="handleEdit" class="btn btn-icon btn-outline-secondary" title="수정">
                <i class="bi bi-pencil-fill"></i>
              </button>
              <button @click="handleDelete" class="btn btn-icon btn-outline-danger" title="삭제">
                <i class="bi bi-trash-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div class="row g-4 mb-5">

        <div class="col-lg-8">
          <div class="info-card main-info-card h-100 p-4 p-md-5">

            <div class="track-section mb-5">
              <div class="track-wrapper">
                <MoathonTrack :percent="currentProgress" :profile-image="userProfileImage" />
              </div>
              <p class="text-center mt-3 text-secondary small">
                목표까지 <span class="text-dark fw-bold">{{ dDayText }}</span> 남았습니다!
              </p>
            </div>

            <hr class="my-5 border-secondary opacity-10">

            <div class="stats-grid">
              <div class="stat-text">
                <span class="label">목표 금액</span>
                <span class="value">{{ Number(moathon.target_amount).toLocaleString() }}원</span>
              </div>

              <div class="stat-text">
                <span class="label">개최일</span>
                <span class="value">{{ moathon.start_date }}</span>
              </div>

              <div class="stat-text">
                <span class="label">종료일</span>
                <span class="value">{{ moathon.end_date }}</span>
              </div>

              <div class="product-embedded">
                <h5 class="section-label mb-3">사용 중인 상품</h5>
                <ProductCard :product="mappedProduct" @click="goProductDetail" />
              </div>
            </div>


          </div>
        </div>

        <div class="col-lg-4">
          <div class="info-card profile-card h-100 d-flex flex-column">
            <div class="d-flex flex-column align-items-center text-center my-5">
              <div class="profile-img-container mb-3">
                <img :src="getImageUrl(moathon.user_info.profile_image)" class="profile-img-lg" alt="프로필" />
              </div>
              <h4 class="nickname">{{ moathon.user_info.nickname }}</h4>

              <div class="mt-2 mb-3">
                <span v-if="isOwner" class="badge bg-secondary-subtle text-secondary rounded-pill px-3 py-1">나의
                  모아톤</span>
                <button v-else @click="handleFollow" :class="['btn-follow btn-sm', { 'following': isFollowing }]">
                  {{ isFollowing ? '팔로잉' : '팔로우' }}
                </button>
              </div>

              <div class="user-metrics d-flex justify-content-center gap-3 small w-100 pt-2">
                <div>
                  <span class="text-secondary d-block mb-1">팔로워</span>
                  <span class="fw-bold text-primary">{{ moathon.user_info.follower_count }}</span>
                </div>
                <div class="vertical-divider"></div>
                <div>
                  <span class="text-secondary d-block mb-1">팔로잉</span>
                  <span class="fw-bold text-dark">{{ moathon.user_info.following_count }}</span>
                </div>
              </div>
            </div>

            <hr class="w-100 my-2 opacity-10 my-4">

            <div class="badges-section flex-grow-1">
              <h4 class="fw-bold">획득한 뱃지</h4>
              <div v-if="moathon.user_info.owner_badges">
                <BadgeLibrary :badges="moathon.user_info.owner_badges"
                  class="sidebar-badge-lib shadow-none border-0 p-0" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-12">
          <CommentSection :moathon-id="moathon.id" :comments="comments" :likes="moathon.likes" :on-like="handleLike" />
        </div>
      </div>

    </div>
  </div>

  <div v-else-if="isLoading" class="loading-container d-flex justify-content-center align-items-center vh-100">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>

  <div v-else class="error-container d-flex flex-column justify-content-center align-items-center vh-100">
    <i class="bi bi-exclamation-circle fs-1 text-muted mb-3"></i>
    <h3 class="text-muted mb-2">모아톤 정보를 불러올 수 없습니다.</h3>
    <button @click="router.push({ name: 'home' })" class="btn btn-primary px-4 rounded-pill mt-3">홈으로 돌아가기</button>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoathonStore } from '@/stores/moathon'
import { useAccountStore } from '@/stores/accounts'
import ProductCard from '@/components/product/ProductCard.vue'
import BadgeLibrary from '@/components/common/BadgeLibrary.vue'
import MoathonTrack from '@/components/moathon/MoathonTrack.vue'
import CommentSection from '@/components/moathon/CommentSection.vue'
import defaultProfile from '/default-profile.png'

const route = useRoute()
const router = useRouter()
const store = useMoathonStore()
const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_API_URL

const isLoading = ref(true)
const currentProgress = ref(0)

// 모아톤 데이터 및 상태 조회
const moathon = computed(() => store.moathonDetail)
const comments = computed(() => moathon.value?.comments || [])
const isOwner = computed(() => moathon.value?.user_info?.nickname === accountStore.user?.nickname)
const isFollowing = computed(() => moathon.value?.user_info?.is_following)

// 사용자 프로필 이미지 URL 조회
const userProfileImage = computed(() => {
  if (moathon.value?.user_info?.profile_image) {
    return getImageUrl(moathon.value.user_info.profile_image)
  }
  return defaultProfile
})

// 상품 정보 변환 (ProductCard 컴포넌트용)
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

// 목표까지 남은 일수 (D-day 계산)
const dDayText = computed(() => {
  if (!moathon.value) return ''
  const end = new Date(moathon.value.end_date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const diffTime = end.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  const result = diffDays >= 0 ? `D-${diffDays}` : `D+${Math.abs(diffDays)}`
  return result
})

// 컴포넌트 마운트 시 모아톤 상세 데이터 조회
onMounted(() => {
  fetchData(route.params.id)
})

// 라우트 변경 시 데이터 재조회
watch(() => route.params.id, (newId) => {
  fetchData(newId)
})

// 진도율 업데이트 감시
watch(moathon, (newData) => {
  if (newData?.progress_rate) {
    currentProgress.value = newData.progress_rate
  }
})

// 컴포넌트 언마운트 시 상태 초기화
onUnmounted(() => store.clearMoathonDetail())

// 프로필 이미지 URL 처리 (절대경로/상대경로 호환)
const getImageUrl = (path) => {
  if (!path) return defaultProfile
  if (path.startsWith('http')) return path
  return `${API_URL}${path}`
}

// 모아톤 목적 텍스트 포맷팅
const formatPurpose = (code) => {
  const map = {
    'GOAL': '목돈 만들기',
    'SHORT': '단기 여유자금',
    'SAFE': '안정적 자산 보관',
    'YIELD': '이자 극대화',
    'HABIT': '저축 습관 형성'
  }
  return map[code] || code
}

// 모아톤 상세 정보 조회 (라우트 ID 기반)
const fetchData = async (id) => {
  if (!id) return

  isLoading.value = true
  store.clearMoathonDetail()

  try {
    await store.fetchMoathonDetail(id)
  } catch (error) {
    if (error.response?.status === 401) {
      alert('로그인이 필요한 서비스입니다.')
      router.push({ name: 'login' })
    }
  } finally {
    isLoading.value = false
  }
}

// 좋아요 토글 (인증 확인)
const handleLike = async () => {
  if (!accountStore.isAuthenticated) {
    if (confirm('로그인이 필요한 서비스입니다.')) router.push({ name: 'login' })
    return
  }
  await store.likeMoathon(route.params.id)
}

// 팔로우 토글 (데이터 갱신 포함)
const handleFollow = async () => {
  if (!accountStore.isAuthenticated) {
    if (confirm('로그인이 필요한 서비스입니다.')) router.push({ name: 'login' })
    return
  }
  if (!moathon.value?.user_info) return
  const result = await accountStore.followUser(moathon.value.user_info.id)
  if (result) {
    await store.fetchMoathonDetail(moathon.value.id)
    await accountStore.getProfile()
  }
}

// 상품 상세 페이지로 이동
const goProductDetail = () => {
  if (mappedProduct.value?.id) {
    router.push({ name: 'productDetail', params: { id: mappedProduct.value.id } })
  }
}

// 모아톤 수정 페이지로 이동
const handleEdit = () => router.push({ name: 'moathonUpdate', params: { id: moathon.value.id } })

// 모아톤 삭제 (확인 후 수행)
const handleDelete = async () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await store.deleteMoathon(moathon.value.id)
    router.push({ name: 'home' })
  }
}
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

/* Animation */
.fade-in {
  animation: fadeIn 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.detail-header {
  position: relative;
}

.moathon-title {
  color: var(--text-primary);
  font-size: 2.2rem;
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.badge-purpose {
  display: inline-block;
  vertical-align: middle;
  background-color: #e8f5e9;
  color: var(--moathon-green);
  font-size: 0.9rem;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 99px;
  transform: translateY(-2px);
}

.btn-icon {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  background: white;
  border: 1px solid #eee;
}

.btn-icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.info-card {
  background: white;
  border-radius: 32px;
  border: 1px solid rgba(0, 0, 0, 0.02);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
  transition: transform 0.3s ease;
}

.track-section {
  position: relative;
}

/* 통계 및 상품 그리드 레이아웃 제어 */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
  align-items: stretch;
}

/* 통계 텍스트 박스 스타일링 */
.stat-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-radius: 24px;
  text-align: center;
}

.stat-text .label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 600;
  margin-bottom: 8px;
}

.stat-text .value {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text-primary);
  word-break: keep-all;
}

.product-embedded {
  grid-column: span 3;
  background-color: white;
  border-radius: 24px;
  padding: 24px;
}

.section-label {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-secondary);
  padding-left: 24px;
}

.profile-card {
  padding: 40px 24px;
}

.profile-img-container {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  padding: 4px;
  border: 2px solid #f1f3f5;
  margin: 0 auto;
}

.profile-img-lg {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.nickname {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
}

/* 팔로우 버튼 */
.btn-follow {
  padding: 8px 24px;
  border-radius: 50px;
  border: none;
  font-weight: 700;
  background: var(--moathon-green);
  color: white;
  transition: all 0.2s;
  box-shadow: 0 4px 10px rgba(27, 94, 32, 0.2);
}

.btn-follow:hover {
  background: #144a18;
  transform: translateY(-2px);
}

.btn-follow.following {
  background: #f1f3f5;
  color: var(--text-secondary);
  box-shadow: none;
  border: 1px solid #e0e0e0;
}

.user-metrics .fw-bold {
  font-size: 1.1rem;
}

.vertical-divider {
  width: 1px;
  height: 24px;
  background-color: #e0e0e0;
  margin: 0 8px;
}

/* 뱃지 섹션 */
.badges-section {
  width: 100%;
  border-radius: 20px;
  margin-top: 20px;
}

.badges-section h4 {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 24px;
  padding-left: 4px;
  font-weight: 700;
}

.loading-container,
.error-container {
  background-color: var(--bg-secondary);
}

.error-container i {
  font-size: 3rem;
  opacity: 0.3;
}

@media (max-width: 991px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .product-embedded {
    grid-column: span 1;
  }
}
</style>