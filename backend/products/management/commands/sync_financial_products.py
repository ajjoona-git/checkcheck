from django.core.management.base import BaseCommand

from products.services.save import sync_all_products


class Command(BaseCommand):
    help = "금융감독원 예·적금 상품 정보를 API로 조회하여 DB에 동기화합니다."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== 예·적금 상품 동기화 시작 ==="))
        sync_all_products()
        self.stdout.write(self.style.SUCCESS("=== 예·적금 상품 동기화 완료 ==="))