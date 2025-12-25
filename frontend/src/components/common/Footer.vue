<template>

  <footer>
    <div class="footer-content">
      <p>모아톤은 사용자의 즐거운 저축 습관 형성을 돕는 가이드 서비스입니다. 실제 금융 상품 가입은 해당 금융기관의 페이지에서 안전하게 진행됩니다.</p>
      <div class="footer-line"></div>
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
        <span>© 2025 Moathon.</span>
        <div class="d-flex gap-4">
          <a href="#" class="text-secondary text-decoration-none">개인정보처리방침</a>
          <a href="#" class="text-secondary text-decoration-none">이용약관</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
footer {
  background: #fbfbfd;
  padding: 60px 0 20px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  border-top: 1px solid #d2d2d7;
}

.footer-content {
  max-width: 980px;
  margin: 0 auto;
  padding: 0 22px;
}

.footer-line {
  height: 1px;
  background: #d2d2d7;
  margin: 24px 0;
}
</style>