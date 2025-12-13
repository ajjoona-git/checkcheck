from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.password_validation import validate_password

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


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("등록되지 않은 이메일입니다.")
        return value


class UserPasswordResetConfirmSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # User 모델에서 비밀번호만 처리 
        fields = ("new_password", "new_password2")

    def validate(self, attrs):
        pw1 = attrs.get("new_password")
        pw2 = attrs.get("new_password2")

        if pw1 != pw2:
            raise serializers.ValidationError(
                {"new_password2": "비밀번호가 일치하지 않습니다."}
            )

        validate_password(pw1, self.instance)
        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data.get['new_password']
        instance.set_password(new_password)
        instance.save()
        return instance