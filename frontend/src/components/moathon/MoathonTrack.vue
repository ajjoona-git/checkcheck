<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import gsap from 'gsap';
import { MotionPathPlugin } from 'gsap/MotionPathPlugin';

gsap.registerPlugin(MotionPathPlugin);

const props = defineProps({
  percent: {
    type: Number,
    required: true,
    default: 0,
    validator: (value) => value >= 0 && value <= 100
  },
  duration: {
    type: Number,
    default: 2
  },
  profileImage: {
    type: String,
    default: null
  }
});

const trackPath = ref(null); 
const runnerIcon = ref(null);
const displayPercent = ref(0);
const pathLength = ref(0); 

// 굵기와 색상 설정
const strokeWidth = 80; 
const trackColor = "#D9534F"; 
const trackBgColor = "#F0E4E4"; 

// 트랙 경로 데이터 (600x300 캔버스, 80px 굵기 대응)
const trackPathData = "M 150, 40 L 450, 40 A 110, 110 0 0, 1 450, 260 L 150, 260 A 110, 110 0 0, 1 150, 40 Z";

const animateTrack = () => {
  if (!pathLength.value) return; 

  const targetOffset = pathLength.value - (props.percent / 100) * pathLength.value;

  // 1. 트랙 라인 그리기
  gsap.set(trackPath.value, { strokeDasharray: pathLength.value });
  
  gsap.fromTo(trackPath.value, 
    { strokeDashoffset: pathLength.value }, 
    { 
      strokeDashoffset: targetOffset,       
      duration: props.duration,
      ease: "power2.out"
    }
  );

  // 2. 러너 이동 (여기가 수정되었습니다!)
  gsap.to(runnerIcon.value, {
    motionPath: {
      path: trackPath.value,
      align: trackPath.value,
      alignOrigin: [0.5, 0.5], 
      end: props.percent / 100,
      start: 0 
    },
    opacity: 1, // [수정됨] 이동하면서 투명도를 1로 변경하여 보이게 함
    duration: props.duration,
    ease: "power2.out"
  });

  // 3. 숫자 카운팅
  gsap.to(displayPercent, {
    value: props.percent,
    duration: props.duration,
    ease: "power2.out",
    onUpdate: () => displayPercent.value = Math.round(displayPercent.value)
  });
};

onMounted(() => {
  nextTick(() => {
    if (trackPath.value) {
      pathLength.value = trackPath.value.getTotalLength();
      setTimeout(() => {
        animateTrack();
      }, 100);
    }
  });
});

watch(() => props.percent, () => {
  if (pathLength.value > 0) animateTrack();
});
</script>

<template>
  <div class="moathon-track-container">
    <svg width="100%" height="100%" viewBox="0 0 600 300" class="track-svg" preserveAspectRatio="xMidYMid meet">
      
      <path
        :d="trackPathData"
        fill="none"
        :stroke="trackBgColor"
        :stroke-width="strokeWidth"
        stroke-linecap="butt" 
      />

      <path
        ref="trackPath"
        :d="trackPathData"
        fill="none"
        :stroke="trackColor" 
        :stroke-width="strokeWidth"
        stroke-linecap="butt" 
        class="progress-path"
      />
      
      <path
        :d="trackPathData"
        fill="none"
        stroke="rgba(255,255,255,0.3)"
        :stroke-width="2"
        stroke-dasharray="10, 10"
      />

      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" class="progress-text">
        <tspan class="percent-number">{{ displayPercent.toFixed(0) }}</tspan>
        <tspan class="percent-symbol">%</tspan>
      </text>
    </svg>

    <div ref="runnerIcon" class="runner-avatar">
      <img v-if="profileImage" :src="profileImage" alt="runner" class="profile-img" />
      <div v-else class="default-coin">$</div>
    </div>
  </div>
</template>

<style scoped>
.moathon-track-container {
  position: relative;
  width: 100%;
  max-width: 600px; 
  aspect-ratio: 2 / 1;
  margin: 0 auto;
}

.track-svg {
  width: 100%;
  height: 100%;
  overflow: visible; 
}

.progress-path {
  stroke-dasharray: 2000; 
  stroke-dashoffset: 2000;
}

.progress-text {
  fill: #333;
  font-family: 'Pretendard', sans-serif;
  font-weight: 800;
}
.percent-number { font-size: 64px; }
.percent-symbol { font-size: 32px; fill: #666; }

/* 러너(프로필) 스타일 */
.runner-avatar {
  position: absolute;
  top: 0; left: 0;
  width: 70px;
  height: 70px;
  z-index: 10;
  pointer-events: none;
  background: white;
  border-radius: 50%;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border: 4px solid white;
  
  /* 초기 위치 보정 */
  transform: translate(115px, 5px); 
  opacity: 0; /* 초기에는 숨김 (GSAP가 opacity: 1로 만듦) */
}

.profile-img { width: 100%; height: 100%; object-fit: cover; }

.default-coin {
  width: 100%; height: 100%;
  background: #FFD700;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: bold; color: #B8860B; font-size: 32px;
}

@media (max-width: 576px) {
  .percent-number { font-size: 48px; }
  .percent-symbol { font-size: 24px; }
  .runner-avatar { width: 50px; height: 50px; border-width: 2px; }
}
</style>