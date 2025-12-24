<template>
  <div class="profile-form-container">
    <form @submit.prevent="submitForm" enctype="multipart/form-data">
      
      <div class="form-group mb-3">
        <label for="profile_image" class="form-label">프로필 사진</label>
        <div class="d-flex align-items-center gap-3">
          <img 
            v-if="previewImage" 
            :src="previewImage" 
            class="preview-img" 
            alt="미리보기" 
          />
          <input type="file" id="profile_image" class="form-control" accept="image/*" @change="onFileChange" />
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="gender" class="form-label">성별<span class="required">*</span></label>
        <select id="gender" class="form-select" v-model="gender" required>
          <option disabled value="">성별을 선택해주세요</option>
          <option value="0">남성</option>
          <option value="1">여성</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="credit_score" class="form-label">신용 점수<span class="required">*</span></label>
        <input type="number" id="credit_score" class="form-control" v-model.number="credit_score" placeholder="예: 850" required min="0" max="1000" />
      </div>

      <div class="form-group mb-3">
        <label for="assets" class="form-label">자산 (만원 단위)<span class="required">*</span></label>
        <input type="number" id="assets" class="form-control" v-model.number="assets" placeholder="예: 1000" required min="0" />
      </div>

      <div class="form-group mb-3">
        <label for="salary" class="form-label">연봉 (만원 단위)<span class="required">*</span></label>
        <input type="number" id="salary" class="form-control" v-model.number="salary" placeholder="예: 3000" required min="0" />
      </div>

      <div class="form-group mb-3">
        <label for="average_monthly_spend" class="form-label">평균 월 지출 (만원 단위)<span class="required">*</span></label>
        <input type="number" id="average_monthly_spend" class="form-control" v-model.number="average_monthly_spend" placeholder="예: 100" required min="0" />
      </div>

      <div class="form-group mb-4">
        <label for="tender" class="form-label">투자 성향<span class="required">*</span></label>
        <select id="tender" class="form-select" v-model="tender" required>
          <option disabled value="">투자 성향을 선택해주세요</option>
          <option value="1">매우 보수적 (안정형)</option>
          <option value="2">보수적 (안정추구형)</option>
          <option value="3">보통 (위험중립형)</option>
          <option value="4">공격적 (적극투자형)</option>
          <option value="5">매우 공격적 (공격투자형)</option>
        </select>
      </div>

      <button type="submit" class="submit-btn btn btn-primary w-100">
        {{ isEdit ? '수정 완료' : '저장하기' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAccountStore } from '@/stores/accounts';

// [Props] 수정 모드 여부
const props = defineProps({
  isEdit: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['success'])
const accountStore = useAccountStore()

// 폼 데이터 Refs
const profile_image = ref(null) // 파일 객체 (전송용)
const previewImage = ref(null)  // 미리보기 URL (화면 표시용)
const gender = ref('')
const credit_score = ref(null)
const assets = ref(null)
const salary = ref(null)
const average_monthly_spend = ref(null)
const tender = ref('')

// [Helper] 이미지 URL 처리
const getImageUrl = (path) => {
  if (!path) return null
  if (path.startsWith('http')) return path
  const API_URL = import.meta.env.VITE_API_URL
  return `${API_URL}${path}`
}

// [핵심] 기존 데이터 채우기 (수정 모드용)
const fillFormData = () => {
  if (props.isEdit && accountStore.user) {
    const u = accountStore.user
    
    // DB의 값(Integer 등)을 Form 타입(String 등)에 맞춰 변환
    // 값이 0인 경우도 고려하여 String() 변환 사용
    gender.value = u.gender !== null ? String(u.gender) : ''
    credit_score.value = u.credit_score
    assets.value = u.assets
    salary.value = u.salary
    average_monthly_spend.value = u.average_monthly_spend
    tender.value = u.tender !== null ? String(u.tender) : ''
    
    // 기존 이미지가 있다면 미리보기에 설정
    if (u.profile_image) {
      previewImage.value = getImageUrl(u.profile_image)
    }
  }
}

// 컴포넌트 마운트 시 데이터 로드 시도
onMounted(() => {
  fillFormData()
})

// 새로고침 등 비동기로 user 데이터가 나중에 들어올 때를 대비
watch(() => accountStore.user, () => {
  fillFormData()
})

const onFileChange = (event) => {
  const files = event.target.files;
  if (files.length > 0) {
    profile_image.value = files[0];
    
    // 새 파일 선택 시 미리보기 즉시 업데이트 (FileReader 사용)
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.value = e.target.result;
    };
    reader.readAsDataURL(files[0]);
  } else {
    profile_image.value = null;
    // 취소 시 기존 이미지 미리보기는 유지하거나 초기화할 수 있음 (여기선 유지)
  }
};

const submitForm = async function () {
  // [유효성 검사] 온보딩일 때는 필수, 수정일 때는 자유롭지만 폼 자체 required 속성이 막아줌
  // 여기서는 간단히 로직 진행
  
  const formData = new FormData();

  // 1. 텍스트 필드: 값이 유효할 때만 전송
  if (gender.value !== '' && gender.value !== null) formData.append('gender', gender.value);
  if (credit_score.value !== null && credit_score.value !== '') formData.append('credit_score', credit_score.value);
  if (assets.value !== null && assets.value !== '') formData.append('assets', assets.value);
  if (salary.value !== null && salary.value !== '') formData.append('salary', salary.value);
  if (average_monthly_spend.value !== null && average_monthly_spend.value !== '') formData.append('average_monthly_spend', average_monthly_spend.value);
  if (tender.value !== '' && tender.value !== null) formData.append('tender', tender.value);

  // 2. 파일 필드: 새 파일이 선택되었을 때만 전송
  if (profile_image.value) {
    formData.append('profile_image', profile_image.value);
  }

  try {
    if (props.isEdit) {
      // 수정 모드 (PATCH)
      await accountStore.editProfile(formData);
      alert('성공적으로 수정되었습니다.');
    } else {
      // 온보딩 모드 (PUT)
      await accountStore.updateProfile(formData);
    }
    emit('success');
  } catch (error) {
    console.error(error); 
    alert(props.isEdit ? '수정에 실패했습니다.' : '저장에 실패했습니다.');
  }
}
</script>

<style scoped>
.required {
  color: red;
  margin-left: 2px;
}
.preview-img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #ddd;
}
.form-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
}
</style>