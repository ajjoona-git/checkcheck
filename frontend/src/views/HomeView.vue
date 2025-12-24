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
          <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
              <h5 class="text-muted small mb-1">MY MOATHON</h5>
              <h2 class="fw-bold m-0">나의 목표 달성 현황</h2>
            </div>
            
            <div class="d-flex gap-2">
              <select 
                v-if="myActiveMoathons.length > 1" 
                v-model="selectedMoathonId" 
                class="form-select form-select-sm w-auto"
              >
                <option v-for="m in myActiveMoathons" :key="m.id" :value="m.id">
                  {{ m.title }}
                </option>
              </select>
              
              <router-link :to="{ name: 'moathonCreate' }" class="btn btn-sm btn-outline-primary fw-bold">
                + 추가
              </router-link>
            </div>
          </div>

          <div class="main-card-wrapper">
            <MoathonCard 
              v-if="selectedMoathon" 
              :moathon="selectedMoathon" 
              :is-highlight="true" 
            />
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
            <router-link :to="{ name: 'moathonCreate' }" class="btn btn-primary px-5 py-3 fw-bold shadow-sm rounded-pill">
              내 맞춤 모아톤 만들기
            </router-link>
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
import { useAccountStore } from '@/stores/accounts'
import { useMoathonStore } from '@/stores/moathon'
import MoathonCard from '@/components/moathon/MoathonCard.vue'

const accountStore = useAccountStore()
const moathonStore = useMoathonStore()

const loading = ref(true)
const selectedMoathonId = ref(null)

// 1. 내 모아톤 상태
const hasActiveMoathon = computed(() => {
  return accountStore.user?.moathons && accountStore.user.moathons.length > 0
})
const myActiveMoathons = computed(() => accountStore.user?.moathons || [])

// 선택된 모아톤
const selectedMoathon = computed(() => {
  if (!selectedMoathonId.value) return myActiveMoathons.value[0]
  return myActiveMoathons.value.find(m => m.id === selectedMoathonId.value) || myActiveMoathons.value[0]
})

// 2. 팔로잉 모아톤 상태
const followingMoathons = computed(() => moathonStore.followingMoathons || [])
const fetchMoathonData = async () => {
  if (accountStore.isAuthenticated) {
    // 혹시 user 정보가 없으면 채우기
    if (!accountStore.user) await accountStore.getProfile()
    // 팔로잉 목록 가져오기
    await moathonStore.getFollowingMoathons()
  }
}

onMounted(async () => {
  try {
    loading.value = true
    // 이미 로그인이 되어있는 경우 (새로고침 등) 바로 실행
    if (accountStore.isAuthenticated) {
      await fetchMoathonData()
    }
  } catch (err) {
    console.error(err)
  } finally {
    // 로그인이 안 되어 있어도 로딩은 꺼줘야 함 (Type A 화면을 위해)
    loading.value = false
  }
})

// 드롭다운 기본값 설정 watcher
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
    // 팔로잉 데이터 등 메인 데이터 호출
    await fetchMoathonData()
  }
}, { immediate: true })
</script>

<style scoped>
/* 전체 배경색을 약간 회색으로 주어 카드 섹션을 돋보이게 할 수도 있음 (선택사항) */
.home-wrapper {
  background-color: #fcfcfc;
  min-height: 100vh;
}

/* [SECTION 1] 대시보드 스타일 */
.dashboard-card {
  transition: transform 0.2s ease-in-out;
}
.dashboard-card:hover {
  border-color: #dee2e6 !important; /* hover 시 테두리 약간 진하게 */
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