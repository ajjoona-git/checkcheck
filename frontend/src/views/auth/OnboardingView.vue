<template>
  <div class="auth-wrapper">
    <div class="auth-card wide fade-in">
      <div class="text-center mb-5">
        <h1 class="auth-title">프로필 정보 입력</h1>
        <p class="auth-subtitle">
          입력한 정보는 고객님을 위한 <br>
          <span class="highlight">맞춤 예/적금 상품 추천</span>에 사용됩니다.
        </p>
      </div>

      <div class="form-container">
        <ProfileForm @success="goHome" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ProfileForm from '@/components/user/ProfileForm.vue';
import { useRouter } from 'vue-router';

const router = useRouter()

// 프로필 작성 완료 후 홈으로 이동
const goHome = function () {
  alert('환영합니다! 가입이 완료되었습니다.')
  router.push({ name: 'home' })
}
</script>

<style scoped>
.auth-wrapper {
  background-color: var(--bg-secondary);
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.auth-card {
  background: white;
  width: 100%;
  max-width: 600px;
  padding: 48px;
  border-radius: 32px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.02);
}

.auth-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.auth-subtitle {
  color: var(--text-secondary);
  font-size: 1.05rem;
  line-height: 1.6;
}

.highlight {
  color: var(--moathon-green);
  font-weight: 700;
  background: rgba(27, 94, 32, 0.08);
  padding: 2px 6px;
  border-radius: 4px;
}

.form-container {
  margin-top: 32px;
}

.fade-in {
  animation: fadeIn 0.6s ease-out;
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

/* 반응형 */
@media (max-width: 576px) {
  .auth-card {
    padding: 24px;
  }

  .auth-title {
    font-size: 1.6rem;
  }
}
</style>