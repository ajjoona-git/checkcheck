<template>
  <div class="auth-wrapper">
    <div class="auth-card fade-in">
      <div class="text-center mb-5">
        <h1 class="auth-title">Welcome Back!</h1>
        <p class="auth-subtitle">모아톤과 함께 저축 마라톤을 이어가세요.</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">이름</label>
          <input 
            type="text" 
            id="username" 
            v-model.trim="username" 
            placeholder="이름을 입력하세요"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="email">이메일</label>
          <input 
            type="email" 
            id="email" 
            v-model.trim="email" 
            placeholder="example@moathon.com"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input 
            type="password" 
            id="password" 
            v-model.trim="password" 
            placeholder="비밀번호를 입력하세요"
            class="form-input"
          />
        </div>

        <button type="submit" class="submit-btn mt-4">로그인</button>
      </form>

      <div class="auth-footer">
        <p>아직 계정이 없으신가요? 
          <router-link :to="{ name: 'signup' }" class="link-text">회원가입</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue';
  import { useAccountStore } from '@/stores/accounts';
  import { useRouter } from 'vue-router';

  const username = ref(null)
  const email = ref(null)
  const password = ref(null)

  const accountStore = useAccountStore()
  const router = useRouter()

  const handleLogin = async () => {
    try {
      const payload = {
        username: username.value,
        email: email.value,
        password: password.value,
      }
      await accountStore.logIn(payload) 
      router.push({ name: 'home' })
    } catch (err) {
      alert('로그인에 실패했습니다. 정보를 확인해주세요.')
    }
  }
</script>

<style scoped>
/* 공통 Auth 레이아웃 스타일 */
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
  max-width: 480px;
  padding: 48px;
  border-radius: 32px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.02);
}

.auth-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--moathon-green);
  margin-bottom: 8px;
}

.auth-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
}

/* 폼 스타일 */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background-color: #f9f9f9;
}

.form-input:focus {
  outline: none;
  border-color: var(--moathon-green);
  background-color: white;
  box-shadow: 0 0 0 4px rgba(27, 94, 32, 0.1);
}

.submit-btn {
  width: 100%;
  background-color: var(--moathon-green);
  color: white;
  border: none;
  padding: 16px;
  border-radius: 16px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover {
  background-color: #144a18; /* 더 진한 녹색 */
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(27, 94, 32, 0.2);
}

.auth-footer {
  text-align: center;
  margin-top: 32px;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.link-text {
  color: var(--moathon-green);
  font-weight: 700;
  text-decoration: none;
  margin-left: 4px;
}

.link-text:hover {
  text-decoration: underline;
}

.fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>