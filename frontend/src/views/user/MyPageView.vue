<template>
  <div class="page-wrapper">
    <div v-if="loading" class="loading-state">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">로딩 중...</span>
      </div>
    </div>

    <div v-else-if="user" class="container py-5 fade-in">

      <UserProfileSection :user="user" :isEditing="isEditing" @toggle-edit="toggleEdit" class="mb-4" />

      <div v-if="isEditing" class="edit-section mb-5 fade-in">
        <div class="card edit-card">
          <h4 class="edit-title">내 정보 수정</h4>
          <ProfileForm :is-edit="true" @success="onUpdateSuccess" />
        </div>
      </div>

      <div v-else class="dashboard-section fade-in">
        <div class="row g-4 mb-4">
          <div class="col-lg-6">
            <div class="card dashboard-card h-100">
              <h5 class="card-title">상세 정보</h5>
              <div class="info-grid">
                <div class="info-item">
                  <span class="label">생년월일</span>
                  <span class="value">{{ user.birth || '미입력' }}</span>
                </div>
                <div class="info-item">
                  <span class="label">성별</span>
                  <span class="value">{{ genderText }}</span>
                </div>
                <div class="info-item">
                  <span class="label">신용점수</span>
                  <span class="value fw-bold" style="color: var(--accent-blue, #0071e3)">{{ user.credit_score }}점</span>
                </div>
                <div class="info-item">
                  <span class="label">총 자산</span>
                  <span class="value">{{ formatMoney(user.assets) }}원</span>
                </div>
                <div class="info-item">
                  <span class="label">연봉</span>
                  <span class="value">{{ formatMoney(user.salary) }}원</span>
                </div>
                <div class="info-item">
                  <span class="label">월 평균 지출</span>
                  <span class="value">{{ formatMoney(user.average_monthly_spend) }}원</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="card dashboard-card h-100">
              <h4 class="card-title">획득한 뱃지</h4>
              <BadgeLibrary :badges="user.badge_collection" class="h-100 shadow-none border-0" />
            </div>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-lg-6">
            <div class="card dashboard-card h-100">
              <h4 class="card-title">나의 상품 금리 비교</h4>
              <RateChart :moathons="user.moathons" />
            </div>
          </div>

          <div class="col-lg-6">
            <div class="card dashboard-card h-100 d-flex flex-column">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h3 class="card-title m-0">나의 모아톤</h3>
                <span v-if="user.moathons.length > 0" class="badge bg-light text-dark rounded-pill border">
                  {{ user.moathons.length }}개
                </span>
              </div>

              <div v-if="user.moathons.length > 0" class="flex-grow-1 d-flex flex-column justify-content-between">
                <div class="moathon-list">
                  <MoathonCard v-for="moathon in paginatedMoathons" :key="moathon.id" :moathon="moathon" />
                </div>

                <div class="pagination-controls mt-4" v-if="totalMoathonPages > 1">
                  <button class="nav-btn" @click="prevMoathonPage" :disabled="currentMoathonPage === 0">
                    <i class="bi bi-chevron-left"></i>
                  </button>

                  <span class="page-indicator">{{ currentMoathonPage + 1 }} / {{ totalMoathonPages }}</span>

                  <button class="nav-btn" @click="nextMoathonPage"
                    :disabled="currentMoathonPage >= totalMoathonPages - 1">
                    <i class="bi bi-chevron-right"></i>
                  </button>
                </div>
              </div>

              <div v-else class="empty-state">
                <div class="empty-icon">🏃‍♂️</div>
                <p>현재 진행 중인 모아톤이 없습니다.</p>
                <router-link :to="{ name: 'moathonCreate' }" class="btn btn-primary-custom btn-sm">
                  모아톤 시작하기
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

import UserProfileSection from '@/components/user/UserProfileSection.vue'
import ProfileForm from '@/components/user/ProfileForm.vue'
import BadgeLibrary from '@/components/common/BadgeLibrary.vue'
import RateChart from '@/components/product/RateChart.vue'
import MoathonCard from '@/components/moathon/MoathonCard.vue'

const store = useAccountStore()
const route = useRoute()
const router = useRouter()

const user = computed(() => store.user)
const loading = ref(true)
const isEditing = ref(false)

const currentMoathonPage = ref(0)
const MOATHON_ITEMS_PER_PAGE = 3

// 전체 모아톤 페이지 수
const totalMoathonPages = computed(() => {
  const count = user.value?.moathons?.length || 0
  if (count === 0) return 1
  return Math.ceil(count / MOATHON_ITEMS_PER_PAGE)
})

// 현재 페이지에 해당하는 모아톤 목록
const paginatedMoathons = computed(() => {
  const list = user.value?.moathons || []
  const start = currentMoathonPage.value * MOATHON_ITEMS_PER_PAGE
  return list.slice(start, start + MOATHON_ITEMS_PER_PAGE)
})

// 이전 페이지로 이동
const prevMoathonPage = () => {
  if (currentMoathonPage.value > 0) currentMoathonPage.value--
}

// 다음 페이지로 이동
const nextMoathonPage = () => {
  if (currentMoathonPage.value < totalMoathonPages.value - 1) currentMoathonPage.value++
}

// 성별 텍스트 변환
const genderText = computed(() => {
  if (user.value?.gender === undefined || user.value?.gender === null) return '-'
  const map = { '0': '남성', '1': '여성' }
  return map[String(user.value.gender)] || '기타'
})

// 화폐 단위 포맷터
const formatMoney = (value) => {
  if (value === undefined || value === null) return '0'
  return Number(value).toLocaleString()
}

// 편집 모드 쿼리 파라미터 감지
watch(() => route.query.edit, (newVal) => {
  isEditing.value = newVal === 'true'
}, { immediate: true })

// 사용자 프로필 로드
onMounted(async () => {
  try {
    loading.value = true
    await store.getProfile()
  } catch (err) {
    // 프로필 로드 실패
    throw err
  } finally {
    loading.value = false
  }
})

// 편집 모드 토글
const toggleEdit = () => {
  const nextState = !isEditing.value
  isEditing.value = nextState
  router.replace({ query: { ...route.query, edit: nextState ? 'true' : undefined } })
}

// 프로필 수정 성공 시 처리
const onUpdateSuccess = async () => {
  isEditing.value = false
  router.replace({ query: { ...route.query, edit: undefined } })
  await store.getProfile()
}
</script>

<style scoped>
.page-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
}

/* 카드 공통 스타일 */
.edit-card,
.dashboard-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  border: 1px solid rgba(0, 0, 0, 0.02);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.03);
}

.card-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 24px;
}

/* 상세 정보 그리드 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
  background-color: var(--bg-secondary);
  padding: 24px;
  border-radius: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 4px;
  font-weight: 500;
}

.value {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* 모아톤 리스트 영역 */
.moathon-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 380px;
}

/* 페이지네이션 컨트롤 */
.pagination-controls {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--bg-secondary);
  padding: 6px 16px;
  border-radius: 30px;
  align-self: center;
  width: fit-content;
}

.nav-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.nav-btn:disabled {
  color: #d0d0d0;
  cursor: not-allowed;
}

.nav-btn:hover:not(:disabled) {
  color: var(--moathon-green);
}

.page-indicator {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-primary);
  min-width: 40px;
  text-align: center;
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 40px 0;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.btn-primary-custom {
  background-color: var(--moathon-green);
  color: white;
  border-radius: 20px;
  padding: 8px 20px;
  font-weight: 600;
  border: none;
  transition: all 0.2s;
}

.btn-primary-custom:hover {
  background-color: #144a18;
  transform: translateY(-2px);
}

.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>