<template>
  <div class="home-wrapper">
    <div v-if="loading" class="text-center py-5 mt-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="container py-5">
      
      <section class="personal-section mb-5">
        
        <div v-if="hasActiveMoathon" class="dashboard-card bg-white p-4 rounded-4 shadow-sm border">
          <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
            <div>
              <h5 class="text-muted small mb-1">MY MOATHON</h5>
              <h2 class="fw-bold m-0">나의 목표 달성 현황</h2>
            </div>
            
            <div class="d-flex gap-2 align-items-center">
              <select 
                v-if="myActiveMoathons.length > 1" 
                v-model="selectedMoathonId" 
                class="form-select form-select-sm w-auto"
              >
                <option v-for="m in myActiveMoathons" :key="m.id" :value="m.id">
                  {{ m.title }}
                </option>
              </select>
              
              <router-link :to="{ name: 'moathonCreate' }" class="btn btn-sm btn-outline-primary fw-bold text-nowrap">
                + 추가
              </router-link>
            </div>
          </div>

          <div class="row g-4 align-items-center">
            <div class="col-lg-7 col-md-12">
              <div class="p-3">
                <MoathonTrack 
                  :percent="currentProgress" 
                  :profile-image="userProfileImage"
                  :duration="2.5" 
                />
                <p class="text-center mt-3 mb-0 text-muted fw-bold small">
                  목표까지 힘내세요, {{ userNickname }}님! 🏃‍♂️
                </p>
              </div>
            </div>

            <div class="col-lg-5 col-md-12">
              <div class="main-card-wrapper h-100">
                <MoathonCard 
                  v-if="selectedMoathon" 
                  :moathon="selectedMoathon" 
                  :is-highlight="true" 
                />
              </div>
            </div>
          </div>
        </div>

        <div v-else class="hero-banner text-center py-5 rounded-4 bg-primary-subtle border border-primary-subtle">
          <div class="py-2">
            <span class="badge bg-primary mb-3 px-3 py-2 rounded-pill">Start Now</span>
            <h1 class="display-6 fw-bold text-dark mb-3">목돈 만들기, 시작이 반입니다!</h1>
            <p class="text-secondary mb-4">
              나에게 딱 맞는 예적금 상품을 추천받고<br>
              친구들과 함께 저축 챌린지를 시작해보세요.
            </p>
            <a 
              href="#" 
              @click.prevent="handleStartRecommendation" 
              class="btn btn-primary px-5 py-3 fw-bold shadow-sm rounded-pill"
            >
              내 맞춤 모아톤 만들기
            </a>
          </div>
        </div>
      </section>

      <section class="social-section">
        <div class="d-flex align-items-center mb-4 gap-2">
          <h3 class="fw-bold m-0">친구들의 소식</h3>
          <span class="badge bg-secondary-subtle text-secondary rounded-pill">Following</span>
        </div>

        <div v-if="followingMoathons.length > 0" class="row g-4">
          <div 
            v-for="moathon in followingMoathons" 
            :key="moathon.id" 
            class="col-12 col-md-6 col-lg-4"
          >
            <MoathonCard :moathon="moathon" />
          </div>
        </div>

        <div v-else class="empty-social-state text-center py-5 bg-light rounded-4 border border-dashed">
          <div class="py-3">
            <h5 class="fw-bold text-dark">아직 친구들의 소식이 없네요</h5>
            <p class="text-muted mb-4">
              커뮤니티에서 다른 사람들의 챌린지를 구경하고<br>
              마음에 드는 친구를 팔로우해보세요!
            </p>
            <router-link :to="{ name: 'community' }" class="btn btn-outline-dark fw-bold px-4 py-2 rounded-pill">
              커뮤니티 탐색하러 가기
            </router-link>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useMoathonStore } from '@/stores/moathon'
import MoathonCard from '@/components/moathon/MoathonCard.vue'
import MoathonTrack from '@/components/moathon/MoathonTrack.vue'
import defaultProfile from '/default-profile.png'

const router = useRouter()
const accountStore = useAccountStore()
const moathonStore = useMoathonStore()
const API_URL = import.meta.env.VITE_API_URL

const loading = ref(true)
const selectedMoathonId = ref(null)

const hasActiveMoathon = computed(() => {
  return accountStore.user?.moathons && accountStore.user.moathons.length > 0
})
const myActiveMoathons = computed(() => accountStore.user?.moathons || [])

const selectedMoathon = computed(() => {
  if (!selectedMoathonId.value) return myActiveMoathons.value[0]
  return myActiveMoathons.value.find(m => m.id === selectedMoathonId.value) || myActiveMoathons.value[0]
})

const currentProgress = computed(() => {
  if (!selectedMoathon.value) return 0
  return parseFloat(selectedMoathon.value.progress_rate || 0)
})

const userNickname = computed(() => accountStore.user?.nickname || '회원')

const userProfileImage = computed(() => {
  const path = accountStore.user?.profile_image
  if (!path) return defaultProfile
  if (path.startsWith('http')) return path
  return `${API_URL}${path}`
})

const followingMoathons = computed(() => moathonStore.followingMoathons || [])

const fetchMoathonData = async () => {
  if (accountStore.isAuthenticated) {
    if (!accountStore.user) await accountStore.getProfile()
    await moathonStore.getFollowingMoathons()
  }
}

