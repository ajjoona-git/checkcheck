from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Moathon
from .serializers import MoathonDetailSerializer, MoathonListSerializer, MoathonCreateSerializer

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


# 단일 모아톤 조회
@api_view(['GET'])
def moathon_detail(request, moathon_pk):
    moathon = Moathon.objects.get(pk=moathon_pk)
    serializer = MoathonDetailSerializer(moathon)
    return Response(serializer.data)

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
    