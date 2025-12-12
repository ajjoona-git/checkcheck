from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    """
    dj-rest-auth 회원가입 시에
    - username, password1, password2, email (기본)
    + nickname, birth 를 추가로 받기 위한 Serializer
    """
    nickname = serializers.CharField(max_length=20, required=True)
    birth = serializers.DateField(required=True)

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data.update(
            {
                "nickname": self.validated_data.get("nickname", ""),
                "birth": self.validated_data.get("birth", None),
            }
        )
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get("nickname")
        user.birth = self.validated_data.get("birth")
        user.save()
        return user