import random
from collections import defaultdict
from datetime import timedelta, date

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone

from faker import Faker

from accounts.models import User, Moathon
from products.models import ProductOption


def clamp_int(x: float, lo: int, hi: int) -> int:
    return int(max(lo, min(hi, round(x))))


class Command(BaseCommand):
    help = "Seed fake Users and Moathon rows (real ProductOption ids only)."

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=20000)
        parser.add_argument("--moathons", type=int, default=40000)
        parser.add_argument("--seed", type=int, default=42)
        parser.add_argument("--password", type=str, default="fakePw!234")  # 로그인 안 할 거라서 동일비번으로 만듬 

    def handle(self, *args, **opts):
        n_users = opts["users"]
        n_moathons = opts["moathons"]
        seed = opts["seed"]
        password = opts["password"]

        random.seed(seed)
        faker = Faker("ko_KR")
        Faker.seed(seed)

        # 1) ProductOption 로드 (실제 존재 id만 사용하기 위해서)
        options = list(
            ProductOption.objects.select_related("product", "product__bank").all()
        )
        if not options:
            self.stdout.write(self.style.ERROR("ProductOption 데이터가 없습니다. 먼저 금융상품 데이터를 적재하세요."))
            return
        
        # 금리 대표값(옵션 선택 편향/상품 인기도 계산에 사용)
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

        # 상품 단위 인기도 가중치 생성
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

        # 쏠림 강도(값이 클수록 상위 상품/은행에 더 몰림)
        ALPHA_PROD = 1.25    # 상품 쏠림 (1.15~1.35 추천)
        ALPHA_BANK = 1.05    # 은행 쏠림 (약하게)
        BANK_EFFECT = 0.25   # 은행 선호 영향 (0~1, 0.2~0.35 추천)

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
        used_nickname = set()

        def unique_nickname(i: int) -> str:
            # seed 마커를 앞에 붙여서 이번 시드로 만든 유저를 식별 가능하게 함
            # 예: seed42_nick12345678
            return f"seed{seed}_nick{random.randint(10_000_000, 99_999_999)}_{i}"

        # 나이 분포: 20~30대 위주 + 40~50대 일부
        def sample_birth_date():
            # 가중치: 20s 45%, 30s 35%, 40s 15%, 50s 5%
            decade = random.choices([20, 30, 40, 50], weights=[45, 35, 15, 5])[0]
            age = random.randint(decade, decade + 9)
            # 오늘 기준 역산
            today = timezone.now().date()
            year = today.year - age
            # 날짜는 faker로 생성하되 연도만 맞춤
            d = faker.date_of_birth(minimum_age=age, maximum_age=age)
            return d.replace(year=year)

        # 신용점수: 500~950, 평균 800 근처
        def sample_credit_score():
            return clamp_int(random.gauss(800, 70), 500, 950)

        # 연봉(원): 평균 4,500만 근처 (폭 넓게)
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
            username = f"fake_{seed}_{i}"  # 유니크 보장
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

                    nickname=unique_nickname(i),
                    birth=birth,
                    gender=random.choice(gender_choices),
                    credit_score=credit,
                    assets=assets,                      # 원
                    salary=salary,                      # 원
                    average_monthly_spend=spend,         # 원
                    tender=tender,
                )
            )

        with transaction.atomic():
            User.objects.bulk_create(users, batch_size=2000)

        # 방금 만든 유저만 다시 로드(필요 필드만)
        user_rows = list(
            User.objects
            .filter(nickname__startswith=f"seed{seed}_nick")
            .values("id", "salary", "assets", "average_monthly_spend")
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
            salary = int(user_row["salary"] or 0)
            assets = int(user_row["assets"] or 0)
            spend = int(user_row["average_monthly_spend"] or 0)

            monthly_income = salary / 12 if salary else 0
            monthly_saving = max(0, monthly_income - spend) * random.uniform(0.5, 0.9)

            r = option_rate(opt) / 100.0
            max_limit = opt.product.max_limit  # 원(가정)

            if ptype == "DEPOSIT":
                start = int(assets * random.uniform(0.10, 0.70)) if assets > 0 else random.randint(3_000_000, 30_000_000)
                expected = int(start * r * (term / 12))
                target = start + max(50_000, expected)
                if purpose == "SAFE":
                    target = int(start * random.uniform(1.00, 1.03))
            else:
                start = int(assets * random.uniform(0.00, 0.10)) if assets > 0 else 0
                monthly = int(max(100_000, monthly_saving))
                monthly = min(monthly, 3_000_000)
                target = start + monthly * term
                if purpose == "GOAL":
                    target = int(target * random.uniform(1.05, 1.25))
                if purpose == "HABIT":
                    target = int(target * random.uniform(0.95, 1.05))

            if max_limit:
                start = min(start, max_limit)
                target = min(target, max_limit)

            if target < start:
                target = start
            return start, target

        # 타이틀: 30% 커스텀, 70% user's moathon
        custom_titles = {
            "GOAL": ["결혼자금", "내집마련", "이사자금", "차량구입", "유학준비"],
            "SHORT": ["비상금", "단기여유자금", "여행모아톤", "이벤트자금"],
            "SAFE": ["안전자산", "현금보관", "예비자금", "원금보장"],
            "HABIT": ["저축습관", "월급루틴", "자동저축", "한달저축"],
            "YIELD": ["이자극대화", "우대금리도전", "금리챙기기"],
        }

        def next_users_moathon_title(used_titles: set):
            base = "user's moathon"
            if base not in used_titles:
                return base
            max_n = 1
            for t in used_titles:
                if t == base:
                    max_n = max(max_n, 1)
                elif t.startswith(base):
                    suf = t[len(base):]
                    if suf.isdigit():
                        max_n = max(max_n, int(suf))
            return f"{base}{max_n + 1}"

        # 5) Moathon bulk 생성 (save() 미호출이므로 title, end_date 직접 생성)
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

                if random.random() < 0.30:
                    base_title = random.choice(custom_titles[purpose])
                    title = base_title
                    n = 2
                    while title in used_titles:
                        title = f"{base_title}{n}"
                        n += 1
                else:
                    title = next_users_moathon_title(used_titles)

                used_titles.add(title)
                calc_end_date = today + timedelta(days=term * 30)

                moathons.append(
                    Moathon(
                        user_id=urow["id"],
                        product_option_id=opt.id,  # 반드시 DB에 존재하는 ProductOption id
                        title=title,
                        start_amount=start_amt,
                        target_amount=target_amt,
                        term_months=term,
                        purpose=purpose,
                        end_date=calc_end_date,
                    )
                )

        with transaction.atomic():
            Moathon.objects.bulk_create(moathons, batch_size=3000)

        self.stdout.write(self.style.SUCCESS(f"Moathons created: {len(moathons)}"))
        self.stdout.write(self.style.SUCCESS("Done."))