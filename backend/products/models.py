from django.db import models

# 금융 기관 정보
class Bank(models.Model):
    fin_co_no = models.CharField(max_length=20, unique=True)  # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)

    def __str__(self):
        return self.kor_co_nm


class Product(models.Model):
    """정기예금 / 적금 상품 기본 정보"""

    class ProductType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "정기예금"
        SAVING = "SAVING", "적금"

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="products",
    )

    product_type = models.CharField(
        max_length=10,
        choices=ProductType.choices,
    )

    fin_prdt_cd = models.CharField(max_length=50)   # 상품코드
    fin_prdt_nm = models.CharField(max_length=200)  # 상품명

    # 공시 정보
    dcls_month = models.CharField(max_length=6, blank=True)  # 공시월 YYYYMM
    dcls_strt_day = models.CharField(max_length=8, blank=True)  # 공시 시작일 YYYYMMDD
    dcls_end_day = models.CharField(max_length=8, blank=True)   # 공시 종료일 YYYYMMDD
    fin_co_subm_day = models.CharField(max_length=14, blank=True)  # 금융회사 제출일

    # 가입 관련 정보
    join_way = models.CharField(max_length=200, blank=True)     # 가입방법 (영업점, 인터넷 등)
    join_member = models.CharField(max_length=200, blank=True)  # 가입대상
    join_deny = models.CharField(max_length=10, blank=True)     # 가입제한 (예: '1'만 사용)

    # 설명/우대조건
    spcl_cnd = models.TextField(blank=True)   # 우대조건
    etc_note = models.TextField(blank=True)   # 기타 유의사항
    mtrt_int = models.TextField(blank=True)   # 만기 후 이자율

    # 한도 및 상태
    max_limit = models.BigIntegerField(null=True, blank=True)  # 최고 한도
    is_active = models.BooleanField(default=True)              # 현재 판매중 여부 (우리 기준)

    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # “같은 금융회사 + 같은 상품코드 + 같은 타입”은 하나만 존재
        unique_together = ("bank", "product_type", "fin_prdt_cd")

    def __str__(self):
        return f"[{self.get_product_type_display()}] {self.fin_prdt_nm} - {self.bank.kor_co_nm}"

class ProductOption(models.Model):
    """
    금융 상품별 기간/금리 옵션 단위
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="options",
    )

    # 저축 금리 정보
    intr_rate_type = models.CharField(max_length=10, blank=True)     # 금리 유형 코드
    intr_rate_type_nm = models.CharField(max_length=20, blank=True)  # 금리 유형명 (단리/복리 등)

    # 적금일 경우에만 의미 있는 필드 (정액/자유 적립 등)
    rsrv_type = models.CharField(max_length=10, blank=True)          # 적립 유형 코드
    rsrv_type_nm = models.CharField(max_length=20, blank=True)       # 적립 유형명

    save_trm = models.CharField(max_length=10, blank=True)   # 저축 기간 (개월)
    intr_rate = models.FloatField(null=True, blank=True)     # 기본 금리
    intr_rate2 = models.FloatField(null=True, blank=True)    # 최고 우대금리

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월 ({self.intr_rate2}%)"
