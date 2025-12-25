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
          <p>복잡한 금리 비교 없이,<br>AI가 당신에게 딱 맞는 상품을 찾아줍니다.</p>
          <div class="recommend-box">
            <!-- <UserProfileSection :user="user" /> -->
            <MoathonRecommendCard :detail="mockRecommendDetail" :warnings="mockWarnings"
              class="landing-recommend-card" />
          </div>
        </div>

        <div class="bento-item wide reveal" style="transition-delay: 0.1s;">
          <h3>함께 달리는 페이스메이커</h3>
          <p>혼자하면 포기하기 쉽지만,<br>친구들과 함께라면 끝까지 갈 수 있습니다.</p>
          <div class="track-box">
            <MoathonTrack :percent="75" :duration="2" :profile-image="defaultProfile" />
            <p class="text-center mt-3 mb-0 text-muted fw-normal small">
              목표까지 힘내세요, <b>말랑이</b>님! 🏃‍♂️
            </p>
          </div>
          <!-- <div class="card-box mt-3">
            <MoathonCard :moathon="mockMoathon" :is-highlight="true" class="landing-moathon-card" />
          </div> -->
        </div>

        <div class="bento-item wide reveal" style="transition-delay: 0.1s;">
          <h3>성취를 기록하는 명예의 전당</h3>
          <p>
            목표 달성의 순간들을 특별한 뱃지로 남겨보세요.<br>
            하나씩 채워가는 즐거움이 꾸준한 저축의 원동력이 됩니다.
          </p>
          <div class="track-box">
            <BadgeLibrary :badges="mockBadgeCollection" />
          </div>
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

        <div class="bento-item feature-card curation reveal">
          <div class="card-bg-icon"><i class="bi bi-stars"></i></div>
          <div class="content">
            <div class="icon-box"><i class="bi bi-stars"></i></div>
            <h3>맞춤 큐레이션</h3>
            <p>내 자산과 연봉을 분석해<br>최적의 상품을 제안합니다.</p>
          </div>
        </div>

        <div class="bento-item feature-card community reveal" style="transition-delay: 0.1s;">
          <div class="card-bg-icon"><i class="bi bi-people-fill"></i></div>
          <div class="content">
            <div class="icon-box"><i class="bi bi-people-fill"></i></div>
            <h3>모아톤 커뮤니티</h3>
            <p>친구들과 목표를 공유하고<br>서로 응원하며 완주하세요.</p>
          </div>
        </div>

        <div class="bento-item feature-card badge-feat reveal" style="transition-delay: 0.2s;">
          <div class="card-bg-icon"><i class="bi bi-award-fill"></i></div>
          <div class="content">
            <div class="icon-box"><i class="bi bi-award-fill"></i></div>
            <h3>소셜 뱃지</h3>
            <p>저축 마일스톤을 달성하고<br>특별한 뱃지를 수집하세요.</p>
          </div>
        </div>

        <div class="bento-item feature-card map reveal" style="transition-delay: 0.3s;">
          <div class="card-bg-icon"><i class="bi bi-geo-alt-fill"></i></div>
          <div class="content">
            <div class="icon-box"><i class="bi bi-geo-alt-fill"></i></div>
            <h3>금융 맵</h3>
            <p>내 주변 가까운 은행 지점과<br>ATM 위치를 찾아드립니다.</p>
          </div>
        </div>

        <div class="bento-item feature-card learning reveal" style="transition-delay: 0.4s;">
          <div class="card-bg-icon"><i class="bi bi-play-circle-fill"></i></div>
          <div class="content">
            <div class="icon-box"><i class="bi bi-play-circle-fill"></i></div>
            <h3>스마트 러닝</h3>
            <p>어려운 금융 용어와 상식을<br>영상으로 쉽게 배워보세요.</p>
          </div>
        </div>

        <div class="bento-item feature-card asset reveal" style="transition-delay: 0.5s;">
          <div class="card-bg-icon"><i class="bi bi-graph-up-arrow"></i></div>
          <div class="content">
            <div class="icon-box"><i class="bi bi-graph-up-arrow"></i></div>
            <h3>자산 시세</h3>
            <p>금, 은 등 주요 원자재의<br>실시간 시세를 확인하세요.</p>
          </div>
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
import { onMounted, onUnmounted, ref } from 'vue'
import UserProfileSection from '@/components/user/UserProfileSection.vue';
import MoathonRecommendCard from '@/components/moathon/MoathonRecommendCard.vue';
import MoathonTrack from '@/components/moathon/MoathonTrack.vue';
import MoathonCard from '@/components/moathon/MoathonCard.vue';
import BadgeLibrary from '@/components/common/BadgeLibrary.vue';
import defaultProfile from '/default-profile.png'

