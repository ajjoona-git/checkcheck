from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Moathon, MoathonComment, MoathonLike
from accounts.services.badge_functions import award_achieve_badges_on_moathon_created, award_social_badges
from .serializers import (
    MoathonDetailSerializer, 
    MoathonListSerializer, 
    MoathonCreateSerializer,
    MoathonUpdateSerializer,
    MoathonCommentSerializer,
    MoathonCommentWriteSerializer,
)

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from datetime import date

User = get_user_model()

# 전체 모아톤 조회
@api_view(['GET'])
def moathon_list(request):
    if request.method == 'GET':
        moathons = Moathon.objects.all().order_by('-id')
        
        paginator = PageNumberPagination()
        paginator.page_size = 24
        result_page = paginator.paginate_queryset(moathons, request)

        serializer = MoathonListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


@extend_schema(
    methods=['GET'],
    responses=MoathonDetailSerializer,
    summary="모아톤 상세 조회"
)
@extend_schema(
    methods=['PATCH'],
    request=MoathonUpdateSerializer,
    responses=MoathonDetailSerializer,
    summary="모아톤 수정"
)
@extend_schema(
    methods=['DELETE'],
    summary="모아톤 삭제"
)
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def moathon_detail(request, moathon_pk):
    """
    특정 모아톤의 상세 조회, 수정, 삭제 API
    - GET: 누구나 조회 가능 (로그인 유저)
    - PATCH/DELETE: 본인만 가능 
    GET/PATCH/DELETE /moathon/<int:moathon_pk>/
    """
    moathon = get_object_or_404(Moathon, pk=moathon_pk)

    if request.method == 'GET':
        serializer = MoathonDetailSerializer(moathon, context={"request": request})
        return Response(serializer.data)
    
    if moathon.user != request.user:
        return Response(
            {"error": "본인의 모아톤만 수정하거나 삭제할 수 있습니다."}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'PATCH':
        serializer = MoathonUpdateSerializer(moathon, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            updated_moathon = serializer.save()
            return Response(MoathonDetailSerializer(updated_moathon, context={"request": request}).data)
        
    elif request.method == 'DELETE':
        moathon.delete()
        return Response(
            {"message": "모아톤이 삭제되었습니다."}, 
            status=status.HTTP_204_NO_CONTENT
        )
        

# 모아톤 생성
@extend_schema(
    request=MoathonCreateSerializer,
    responses=MoathonDetailSerializer,
    summary="모아톤 생성"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def moathon_create(request):
    create_serializer = MoathonCreateSerializer(data=request.data)
    if create_serializer.is_valid(raise_exception=True):
        product_option = create_serializer.validated_data['product_option']
        try:
            term_months = int(product_option.save_trm)
        except (ValueError, TypeError):
            term_months = 12
        moathon = create_serializer.save(user=request.user, term_months=term_months)
        response_serializer = MoathonDetailSerializer(moathon)
        # 모아톤 생성 직후 뱃지 지급
        award_achieve_badges_on_moathon_created(request.user, moathon)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
# 댓글 목록 조회 
@extend_schema(
    methods=["GET"],
    responses=MoathonCommentSerializer,
    summary="모아톤 댓글 목록 조회"
)
@extend_schema(
    methods=["POST"],
    request=MoathonCommentWriteSerializer,
    responses=MoathonCommentSerializer,
    summary="모아톤 댓글 작성"
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def moathon_comment_list_create(request, moathon_pk):
    moathon = get_object_or_404(Moathon, pk=moathon_pk)

    if request.method == "GET":
        qs = (
            MoathonComment.objects
            .filter(moathon=moathon)
            .select_related("user")
            .order_by("-created_at", "-id")
        )

        paginator = PageNumberPagination()
        paginator.page_size = 50
        page = paginator.paginate_queryset(qs, request)

        serializer = MoathonCommentSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    write_serializer = MoathonCommentWriteSerializer(data=request.data)
    if write_serializer.is_valid(raise_exception=True):
        comment = write_serializer.save(user=request.user, moathon=moathon)
        return Response(MoathonCommentSerializer(comment).data, status=status.HTTP_201_CREATED)


@extend_schema(
    methods=["PATCH"],
    request=MoathonCommentWriteSerializer,
    responses=MoathonCommentSerializer,
    summary="모아톤 댓글 수정"
)
@extend_schema(
    methods=["DELETE"],
    summary="모아톤 댓글 삭제"
)
@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def moathon_comment_detail(request, moathon_pk, comment_pk):
    """
    특정 모아톤 댓글의 수정/삭제 API
    - PATCH/DELETE: 본인만 가능
    PATCH/DELETE /moathon/<int:moathon_pk>/comments/<int:comment_pk>/
    """
    comment = get_object_or_404(
        MoathonComment.objects.select_related("user", "moathon"),
        pk=comment_pk
    )

    if comment.user != request.user:
        return Response(
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "PATCH":
        if "content" not in request.data:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        write_serializer = MoathonCommentWriteSerializer(comment, data=request.data, partial=True)
        if write_serializer.is_valid(raise_exception=True):
            updated = write_serializer.save()
            return Response(MoathonCommentSerializer(updated).data, status=status.HTTP_200_OK)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# 모아톤 좋아요/취소 토글
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def moathon_like_toggle(request, moathon_pk):
    user = request.user
    moathon = get_object_or_404(Moathon, pk=moathon_pk)

    with transaction.atomic():
        like, created = MoathonLike.objects.get_or_create(user=user, moathon=moathon)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

    # 좋아요/취소 직후 배지 갱신(즉시 반영)
    award_social_badges(user)               # 응원단장 체크
    award_social_badges(moathon.user)       # 인기스타 체크(받은 좋아요)

    like_count = MoathonLike.objects.filter(moathon=moathon).count()
    return Response({"liked": liked, "like_count": like_count})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_moathon_list(request):
    """
    내가 팔로우하는 유저들의 '진행 중인' 모아톤 조회
    """
    user = request.user
    
    # 내가 팔로우하는 유저들의 ID 리스트 추출
    following_ids = user.following_relations.values_list('following_id', flat=True)

    # 조건 필터링
    # - 작성자가 팔로잉 목록에 포함됨 (user__id__in)
    # - 종료일이 오늘보다 같거나 큼 (end_date__gte -> 진행 중)
    # - 최신순 정렬
    today = date.today()
    
    moathons = Moathon.objects.filter(
        user__id__in=following_ids,
        end_date__gte=today
    ).select_related('user').order_by('-created_at') 

    serializer = MoathonListSerializer(moathons, many=True)
    
    return Response(serializer.data)