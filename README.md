# SSU 데이터톤

**팀명:** 초록 멀티탭

**팀원:** 홍준우, 남지윤, 신지원, 조영찬

---

## 프로젝트 개요

뉴스 데이터와 학술 논문 데이터를 비교 분석하여 **사회적 주목도**와 **학술적 연구도** 간의 간극을 파악하고, **블루오션 연구 주제**를 발굴하는 프로젝트입니다.

### 주요 분석 내용
- 뉴스/논문 키워드 추출 및 빈도 분석
- TF-IDF 기반 핵심 키워드 도출
- 동시 출현(Co-occurrence) 빈도 분석
- 간극 분석(Gap Analysis)을 통한 블루오션/학술선도 주제 발굴
- 다양한 시각화 (히트맵, 산점도, 워드클라우드 등)

---

## 사용 라이브러리

```
pandas>=2.0.0
matplotlib>=3.7.0
numpy>=1.24.0
openpyxl>=3.1.0
wordcloud>=1.9.0
```

---

## Raw Data

| 파일명 | 설명 |
|--------|------|
| `news_data.xlsx` | 뉴스 기사 데이터 (키워드, 제목, 카테고리 등) |
| `datathon_data.json` | 학술 논문 데이터 (키워드, 제목, 저자 등) |

---

## 소스 파일 소개

### 설정 파일

| 파일명 | 설명 |
|--------|------|
| `config.py` | 전체 분석 설정 관리 (경로, 파라미터, 동의어 매핑, 불용어, 분석 대상 키워드, 카테고리 분류 등) |

### 분석 파이프라인 (Phase 1~5)

| 파일명 | 설명 |
|--------|------|
| `phase1_preprocess.py` | 데이터 전처리 - 뉴스/논문에서 키워드 추출 및 빈도 계산 |
| `phase2_tfidf.py` | 형태소 분석 + TF-IDF 분석 - 동의어 통합, 불용어 제거 후 TF-IDF 계산 |
| `phase3_cooccurrence.py` | 동시 출현 빈도 분석 + 간극 분석 - 블루오션/학술선도 주제 발굴 |
| `phase4_visualization.py` | 시각화 - 간극 분석 차트, 산점도, 히트맵, 빈도 비교 등 |
| `phase5_keyword_pair_mentions.py` | 특정 키워드 조합별 문서 발췌 및 정리 |
| `phase5_visualize_wordcloud.py` | 키워드 조합별 맥락 워드클라우드 시각화 |

### 추가 분석

| 파일명 | 설명 |
|--------|------|
| `top5_cooccurrence_analysis.py` | Paper/News 상위 5개 키워드 간 동시 출현 분석 |
| `paper_top_co_keywords.py` | 논문 데이터에서 주요 키워드와 동시 등장하는 키워드 분석 및 시각화 |

---

## 출력 디렉토리

| 디렉토리 | 설명 |
|----------|------|
| `output/` | 분석 결과 JSON 파일 (키워드 빈도, TF-IDF, 동시출현, 간극분석 등) |
| `visualizations/` | 시각화 이미지 파일 (PNG) |

### 주요 출력 파일

```
output/
├── news_keywords.json      # 뉴스 키워드 빈도
├── paper_keywords.json     # 논문 키워드 빈도
├── common_keywords.json    # 공통 키워드
├── news_tfidf.json         # 뉴스 TF-IDF 결과
├── paper_tfidf.json        # 논문 TF-IDF 결과
├── keyword_analysis.json   # 공통/고유 키워드 분석
├── news_cooccurrence.json  # 뉴스 동시출현 분석
├── paper_cooccurrence.json # 논문 동시출현 분석
└── gap_analysis.json       # 간극 분석 결과
```

---

## 사용 방법

### 1. 환경 설정

```bash
# 가상환경 생성 (선택)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 패키지 설치
pip install -r requirements.txt
pip install wordcloud  # 워드클라우드 생성 시 필요
```

### 2. 분석 실행

