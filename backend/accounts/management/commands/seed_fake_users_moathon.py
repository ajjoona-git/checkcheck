import random
from collections import defaultdict
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone
from faker import Faker
from accounts.models import User
from challenges.models import Moathon
from products.models import ProductOption

# 하한과 상한을 기반으로 데이터 품질, 현실성 반영
def clamp_int(x: float, lo: int, hi: int) -> int:
    return int(max(lo, min(hi, round(x))))


class Command(BaseCommand):
    help = "Seed fake Users and Moathon rows (real ProductOption ids only)."

    # 명령어 실행시 옵션
    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=20000)
        parser.add_argument("--moathons", type=int, default=40000)
        parser.add_argument("--seed", type=int, default=42)
        parser.add_argument("--password", type=str, default="fakePw!234")  # 로그인 안 할 거라서 동일비번으로 만듦

    # 실제 실행 로직
    def handle(self, *args, **opts):
        n_users = opts["users"]
        n_moathons = opts["moathons"]
        seed = opts["seed"]
        password = opts["password"]

        random.seed(seed)
        faker = Faker("ko_KR")
        Faker.seed(seed)

        # 1) ProductOption 로드 (실제 존재 id만 사용)
        options = list(
            ProductOption.objects.select_related("product", "product__bank").all()
        )
        if not options:
            self.stdout.write(self.style.ERROR("ProductOption 데이터가 없습니다. 먼저 금융상품 데이터를 적재하세요."))
            return

        # 옵션을 비교할 때 최고 우대금리 존재하면 최고 우대금리 아니면 기본 금리
        def option_rate(opt: ProductOption) -> float:
            v = opt.intr_rate2 if opt.intr_rate2 is not None else opt.intr_rate
            try:
                return float(v or 0.0)
            except Exception:
                return 0.0

        # 타입/기간 인덱싱 (기간은 save_trm에서 int 파싱 가능한 것만)
        by_type = {"DEPOSIT": [], "SAVING": []}
        by_type_term = {"DEPOSIT": defaultdict(list), "SAVING": defaultdict(list)}

        for o in options:
            ptype = o.product.product_type
            if ptype not in by_type:
                continue
            by_type[ptype].append(o)
            try:
                term = int(str(o.save_trm).strip())
            except ValueError:
                continue
            by_type_term[ptype][term].append(o)

        if not by_type["DEPOSIT"] and not by_type["SAVING"]:
            self.stdout.write(self.style.ERROR("DEPOSIT/SAVING 타입의 ProductOption을 찾지 못했습니다."))
            return

        # 옵션을 상품 기준으로 모아두는 인덱스(상품을 고르고 -> 존재하는 옵션 고르기 위함)
        opts_by_product = defaultdict(list)
        opts_by_product_term = defaultdict(lambda: defaultdict(list))
        product_best_rate = defaultdict(float)  # 상품별 대표 금리(최고금리)
        product_type = {}
        product_bank = {}

        for o in options:
            pid = o.product_id
            p = o.product
            ptype = p.product_type
            if ptype not in ("DEPOSIT", "SAVING"):
                continue

            product_type[pid] = ptype
            product_bank[pid] = p.bank_id

            r = option_rate(o)
            if r > product_best_rate[pid]:
                product_best_rate[pid] = r

            opts_by_product[pid].append(o)
            try:
                term = int(str(o.save_trm).strip())
                opts_by_product_term[pid][term].append(o)
            except ValueError:
                pass

        # 특정 상품, 은행으로 가입이 몰리는 현상 반영 (숫자가 클수록 쏠림 커짐)
        ALPHA_PROD = 1.25    # 상품 쏠림
        ALPHA_BANK = 1.05    # 은행 쏠림
        BANK_EFFECT = 0.25   # 은행 선호 영향

        bank_ids = sorted(set(product_bank.values()))
        bank_weight = {bid: 1.0 / ((i + 1) ** ALPHA_BANK) for i, bid in enumerate(bank_ids, start=0)}

        product_weight = {}
        for ptype in ("DEPOSIT", "SAVING"):
            pids = [pid for pid, t in product_type.items() if t == ptype]
            # 대표금리 높은 상품일수록 랭크 상위
            pids.sort(key=lambda pid: product_best_rate[pid], reverse=True)

            for rank, pid in enumerate(pids, start=1):
                w = 1.0 / (rank ** ALPHA_PROD)
                bw = bank_weight.get(product_bank.get(pid), 1.0)
                w *= (bw ** BANK_EFFECT)
                product_weight[pid] = w

        products_by_type = {"DEPOSIT": [], "SAVING": []}
        products_by_type_term = {"DEPOSIT": defaultdict(list), "SAVING": defaultdict(list)}

        for pid in product_weight.keys():
            ptype = product_type.get(pid)
            if ptype not in products_by_type:
                continue
            products_by_type[ptype].append(pid)
            for term in opts_by_product_term[pid].keys():
                products_by_type_term[ptype][term].append(pid)

        # 2) User 생성
        users = []

        # 닉네임 유니크 보장
        def unique_nickname(email: str) -> str:
            local = (email or "").split("@", 1)[0].strip().lower()
            base = local or "user"
            nickname = base
            suffix = 2
            while User.objects.filter(nickname=nickname).exists():
                nickname = f"{base}_{suffix}"
                suffix += 1
            return nickname

        # 나이 분포: 20~30대 위주 + 40~50대 일부
        def sample_birth_date():
            decade = random.choices([20, 30, 40, 50], weights=[45, 35, 15, 5])[0]
            age = random.randint(decade, decade + 9)
            today = timezone.now().date()
            year = today.year - age
            # 날짜는 faker로 생성하되 연도만 맞춤
            d = faker.date_of_birth(minimum_age=age, maximum_age=age)
            return d.replace(year=year)

        # 신용점수: 500~950, 평균 800 근처
        def sample_credit_score():
            return clamp_int(random.gauss(800, 70), 500, 950)

        # 연봉(원): 평균 4,500만 근처
        def sample_salary_won():
            return clamp_int(random.gauss(45_000_000, 18_000_000), 18_000_000, 150_000_000)

        # 자산(원): 0~6억 정도 중심 + 꼬리
        def sample_assets_won():
            v = abs(random.gauss(60_000_000, 90_000_000))
            return clamp_int(v, 0, 1_500_000_000)  # 상한 15억

        # 월 지출(원): 월소득의 30~65% 정도 + 노이즈
        def sample_spend_won(salary_won: int, assets_won: int):
            monthly_income = salary_won / 12
            base = monthly_income * random.uniform(0.30, 0.65)
            # 자산 낮으면 지출 여력 낮게
            if assets_won < 10_000_000:
                base *= random.uniform(0.90, 1.05)
            return clamp_int(random.gauss(base, 250_000), 300_000, 8_000_000)

        # 투자성향: 신용/자산 높을수록 공격적 약간 증가
        tender_choices = ["1", "2", "3", "4", "5"]
        def sample_tender(credit: int, assets_won: int):
            if credit >= 830 or assets_won >= 200_000_000:
                return random.choices(tender_choices, weights=[5, 15, 35, 30, 15])[0]
            return random.choices(tender_choices, weights=[20, 30, 35, 12, 3])[0]

        gender_choices = ["0", "1"]

        # “진짜 유저처럼” 보이게: 이름/이메일/username 채움
        hashed_pw = make_password(password)
        now = timezone.now()

        used_usernames = set(
            User.objects.values_list("username", flat=True)
        )

        for i in range(n_users):
            username = f"fake_{seed}_{i}"
            first = faker.first_name()
            last = faker.last_name()
            base_username = f"{last}{first}"   # 김순옥

            # username 중복 방지: 김순옥, 김순옥2, 김순옥3 ...
            username = base_username
            n = 2
            while username in used_usernames:
                username = f"{base_username}{n}"
                n += 1
            used_usernames.add(username)

            email = faker.free_email()
            birth = sample_birth_date()

            salary = sample_salary_won()
            assets = sample_assets_won()
            credit = sample_credit_score()
            spend = sample_spend_won(salary, assets)
            tender = sample_tender(credit, assets)

            # date_joined도 그럴듯하게 과거로 분산
            joined = now - timedelta(days=random.randint(0, 365 * 3))

            users.append(
                User(
                    username=username,
                    email=email,
                    password=hashed_pw,
                    is_active=True,
                    is_staff=False,
                    is_superuser=False,
                    date_joined=joined,

                    nickname=unique_nickname(email),
                    birth=birth,
                    gender=random.choice(gender_choices),
                    credit_score=credit,
                    assets=assets,                      # 원
                    salary=salary,                      # 원
                    average_monthly_spend=spend,        # 원
                    tender=tender,
                )
            )
        last_id = User.objects.order_by("-id").values_list("id", flat=True).first() or 0

        with transaction.atomic():
            User.objects.bulk_create(users, batch_size=2000)

        # 방금 만든 유저만 다시 로드(필요 필드만)
        user_rows = list(
            User.objects
            .filter(id__gt=last_id)
            .values("id", "nickname", "salary", "assets", "average_monthly_spend")
        )
        self.stdout.write(self.style.SUCCESS(f"Users created: {len(user_rows)}"))

        # 3) 유저별 Moathon 개수 분포 → 총 moathons 맞춤
        # 1~5개 분포: 평균 2개 근처
        weights = {1: 35, 2: 45, 3: 12, 4: 6, 5: 2}
        counts = [random.choices(list(weights.keys()), weights=list(weights.values()))[0] for _ in range(n_users)]
        total = sum(counts)

        idxs = list(range(n_users))
        random.shuffle(idxs)
        ptr = 0
        while total > n_moathons:
            i = idxs[ptr % n_users]
            if counts[i] > 1:
                counts[i] -= 1
                total -= 1
            ptr += 1
        while total < n_moathons:
            i = idxs[ptr % n_users]
            if counts[i] < 5:
                counts[i] += 1
                total += 1
            ptr += 1

        # 4) Moathon 생성 규칙 (목적/타입/기간/옵션/금액)
        PURPOSES = ["GOAL", "SHORT", "SAFE", "HABIT", "YIELD"]
        # 목적 분포: GOAL 40%, YIELD 5%, 나머지 균등
        PURPOSE_WEIGHTS = [40, 55/3, 55/3, 55/3, 5]

        def choose_purpose():
            return random.choices(PURPOSES, weights=PURPOSE_WEIGHTS)[0]

        def choose_product_type(purpose: str):
            # 목적 기반 타입 선호(현실감)
            if purpose == "YIELD":
                return random.choices(["DEPOSIT", "SAVING"], weights=[90, 10])[0]
            if purpose == "SAFE":
                return random.choices(["DEPOSIT", "SAVING"], weights=[75, 25])[0]
            if purpose == "GOAL":
                return random.choices(["SAVING", "DEPOSIT"], weights=[75, 25])[0]
            if purpose == "HABIT":
                return random.choices(["SAVING", "DEPOSIT"], weights=[85, 15])[0]
            # SHORT
            return random.choices(["DEPOSIT", "SAVING"], weights=[55, 45])[0]


        def sample_term_months(ptype: str):
            available_terms = list(by_type_term[ptype].keys())
            if not available_terms:
                return 12
            popular = [6, 12, 24, 36]
            candidates = [t for t in popular if t in available_terms]
            if candidates:
                w_map = {6: 20, 12: 45, 24: 25, 36: 10}
                w = [w_map[t] for t in candidates]
                return random.choices(candidates, weights=w)[0]
            return random.choice(available_terms)

        def pick_option(ptype: str, term: int, purpose: str, used_option_ids: set):
            prod_pool = products_by_type_term[ptype].get(term) or products_by_type[ptype]
            if not prod_pool:
                pool = by_type_term[ptype].get(term) or by_type[ptype]
                opt = random.choice(pool)
                used_option_ids.add(opt.id)
                return opt

            weights_ = [product_weight.get(pid, 1.0) for pid in prod_pool]
            pid = random.choices(prod_pool, weights=weights_, k=1)[0]

            cand = opts_by_product_term[pid].get(term) or opts_by_product[pid]

            cand2 = [o for o in cand if o.id not in used_option_ids]
            if cand2:
                cand = cand2

            if purpose == "YIELD":
                cand = sorted(cand, key=option_rate, reverse=True)
                top = cand[: max(10, len(cand) // 10)]  # 상위 10% 또는 최소 10개
                opt = random.choice(top)
            else:
                opt = random.choice(cand)

            used_option_ids.add(opt.id)
            return opt

        def amounts_for(user_row: dict, opt: ProductOption, ptype: str, purpose: str, term: int):
            import math

            salary = int(user_row.get("salary") or 0)
            assets = int(user_row.get("assets") or 0)
            spend  = int(user_row.get("average_monthly_spend") or 0)

            monthly_income = salary / 12 if salary else 0.0
            disposable = max(0.0, monthly_income - spend)  # 월 가처분

            r = option_rate(opt) / 100.0  # 연 이율
            max_limit = opt.product.max_limit
            if max_limit is not None:
                try:
                    max_limit = int(max_limit)
                    if max_limit <= 0:
                        max_limit = None
                except Exception:
                    max_limit = None

            # 목적별 목표 “도전 정도” (너무 뻥튀기 방지)
            goal_factor = {
                "SAFE":  (0.98, 1.02),
                "SHORT": (0.98, 1.05),
                "HABIT": (0.97, 1.04),
                "GOAL":  (1.00, 1.10),
                "YIELD": (1.00, 1.06),
            }
            lo_f, hi_f = goal_factor.get(purpose, (1.0, 1.0))
            f = random.uniform(lo_f, hi_f)

            # 반올림/올림 유틸
            def round_to(x: int, base: int) -> int:
                return int(round(x / base) * base)

            def ceil_to(x: int, base: int) -> int:
                return int(math.ceil(x / base) * base)

            # ----- 금액 생성 -----
            if ptype == "DEPOSIT":
                hi = assets if assets > 0 else 30_000_000
                if max_limit is not None:
                    hi = min(hi, max_limit)

                lo = 1_000_000 if hi >= 1_000_000 else max(0, hi)

                # hi가 lo보다 작아지는 극단 케이스 방지
                if hi < lo:
                    hi = lo

                start = int(random.uniform(lo, max(lo, hi * 0.7)))  # 자산/한도 기반

                expected = start * (1 + r * (term / 12))            # (단순) 만기 예상
                target = int(expected * f)

                # 너무 비슷하면 최소 증가폭 보장 (절대값 + 비율 혼합)
                min_gain = max(50_000, int(start * 0.002))
                target = max(target, start + min_gain)

            else:  # SAVING
                # 월납입: 가처분 기반 (최저 5만) + 상한 300만
                monthly = int(min(disposable * random.uniform(0.25, 0.8), 3_000_000))
                monthly = max(50_000, monthly)

                # start(목돈): 기존 monthly*6 캡은 0~30만 쏠림이 심함 → assets 기반으로 별도 샘플링
                if assets > 0:
                    start = int(assets * random.uniform(0.0, 0.08))  # 0~8% 정도
                    start = min(start, 30_000_000)                   # 과도 방지
                else:
                    start = 0

                # 한도 처리: monthly=0 되는 버그성 케이스 방지
                if max_limit is not None:
                    # start + monthly*term <= max_limit 만족하도록 start를 먼저 줄임
                    max_start = max(0, max_limit - monthly * term)
                    start = min(start, max_start)

                    # room이 부족해서 monthly_cap이 0이 될 상황이면 start를 더 줄여 room 확보
                    room = max(0, max_limit - start)
                    monthly_cap = room // max(1, term)

                    if monthly_cap < 50_000:
                        # 최소 월납입 5만을 확보하도록 start를 재조정
                        start = max(0, max_limit - 50_000 * term)
                        room = max(0, max_limit - start)
                        monthly_cap = room // max(1, term)

                    monthly = min(monthly, monthly_cap)
                    monthly = max(50_000, monthly)  # 최종 0 방지

                principal = start + monthly * term
                avg_balance = start + monthly * (term - 1) / 2
                interest = avg_balance * r * (term / 12)
                expected = principal + interest

                target = int(expected * f)
                target = min(target, int(expected * 1.12))

                # 핵심: 1%만 두면 1만원 반올림에서 증가분이 사라짐 → 절대 최소 증가폭 보장
                min_gain = max(20_000, int(principal * 0.01))  # 최소 2만원 또는 1%
                target = max(target, principal + min_gain)

            # ----- 최종 정리(반올림/한도/안전장치) -----
            # start는 반올림, target은 올림(증가분 소실 방지)
            start = round_to(start, 10_000)
            target = ceil_to(target, 10_000)

            if max_limit is not None:
                start = min(start, max_limit)
                target = min(target, max_limit)

            # 최후 안전장치: target이 start보다 작거나 같으면 +1만원 시도
            if target <= start:
                if max_limit is None:
                    target = start + 10_000
                else:
                    target = min(max_limit, start + 10_000)
                    # max_limit이 start와 같아 올릴 수 없는 경우는 그대로 둠(상품 한도 때문)

            return start, target

        # 타이틀: 80% 커스텀, 20% user's moathon
        custom_titles = {
            "GOAL": [
                "결혼자금", "신혼여행 자금", "예식비용", "혼수마련", "청첩장 비용",
                "내집마련", "청약통장 플랜", "전세자금", "보증금 모으기", "주택자금",
                "이사자금", "이사비용", "인테리어 자금", "가구·가전 구입", "리모델링 자금",
                "차량 구입", "첫 차 마련", "중고차 자금", "자동차 계약금", "면허·보험 준비",
                "유학 준비", "어학연수", "학비 모으기", "등록금 플랜", "교환학생 준비",
                "창업자금", "사업 시드", "장비 구입비", "초기 운영 자금", "스몰비즈플랜",
                "자격증 비용", "시험준비비", "수강료 모으기", "부트캠프 등록금", "커리어 업그레이드",
                "부모님 선물", "가족여행 자금", "효도여행", "기념일 선물", "집들이 선물",
                "출산 준비", "육아용품", "산후조리원", "가정 보험 준비", "가족 확장 플랜",
            ],
            "SHORT": [
                "비상금", "생활비 버퍼", "급전 대비", "돌발지출 대비", "긴급 예산",
                "단기 여유자금", "월말방어", "주말소비통제", "소확행예산", "이번달 여유",
                "여행 모아톤", "항공권 모으기", "숙소비용", "맛집투어 자금", "휴가 비용",
                "이벤트 자금", "생일선물비", "기념일 데이트", "연말모임비", "경조사비",
                "의료비 예비", "치과 비용", "검진 비용", "약값 모으기", "병원비 버퍼",
                "수리 비용", "차량 수리비", "핸드폰 교체비", "가전수리비", "집 수리 예산",
                "취미 예산", "운동 등록비", "레슨비용", "덕질 예산", "공연·전시 예산",
                "이직 준비", "면접 정장비", "포트폴리오비", "취업준비비", "이직 버퍼",
            ],
            "SAFE": [
                "안전자산", "현금 보관", "현금 쿠션", "원금 보장", "무위험보관",
                "예비자금", "생활 안정 자금", "가계안전망", "리스크 제로", "안정 플랜",
                "목돈 보관", "대기 자금", "잠깐 보관", "현금파킹", "대기 예치",
                "비상금 플랜", "긴급 자금 통장", "안전통장", "세이프박스", "마음안정 통장",
                "가족 안전망", "부모님 비상금", "아이 교육 예비", "가정 안정 자금", "가족 쿠션",
                "보험료 대비", "연납 보험료", "자동 이체 버퍼", "고정비 방어", "지출 안정화",
                "환율 변동 대비", "해외 결제 대비", "여행 비상금", "비상 현금", "예비 달러",
            ],
            "HABIT": [
                "저축 습관", "월급루틴", "자동저축", "한달저축", "매일저축",
                "1일 1저축", "주간저축", "월간저축", "루틴챌린지", "습관만들기",
                "라떼값 저축", "커피값 모으기", "배달비 절약", "소비줄이기", "지출다이어트",
                "선저축 후소비", "통장 쪼개기", "용돈관리", "가계부 루틴", "소비통제",
                "적금루틴", "자동이체 습관", "만기까지 버티기", "완주챌린지", "꾸준함 훈련",
                "월급날 저축", "주급저축", "잔돈모으기", "잔액저축", "남는돈 저축",
                "노플렉스 챌린지", "무지출데이", "지출리셋", "소비리셋", "절약모드",
            ],
            "YIELD": [
                "이자극대화", "우대금리 도전", "금리 챙기기", "이자 수확", "금리사냥",
                "고금리플랜", "금리상승 기대", "최고금리찾기", "우대조건 올클", "금리최적화",
                "복리의 마법", "이자 재투자", "이자불리기", "수익률 루틴", "수익챌린지",
                "만기이자 극대화", "우대금리 모으기", "조건충족플랜", "월별 우대 달성", "혜택 풀세팅",
                "금리비교", "상품 갈아타기", "리밸런싱", "금리런", "고금리 환승",
                "단리vs복리", "복리우선", "이자 계산 습관", "우대체크", "금리체크",
                "파킹+적금", "파킹 최적화", "예치전략", "분산예치", "금리분산",
            ],
        }

        def next_users_moathon_title(nickname: str, used_titles: set):
            nick = (nickname or "user").strip()
            base = f"{nick}'s moathon"

            if base not in used_titles:
                return base

            n = 2
            while f"{base}{n}" in used_titles:
                n += 1
            return f"{base}{n}"

        # 5) Moathon bulk 생성 (save() 미호출이므로 title, start_date, end_date 직접 생성)
        moathons = []
        today = timezone.now().date()
        for urow, k in zip(user_rows, counts):
            used_option_ids = set()
            used_titles = set()

            for _ in range(k):
                purpose = choose_purpose()
                ptype = choose_product_type(purpose)
                term = sample_term_months(ptype)

                opt = pick_option(ptype, term, purpose, used_option_ids)
                start_amt, target_amt = amounts_for(urow, opt, ptype, purpose, term)

                if random.random() < 0.80:
                    base_title = random.choice(custom_titles[purpose])
                    title = base_title
                    n = 2
                    while title in used_titles:
                        title = f"{base_title}{n}"
                        n += 1
                else:
                    title = next_users_moathon_title(urow["nickname"], used_titles)

                used_titles.add(title)

                days_ago = random.randint(0, 365) # 0일(오늘) ~ 365일 전 사이
                rand_start_date = today - timedelta(days=days_ago)
                calc_end_date = rand_start_date + timedelta(days=term * 30)

                moathons.append(
                    Moathon(
                        user_id=urow["id"],
                        product_option_id=opt.id,  # 반드시 DB에 존재하는 ProductOption id
                        title=title,
                        start_amount=start_amt,
                        target_amount=target_amt,
                        term_months=term,
                        purpose=purpose,
                        start_date=rand_start_date, # 랜덤 시작일
                        end_date=calc_end_date,     # 시작일 기준 종료일
                    )
                )

        with transaction.atomic():
            Moathon.objects.bulk_create(moathons, batch_size=3000)

        self.stdout.write(self.style.SUCCESS(f"Moathons created: {len(moathons)}"))
        self.stdout.write(self.style.SUCCESS("Done."))