const handleStartRecommendation = () => {
  if (!accountStore.isAuthenticated) {
    const userConfirm = confirm('로그인이 필요한 서비스입니다.\n로그인 페이지로 이동하시겠습니까?')
    if (userConfirm) {
      router.push({ name: 'login' })
    }
    return
  }

  const user = accountStore.user
  const isProfileIncomplete = user?.gender === null || user?.credit_score === null || user?.assets === null || user?.salary === null || user?.average_monthly_spend === null || user?.tender === null
  if (isProfileIncomplete) {
    const confirmMsg = confirm(
      '상품 추천을 위해 추가 정보가 필요합니다.\n\n프로필 수정 페이지로 이동하여 정보를 입력하시겠습니까?'
    )
    if (confirmMsg) {
      router.push({ 
        name: 'mypage',
        query: { edit: 'true' }
      })
    }
    return
  }

  router.push({ name: 'moathonRecommend' })
}

onMounted(async () => {
  try {
    loading.value = true
    if (accountStore.isAuthenticated) {
      await fetchMoathonData()
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

watch(myActiveMoathons, (newVal) => {
  if (newVal && newVal.length > 0 && !selectedMoathonId.value) {
    selectedMoathonId.value = newVal[0].id
  }
}, { immediate: true })

watch(() => accountStore.isAuthenticated, async (newValue) => {
  if (newValue) {
    console.log('로그인 완료 감지 -> 데이터 로드 시작')
    if (!accountStore.user) {
      await accountStore.getProfile()
    }
    await fetchMoathonData()
  }
}, { immediate: true })
</script>

<style scoped>
/* 전체 레이아웃 배경 */
.home-wrapper {
  background-color: var(--bg-secondary); /* #f5f5f7 */
  min-height: calc(100vh - 80px); /* Navbar 높이 고려 */
  padding-bottom: 60px;
}

/* [SECTION 1] 대시보드 카드 스타일 (Bento Grid 스타일) */
.dashboard-card {
  background-color: white;
  border-radius: 32px !important; /* 더 둥글게 */
  border: 1px solid rgba(0, 0, 0, 0.04) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03) !important;
  padding: 40px !important;
  transition: transform 0.3s ease;
}

.dashboard-card h2 {
  color: var(--text-primary);
  font-weight: 800;
}

.dashboard-card h5 {
  color: var(--moathon-green);
  font-weight: 700;
  letter-spacing: 0.05em;
}

/* 드롭다운 스타일 커스텀 */
.form-select {
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
}
.form-select:focus {
  border-color: var(--moathon-green);
  box-shadow: 0 0 0 0.25rem rgba(27, 94, 32, 0.1);
}

/* 추가 버튼 스타일 */
.btn-outline-primary {
  border-color: var(--moathon-green);
  color: var(--moathon-green);
  border-radius: 12px;
  transition: all 0.2s;
}
.btn-outline-primary:hover {
  background-color: var(--moathon-green);
  color: white;
}

/* [SECTION 1] 히어로 배너 (진행 중인 모아톤 없을 때) */
.hero-banner {
  /* Green 계열의 은은한 그라데이션으로 변경 */
  background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%) !important;
  border: 1px solid rgba(27, 94, 32, 0.1) !important;
  border-radius: 32px !important;
  box-shadow: 0 20px 40px rgba(27, 94, 32, 0.05);
  padding: 80px 20px !important;
}

.hero-banner h1 {
  color: var(--text-primary) !important;
  font-weight: 800;
  margin-bottom: 16px;
}

.hero-banner p {
  color: var(--text-secondary) !important;
  font-size: 1.1rem;
  margin-bottom: 32px;
}

.hero-banner .badge {
  background-color: var(--moathon-green) !important;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* 메인 CTA 버튼 (내 맞춤 모아톤 만들기) */
.hero-banner .btn-primary {
  background-color: var(--moathon-green) !important;
  border: none;
  padding: 16px 40px;
  font-size: 1.1rem;
  box-shadow: 0 10px 20px rgba(27, 94, 32, 0.2) !important;
  transition: transform 0.2s, box-shadow 0.2s;
}

.hero-banner .btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(27, 94, 32, 0.3) !important;
  background-color: #144a18 !important; /* hover 시 조금 더 진하게 */
}

/* [SECTION 2] 친구들의 소식 섹션 */
.social-section h3 {
  color: var(--text-primary);
  font-weight: 800;
}

.social-section .badge {
  background-color: rgba(0, 0, 0, 0.05) !important;
  color: var(--text-secondary) !important;
  font-weight: 600;
}

/* 빈 상태(Empty State) 스타일 */
.empty-social-state {
  background-color: white !important;
  border: 2px dashed #e0e0e0 !important;
  border-radius: 24px !important;
  padding: 60px 20px !important;
}

.empty-social-state h5 {
  color: var(--text-primary);
  margin-bottom: 8px;
}

.empty-social-state .btn-outline-dark {
  border-color: var(--text-primary);
  color: var(--text-primary);
  transition: all 0.2s;
}

.empty-social-state .btn-outline-dark:hover {
  background-color: var(--text-primary);
  color: white;
}

/* 스피너 색상 강제 지정 */
.spinner-border.text-primary {
  color: var(--moathon-green) !important;
}

/* 반응형 패딩 조정 */
@media (max-width: 768px) {
  .dashboard-card {
    padding: 24px !important;
    border-radius: 24px !important;
  }
  
  .hero-banner {
    padding: 40px 20px !important;
  }
  
  .hero-banner h1 {
    font-size: 1.8rem;
  }
}
</style>