const mockRecommendDetail = ref({
  bank_name: '모아톤은행',
  product_name: '트래블 적금',
  rsrv_type_nm: '정액적립식',
  save_trm: '12',
  intr_rate: 3.5,
  intr_rate2: 4.5,
  intr_rate_type_nm: '단리',
  spcl_cnd: "급여이체 실적이 있는 경우 연 0.5%p 우대\nKB국민카드 결제 실적이 있는 경우 연 0.3%p 우대",
  etc_note: "말랑이님의 '유럽여행' 목표 달성을 위해 가장 적합한 상품이에요. \n안정적인 1금융권 상품 중 가장 높은 우대금리를 제공합니다."
})

const mockWarnings = ref([
  '최고 금리는 우대 조건 달성 시 적용됩니다.',
  '이 예금은 예금자보호법에 따라 보호됩니다.',
  '만기 전 해지 시 약정 이율보다 낮은 금리가 적용될 수 있습니다.'
])

const mockMoathon = ref({
  title: '유럽 여행 자금 만들기',
  bank: '모아톤은행',
  nickname: '말랑이',
  product_name: '트래블 적금',
  progress_rate: 75,
})

const mockBadgeCollection = ref([
  {
    name: '저축의 시작',
    quantity: 3,
    url: '/src/assets/badges/badge_achieve_3days.png'
  },
  {
    name: '완주 트로피',
    quantity: 2,
    url: '/src/assets/badges/badge_track_100.png'
  },
  {
    name: "시작이 반",
    quantity: 1,
    url: "/src/assets/badges/badge_achieve_start.png"
  },
  {
    name: "억만장자의 꿈",
    quantity: 1,
    url: "/src/assets/badges/badge_achieve_billionaire.png"
  },
  {
    name: "응원 단장",
    quantity: 0,
    url: "frontend/src/assets/badges/badge_social_cheerleader.png"
  },
  {
    name: "티끌 모아 태산",
    quantity: 1,
    url: "frontend/src/assets/badges/badge_achieve_deposit.png"
  }
])

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
  justify-content: space-between;
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
  background: linear-gradient(135deg, #1b5e1f2c 0%, #1b5e1f33 100%);
}

.bento-item.wide {
  grid-column: span 6;
    background: var(--bg-secondary);
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

.track-box {
  padding: 40px 16px 30px;
}

.recommend-box {
  padding: 40px 0;
}

/* --- Feature Card Styles (Core Section) --- */
.feature-card {
  grid-column: span 4;
  min-height: 260px;
  position: relative;
  overflow: hidden;

  background: var(--bg-secondary);
  border: 1px solid rgba(0, 0, 0, 0.02);
  border-radius: 24px;

  transition: var(--transition-base, all 0.4s ease);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 32px;
}

/* Hover 시 효과 */
.feature-card:hover {
  transform: translateY(-8px);
  background: var(--card-bg);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08);
  border-color: rgba(27, 94, 32, 0.1);
}

/* 배경에 깔리는 거대 아이콘 */
.card-bg-icon {
  position: absolute;
  top: -20px;
  right: -20px;
  font-size: 10rem;
  color: var(--moathon-deep);
  opacity: 0.1;
  transform: rotate(-10deg);
  transition: all 0.5s ease;
  pointer-events: none;
  z-index: 0;
}

/* Hover 시 배경 아이콘 애니메이션 */
.feature-card:hover .card-bg-icon {
  transform: rotate(0deg) scale(1.1);
  opacity: 0.15;
  color: var(--moathon-green);
}

/* 카드 내용물 */
.content {
  position: relative;
  z-index: 1;
}

/* 아이콘 박스 (작은 아이콘) */
.icon-box {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: white;
  background: var(--moathon-deep);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.feature-card h3 {
  font-size: 1.4rem;
  font-weight: 800;
  margin-bottom: 10px;
}

.feature-card p {
  font-size: 1.05rem;
  line-height: 1.5;
  margin: 0;
  font-weight: 500;
}

/* 반응형 처리 */
@media (max-width: 992px) {
  .feature-card {
    grid-column: span 6;
  }
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

@media (max-width: 576px) {
  .feature-card {
    grid-column: span 12;
  }
}
</style>