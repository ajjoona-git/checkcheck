from __future__ import annotations

from decimal import Decimal, InvalidOperation
from datetime import date, datetime
import pandas as pd

from django.core.management.base import BaseCommand
from django.db import transaction

from visualizations.models import CommodityAsset, CommodityPrice


def to_date(x) -> date:
    if pd.isna(x):
        raise ValueError("Date 값이 비어있습니다.")

    if isinstance(x, pd.Timestamp):
        return x.date()
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x

    dt = pd.to_datetime(str(x).strip(), errors="raise")
    return dt.date()


def to_decimal_remove_commas(x) -> Decimal:
    """
    '1,245.29' -> Decimal('1245.29')
    콤마 제거, 소수점 유지
    """
    if pd.isna(x):
        raise ValueError("숫자 값이 비어있습니다.")

    s = str(x).strip()
    s = s.replace(",", "").replace(" ", "")
    s = s.replace("$", "").replace("₩", "")
    s = s.replace("−", "-")  # 유니코드 마이너스 대응

    try:
        return Decimal(s)
    except (InvalidOperation, ValueError) as e:
        raise ValueError(f"Decimal 변환 실패: 원본={x!r}, 정리={s!r}") from e


class Command(BaseCommand):
    help = "Import commodity prices from XLSX (Date, Close/Last, Volume, Open, High, Low)."

    def add_arguments(self, parser):
        parser.add_argument("--asset", required=True, help="예: silver 또는 gold (CommodityAsset PK)")
        parser.add_argument("--path", required=True, help="xlsx 파일 경로")
        parser.add_argument("--sheet", default=0, help="시트명 또는 인덱스(기본 0)")
        parser.add_argument("--truncate", action="store_true", help="해당 asset의 기존 데이터 삭제 후 재적재")

    @transaction.atomic
    def handle(self, *args, **options):
        asset_code: str = options["asset"]
        xlsx_path: str = options["path"]
        sheet = options["sheet"]
        truncate: bool = options["truncate"]

        asset_obj, _ = CommodityAsset.objects.get_or_create(asset=asset_code)

        df = pd.read_excel(xlsx_path, sheet_name=sheet, engine="openpyxl")

        required_cols = ["Date", "Close/Last", "Volume", "Open", "High", "Low"]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"필수 컬럼 누락: {missing} / 현재 컬럼: {df.columns.tolist()}")

        if truncate:
            CommodityPrice.objects.filter(commodity=asset_obj).delete()

        pre = CommodityPrice.objects.filter(commodity=asset_obj).count()

        objects = []
        for _, row in df.iterrows():
            objects.append(
                CommodityPrice(
                    commodity=asset_obj,
                    date=to_date(row["Date"]),
                    close_last=to_decimal_remove_commas(row["Close/Last"]),
                    volume=to_decimal_remove_commas(row["Volume"]),
                    open=to_decimal_remove_commas(row["Open"]),
                    high=to_decimal_remove_commas(row["High"]),
                    low=to_decimal_remove_commas(row["Low"]),
                )
            )

        # ignore_conflicts=True로 두되, 이제 값이 None이면 위에서 ValueError로 바로 터짐
        CommodityPrice.objects.bulk_create(objects, ignore_conflicts=True)

        post = CommodityPrice.objects.filter(commodity=asset_obj).count()
        self.stdout.write(self.style.SUCCESS(
            f"Import done: asset={asset_code}, rows_in_file={len(objects)}, inserted={post - pre}, total_now={post}"
        ))
