# MOATHON (모아톤)

> 모아톤은 추천시스템으로 개인 맞춤 예·적금 상품/옵션을 제안하고, 마라톤처럼 목표 달성까지 꾸준히 달리도록 커뮤니티와 리워드로 완주를 돕는 금융 루틴 서비스입니다.
> 

---

## 1. 팀원 정보 및 역할 분담

### 1.1 역할 분담

| 박준아(팀장) | 정환승(팀원) |
| --- | --- |
| PM, FE, API 연결 | AI, BE, DB |
| - GitHub 관리- 모아톤(게시글) CRUD API 구현- 카카오맵, 유튜브 API 활용한 기능 구현- 프론트엔드 - 백엔드 API 연결- 컴포넌트 아키텍처- 페이지 디자인 | - AI 추천 시스템 구현- 데이터 생성 및 외부 API 연결- ERD- 서버 API 구성- 기획서 및  발표 자료 |

---

## 2. 서비스 주요 기능 설명

### 2.1 금융상품 추천 시스템

- **기능 요약:**
    - 사용자가 입력한 **시작금액(Start amount) · 목표금액(Target amount) · 목표기간(Term_months) · 목적(Purpose)**과 사용자 프로필 정보를 결합해 **개인화 추천**을 수행합니다.
    - **Stage 1 (ML 랭킹)**: 정형·수치 피처 기반으로 추천 가능성이 높은 후보 상품을 **Top-10으로 압축**합니다.
    - **Stage 2 (LLM 의미적 재랭킹)**: 사용자의 목적·성향을 자연어 수준에서 해석해 Top-10 후보를 **적합도 기준으로 재정렬**하고, 최종 **금융상품 1개 + 세부 옵션 1개**를 선택합니다.
    - 최종 결과로 **추천 상품/옵션**과 함께, 선택 근거(요약)를 제공해 **설명 가능한 추천**을 목표로 합니다.
- **사용자 입력:**
    - Target amount : 목표하는 금액
    - Start amount : 초기 투자 가능 금액
    - Term_months : 목표 기간(개월)
    - Purpose : 목적
        - 목돈 마련
        - 단기 여유자금
        - 안정적 자산 보관
        - 저축 습관 형성
        - 이자 극대화
- **추천 결과:** 금융 상품 및 옵션 최종 1개
- **예외 처리:**
    - **LLM 단계 장애 대응 :** LLM 타임아웃·형식 깨짐·응답 실패 시 **규칙 기반 옵션 선택**으로 폴백하여 서비스 중단을 방지

---

### 2.2 모아톤 커뮤니티

- **기능 요약**
    - 사용자가 자신의 **모아톤**을 공유하고, 다른 사용자와 **응원·피드백·상호작용**을 하며 즐거운 저축을 돕는 커뮤니티 기능입니다.
- **주요 화면/기능**
    - **모아톤 CRUD**
        - 모아톤 **작성**: 추천받은 상품/옵션(또는 선택한 상품)을 바탕으로 목표/기간/목적 설정 후 게시
        - 모아톤 **목록 조회**: 전체 모아톤 리스트
        - 모아톤 **상세 조회**: 작성자 정보, 목표/기간/진행률, 선택 상품/옵션, 댓글/좋아요 등 확인
        - 모아톤 **수정/삭제**: 목표/설명 등 일부 항목 수정 및 게시글 삭제
    - **댓글**
        - 댓글 **목록 조회/작성**
        - 댓글 **수정/삭제**
    - **좋아요**
        - 모아톤 **좋아요 등록/취소**
        - 좋아요 수 표시
    - **팔로우**
        - 사용자 **팔로우/언팔로우**
        - 메인 페이지에서 내가 팔로우한 사용자의 모아톤을 확인할 수 있음
- **권한/정책**
    - **로그인 필수**
        - 모아톤 작성/상세 조회/수정/삭제, 댓글 작성/수정/삭제, 좋아요, 팔로우 기능은 **인증된 사용자만** 가능
        - 목록 조회는 비로그인 허용
    - **작성자 권한**
        - 모아톤 **수정/삭제는 작성자만** 허용
        - 댓글 **수정/삭제는 댓글 작성자만** 허용
    - **좋아요 정책**
        - 사용자 1명은 특정 모아톤에 **1회만 좋아요 가능**
        - 중복 좋아요 방지

