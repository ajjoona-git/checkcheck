from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Moathon
from .serializers import (
    MoathonDetailSerializer, 
    MoathonListSerializer, 
    MoathonCreateSerializer,
    MoathonUpdateSerializer,
)

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

# 전체 모아톤 조회
@api_view(['GET'])
def moathon_list(request):
    if request.method == 'GET':
        moathons = Moathon.objects.all().order_by('-id')
        
        paginator = PageNumberPagination()
        paginator.page_size = 50
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
        serializer = MoathonDetailSerializer(moathon)
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
            return Response(MoathonDetailSerializer(updated_moathon).data)
        
    elif request.method == 'DELETE':
        moathon.delete()
        return Response(
            {"message": "모아톤이 삭제되었습니다."}, 
            status=status.HTTP_204_NO_CONTENT
        )
        

@extend_schema(
    request=MoathonCreateSerializer,
    responses=MoathonDetailSerializer,
    summary="모아톤 생성"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def moathon_create(request):
    """
    모아톤 생성 API
    POST /moathons/create/
    """
    create_serializer = MoathonCreateSerializer(data=request.data)
    if create_serializer.is_valid(raise_exception=True):
        product_option = create_serializer.validated_data['product_option']
        try:
            term_months = int(product_option.save_trm)
        except (ValueError, TypeError):
            term_months = 12
        moathon = create_serializer.save(user=request.user, term_months=term_months)
        response_serializer = MoathonDetailSerializer(moathon)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    