분석은 Phase 순서대로 실행합니다:

```bash
# Phase 1: 데이터 전처리 (키워드 추출)
python phase1_preprocess.py

# Phase 2: TF-IDF 분석
python phase2_tfidf.py

# Phase 3: 동시 출현 분석 + 간극 분석
python phase3_cooccurrence.py

# Phase 4: 시각화 생성
python phase4_visualization.py

# Phase 5: 키워드 조합 분석 (선택)
python phase5_keyword_pair_mentions.py
python phase5_visualize_wordcloud.py
```

### 3. 추가 분석 (선택)

```bash
# 상위 5개 키워드 동시 출현 분석
python top5_cooccurrence_analysis.py

# 논문 동시 출현 키워드 시각화
python paper_top_co_keywords.py
```

---

## 분석 설정 커스터마이징

`config.py`에서 다양한 분석 파라미터를 조정할 수 있습니다:

```python
# TF-IDF 상위 키워드 추출 개수
NEWS_TFIDF_TOP_N = 500
PAPER_TFIDF_TOP_N = 500

# 간극 분석 기준
GAP_NEWS_MIN_FREQ = 100      # 블루오션 판정 시 뉴스 최소 빈도
GAP_PAPER_MIN_FREQ = 50      # 학술선도 판정 시 논문 최소 빈도
GAP_BLUE_OCEAN_THRESHOLD = 5 # 블루오션 간극 지수 기준

# 동의어 매핑, 불용어, 분석 대상 키워드 등도 수정 가능
```

---

## 프로젝트 구조

```
ssu-datathon/
├── README.md                        # 프로젝트 설명서
├── requirements.txt                 # 패키지 의존성
├── config.py                        # 전체 분석 설정 관리
│
├── news_data.xlsx                   # [Raw Data] 뉴스 기사 데이터
├── datathon_data.json               # [Raw Data] 학술 논문 데이터
│
├── phase1_preprocess.py             # Phase 1: 데이터 전처리
├── phase2_tfidf.py                  # Phase 2: TF-IDF 분석
├── phase3_cooccurrence.py           # Phase 3: 동시출현/간극분석
├── phase4_visualization.py          # Phase 4: 시각화 생성
├── phase5_keyword_pair_mentions.py  # Phase 5: 키워드 조합 분석
├── phase5_visualize_wordcloud.py    # Phase 5: 워드클라우드 시각화
│
├── top5_cooccurrence_analysis.py    # 상위 5개 키워드 동시출현 분석
├── paper_top_co_keywords.py         # 논문 주요 키워드와 연관어 분석
│
├── malgun.ttf                       # 한글 폰트 (시각화용)
│
├── output/                          # 분석 결과 JSON 파일
│   ├── news_keywords.json           # 뉴스 키워드 빈도
│   ├── paper_keywords.json          # 논문 키워드 빈도
│   ├── common_keywords.json         # 공통 키워드
│   ├── news_tfidf.json              # 뉴스 TF-IDF 결과
│   ├── paper_tfidf.json             # 논문 TF-IDF 결과
│   ├── keyword_analysis.json        # 공통/고유 키워드 분석
│   ├── news_cooccurrence.json       # 뉴스 동시출현 분석
│   ├── paper_cooccurrence.json      # 논문 동시출현 분석
│   ├── gap_analysis.json            # 간극 분석 결과
│   └── phase5_keyword_pair_mentions.json
│
└── visualizations/                  # 시각화 이미지 (PNG)
    ├── 1_gap_analysis.png           # 간극 분석 차트
    ├── 2_scatter_comparison.png     # 산점도 비교
    ├── 3_tfidf_comparison.png       # TF-IDF 비교
    ├── 4_cooccurrence_heatmap.png   # 동시출현 히트맵
    ├── 5_category_comparison.png    # 카테고리 비교
    ├── 6_frequency_comparison.png   # 빈도 비교
    └── wordcloud_*.png              # 키워드 조합별 워드클라우드
```
