from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    PasswordResetSerializer,
    UserPasswordResetConfirmSerializer,
)

User = get_user_model()

# 비밀번호 잃어버렸을 때, 이메일로 재설정 연결 
@api_view(['POST'])
@permission_classes([AllowAny])
def find_password(request):
    serializer = PasswordResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"detail": "비밀번호 재설정 메일이 발송되었다면, 입력하신 이메일에서 확인하실 수 있습니다."},
            status=status.HTTP_200_OK,
        )
    # uid, token 생성
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # 프론트 비밀번호 재설정 페이지 URL (Vue 라우트)
    frontend_base_url = getattr(settings, "FRONTEND_BASE_URL", "http://localhost:5173")
    reset_url = f"{frontend_base_url}/reset-password/{uid}/{token}"

    subject = "[모아톤] 비밀번호 재설정 안내"
    message = (
        f"{user.nickname}님, 안녕하세요.\n\n"
        f"아래 링크를 클릭하여 비밀번호를 재설정해 주세요.\n\n"
        f"{reset_url}\n\n"
        f"만약 비밀번호 재설정을 요청하지 않으셨다면 이 메일은 무시하셔도 됩니다."
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@moathon.com")

    send_mail(
        subject,
        message,
        from_email,
        [email],
        fail_silently=False,
    )

    return Response(
        {"detail": "비밀번호 재설정 메일이 발송되었다면, 입력하신 이메일에서 확인하실 수 있습니다."},
        status=status.HTTP_200_OK,
    )

# 비밀번호 재설정
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    uidb64 = request.data.get("uid")
    token = request.data.get("token")

    if not uidb64 or not token:
        return Response(
            {"detail": "잘못된 요청입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    # uid 디코딩 → User 조회
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        return Response(
            {"detail": "유효하지 않은 사용자입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # token 검증
    if not default_token_generator.check_token(user, token):
        return Response(
            {"detail": "토큰이 유효하지 않거나 만료되었습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 비밀번호 검증 + 저장 
    serializer = UserPasswordResetConfirmSerializer(
        instance=user,
        data=request.data,
        partial=True,  # 비밀번호 필드만 업데이트
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()  # 내부에서 set_password 호출

    return Response(
        {"detail": "비밀번호가 성공적으로 변경되었습니다."},
        status=status.HTTP_200_OK,
    )