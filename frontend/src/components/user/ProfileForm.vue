<template>
  <div class="onboarding-container">
    <form @submit.prevent="submitForm" enctype="multipart/form-data">
      <div class="form-group">
        <label for="profile_image">프로필 사진</label>
        <input type="file" id="profile_image" accept="image/*" @change="onFileChange" />
      </div>

      <div class="form-group">
        <label for="gender">성별<span class="required">*</span></label>
        <select id="gender" v-model="gender" required>
          <option disabled value="">성별을 선택해주세요</option>
          <option value="0">남성</option>
          <option value="1">여성</option>
        </select>
      </div>

      <div class="form-group">
        <label for="credit_score">신용 점수<span class="required">*</span></label>
        <input type="number" id="credit_score" v-model.number="credit_score" placeholder="예: 850" required min="0"
          max="1000" />
      </div>

      <div class="form-group">
        <label for="assets">자산 (원)<span class="required">*</span></label>
        <input type="number" id="assets" v-model.number="assets" placeholder="예: 1000" required min="0" />
      </div>

      <div class="form-group">
        <label for="salary">연봉 (원)<span class="required">*</span></label>
        <input type="number" id="salary" v-model.number="salary" placeholder="예: 3000" required min="0" />
      </div>

      <div class="form-group">
        <label for="average_monthly_spend">평균 월 지출 (원)<span class="required">*</span></label>
        <input type="number" id="average_monthly_spend" v-model.number="average_monthly_spend" placeholder="예: 100"
          required min="0" />
      </div>

      <div class="form-group">
        <label for="tender">투자 성향<span class="required">*</span></label>
        <select id="tender" v-model="tender" required>
          <option disabled value="">투자 성향을 선택해주세요</option>
          <option value="1">매우 보수적 (안정형)</option>
          <option value="2">보수적 (안정추구형)</option>
          <option value="3">보통 (위험중립형)</option>
          <option value="4">공격적 (적극투자형)</option>
          <option value="5">매우 공격적 (공격투자형)</option>
        </select>
      </div>

      <button type="submit" class="submit-btn">저장하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAccountStore } from '@/stores/accounts';

const emit = defineEmits(['success'])

const accountStore = useAccountStore()

const profile_image = ref(null)
const gender = ref('')
const credit_score = ref(null)
const assets = ref(null)
const salary = ref(null)
const average_monthly_spend = ref(null)
const tender = ref('')

const onFileChange = (event) => {
  const files = event.target.files;
  if (files.length > 0) {
    profile_image.value = files[0];
  } else {
    profile_image.value = null;
  }
};

const submitForm = async function () {
  if (!gender.value || !credit_score.value || !assets.value ||
    !salary.value || !average_monthly_spend.value || !tender.value) {
    alert('모든 필수 항목을 입력해주세요.');
    return;
  }

  const formData = new FormData();

  formData.append('gender', gender.value);
  formData.append('credit_score', credit_score.value);
  formData.append('assets', assets.value);
  formData.append('salary', salary.value);
  formData.append('average_monthly_spend', average_monthly_spend.value);
  formData.append('tender', tender.value);

  if (profile_image.value) {
    formData.append('profile_image', profile_image.value);
  }

  try {
    await accountStore.updateProfile(formData);
    emit('success')
  } catch (error) {
    alert('저장에 실패했습니다.')
  }
}
</script>

<style scoped>
.required {
  color: red;
  margin-left: 2px;
}
</style>