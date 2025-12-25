<template>
  <div class="user-profile card">
    <div class="card-body p-4 p-lg-5">
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-center align-items-md-start gap-4">
        
        <div class="d-flex gap-4 align-items-center">
          <div class="profile-img-wrapper">
            <img :src="profileImage" class="profile-img" alt="프로필" />
          </div>
          
          <div class="info-text">
            <div class="d-flex align-items-center gap-2 mb-1">
              <h2 class="m-0 fw-bold user-name">{{ user.nickname }}</h2>
              <span class="status-badge" :class="tenderClass">
                {{ tenderText }}
              </span>
            </div>
            
            <p class="user-email">{{ user.email }}</p>
            
            <div class="social-stats">
              <span>팔로워 <b class="text-dark">{{ user.follower_count || 0 }}</b></span>
              <span class="divider">·</span>
              <span>팔로잉 <b class="text-dark">{{ user.following_count || 0 }}</b></span>
            </div>
          </div>
        </div>

        <button class="btn btn-outline-custom" @click="$emit('toggle-edit')">
          <i class="bi" :class="isEditing ? 'bi-x-lg' : 'bi-pencil-fill'"></i>
          {{ isEditing ? '취소' : '정보 수정' }}
        </button>
      </div>
      
      </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  user: { type: Object, required: true, default: () => ({}) },
  isEditing: Boolean
})

defineEmits(['toggle-edit'])

const profileImage = computed(() => {
  if (!props.user.profile_image) return '/default-profile.png'
  if (props.user.profile_image.startsWith('http')) return props.user.profile_image
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
  return `${API_URL}${props.user.profile_image}`
})

const tenderText = computed(() => {
  const map = {
    '1': '안정형', '2': '안정추구형', '3': '위험중립형',
    '4': '적극투자형', '5': '공격투자형'
  }
  return map[String(props.user.tender)] || '미설정'
})

const tenderClass = computed(() => {
  const t = String(props.user.tender)
  if (t === '1' || t === '2') return 'safe'
  if (t === '4' || t === '5') return 'danger'
  return 'neutral'
})
</script>

<style scoped>
.user-profile.card {
  border: none;
  border-radius: 32px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.04);
  background: white;
}

.profile-img-wrapper {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  padding: 4px;
  border: 2px solid rgba(27, 94, 32, 0.1);
}

.profile-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  color: var(--text-primary);
  font-size: 1.8rem;
}

.status-badge {
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 700;
  vertical-align: middle;
}
.status-badge.safe { background-color: #e8f5e9; color: var(--moathon-green); }
.status-badge.danger { background-color: #ffebee; color: #d32f2f; }
.status-badge.neutral { background-color: #f5f5f5; color: var(--text-secondary); }

.user-email { color: var(--text-secondary); margin-bottom: 8px; }

.social-stats {
  font-size: 0.95rem;
  color: var(--text-secondary);
}
.divider { margin: 0 8px; color: #dee2e6; }

.btn-outline-custom {
  border: 1px solid #e0e0e0;
  color: var(--text-primary);
  border-radius: 12px;
  padding: 8px 16px;
  font-weight: 600;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}
.btn-outline-custom:hover {
  background-color: var(--bg-secondary);
  border-color: #d0d0d0;
}
</style>