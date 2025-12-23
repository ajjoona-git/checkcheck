from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Count
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from challenges.models import Moathon
from .models import Badge, UserBadge, UserFollow
from accounts.services.badge_functions import award_social_badges

from .serializers import (
    PasswordResetSerializer,
    UserPasswordResetConfirmSerializer,
    MoathonListWithRatesSerializer,
    ProfileUpdateSerializer,
    OnboardingPutSerializer,
)

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

User = get_user_model()

# 비밀번호 잃어버렸을 때, 이메일로 재설정 연결
@extend_schema(
    tags=["Accounts"],
    summary="비밀번호 재설정 메일 발송",
    request=PasswordResetSerializer,
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            "요청 예시",
            value={"email": "user@example.com"},
            request_only=True,
        ),
        OpenApiExample(
            "응답 예시",
            value={"detail": "비밀번호 재설정 메일이 발송되었다면, 입력하신 이메일에서 확인하실 수 있습니다."},
            response_only=True,
        ),
    ],
)
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
@extend_schema(
    tags=["Accounts"],
    summary="비밀번호 재설정",
    request=OpenApiTypes.OBJECT,
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            "요청 예시",
            value={
                "uid": "Mg",
                "token": "set-password-token",
                "new_password": "NewPw!234",
                "new_password2": "NewPw!234",
            },
            request_only=True,
        ),
        OpenApiExample(
            "응답 예시",
            value={"detail": "비밀번호가 성공적으로 변경되었습니다."},
            response_only=True,
        ),
    ],
)
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

# 프로필 조회
@extend_schema(
    tags=["Accounts"],
    summary="프로필 조회",
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    # 역참조 related_name이 users_moathon 이므로 Prefetch 대상도 그 이름을 써야 함
    user = (
        User.objects
        .prefetch_related(
            Prefetch(
                "users_moathon",
                queryset=(
                    Moathon.objects
                    .select_related(
                        "user",
                        "product_option",
                        "product_option__product",
                        "product_option__product__bank",
                    )
                    .order_by("-created_at")
                ),
            ),
            Prefetch(
                "badges",  # UserBadge.user related_name='badges' 
                queryset=UserBadge.objects.select_related("badge", "moathon"),
            ),
        )
        .get(pk=request.user.pk)
    )

    moathons_qs = user.users_moathon.all()
    moathons_data = MoathonListWithRatesSerializer(moathons_qs, many=True).data

    profile_image_url = None
    if getattr(user, "profile_image", None) and user.profile_image:
        try:
            profile_image_url = request.build_absolute_uri(user.profile_image.url)
        except Exception:
            profile_image_url = None

    # 팔로워/팔로잉 수
    follower_count = UserFollow.objects.filter(following=user).count()
    following_count = UserFollow.objects.filter(follower=user).count()

    # 뱃지 도감
    all_badges = Badge.objects.all()

    obtained_stats = (
        user.badges  # Prefetch로 로드된 UserBadge related manager
        .values("badge")
        .annotate(count=Count("id"))
    )
    obtained_map = {item["badge"]: item["count"] for item in obtained_stats}

    badges_collection = []
    for badge in all_badges:
        cnt = obtained_map.get(badge.id, 0)
        badges_collection.append({
            "id": badge.id,
            "type": badge.type,
            "name": badge.name,
            "description": badge.description,
            "url": badge.badge_url,
            "is_obtained": cnt > 0,
            "quantity": cnt,
        })

    data = {
        "profile_image": profile_image_url,
        "email": user.email,
        "nickname": user.nickname,
        "birth": user.birth,
        "gender": user.gender,
        "credit_score": user.credit_score,
        "assets": user.assets,
        "salary": user.salary,
        "average_monthly_spend": user.average_monthly_spend,
        "tender": user.tender,
        "follower_count": follower_count,
        "following_count": following_count,
        "badge_collection": badges_collection,

        "moathons": moathons_data,
    }
    return Response(data)

# 프로필 수정
@extend_schema(
    tags=["Accounts"],
    summary="프로필 수정(PATCH/PUT)",
    request=ProfileUpdateSerializer,
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(["PATCH", "PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def profile_update(request):
    user = request.user
    # PATCH면 TRUE / PUT면 FALSE
    partial = (request.method == "PATCH")

    serializer = ProfileUpdateSerializer(user, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    # 응답에서 이미지 URL은 절대경로로 주는 게 FE에서 편함
    data = serializer.data
    if getattr(user, "profile_image", None):
        try:
            data["profile_image"] = request.build_absolute_uri(user.profile_image.url)
        except Exception:
            pass

    return Response(data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Accounts"],
    summary="온보딩 최종 제출(PUT)",
    request=OnboardingPutSerializer,
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            "요청 예시",
            value={
                "gender": "M",
                "credit_score": 850,
                "assets": 12000000,
                "salary": 3200000,
                "average_monthly_spend": 1400000,
                "tender": "SAFE",
            },
            request_only=True,
        ),
        OpenApiExample(
            "응답 예시",
            value={"onboarding_completed": True},
            response_only=True,
        ),
    ],
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def onboarding(request):
    user = request.user

    required_fields = [
        "gender",
        "credit_score",
        "assets",
        "salary",
        "average_monthly_spend",
        "tender",
    ]
    missing = [f for f in required_fields if f not in request.data]
    if missing:
        return Response(
            {
                "detail": "온보딩 제출은 필수 항목을 모두 포함해야 합니다.",
                "missing_fields": missing,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = OnboardingPutSerializer(user, data=request.data, partial=False)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    # 최소 응답(저장 성공 + 완료 여부). 원하면 serializer.data 전체를 내려도 됨.
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )

@extend_schema(summary="뱃지 컬렉션 조회")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def badge_collection(request):
    user = request.user

    # 1. 모든 뱃지 마스터 정보 가져오기 (badge_url 필드가므로 'url'을 맞추어 사용)
    all_badges = Badge.objects.all()

    # 2. 유저가 획득한 뱃지 정보 가져오기, 뱃지 ID별로 그룹화하여 개수 세기
    obtained_stats = UserBadge.objects.filter(user=user).values('badge').annotate(count=Count('id'))

    # 딕셔너리로 변환하여 매핑 { badge_id: count }
    obtained_map = {item['badge']: item['count'] for item in obtained_stats}

    # 3. 데이터 조합
    collection_data = []
    for badge in all_badges:
        count = obtained_map.get(badge.id, 0)

        collection_data.append({
            "id": badge.id,
            "type": badge.type,
            "name": badge.name,
            "description": badge.description,
            "url": badge.badge_url,  # 수정: badge_url로 변경
            "is_obtained": count > 0, # 획득 여부
            "quantity": count,        # 획득 횟수
        })

    return Response({
        "collection": collection_data
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_toggle(request, user_pk):
    me = request.user
    target = get_object_or_404(User, pk=user_pk)

    if me.id == target.id:
        return Response(status=400)

    with transaction.atomic():
        rel, created = UserFollow.objects.get_or_create(follower=me, following=target)
        if not created:
            rel.delete()
            followed = False
        else:
            followed = True

    # 팔로우/언팔로우 직후 배지 갱신(즉시 반영)
    award_social_badges(target)  # 팔로팔로미(팔로워 수) 체크는 target 기준

    follower_count = UserFollow.objects.filter(following=target).count()
    return Response({"followed": followed, "follower_count": follower_count})