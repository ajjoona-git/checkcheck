from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import render, get_object_or_404
from .models import Product, ProductOption
from .serializers import ProductListSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    """
    전체 금융 상품 조회 API
    
    GET /products/
    """
    products = Product.objects.all()

    bank_name = request.query_params.get('bank')       # 은행명 (UI: 은행 선택)
    product_type = request.query_params.get('type')    # 상품 유형 (UI: 예금/적금 탭)
    save_trm = request.query_params.get('period')      # 예치 기간 (UI: 예치기간)

    if product_type:
        products = products.filter(product_type=product_type)

    if bank_name and bank_name != '전체':
        products = products.filter(bank__kor_co_nm=bank_name)

    if save_trm and save_trm != '전체기간':
        products = products.filter(options__save_trm=save_trm).distinct()
    
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)