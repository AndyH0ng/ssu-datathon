"""
Phase 3: 동시 출현 빈도 분석 (Co-occurrence Analysis)
- 뉴스: 사회적 주목도 계산
- 논문: 학술적 연구도 계산
- 간극 분석: 블루오션 연구 주제 발굴
"""

import pandas as pd
import json
from collections import Counter, defaultdict
from itertools import combinations

# config에서 설정 import
from config import (
    NEWS_FILES, PAPER_FILE, OUTPUT_DIR,
    NEWS_EXCLUDE_CATEGORIES,
    SYNONYM_MAP, TOPIC_KEYWORDS,
    GAP_NEWS_MIN_FREQ, GAP_PAPER_MIN_FREQ,
    GAP_BLUE_OCEAN_THRESHOLD, GAP_ACADEMIC_THRESHOLD,
    normalize_keyword, is_valid_keyword, init_dirs
)


def extract_docs_with_keywords(source='news'):
    """문서별 키워드 추출"""
    all_docs = []

    if source == 'news':
        for file in NEWS_FILES:
            df = pd.read_excel(file)
            # 카테고리 필터링
            df = df[~df['통합 분류1'].isin(NEWS_EXCLUDE_CATEGORIES)]
            for kw in df['키워드'].dropna():
                keywords = [normalize_keyword(k.strip()) for k in str(kw).split(',') if k.strip()]
                keywords = [k for k in keywords if is_valid_keyword(k)]  # 불용어 필터링
                keywords = list(set(keywords))
                if keywords:
                    all_docs.append(keywords)
    else:
        with open(PAPER_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data['NODE_LIST']:
            kywd = item.get('KYWD')
            if kywd:
                keywords = [normalize_keyword(k.strip()) for k in str(kywd).split(',') if k.strip()]
                keywords = [k for k in keywords if is_valid_keyword(k)]  # 불용어 필터링
                keywords = list(set(keywords))
                if keywords:
                    all_docs.append(keywords)

    return all_docs


def calculate_cooccurrence(docs, target_keywords):
    """동시 출현 빈도 계산"""
    cooccur = defaultdict(lambda: defaultdict(int))
    keyword_freq = Counter()

    for doc in docs:
        doc_set = set(doc)
        for kw in doc_set:
            keyword_freq[kw] += 1

        for target in target_keywords:
            if target in doc_set:
                for other in doc_set:
                    if other != target:
                        cooccur[target][other] += 1

    return cooccur, keyword_freq


def analyze_source(source_name, docs, target_keywords):
    """소스별 분석"""
    print(f"\n{'=' * 50}")
    print(f"{source_name} 동시 출현 분석")
    print('=' * 50)
    print(f"총 문서 수: {len(docs):,}")

    cooccur, keyword_freq = calculate_cooccurrence(docs, target_keywords)

    results = {}
    for target in target_keywords:
        if target in cooccur and cooccur[target]:
            top_by_count = sorted(cooccur[target].items(), key=lambda x: x[1], reverse=True)[:20]
            results[target] = {
                'freq': keyword_freq.get(target, 0),
                'top_cooccur': [{'keyword': k, 'count': v} for k, v in top_by_count]
            }

    print(f"\n[주요 키워드별 동시 출현 상위 키워드]")
    for target in target_keywords[:15]:
        if target in results:
            print(f"\n▶ {target} (출현: {results[target]['freq']:,}회)")
            for item in results[target]['top_cooccur'][:5]:
                print(f"   - {item['keyword']}: {item['count']:,}")

    return results, cooccur, keyword_freq


def calculate_gap_index(news_results, paper_results, news_docs, paper_docs):
    """간극 지수 계산"""
    print("\n" + "=" * 50)
    print("간극 분석 (Gap Analysis)")
    print("=" * 50)

    gap_analysis = []
    all_keywords = set(news_results.keys()) | set(paper_results.keys())

    for kw in all_keywords:
        news_freq = news_results.get(kw, {}).get('freq', 0)
        paper_freq = paper_results.get(kw, {}).get('freq', 0)

        news_ratio = news_freq / len(news_docs) * 1000 if news_docs else 0
        paper_ratio = paper_freq / len(paper_docs) * 1000 if paper_docs else 0
        gap = news_ratio - paper_ratio

        gap_analysis.append({
            'keyword': kw,
            'news_freq': news_freq,
            'paper_freq': paper_freq,
            'news_ratio': round(news_ratio, 4),
            'paper_ratio': round(paper_ratio, 4),
            'gap_index': round(gap, 4)
        })

    gap_analysis.sort(key=lambda x: x['gap_index'], reverse=True)

    # 블루오션
    print("\n[블루오션 연구 주제 후보]")
    print("(사회적 주목도↑ & 학술적 연구도↓)")
    print("-" * 70)
    print(f"{'키워드':<15} | {'뉴스빈도':>10} | {'논문빈도':>10} | {'뉴스비율':>10} | {'논문비율':>10} | {'간극':>10}")
    print("-" * 70)

    blue_ocean = [g for g in gap_analysis
                  if g['news_freq'] > GAP_NEWS_MIN_FREQ and g['gap_index'] > GAP_BLUE_OCEAN_THRESHOLD][:20]
    for item in blue_ocean:
        print(f"{item['keyword']:<15} | {item['news_freq']:>10,} | {item['paper_freq']:>10,} | "
              f"{item['news_ratio']:>10.2f} | {item['paper_ratio']:>10.2f} | {item['gap_index']:>10.2f}")

    # 학술선도
    print("\n[학술 선도 연구 주제]")
    print("(학술적 연구도↑ & 사회적 주목도↓)")
    print("-" * 70)

    academic_lead = [g for g in gap_analysis
                     if g['paper_freq'] > GAP_PAPER_MIN_FREQ and g['gap_index'] < GAP_ACADEMIC_THRESHOLD]
    academic_lead.sort(key=lambda x: x['gap_index'])
    for item in academic_lead[:20]:
        print(f"{item['keyword']:<15} | {item['news_freq']:>10,} | {item['paper_freq']:>10,} | "
              f"{item['news_ratio']:>10.2f} | {item['paper_ratio']:>10.2f} | {item['gap_index']:>10.2f}")

    return gap_analysis


def save_results(news_results, paper_results, gap_analysis):
    """결과 저장"""
    print("\n" + "=" * 50)
    print("결과 저장 중...")
    print("=" * 50)

    with open(OUTPUT_DIR / 'news_cooccurrence.json', 'w', encoding='utf-8') as f:
        json.dump(news_results, f, ensure_ascii=False, indent=2)
    print(f"  저장: {OUTPUT_DIR / 'news_cooccurrence.json'}")

    with open(OUTPUT_DIR / 'paper_cooccurrence.json', 'w', encoding='utf-8') as f:
        json.dump(paper_results, f, ensure_ascii=False, indent=2)
    print(f"  저장: {OUTPUT_DIR / 'paper_cooccurrence.json'}")

    with open(OUTPUT_DIR / 'gap_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(gap_analysis, f, ensure_ascii=False, indent=2)
    print(f"  저장: {OUTPUT_DIR / 'gap_analysis.json'}")


def main():
    print("\n" + "#" * 60)
    print("#  Phase 3: 동시 출현 빈도 분석 + 간극 분석")
    print("#" * 60)

    init_dirs()

    print("\n뉴스 데이터 로딩 중...")
    news_docs = extract_docs_with_keywords('news')
    print(f"뉴스 문서 수: {len(news_docs):,}")

    print("\n논문 데이터 로딩 중...")
    paper_docs = extract_docs_with_keywords('paper')
    print(f"논문 문서 수: {len(paper_docs):,}")

    news_results, _, _ = analyze_source("뉴스 (사회적 주목도)", news_docs, TOPIC_KEYWORDS)
    paper_results, _, _ = analyze_source("논문 (학술적 연구도)", paper_docs, TOPIC_KEYWORDS)

    gap_analysis = calculate_gap_index(news_results, paper_results, news_docs, paper_docs)

    save_results(news_results, paper_results, gap_analysis)

    print("\n" + "#" * 60)
    print("#  Phase 3 완료!")
    print("#" * 60)


if __name__ == '__main__':
    main()
