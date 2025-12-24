<template>
  <nav class="nav-bar navbar navbar-expand-lg">
    <div class="nav-content">
      <RouterLink class="nav-logo" :to="{ name: 'home' }">
          <img :src="logo" alt="Moathon" class="logo" />
      </RouterLink>

      <button 
        class="navbar-toggler border-0 p-0" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNavAltMarkup" 
        aria-controls="navbarNavAltMarkup" 
        aria-expanded="false" 
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse ms-4" id="navbarNavAltMarkup">
        <div class="navbar-nav me-auto align-items-center gap-lg-4 gap-2 my-3 my-lg-0">
          <RouterLink v-if="accountStore.isAuthenticated" class="nav-link" :to="{ name: 'moathonRecommend' }">모아톤 추천받기</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'community' }">모아톤 커뮤니티</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'products' }">예·적금 조회</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'bank' }">은행 위치</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'commodity' }">시세 확인</RouterLink>
          <RouterLink class="nav-link" :to="{ name: 'videoSearch' }">유튜브 검색</RouterLink>
        </div>

        <div class="navbar-nav ms-lg-4 align-items-center gap-4">
          <template v-if="!accountStore.isAuthenticated">
            <RouterLink class="auth-link login" :to="{ name: 'login' }">로그인</RouterLink>
            <RouterLink class="auth-link signup" :to="{ name: 'signup' }">회원가입</RouterLink>
          </template>

          <template v-else>
            <RouterLink class="auth-link profile" :to="{ name: 'mypage' }">프로필</RouterLink>
            <a href="#" @click.prevent="logOut" class="auth-link logout">로그아웃</a>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
  import { RouterLink } from 'vue-router';
  import { useAccountStore } from '@/stores/accounts';
  import { useMoathonStore } from '@/stores/moathon'
  import logo from '@/assets/logo.svg'

  const accountStore = useAccountStore()
  const moathonStore = useMoathonStore()
  
  const logOut = async function () {
    // 1. 계정 스토어 로그아웃 (API 호출 + 토큰 삭제)
    // 에러가 나도 내부 catch/finally에서 처리되므로 멈추지 않음
    await accountStore.logOut()
    
    // 2. 모아톤 스토어 초기화 (혹시 몰라 한 번 더)
    if (typeof moathonStore.resetState === 'function') {
      moathonStore.resetState()
    }
    
    // 3. 메인으로 이동하며 새로고침 (가장 확실한 메모리 정리)
    window.location.href = '/'
  }
</script>

<style scoped>
.nav-bar {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 64px;
  background: var(--glass-bg, rgba(255, 255, 255, 0.8));
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  z-index: 1000;
  border-bottom: 1px solid rgba(0,0,0,0.05);
  padding: 0;
}

.nav-content {
  width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 22px;
  display: flex; align-items: center; justify-content: space-between; height: 100%;
}

.nav-logo { 
  font-weight: 800; font-size: 1.2rem; color: #1d1d1f; text-decoration: none;
  display: flex; align-items: center; gap: 8px; margin-right: auto;
}
.nav-logo span { width: 20px; height: 20px; background: #1b5e20; border-radius: 4px; }

.logo {
  width: 60px; height: auto;
  cursor: pointer;
}

.custom-nav-link {
  color: #86868b; font-size: 0.95rem; font-weight: 500; text-decoration: none;
  transition: all 0.2s ease; white-space: nowrap;
}
.custom-nav-link:hover, .custom-nav-link.router-link-active { color: #1d1d1f; font-weight: 700; }

.auth-link { font-size: 0.9rem; font-weight: 600; text-decoration: none; transition: all 0.2s ease; }
.auth-link.login, .auth-link.logout, .auth-link.profile { color: #1d1d1f; }
.auth-link.signup { background-color: #1d1d1f; color: #ffffff; padding: 8px 16px; border-radius: 20px; }
.auth-link.signup:hover { background-color: #333; }

@media (max-width: 991px) {
  .nav-bar { height: auto; min-height: 60px; }
  .nav-content { flex-wrap: wrap; }
  .navbar-collapse {
    background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px);
    width: 100%; border-radius: 0 0 16px 16px; padding: 20px; margin-top: 10px;
    border-top: 1px solid rgba(0,0,0,0.05); box-shadow: 0 10px 20px rgba(0,0,0,0.05);
  }
}
</style>