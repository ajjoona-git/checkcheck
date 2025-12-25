<template>
  <nav class="nav-bar navbar navbar-expand-lg">
    <div class="nav-content">
      
      <RouterLink class="nav-logo" :to="{ name: 'home' }">
        <img :src="logo" alt="Moathon" class="logo-img" />
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
        <span class="toggler-icon">
          <i class="bi bi-list"></i>
        </span>
      </button>

      <div class="collapse navbar-collapse ms-lg-4" id="navbarNavAltMarkup">
        
        <div class="navbar-nav me-auto align-items-lg-center gap-lg-1 my-3 my-lg-0">
          <RouterLink v-if="accountStore.isAuthenticated" class="custom-nav-link" :to="{ name: 'moathonRecommend' }">
            모아톤 추천받기
          </RouterLink>
          <RouterLink class="custom-nav-link" :to="{ name: 'community' }">모아톤 커뮤니티</RouterLink>
          <RouterLink class="custom-nav-link" :to="{ name: 'products' }">예·적금 조회</RouterLink>
          <RouterLink class="custom-nav-link" :to="{ name: 'bank' }">은행 위치</RouterLink>
          <RouterLink class="custom-nav-link" :to="{ name: 'commodity' }">금·은 시세</RouterLink>
          <RouterLink class="custom-nav-link" :to="{ name: 'videoSearch' }">금융튜브</RouterLink>
        </div>

        <div class="navbar-nav ms-lg-4 align-items-lg-center gap-3 auth-group">
          <template v-if="!accountStore.isAuthenticated">
            <RouterLink class="auth-link login" :to="{ name: 'login' }">로그인</RouterLink>
            <RouterLink class="auth-link signup" :to="{ name: 'signup' }">회원가입</RouterLink>
          </template>

          <template v-else>
            <RouterLink class="auth-link profile" :to="{ name: 'mypage' }">
              <i class="bi bi-person-circle me-1"></i> 마이페이지
            </RouterLink>
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
    await accountStore.logOut()
    if (typeof moathonStore.resetState === 'function') {
      moathonStore.resetState()
    }
    window.location.href = '/'
  }
</script>

<style scoped>
/* Navbar Container */
.nav-bar {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 70px;
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 1000;
  border-bottom: 1px solid rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.nav-content {
  width: 100%; max-width: 1280px; margin: 0 auto; padding: 0 24px;
  display: flex; align-items: center; justify-content: space-between; height: 100%;
}

/* Logo */
.nav-logo {
  display: flex; align-items: center; text-decoration: none;
  margin-right: 10px;
}

.logo-img {
  height: 36px; width: auto;
}

/* Mobile Toggler */
.navbar-toggler { border: none; outline: none; box-shadow: none; }
.toggler-icon { font-size: 1.8rem; color: #333; }

/* Navigation Links */
.custom-nav-link {
  color: var(--text-secondary, #666);
  font-size: 0.95rem;
  font-weight: 600;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 12px;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.custom-nav-link:hover {
  color: var(--moathon-green, #1b5e20);
  background-color: rgba(27, 94, 32, 0.04);
}

.custom-nav-link.router-link-active {
  color: var(--moathon-green, #1b5e20);
  font-weight: 800;
  background-color: rgba(27, 94, 32, 0.08);
}

/* Auth Buttons */
.auth-group {
  display: flex;
  flex-direction: row;
}

.auth-link {
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 700;
  transition: all 0.2s;
  padding: 8px 12px;
  border-radius: 12px;
}

.auth-link.login, .auth-link.logout {
  color: var(--text-secondary, #555);
}
.auth-link.login:hover, .auth-link.logout:hover {
  color: var(--text-primary, #111);
  background-color: rgba(0,0,0,0.03);
}

.auth-link.profile {
  color: var(--text-primary, #333);
  display: flex; align-items: center;
}
.auth-link.profile:hover {
  color: var(--moathon-green, #1b5e20);
}

/* 회원가입 버튼 (강조) */
.auth-link.signup {
  background-color: var(--moathon-green, #1b5e20);
  color: white;
  padding: 8px 20px;
  border-radius: 50px;
  box-shadow: 0 4px 10px rgba(27, 94, 32, 0.2);
}

.auth-link.signup:hover {
  background-color: #144a18;
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(27, 94, 32, 0.3);
}

/* Mobile Responsive */
@media (max-width: 991px) {
  .nav-bar { height: auto; min-height: 64px; }
  .nav-content { flex-wrap: wrap; padding: 12px 20px; }
  
  .navbar-collapse {
    width: 100%;
    margin-top: 16px;
    background: white;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.05);
  }

  .custom-nav-link {
    padding: 12px;
    width: 100%;
    text-align: center;
  }

  .auth-group {
    margin-top: 16px;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    text-align: center;
  }

  .auth-link { width: 100%; display: block; }
  .auth-link.signup { width: 100%; }
}
</style>