---

### 2.3 뱃지 리워드

- **기능 요약**
    - 사용자의 행동(모아톤 생성/참여, 커뮤니티 활동 등)에 따라 **뱃지를 지급**하여, 저축 루틴을 **지속·완주**하도록 동기를 부여하는 리워드 시스템입니다.
    - 뱃지는 마이페이지/프로필 등에 노출되어 **성취 기록**이 되고, 커뮤니티 내에서 **사회적 동기(인정/응원)**를 강화합니다.
- **뱃지 종류**
    - **track**
        - 첫 번째 숨 고르기: 모아톤 1/4지점 도달
        - 반환점 터치: 모아톤 절반 도달
        - 막판 스퍼트!: 모아톤 3/4지점 도달
        - 완주 트로피: 모아톤 만기 달성
    - **achieve**
        - 시작이 반: 모아톤 첫 회원가입 시
        - 티끌 모아 태산: 첫 번째 모아톤을 생성 시
        - 작심삼일 탈출: 모아톤을 생성하고 3일 이상 유지
        - 프로 완주러: 모아톤을 3회 이상 완주
        - 억만장자의 꿈: 만기가 36개월 이상인 모아톤 시작
    - **소통·커뮤니티 뱃지**
        - 응원 단장: 좋아요 10회 누르기
        - 소통 요정: 댓글 5회 누적
        - 인기 스타: 모아톤 좋아요 20개 받기
        - 팔로팔로미: 팔로워 10명 달성
- **트리거**
    - **회원가입 시**
    - **로그인 시**
    - **이벤트(모아톤 생성, 좋아요, 팔로우) 발생 시**
- **중복 지급 방지 로직**
    - **DB 레벨 중복 방지**
    - **이벤트 중복 트리거 방지**
    - **동시성 대응**
        - **동시 요청에서도 1회만 지급**되도록 처리

---

## 3. 금융 상품 추천 알고리즘 기술적 설명

### 3.1 전체 구조 개요 (2-Stage)

모아톤 추천은 **ML 기반 후보 압축(Stage 1)** + **LLM 기반 의미 재랭킹(Stage 2)**을 결합한 하이브리드 구조입니다.

핵심 목표는 **(1) 정형 피쳐를 활용해 안정적으로 후보를 좁힌 뒤 (2) 사용자 맥락을 반영해 최종 1개 옵션을 선택**하는 것입니다.

- Stage 1: ML(XGBoost) 기반 랭킹(Top-10 후보 생성)
- Stage 2: LLM(gpt-5-mini) 기반 의미적 재랭킹(최종 1개 옵션 선택 + 설명 생성)

---

### 3.2 Stage 1: ML 랭킹(후보 압축)

### 사용 피처

Stage 1은 **정형화 가능한 특성**을 중심으로 모델 입력을 구성합니다.

- **사용자/목표 기반 피처**
    - 목표 금액/시작 금액
    - 목표 기간
    - 목적(Purpose: GOAL/SHORT/SAFE/HABIT/YIELD)
- **사용자 프로필 피처**
    - 나이/성별/신용등급/자산/연봉/한 달 평균 소비액/리스크 성향
- **상품/옵션 정형 피처**
    - 금리
    - 기간
    - 금리유형(단리/복리)
    - 적립유형(정액적립식/자유적립식)

### 모델

- **XGBoost (XGBClassifier)**
    - 멀티클래스 확률 예측을 활용해 상품을 점수화
    - 출력 확률을 추천 점수로 사용해 **랭킹(정렬) 문제로 변환**

> 대규모 후보군에 대해 모델이 추정한 선택 가능성 점수를 계산하고, 점수가 높은 상품을 Top-10 추천 후보로 선정
> 

### 학습 데이터 구성 방식

- **학습 단위**
    - `user_input + user_features + productoption_features → product_id`
- **라벨 설계**
    - Stage 1은 **상품(Product) 단위 라벨**로 먼저 학습하여 후보군을 만들고,
    - 세부 옵션은 Stage 2에서 “텍스트/맥락”을 반영해 최종 결정
- **데이터 소스**
    - 금융감독원 예·적금 상품/옵션 데이터
    - 사용자 데이터(페이크)

### 추론 파이프라인

