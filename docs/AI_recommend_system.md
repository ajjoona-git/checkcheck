## 1. 금융 상품 추천 알고리즘 기술적 설명

### 1.1 전체 구조 개요 (2-Stage)

모아톤 추천은 **ML 기반 후보 압축(Stage 1)** + **LLM 기반 의미 재랭킹(Stage 2)**을 결합한 하이브리드 구조입니다.

핵심 목표는 **(1) 정형 피쳐를 활용해 안정적으로 후보를 좁힌 뒤 (2) 사용자 맥락을 반영해 최종 1개 옵션을 선택**하는 것입니다.

- Stage 1: ML(XGBoost) 기반 랭킹(Top-10 후보 생성)
- Stage 2: LLM(gpt-5-mini) 기반 의미적 재랭킹(최종 1개 옵션 선택 + 설명 생성)

---

### 1.2 Stage 1: ML 랭킹(후보 압축)

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

### 1.3 Stage 2: LLM 의미적 재랭킹(최종 선택)

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

### 1.4 설계 의사결정 포인트

**왜 2-Stage 구조인가?**

- **성능/비용/지연 최적화**: 전체 상품(수백)·옵션(수천)을 매번 LLM로 평가하면 비용과 응답 시간이 급증합니다. Stage 1(XGBoost)이 **Top-10 상품으로 후보군을 압축**해 LLM 입력 크기와 호출 비용을 안정적으로 통제합니다.
- **역할 분리로 품질 향상**: Stage 1은 정형·수치 피처 기반으로 “선택될 가능성이 높은 후보”를 빠르게 추리고, Stage 2는 **정성 텍스트와 목적 맥락**을 반영해 최종 옵션을 결정합니다.

---

## 2. 생성형 AI 활용 내용 (추천 로직)

GMS의 **gpt-5-mini**를 추천 로직(Stage 2)에 적용해, Stage 1에서 추린 Top-10 후보 중에서 사용자 목표·성향과 상품 텍스트 정보(우대조건/유의사항 등)를 함께 고려하여 **최종 상품·옵션 1개를 선택**하고, 선택 이유와 주의사항을 **구조화된 JSON 형태**로 반환하도록 구성했습니다.
