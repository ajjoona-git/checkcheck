from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter

from django.shortcuts import render, get_object_or_404
from .models import Product, ProductOption
from .serializers import ProductListSerializer

@extend_schema(
    parameters=[
        OpenApiParameter(name='bank', description='은행명 (예: 우리은행)', required=False, type=str),
        OpenApiParameter(name='type', description='상품 유형 (예: DEPOSIT, SAVING)', required=False, type=str),
        OpenApiParameter(name='period', description='예치 기간 (예: 12)', required=False, type=int),
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    """
    전체 금융 상품 조회 API
    
    GET /products/
    """
    products = Product.objects.filter(is_active=True)

    bank_name = request.query_params.get('bank')       # 은행명 (UI: 은행 선택)
    product_type = request.query_params.get('type')    # 상품 유형 (UI: 예금/적금 탭)
    save_trm = request.query_params.get('period')      # 예치 기간 (UI: 예치기간)

    if product_type:
        products = products.filter(product_type=product_type)

    if bank_name and bank_name != '전체':
        products = products.filter(bank__kor_co_nm=bank_name)

    if save_trm and save_trm != '전체기간':
        products = products.filter(options__save_trm=save_trm).distinct()
    
    paginator = PageNumberPagination()
    paginator.page_size = 50
    result_page = paginator.paginate_queryset(products, request)

    if result_page is not None:
        serializer = ProductListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, product_id):
    """
    금융 상품 상세 조회 API
    
    GET /products/<int:product_id>/
    """
    product = get_object_or_404(Product, pk=product_id)
    serializer = ProductListSerializer(product)
    return Response(serializer.data)