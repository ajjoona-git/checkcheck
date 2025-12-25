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
import { useRouter, useRoute } from 'vue-router'
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
.home-wrapper {
  background-color: #fcfcfc;
  min-height: 100vh;
}

/* [SECTION 1] 대시보드 스타일 */
.dashboard-card {
  transition: transform 0.2s ease-in-out;
}

/* [SECTION 1] 히어로 배너 스타일 */
.hero-banner {
  background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);
}

/* [SECTION 2] 빈 상태(Empty State) 스타일 */
.border-dashed {
  border-style: dashed !important;
  border-color: #cbd5e1 !important;
}

.empty-social-state {
  background-color: #f8fafc;
}
</style>