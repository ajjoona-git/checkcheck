<template>
  <div class="user-profile card mb-4">
    <div class="card-body p-4">
      <div class="d-flex justify-content-between align-items-start mb-4">
        <div class="d-flex gap-4 align-items-center">
          <img :src="profileImage" class="profile-img-lg" alt="프로필" />
          
          <div class="info-text">
            <h2 class="mb-1 fw-bold">
              {{ user.nickname }} 
              <span class="badge bg-primary ms-2" style="font-size: 0.6em; vertical-align: middle;">
                {{ tenderText }}
              </span>
            </h2>
            <p class="text-muted mb-2">{{ user.email }}</p>
            
            <div class="social-stats small text-secondary">
              팔로워 <b class="text-dark">{{ user.follower_count || 0 }}</b> · 
              팔로잉 <b class="text-dark">{{ user.following_count || 0 }}</b>
            </div>
          </div>
        </div>

        <button class="btn btn-outline-secondary btn-sm" @click="$emit('toggle-edit')">
          {{ isEditing ? '취소' : '정보 수정' }}
        </button>
      </div>

      <hr class="my-4 opacity-25">

      <h5 class="mb-3 fw-bold text-dark">상세 정보</h5>
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
          <span class="value fw-bold text-primary">{{ user.credit_score }}점</span>
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
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    required: true,
    default: () => ({})
  },
  isEditing: Boolean
})

defineEmits(['toggle-edit'])

// 이미지 경로 처리 (기존 로직 유지 또는 helper 함수 사용)
const profileImage = computed(() => {
  if (!props.user.profile_image) return '/default-profile.png'
  if (props.user.profile_image.startsWith('http')) return props.user.profile_image
  // .env 설정을 가져오거나 직접 입력 (상황에 맞게 조정하세요)
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
  return `${API_URL}${props.user.profile_image}`
})

// [매핑] 성별 (0: 남성, 1: 여성) - ProfileForm 기준
const genderText = computed(() => {
  if (props.user.gender === undefined || props.user.gender === null) return '-'
  const map = { '0': '남성', '1': '여성' }
  // DB에서 숫자로 올 수도 있고 문자로 올 수도 있어 String 변환 후 매핑
  return map[String(props.user.gender)] || '기타'
})

// [매핑] 투자 성향 (1~5) - ProfileForm 기준
const tenderText = computed(() => {
  const map = {
    '1': '안정형 (매우 보수적)',
    '2': '안정추구형 (보수적)',
    '3': '위험중립형 (보통)',
    '4': '적극투자형 (공격적)',
    '5': '공격투자형 (매우 공격적)'
  }
  return map[String(props.user.tender)] || '투자 성향 미설정'
})

// [유틸] 금액 포맷팅 (세 자리 콤마)
const formatMoney = (value) => {
  if (value === undefined || value === null) return '0'
  return Number(value).toLocaleString()
}
</script>

<style scoped>
.profile-img-lg {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #dee2e6;
}

/* 그리드 레이아웃: 반응형으로 2열 or 3열 배치 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  background-color: #f8f9fa; /* 연한 회색 배경 */
  padding: 20px;
  border-radius: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 4px;
}

.value {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
}
</style>