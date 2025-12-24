<template>
  <div class="container py-5">
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">로딩 중...</span>
      </div>
    </div>
    
    <div v-else-if="user" class="mypage-content">
      <UserProfileSection 
        :user="user" 
        :isEditing="isEditing" 
        @toggle-edit="toggleEdit"
      />

      <div v-if="isEditing" class="edit-section mb-4fade-in">
        <div class="card p-4 bg-light border-0">
          <h4 class="mb-3">내 정보 수정</h4>
          <ProfileForm 
            :is-edit="true" 
            @success="onUpdateSuccess" 
          />
        </div>
      </div>

      <div v-else class="dashboard-section fade-in">
        <div class="row">
          <div class="col-lg-12">
            <BadgeLibrary :badges="user.badge_collection" />
          </div>
        </div>

        <div class="row">
          <div class="col-lg-6">
            <RateChart :moathons="user.moathons" />
          </div>
          
          <div class="col-lg-6">
            <div class="card p-4">
              <h3 class="mb-3">진행 중인 모아톤</h3>
              <div v-if="user.moathons.length > 0">
                <MoathonCard 
                  v-for="moathon in user.moathons" 
                  :key="moathon.id" 
                  :moathon="moathon"
                  class="mb-3"
                />
              </div>
              <div v-else class="text-center py-5 text-muted">
                <p>진행 중인 모아톤이 없습니다.</p>
                <router-link :to="{ name: 'moathonCreate' }" class="btn btn-primary btn-sm">
                  모아톤 시작하기
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'

import UserProfileSection from '@/components/user/UserProfileSection.vue'
import ProfileForm from '@/components/user/ProfileForm.vue'
import BadgeLibrary from '@/components/common/BadgeLibrary.vue'
import RateChart from '@/components/product/RateChart.vue'
import MoathonCard from '@/components/moathon/MoathonCard.vue'

const store = useAccountStore()
const user = computed(() => store.user)
const loading = ref(true)
const isEditing = ref(false)
onMounted(async () => {
  try {
    await store.getProfile()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

const toggleEdit = () => {
  isEditing.value = !isEditing.value
}

const onUpdateSuccess = async () => {
  isEditing.value = false
}
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>