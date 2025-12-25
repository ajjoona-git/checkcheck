<template>
  <div class="profile-form-container">
    <form @submit.prevent="submitForm" enctype="multipart/form-data">

      <div class="form-group mb-4 text-center">
        <label class="form-label d-block mb-3">프로필 사진</label>

        <div class="profile-upload-wrapper">
          <div class="image-preview-box">
            <img v-if="previewImage" :src="previewImage" class="preview-img" alt="프로필 미리보기" />
            <div v-else class="preview-placeholder">
              <i class="bi bi-person-fill"></i>
            </div>
          </div>

          <label for="profile_image" class="upload-btn">
            <i class="bi bi-camera-fill"></i>
          </label>
          <input type="file" id="profile_image" class="d-none" accept="image/*" @change="onFileChange" />
        </div>

        <p class="text-muted small mt-2">클릭하여 사진을 변경하세요</p>
      </div>

      <div class="row g-3">
        <div class="col-md-6 form-group">
          <label for="gender" class="form-label">성별<span class="required">*</span></label>
          <select id="gender" class="form-select custom-input" v-model="gender" required>
            <option disabled value="">선택해주세요</option>
            <option value="0">남성</option>
            <option value="1">여성</option>
          </select>
        </div>

        <div class="col-md-6 form-group">
          <label for="credit_score" class="form-label">신용 점수<span class="required">*</span></label>
          <input type="number" id="credit_score" class="form-control custom-input" v-model.number="credit_score"
            placeholder="예: 850" required min="0" max="1000" />
        </div>

        <div class="col-md-6 form-group">
          <label for="assets" class="form-label">자산 (원)<span class="required">*</span></label>
          <input type="number" id="assets" class="form-control custom-input" v-model.number="assets"
            placeholder="예: 100000000" required min="0" />
        </div>

        <div class="col-md-6 form-group">
          <label for="salary" class="form-label">연봉 (원)<span class="required">*</span></label>
          <input type="number" id="salary" class="form-control custom-input" v-model.number="salary"
            placeholder="예: 34000000" required min="0" />
        </div>

        <div class="col-md-12 form-group">
          <label for="average_monthly_spend" class="form-label">평균 월 지출 (원)<span class="required">*</span></label>
          <input type="number" id="average_monthly_spend" class="form-control custom-input"
            v-model.number="average_monthly_spend" placeholder="예: 880000" required min="0" />
        </div>

        <div class="col-md-12 form-group mb-4">
          <label for="tender" class="form-label">투자 성향<span class="required">*</span></label>
          <select id="tender" class="form-select custom-input" v-model="tender" required>
            <option disabled value="">나의 투자 성향은?</option>
            <option value="1">매우 보수적 (안정형)</option>
            <option value="2">보수적 (안정추구형)</option>
            <option value="3">보통 (위험중립형)</option>
            <option value="4">공격적 (적극투자형)</option>
            <option value="5">매우 공격적 (공격투자형)</option>
          </select>
        </div>
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

const accountStore = useAccountStore()

const profile_image = ref(null)
const previewImage = ref(null)
const gender = ref('')
const credit_score = ref(null)
const assets = ref(null)
const salary = ref(null)
const average_monthly_spend = ref(null)
const tender = ref('')

const props = defineProps({
  isEdit: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['success'])

// 이미지 URL 가져오기
const getImageUrl = (path) => {
  if (!path) return null
  if (path.startsWith('http')) return path
  const API_URL = import.meta.env.VITE_API_URL
  return `${API_URL}${path}`
}

// 기존 프로필 데이터로 폼 채우기
const fillFormData = () => {
  if (props.isEdit && accountStore.user) {
    const u = accountStore.user

    gender.value = u.gender !== null ? String(u.gender) : ''
    credit_score.value = u.credit_score
    assets.value = u.assets
    salary.value = u.salary
    average_monthly_spend.value = u.average_monthly_spend
    tender.value = u.tender !== null ? String(u.tender) : ''

    if (u.profile_image) {
      previewImage.value = getImageUrl(u.profile_image)
    }
  }
}

// 컴포넌트 마운트 시 및 사용자 데이터 변경 시 폼 채우기
onMounted(() => {
  fillFormData()
})

// 사용자 데이터 변경 시 폼 채우기
watch(() => accountStore.user, () => {
  fillFormData()
})

// 프로필 이미지 변경 시 미리보기 업데이트
const onFileChange = (event) => {
  const files = event.target.files;
  if (files.length > 0) {
    profile_image.value = files[0];

    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.value = e.target.result;
    };
    reader.readAsDataURL(files[0]);
  } else {
    profile_image.value = null;
  }
};

// 폼 제출 처리
const submitForm = async function () {
  const formData = new FormData();

  if (gender.value !== '' && gender.value !== null) formData.append('gender', gender.value);
  if (credit_score.value !== null && credit_score.value !== '') formData.append('credit_score', credit_score.value);
  if (assets.value !== null && assets.value !== '') formData.append('assets', assets.value);
  if (salary.value !== null && salary.value !== '') formData.append('salary', salary.value);
  if (average_monthly_spend.value !== null && average_monthly_spend.value !== '') formData.append('average_monthly_spend', average_monthly_spend.value);
  if (tender.value !== '' && tender.value !== null) formData.append('tender', tender.value);

  if (profile_image.value) {
    formData.append('profile_image', profile_image.value);
  }

  try {
    if (props.isEdit) {
      await accountStore.editProfile(formData);
      alert('성공적으로 수정되었습니다.');
    } else {
      await accountStore.updateProfile(formData);
    }
    emit('success');
  } catch (error) {
    alert(props.isEdit ? '수정에 실패했습니다.' : '저장에 실패했습니다.');
  }
}
</script>

<style scoped>
/* 공통 폼 스타일 */
.form-label {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.custom-input {
  border-radius: 12px;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  font-size: 1rem;
  transition: all 0.2s;
  background-color: #fcfcfc;
}

.custom-input:focus {
  border-color: var(--moathon-green);
  box-shadow: 0 0 0 4px rgba(27, 94, 32, 0.1);
  background-color: white;
}

.required {
  color: #ff5252;
  margin-left: 2px;
}

/* 프로필 이미지 업로드 스타일 */
.profile-upload-wrapper {
  position: relative;
  display: inline-block;
  width: 100px;
  height: 100px;
}

.image-preview-box {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  background-color: #f1f3f5;
  overflow: hidden;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #adb5bd;
}

/* 버튼 스타일 수정: 래퍼 기준 절대 위치 (박스 밖) */
.upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 36px;
  height: 36px;
  background-color: var(--moathon-green);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
  z-index: 10;
}

.upload-btn:hover {
  transform: scale(1.1);
  background-color: #144a18;
}

/* 제출 버튼 */
.submit-btn {
  background-color: var(--moathon-green);
  border: none;
  border-radius: 12px;
  padding: 14px;
  font-weight: 700;
  font-size: 1.05rem;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(27, 94, 32, 0.2);
}

.submit-btn:hover {
  background-color: #144a18;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(27, 94, 32, 0.3);
}

.row.g-3 {
  --bs-gutter-y: 1.5rem;
}
</style>