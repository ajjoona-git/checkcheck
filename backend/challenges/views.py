from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from accounts.models import Moathon
from products.models import ProductOption
from .serializers import MoathonDetailSerializer, MoathonListSerializer, MoathonInitialSerializer
from datetime import timedelta, date

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
