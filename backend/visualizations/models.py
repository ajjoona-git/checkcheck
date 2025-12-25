from django.db import models

# 원자재 종류(금, 은 등) 기록
class CommodityAsset(models.Model):
    asset = models.CharField(
        max_length=20,
        primary_key=True,  
    )
    
# 원자재 가격 내역 기록
class CommodityPrice(models.Model):
    commodity = models.ForeignKey(
        CommodityAsset,
        on_delete=models.CASCADE,
        related_name='prices',
    )
    date = models.DateField()
    close_last = models.DecimalField(max_digits=20, decimal_places=6)
    volume = models.DecimalField(max_digits=20, decimal_places=6)
    open = models.DecimalField(max_digits=20, decimal_places=6)
    high = models.DecimalField(max_digits=20, decimal_places=6)
    low = models.DecimalField(max_digits=20, decimal_places=6)

