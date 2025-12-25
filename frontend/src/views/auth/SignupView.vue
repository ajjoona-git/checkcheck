<template>
  <div class="auth-wrapper">
    <div class="auth-card fade-in">
      <div class="text-center mb-5">
        <h1 class="auth-title">Sign Up</h1>
        <p class="auth-subtitle">모아톤의 새로운 러너가 되어주세요!</p>
      </div>

      <form @submit.prevent="signUp">
        <div class="form-group">
          <label for="username">이름</label>
          <input type="text" id="username" v-model.trim="username" class="form-input" placeholder="실명을 입력하세요" />
        </div>

        <div class="form-group">
          <label for="email">이메일</label>
          <input type="email" id="email" v-model.trim="email" class="form-input" placeholder="example@moathon.com" />
        </div>
        
        <div class="row">
          <div class="col-6 form-group">
            <label for="password1">비밀번호</label>
            <input type="password" id="password1" v-model.trim="password1" class="form-input" placeholder="비밀번호" />
          </div>
          <div class="col-6 form-group">
            <label for="password2">확인</label>
            <input type="password" id="password2" v-model.trim="password2" class="form-input" placeholder="비밀번호 확인" />
          </div>
        </div>
        
        <div class="form-group">
          <label for="nickname">닉네임</label>
          <input type="text" id="nickname" v-model.trim="nickname" class="form-input" placeholder="커뮤니티에서 사용할 별명" />
        </div>
        
        <div class="form-group">
          <label for="birth">생년월일</label>
          <input type="date" id="birth" v-model.trim="birth" class="form-input" />
        </div>
        
        <button type="submit" class="submit-btn mt-4">가입하기</button>
      </form>

      <div class="auth-footer">
        <p>이미 계정이 있으신가요? 
          <router-link :to="{ name: 'login' }" class="link-text">로그인</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { useAccountStore } from '@/stores/accounts';
  import { ref } from 'vue';

  const username = ref(null)
  const email = ref(null)
  const password1 = ref(null)
  const password2 = ref(null)
  const nickname = ref(null)
  const birth = ref(null)

  const accountStore = useAccountStore()

  const signUp = function () {
    const payload = { 
      username: username.value, 
      email: email.value, 
      password1: password1.value, 
      password2: password2.value, 
      nickname: nickname.value, 
      birth: birth.value, 
    }
    accountStore.signUp(payload)
  }
</script>

<style scoped>
/* LoginView와 동일한 스타일을 적용하여 통일감 유지 */
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
  max-width: 520px; /* 필드가 많아서 조금 더 넓게 */
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

.auth-subtitle { color: var(--text-secondary); }

.form-group { margin-bottom: 20px; }

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
  background-color: #144a18;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(27, 94, 32, 0.2);
}

.auth-footer {
  text-align: center;
  margin-top: 32px;
  color: var(--text-secondary);
}

.link-text {
  color: var(--moathon-green);
  font-weight: 700;
  text-decoration: none;
  margin-left: 4px;
}

/* Row/Col 유틸리티 (Bootstrap이 있다면 생략 가능하지만 명시적 스타일링) */
.row { display: flex; gap: 16px; }
.col-6 { flex: 1; }

.fade-in { animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>