1. 사용자 입력값 + 프로필 → **피처 벡터 생성**
2. 각 상품에 대한 (유저,옵션) row를 만들어 점수화
3. 확률 점수 기준으로 내림차순 정렬 → **Top-10 후보 상품** 추출
4. 후보 상품의 옵션을 로딩하여 Stage 2 입력으로 전달

### 평가지표

Stage 1은 정답 1개를 맞추는 정확도보다 **추천 후보군 품질**이 중요하기 때문에 Hit@K 활용

- **Hit@K**: 정답 상품이 Top-K 안에 들어오는 비율 (추천 시스템에서 핵심)
- **Logloss(mlogloss)**: 확률 예측의 안정성 점검용

### 출력

**Top-10 상품 리스트**

---

### 3.3 Stage 2: LLM 의미적 재랭킹(최종 선택)

- **입력**
    - `user`: 사용자 모델로부터 추출한 프로필 요약(dict)
        - `age`, `gender`, `credit_score`, `assets`, `salary`, `average_monthly_spend`, `tender`
    - `goal`: 추천 요청 목표
        - `purpose`, `target_amount`, `start_amount`, `term_months`
        - 파생값: `need_amount = max(target-start, 0)`, `need_per_month = need_amount / term_months`
    - `top10_products`: Stage 1 결과 상위 10개 상품 목록(각 항목에 `product_id` 및 score/prob 포함)
    - `candidates`: Stage 2에서 최종 선택 가능한 **옵션 후보 리스트**
        - Top10 상품 각각에 대해 옵션을 최대 `per_product_candidates(기본 3개)`개로 **사전 단축(shortlist)** 하여 구성
        - 후보 옵션 필드:
            - `option_id`, `product_id`, `save_trm`, `intr_rate`, `intr_rate2`,
            - `intr_rate_type_nm`, `rsrv_type_nm`, `join_deny`
    - `product_texts`: 상품 단위 텍스트/메타 정보
        - `product_name`, `bank_name`, `product_type`, `join_deny`,
        - `spcl_cnd`, `etc_note`, `mtrt_int`
- **프롬프트 구성**
    - 호출 엔드포인트: `GMS_URL`
    - 모델: `gpt-5-mini` (`settings.GMS_MODEL` 미지정 시 기본)
    - 메시지 구성(고정 3개):
        1. **developer**: `Answer in Korean. 반드시 JSON만 출력하고 다른 텍스트는 출력하지 마세요.`
        2. **system**: 아래 `SYSTEM_INSTRUCTIONS`로 역할/제약/우선순위/출력 스키마를 강제
        3. **user**: `payload`를 JSON 문자열로 전달
    - JSON 추출/파싱:
        - 모델이 `json 코드블록` 형태로 응답해도 제거 후 `{...}` 구간만 찾아 파싱
- **의사결정 규칙**
    - **(0) 후보 옵션 사전 단축(LLM 입력 최적화)**
        - Top10의 각 상품에 대해 옵션 전체를 다 넣지 않고, 상품별로 최대 3개만 후보로 올립니다.
        - 단축 기준(정확히 코드 기준):
            - 1순위: `abs(save_trm - term_months)`가 작은 옵션
            - 2순위(tie-break): “우대금리 우선” 점수(`intr_rate2`가 있으면 intr_rate2, 없으면 intr_rate)를 더 높은 옵션
    - **(1) LLM 최종 선택**
        - LLM은 `SYSTEM_INSTRUCTIONS`에 따라:
            - `top10_product_ids` 안에서 `product_id` 선택
            - `candidates` 안에서 `option_id` 1개 선택
            - 우선순위:
                1. 목표 `term_months`와 `save_trm`이 같거나 가장 가까운 옵션
                2. `purpose == YIELD`면 `intr_rate2` 우선(단, 기간이 너무 어긋나면 감점)
                    
                    그 외 목적은 기간 최우선 + 금리 tie-break
                    
                3. `product_texts`의 `spcl_cnd / etc_note / mtrt_int`에서 리스크/제약을 뽑아 `warnings`에 요약
    - **(2) 출력 안정화**
        - `reasons`/`warnings`는 리스트 형태로 강제하고 공백 제거
        - `reasons`가 2개 미만이면 기본 문구로 보정(서비스 품질 및 형식 안정화)
        - `reasons` 최대 5개, `warnings` 최대 4개로 길이 제한
    - **(3) 환각 방지 검증**
        - LLM이 반환한 `product_id`가 Top10에 없거나,
        - `option_id`가 candidates에 없으면
        - **즉시 예외 처리 후 fallback 로직으로 전환**(hallucination 차단)
