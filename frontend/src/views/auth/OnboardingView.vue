<template>
  <div>
    <h1>프로필 정보 입력</h1>
    <p>입력한 정보는 고객님을 위한 맞춤 예/적금 상품 추천에 사용됩니다.</p>

    <ProfileForm @success="goHome" />
  </div>
</template>

<script setup>
  import ProfileForm from '@/components/user/ProfileForm.vue';
  import { useRouter } from 'vue-router';

  const router = useRouter()

  const goHome = function () {
    alert('환영합니다! 가입이 완료되었습니다.')
    router.push({ name: 'home' })
  }
</script>

<style scoped>

</style>