from django.db import models

# Create your models here.
class CommodityAsset(models.Model):
    asset = models.CharField(
        max_length=20,
        primary_key=True,  
    )

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

