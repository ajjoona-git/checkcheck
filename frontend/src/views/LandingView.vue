<template>
  <div class="landing-container">
    <section class="hero">
      <div class="reveal">
        <h1 class="hero-title">Moathon</h1>
        <p class="hero-subtitle">함께 완주하는 저축 마라톤.</p>
        <div class="mt-4">
          <a href="#features" class="cta-button secondary">서비스 둘러보기</a>
        </div>
      </div>
    </section>

    <section id="features" class="section-padding container">
      <div class="reveal">
        <span class="section-label">Easy & Joy Saving</span>
        <h2 class="section-heading">고르는 스트레스는 줄이고,<br>달리는 재미는 더하고.</h2>
        <p class="section-desc">
          수많은 예·적금 중 <b>‘지금의 나’에게 맞는 선택지</b>를 추천받을 수 있고, <br>
          <b>사람들과 소통하며 지루하지 않게</b> 완주할 수 있습니다.
        </p>
      </div>

      <div class="bento-grid mt-5">
        <div class="bento-item tall reveal">
          <h3>나만의 금융 파트너</h3>
          <p>데이터 기반 추천 알고리즘</p>
          <div class="icon-box">📊</div>
        </div>
        <div class="bento-item wide reveal" style="transition-delay: 0.1s;">
          <h3>함께 달리는 페이스메이커</h3>
          <p>친구들과 함께하는 챌린지</p>
        </div>
      </div>
    </section>

    <!-- CORE FEATURES -->
    <section id="core" class="section-padding container">
      <div class="reveal">
        <span class="section-label">Function</span>
        <h2 class="section-heading">모아톤의 기능을 소개합니다.</h2>
      </div>

      <div class="bento-grid mt-4">
        <div class="bento-item small reveal">
          <h3>맞춤 큐레이션</h3>
          <p>성향과 목적을 분석한 추천.</p>
        </div>
        <div class="bento-item small reveal" style="transition-delay: 0.1s;">
          <h3>모아톤 커뮤니티</h3>
          <p>모아톤 현황으로 소통</p>
        </div>
        <div class="bento-item small reveal" style="transition-delay: 0.2s;">
          <h3>소셜 뱃지</h3>
          <p>성취를 기록하고 공유.</p>
        </div>
        <div class="bento-item small reveal" style="transition-delay: 0.3s;">
          <h3>금융 맵</h3>
          <p>가까운 은행 지점 찾기.</p>
        </div>
        <div class="bento-item small reveal" style="transition-delay: 0.4s;">
          <h3>스마트 러닝</h3>
          <p>금융 상식을 영상으로 만나보세요.</p>
        </div>
        <div class="bento-item small reveal" style="transition-delay: 0.5s;">
          <h3>자산 시세</h3>
          <p>금·은 실시간 흐름 파악.</p>
        </div>
      </div>
    </section>

    <section class="section-padding text-center">
      <div class="reveal">
        <h2 class="section-heading">완주할 준비가 되셨나요?</h2>
        <p class="section-desc mx-auto">이미 수많은 사용자가 모아톤과 함께 즐거운 저축을 경험하고 있습니다.</p>
        <RouterLink :to="{ name: 'signup' }" class="cta-button">오늘부터 1일 시작</RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

let observer = null

onMounted(() => {
  // 1. Scroll Reveal Animation
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
      }
    });
  }, { threshold: 0.15 });

  const revealElements = document.querySelectorAll('.reveal');
  revealElements.forEach(el => observer.observe(el));

  // 2. Internal Anchor Smooth Scroll
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>

<style scoped>
/* Page Specific Styles */

/* Hero Section */
.hero {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  position: relative;
  overflow: hidden;
  background: radial-gradient(circle at 50% 50%, rgba(0, 217, 126, 0.08) 0%, #fff 70%);
}

.hero-title {
  font-size: clamp(3.2rem, 9vw, 6.5rem);
  font-weight: 800;
  letter-spacing: -0.05em;
  margin-bottom: 0.8rem;
  background: linear-gradient(180deg, #1d1d1f 60%, #86868b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: clamp(1.4rem, 4vw, 2.2rem);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2.5rem;
}

/* Buttons */
.cta-button {
  background: var(--moathon-green, #1b5e20);
  color: white;
  padding: 14px 32px;
  border-radius: 980px;
  font-weight: 700;
  font-size: 1.15rem;
  text-decoration: none;
  transition: all 0.5s ease;
  display: inline-block;
  box-shadow: 0 10px 25px rgba(0, 217, 126, 0.3);
}

.cta-button:hover {
  transform: scale(1.05);
  box-shadow: 0 15px 35px rgba(0, 217, 126, 0.4);
  color: white;
}

.cta-button.secondary {
  background: transparent;
  border: 1.5px solid var(--moathon-green, #1b5e20);
  color: var(--moathon-deep, #7d9b76);
  box-shadow: none;
}

/* Sections */
.section-padding {
  padding: 140px 0;
}

.section-label {
  color: var(--moathon-deep, #7d9b76);
  font-weight: 700;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 1.2rem;
  display: block;
}

.section-heading {
  font-size: clamp(2.2rem, 6vw, 3.8rem);
  font-weight: 800;
  margin-bottom: 1.8rem;
  letter-spacing: -0.03em;
}

.section-desc {
  font-size: 1.4rem;
  color: var(--text-secondary);
  max-width: 720px;
  margin-bottom: 4rem;
  font-weight: 500;
}

/* Bento Grid */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-gap: 24px;
}

.bento-item {
  background: var(--bg-secondary);
  border-radius: 36px;
  padding: 48px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 320px;
  transition: all 0.5s ease;
  border: 1px solid rgba(0, 0, 0, 0.02);
}

.bento-item:hover {
  transform: scale(1.02);
  background: #fff;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.08);
}

.bento-item.tall {
  grid-column: span 6;
  grid-row: span 2;
  min-height: 540px;
  background: linear-gradient(135deg, #f0fdf4 0%, #e1fdf0 100%);
}

.bento-item.wide {
  grid-column: span 6;
}

.bento-item.small {
  grid-column: span 4;
}

.bento-item h3 {
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 12px;
  color: #1d1d1f;
}

.bento-item p {
  color: var(--text-secondary);
  font-size: 1.15rem;
  margin: 0;
  line-height: 1.5;
}

.icon-box {
  position: absolute;
  top: 48px;
  right: 48px;
  width: 64px;
  height: 64px;
  background: #fff;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}

@media (max-width: 768px) {

  .bento-item.tall,
  .bento-item.wide,
  .bento-item.small {
    grid-column: span 12;
  }

  .section-padding {
    padding: 80px 0;
  }

  .hero-title {
    font-size: 3.5rem;
  }
}
</style>