- **출력**
    - 성공(LLM 정상 선택) 시 `Stage2Output`:
        - `product_id`: 최종 선택 상품 ID
        - `option_id`: 최종 선택 옵션 ID
        - `reasons`: 선택 근거 리스트(최소 2개 보장, 최대 5개)
        - `warnings`: 주의사항 리스트(최대 4개)
        - `used_fallback = False`
    - **Fallback(LLM 실패/형식 오류/검증 실패 등 예외 발생)**
        1. Stage1 1등 상품(`top10_products[0]["product_id"]`)을 `best_pid`로 선택
        2. 해당 상품에서 옵션 1개만 shortlist(기간 근접 + 금리 기준)하여 선택
        3. `reasons`는 “기간 근접성”을 포함해 구성하고, 금리 정보가 있으면 추가
        4. `join_deny` 값이 있으면 가입 제한 경고를 `warnings`에 추가
        5. `used_fallback = True`
        - 만약 이 fallback shortlist조차 비어 있으면, 최후에는 `candidates[0]`을 선택하여 서비스가 끊기지 않도록 처리

---

### 3.4 설계 의사결정 포인트

**왜 2-Stage 구조인가?**

- **성능/비용/지연 최적화**: 전체 상품(수백)·옵션(수천)을 매번 LLM로 평가하면 비용과 응답 시간이 급증합니다. Stage 1(XGBoost)이 **Top-10 상품으로 후보군을 압축**해 LLM 입력 크기와 호출 비용을 안정적으로 통제합니다.
- **역할 분리로 품질 향상**: Stage 1은 정형·수치 피처 기반으로 “선택될 가능성이 높은 후보”를 빠르게 추리고, Stage 2는 **정성 텍스트와 목적 맥락**을 반영해 최종 옵션을 결정합니다.

---

## 4. 생성형 AI 활용 내용 (추천 로직)

GMS의 **gpt-5-mini**를 추천 로직(Stage 2)에 적용해, Stage 1에서 추린 Top-10 후보 중에서 사용자 목표·성향과 상품 텍스트 정보(우대조건/유의사항 등)를 함께 고려하여 **최종 상품·옵션 1개를 선택**하고, 선택 이유와 주의사항을 **구조화된 JSON 형태**로 반환하도록 구성했습니다.

---

## 5. 소감

---

## 6. 프로젝트 실행하는 방법

### frontend/.env.local

```
VITE_API_URL='http://127.0.0.1:8000'

VITE_YOUTUBE_API_KEY=''
VITE_YOUTUBE_API_URL='https://www.googleapis.com/youtube/v3'

VITE_KAKAO_API_KEY=''

```

### backend/.env

```bash
DJANGO_SECRET_KEY=""

# 개발 환경에서는 True
# 운영 환경에서는 반드시 False
DJANGO_DEBUG=True

# 금감원 api
FSS_API_KEY=

EMAIL_HOST_USER=ajjoona@gmail.com
EMAIL_HOST_PASSWORD=

# GMS_KEY
GMS_KEY=

```

---

## 프론트엔드 (Vue.js) 초기 설정

### 서버 실행

```bash
cd ../frontend
npm install
npm run dev
```

---

## 백엔드 (Django) 초기 설정

### 가상환경 설정

```bash
cd ../backend
python -m venv venv
source venv/Script/activate
pip install -r requirements.txt
```

### DB 설정(데이터 적재)

```bash
python manage.py makemigrations
python manage.py migrate

# 금융상품 데이터
python manage.py sync_financial_products

# 페이크 유저
python manage.py seed_fake_users_moathon --users 30 --moathons 100 --seed 42

# 금/은 데이터
python manage.py import_commodity --asset silver --path data/Silver_prices.xlsx
python manage.py import_commodity --asset gold --path data/Gold_prices.xlsx

# 뱃지 데이터
python manage.py loaddata accounts/badge.json

# 댓글 팔로우 좋아요 뱃지
python manage.py loaddata accounts/accounts_social.json
python manage.py loaddata challenges/challenges_social.json
```

### 서버 실행

```bash
python manage.py runserver
```