# MOATHON (모아톤): 함께 완주하는 저축 마라톤

### *"고르는 스트레스는 줄이고, 달리는 재미는 더하고"*

모아톤은 개인 맞춤형 예·적금 상품을 AI로 추천하고, 마라톤처럼 목표 달성까지 커뮤니티와 리워드를 통해 완주를 돕는 **금융 루틴 서비스**입니다. 단순히 상품을 가입하는 것을 넘어, 사용자가 설정한 저축 목표를 끝까지 달성할 수 있도록 돕는 **페이스메이커** 역할을 지향합니다.

## 기술 스택 (Tech Stack)

### Frontend
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-FFE162?style=for-the-badge&logo=pinia&logoColor=black)
![Bootstrap](https://img.shields.io/badge/Bootstrap5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![GSAP](https://img.shields.io/badge/GSAP-88CE02?style=for-the-badge&logo=greensock&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white)

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-A30000?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

### AI & Data
![Scikit-Learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

### External APIs
![KakaoMap](https://img.shields.io/badge/Kakao_Map_API-FFCD00?style=for-the-badge&logo=kakao&logoColor=black)
![Youtube](https://img.shields.io/badge/Youtube_Data_API-FF0000?style=for-the-badge&logo=youtube&logoColor=white)
![FSS](https://img.shields.io/badge/Financial_Supervisory_Service-1D4F91?style=for-the-badge&logo=bank&logoColor=white)

### Collaboration & Tools
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)

<br><br>

## 서비스 아키텍처

**Vue3 Composition API**와 **Django REST Framework**를 활용하여 **RESTful API** 기반으로 서비스를 구축했습니다. 특히 AI 추천 시스템을 백엔드 로직에 통합하여 실시간으로 개인화된 상품을 제안하도록 설계했습니다.

![시스템 아키텍처](./docs/diagrams/system-architecture.png)

<br><br>

## 주요 기능 시연 (Service Demo)

<p align="center">
  <a href="https://d314hr75zv7jjv.cloudfront.net/" target="_blank">
    <img src="https://img.shields.io/badge/🚀%20Live%20Service-바로가기-4CAF50?style=for-the-badge" />
  </a>
</p>

### 1. 시작 및 온보딩 (Onboarding)
사용자에게 첫인상을 주는 랜딩 페이지와 회원가입, 그리고 초기 데이터를 수집하는 온보딩 과정입니다.

| Landing Page | Signup | Onboarding |
| :---: | :---: | :---: |
| <img src="./docs/result_gifs/Landing.gif" width="250" /> | <img src="./docs/result_gifs/SignUp.gif" width="250" /> | <img src="./docs/result_gifs/Onboarding.gif" width="250" /> |
| **서비스 소개 및 진입** | **회원가입** | **초기 투자 성향/목표 설정** |

<br>

### 2. AI 상품 추천 및 모아톤 생성 (AI Recommend)
사용자의 프로필과 목표를 기반으로 AI가 최적의 상품을 추천하고, 이를 바탕으로 '모아톤(저축 챌린지)'을 생성합니다.

| AI Recommendation | Moathon Create | Moathon Update |
| :---: | :---: | :---: |
| <img src="./docs/result_gifs/MoathonRecommend.gif" width="250" /> | <img src="./docs/result_gifs/Recommend-MoathonCreate.gif" width="250" /> | <img src="./docs/result_gifs/MoathonUpdate.gif" width="250" /> |
| **목표 설정 및 AI 맞춤 상품 추천** | **추천 상품으로 모아톤 생성** | **모아톤 정보 수정** |

<br>

### 3. 금융 상품 조회 및 가입 (Products)
AI 추천 외에도 전체 예·적금 상품을 직접 비교하고 선택하여 모아톤을 시작할 수 있습니다.

| Product List | Product Detail | Create with Option |
| :---: | :---: | :---: |
| <img src="./docs/result_gifs/Products.gif" width="250" /> | <img src="./docs/result_gifs/ProductDetail.gif" width="250" /> | <img src="./docs/result_gifs/ProductOption-MoathonCreate.gif" width="250" /> |
| **전체 금융 상품 조회/필터링** | **상품 상세 금리/조건 확인** | **옵션 선택 후 모아톤 시작** |

<br>

### 4. 커뮤니티 및 프로필 (Community & Profile)
다른 유저들과 함께 저축 현황을 공유하고 응원하며, 나의 활동 내역(뱃지)을 관리합니다.

| Moathon Detail | User Following | Profile & Badges |
| :---: | :---: | :---: |
| <img src="./docs/result_gifs/MoathonDetail.gif" width="250" /> | <img src="./docs/result_gifs/Following.gif" width="250" /> | <img src="./docs/result_gifs/Profile.gif" width="250" /> |
| **모아톤 상세 정보 / 댓글 / 좋아요** | **유저 팔로우 및 피드** | **마이페이지 / 뱃지 콜렉션** |

<br>

### 5. 금융 유틸리티 (Utilities)
사용자의 금융 생활을 돕는 부가 기능 모음입니다.

| Bank Map | Commodity Chart | Finance Tube |
| :---: | :---: | :---: |
| <img src="./docs/result_gifs/BankMap.gif" width="250" /> | <img src="./docs/result_gifs/CommodityChart.gif" width="250" /> | <img src="./docs/result_gifs/FinanceTube.gif" width="250" /> |
| **내 주변 은행 찾기 (Kakao Map)** | **금/은 시세 차트 (Chart.js)** | **금융튜브 (Youtube API)** |

<br><br>


## 서비스 상세 기능

### 1. 금융상품 추천 시스템 (Personalized Recommendation)
사용자의 자산 현황과 재무 목표를 분석하여 최적의 예·적금 상품을 제안합니다.

- **기능 요약:**
    - **개인화 추천:** 사용자 프로필(나이, 자산, 소비패턴 등)과 목표(금액, 기간, 용도)를 결합하여 분석
    - **설명 가능한 추천(XAI):** 단순 상품 나열이 아닌, *"왜 이 상품이 적합한지"*에 대한 구체적인 근거(Summary) 제공
    - **예외 처리(Fallback):** AI 모델/LLM 장애 발생 시에도 서비스가 중단되지 않도록 규칙 기반(Rule-based) 폴백 시스템 가동

- **사용자 입력 정보:**
    - **목표:** 목표 금액(Target), 시작 금액(Start), 기간(개월 수)
    - **목적(Purpose):** 목돈 마련, 단기 여유자금, 안정적 자산 보관, 저축 습관 형성, 이자 극대화

### 2. 모아톤 커뮤니티 (Moathon Community)
저축을 혼자 하는 것이 아니라, '함께' 하는 챌린지 형태로 만들어 동기 부여를 제공합니다.

- **모아톤(게시글) 관리:**
    - 추천받은 상품으로 '모아톤' 챌린지 생성 (목표 및 다짐 작성)
    - 진행률(%) 시각화 및 상세 정보(옵션/금리) 공유
- **소셜 인터랙션:**
    - **응원하기(좋아요):** 서로의 목표 달성을 응원 (중복 방지 적용)
    - **댓글/피드백:** 금융 꿀팁 공유 및 격려 메시지 작성
    - **팔로우:** 관심 있는 유저의 모아톤 활동을 메인 피드에서 확인
- **권한 및 정책:**
    - 비로그인 유저: 목록 조회만 가능 (Eye-shopping)
    - 로그인 유저: 작성, 수정, 삭제, 좋아요, 팔로우 등 모든 상호작용 가능 (작성자 본인 확인 로직 포함)

### 3. 게이미피케이션 & 리워드 (Badge System)
사용자의 활동에 따라 뱃지를 지급하여 지속적인 서비스 이용을 유도합니다.

- **뱃지 카테고리:**
    - **Track (진행률):** 첫 숨 고르기(25%), 반환점(50%), 막판 스퍼트(75%), 완주 트로피(100%)
    - **Achieve (성취):** 작심삼일 탈출(3일 유지), 억만장자의 꿈(장기 적금), 프로 완주러 등
    - **Social (소통):** 응원 단장(좋아요), 소통 요정(댓글), 인기 스타, 팔로팔로미
- **기술적 특징:**
    - **동시성 제어:** 따닥(Double Click) 이슈 방지를 위한 중복 지급 방지 로직 적용
    - **트리거:** 회원가입, 로그인, 특정 이벤트(좋아요/생성) 발생 시 즉시 조건 검사 및 지급


## 2-Stage 하이브리드 추천 알고리즘

모아톤은 **안정성(ML)**과 **해석력(LLM)**을 모두 잡기 위해 **2-Stage 파이프라인**을 자체 구축했습니다.

핵심 목표는 **(1) 정형 피쳐를 활용해 안정적으로 후보를 좁힌 뒤 (2) 사용자 맥락을 반영해 최종 1개 옵션을 선택**하는 것입니다.

- Stage 1: ML(XGBoost) 기반 랭킹(Top-10 후보 생성)
- Stage 2: LLM(gpt-5-mini) 기반 의미적 재랭킹(최종 1개 옵션 선택 + 설명 생성)

### Stage 1: ML 랭킹(후보 압축)

Stage 1은 **정형화 가능한 특성**을 중심으로 모델 입력을 구성합니다.

- **모델**: XGBoost Classifier (Ranking)

- **활용 데이터:**

    - **User**: 나이, 자산, 연봉, 소비패턴, 리스크 성향 등 정형 데이터

    - **Product**: 금리, 기간, 단리/복리, 적립 유형

- **역할**: 전체 상품군 → 확률 점수 기반 **Top-10 후보군 추출** (Hit@K 지표로 성능 검증)

### Stage 2: LLM 의미적 재랭킹(최종 선택)
압축된 후보군 중에서 사용자의 '목적(Purpose)'과 텍스트 맥락을 고려해 최종 결정을 내립니다.

- **모델**: GPT-5-mini (Fine-tuned/Prompted)

- **프로세스:**

    1. **옵션 단축:** Top-10 상품의 수많은 옵션 중, 목표 기간과 가장 유사한 옵션들을 1차 필터링

    2. **LLM 추론:** 사용자의 목적(예: "결혼 자금 마련")을 해석하여 금리가 조금 낮더라도 안정적인 상품을 고르거나, 기간이 딱 맞는 상품을 선택

    3. **검증(Hallucination Check):** AI가 선택한 상품이 실제 후보군에 존재하는지 ID 매칭 검증

- **출력**: 최종 상품 ID, 옵션 ID, **추천 사유(Reasons), 유의사항(Warnings)**

### [더 자세한 AI 추천 시스템 설명 보러가기](./docs/AI_recommend_system.md)

<br><br>

## 팀 소개

### 팀원 및 역할

| 박준아 (팀장) | 정환승 (팀원) |
| :--- | :--- |
| **PM, Frontend, Integration** | **AI, Backend, Data Engineer** |
| • 프론트엔드 아키텍처 (Vue3) <br> • UI/UX 디자인 및 컴포넌트 구현 <br> • Axios Interceptor 및 API 연동 <br> • 카카오맵/유튜브 API 활용 기능 <br> • GitHub 관리 | • DB 모델링 (ERD) <br> • API 설계 <br> • AI 추천 시스템 구현 <br> • 금융 데이터 수집 및 전처리 <br> • 기획서 및  발표 자료 |

<br>

### 팀 회고 (Retrospective)

| 이름 | 회고 및 배운 점 |
| :---: | :--- |
| 박준아 | 프론트와 백엔드가 어떻게 데이터를 주고 받는지 확실하게 배웠습니다. 규모가 작은 프로젝트에서는 프론트의 역할과 책임이 훨씬 무겁다고 느꼈습니다. 기능 단위가 가볍기 때문에 백엔드에서 데이터를 생성하고 DB에서 가져오고 조립하는 과정이 복잡하지는 않았습니다. 오히려 RESTful API로 데이터를 주고 받는 과정에서 오류 처리를 어떻게 해야하고, 응답받은 데이터를 화면에 구현하는 과정이 훨씬 어려웠습니다. 기능 단위가 커지고 프로젝트 규모가 커진다면 백엔드 로직이 훨씬 복잡하고 어려워지고, 반면에 프론트엔드의 작업은 프로젝트의 규모와 상관없을 것 같다고 느꼈습니다. <br> 3주만에 기획-개발-테스트를 모두 해냈다는 사실이 무척 뿌듯합니다. 그럼에도 아직 구현하지 못한 기능이 많기 때문에 더 공부해서 도전해보고 싶은 마음입니다. 대표적으로 뱃지를 획득한 경우, django의 signals에서 조건이 충족되면 자동으로 발급되어 DB에 기록됩니다. 하지만 프론트에서 DB의 내용을 가져오려면 API를 호출하는 방법밖에 없습니다. 때문에 뱃지가 발급됨과 동시에 유저에게 알림을 주기 위해서는 polling이나 socket을 도입해야 합니다. 이 기능과 배포까지 완성해보고 싶습니다.|
| 정환승 | ML 모델을 학습할 때 페이크 데이터 기반으로 진행한 점은 조금 아쉬웠습니다. 실제 사용자 데이터가 있었다면 추천 품질을 더 현실적으로 검증할 수 있었고, 특히 뱃지 같은 리워드/커뮤니티 활동 지표도 유저 성향을 보여주는 좋은 피처가 될 것 같았는데 시간적 제약 때문에 학습 단계에까지 반영해보지 못한 점이 아쉽습니다. 그래도 “사용자 기반 추천시스템”을 직접 설계해보고자 ML 모델로 후보를 좁히는 구조를 만들고, 생성형 AI를 함께 활용해 최종 상품·옵션을 선택하고 근거를 생성하는 흐름까지 구현하면서 추천 시스템을 서비스 관점에서 설계하는 방법을 배울 수 있었습니다. 또한 추천 결과가 실제 기능으로 자연스럽게 이어지도록 REST API를 리소스 단위로 설계·구현하며 인증/권한/정책을 정리하는 과정에서, 단순히 기능을 만드는 것을 넘어 운영 가능한 형태로 구조화하는 경험을 할 수 있었습니다. |

<br><br>

## 프로젝트 실행 방법

이 프로젝트는 로컬 개발 환경에서 실행할 수 있습니다.

### 1. Backend Setup (Django)

```bash
# 레포지토리 클론
git clone https://github.com/ajjoona-git/moathon.git
cd moathon/backend

# 가상환경 생성 및 실행
python -m venv venv
source venv/Script/activate

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정 (.env 파일 생성)
# DJANGO_SECRET_KEY, DEBUG=True, API_KEY 등을 설정하세요.
```

#### DB 설정 (데이터 적재)

```bash
# 데이터베이스 마이그레이션
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

# 서버 실행
python manage.py runserver
```

<br>

### 2. Frontend Setup (Vue.js)

```bash
cd ../frontend

# 의존성 설치
npm install

# 환경 변수 설정 (.env.local 파일 생성)
# VITE_API_URL 등 설정

# 개발 서버 실행
npm run dev
```
