"""
Phase 2: 형태소 분석 + TF-IDF 분석
- 한/영 키워드 통합
- 유의어 통합
- 불용어 제거
- TF-IDF 계산
"""

import pandas as pd
import json
from collections import Counter, defaultdict
from math import log

# config에서 설정 import
from config import (
    NEWS_FILES, PAPER_FILE, OUTPUT_DIR,
    NEWS_EXCLUDE_CATEGORIES,
    SYNONYM_MAP, STOPWORDS,
    NEWS_TFIDF_TOP_N, PAPER_TFIDF_TOP_N, COMMON_KEYWORD_TOP_N,
    normalize_keyword, is_valid_keyword, init_dirs
)


def extract_and_normalize_news():
    """뉴스 키워드 추출 및 정규화"""
    print("=" * 50)
    print("뉴스 키워드 추출 및 정규화 중...")
    print("=" * 50)

    all_docs = []
    all_keywords = []

    for file in NEWS_FILES:
        print(f"  처리 중: {file}")
        df = pd.read_excel(file)

        # 카테고리 필터링
        df = df[~df['통합 분류1'].isin(NEWS_EXCLUDE_CATEGORIES)]

        for kw in df['키워드'].dropna():
            keywords = [k.strip() for k in str(kw).split(',') if k.strip()]
            normalized = []
            for k in keywords:
                nk = normalize_keyword(k)
                if is_valid_keyword(nk):
                    normalized.append(nk)

            if normalized:
                all_docs.append(set(normalized))
                all_keywords.extend(normalized)

    keyword_counter = Counter(all_keywords)

    print(f"\n[뉴스 정규화 결과]")
    print(f"  문서 수: {len(all_docs):,}")
    print(f"  총 키워드: {len(all_keywords):,}")
    print(f"  고유 키워드: {len(keyword_counter):,}")

    return all_docs, keyword_counter


def extract_and_normalize_papers():
    """논문 키워드 추출 및 정규화"""
    print("\n" + "=" * 50)
    print("논문 키워드 추출 및 정규화 중...")
    print("=" * 50)

    with open(PAPER_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_docs = []
    all_keywords = []

    for item in data['NODE_LIST']:
        kywd = item.get('KYWD')
        if kywd:
            keywords = [k.strip() for k in str(kywd).split(',') if k.strip()]
            normalized = []
            for k in keywords:
                nk = normalize_keyword(k)
                if is_valid_keyword(nk):
                    normalized.append(nk)

            if normalized:
                all_docs.append(set(normalized))
                all_keywords.extend(normalized)

    keyword_counter = Counter(all_keywords)

    print(f"\n[논문 정규화 결과]")
    print(f"  문서 수: {len(all_docs):,}")
    print(f"  총 키워드: {len(all_keywords):,}")
    print(f"  고유 키워드: {len(keyword_counter):,}")

    return all_docs, keyword_counter


def calculate_tfidf(docs, keyword_counter, top_n):
    """TF-IDF 계산"""

    total_docs = len(docs)

    df_counter = Counter()
    for doc in docs:
        for kw in doc:
            df_counter[kw] += 1

    tfidf_scores = {}
    for kw, tf in keyword_counter.items():
        df = df_counter.get(kw, 1)
        idf = log(total_docs / df) + 1
        tfidf_scores[kw] = tf * idf

    sorted_tfidf = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_tfidf[:top_n], df_counter


def print_top_keywords(tfidf_list, name, top_n=100):
    """상위 키워드 출력"""
    print(f"\n{'=' * 50}")
    print(f"{name} TF-IDF 상위 {top_n}개 키워드")
    print("=" * 50)

    for i, (kw, score) in enumerate(tfidf_list[:top_n], 1):
        print(f"{i:3}. {kw}: {score:,.2f}")


def find_common_and_unique(news_tfidf, paper_tfidf, news_counter, paper_counter):
    """공통/고유 키워드 분석"""
    print("\n" + "=" * 50)
    print("공통/고유 키워드 분석")
    print("=" * 50)

    news_top = set(dict(news_tfidf[:COMMON_KEYWORD_TOP_N]).keys())
    paper_top = set(dict(paper_tfidf[:COMMON_KEYWORD_TOP_N]).keys())

    common = news_top & paper_top
    news_only = news_top - paper_top
    paper_only = paper_top - news_top

    print(f"\n공통 키워드 (상위 {COMMON_KEYWORD_TOP_N} 기준): {len(common)}개")
    print(f"뉴스에만 있는 키워드: {len(news_only)}개")
    print(f"논문에만 있는 키워드: {len(paper_only)}개")

    common_detail = []
    for kw in common:
        common_detail.append({
            'keyword': kw,
            'news_freq': news_counter.get(kw, 0),
            'paper_freq': paper_counter.get(kw, 0),
        })
    common_detail.sort(key=lambda x: x['paper_freq'], reverse=True)

    print(f"\n[공통 키워드 상위 50개]")
    print(f"{'키워드':<20} | {'뉴스빈도':>10} | {'논문빈도':>10}")
    print("-" * 50)
    for item in common_detail[:50]:
        print(f"{item['keyword']:<20} | {item['news_freq']:>10,} | {item['paper_freq']:>10,}")

    paper_only_detail = [(kw, paper_counter.get(kw, 0)) for kw in paper_only]
    paper_only_detail.sort(key=lambda x: x[1], reverse=True)

    print(f"\n[논문에만 있는 키워드 상위 30개] - 학술 특화 주제")
    for i, (kw, freq) in enumerate(paper_only_detail[:30], 1):
        print(f"  {i:2}. {kw}: {freq}")

    news_only_detail = [(kw, news_counter.get(kw, 0)) for kw in news_only]
    news_only_detail.sort(key=lambda x: x[1], reverse=True)

    print(f"\n[뉴스에만 있는 키워드 상위 30개] - 사회적 관심 주제")
    for i, (kw, freq) in enumerate(news_only_detail[:30], 1):
        print(f"  {i:2}. {kw}: {freq:,}")

    return {
        'common': common_detail,
        'news_only': news_only_detail,
        'paper_only': paper_only_detail
    }


def save_results(news_tfidf, paper_tfidf, news_counter, paper_counter, keyword_analysis):
    """결과 저장"""
    print("\n" + "=" * 50)
    print("결과 저장 중...")
    print("=" * 50)

    with open(OUTPUT_DIR / 'news_tfidf.json', 'w', encoding='utf-8') as f:
        json.dump({
            'tfidf': [{'keyword': k, 'score': s, 'freq': news_counter.get(k, 0)}
                      for k, s in news_tfidf],
        }, f, ensure_ascii=False, indent=2)
    print(f"  저장: {OUTPUT_DIR / 'news_tfidf.json'}")

    with open(OUTPUT_DIR / 'paper_tfidf.json', 'w', encoding='utf-8') as f:
        json.dump({
            'tfidf': [{'keyword': k, 'score': s, 'freq': paper_counter.get(k, 0)}
                      for k, s in paper_tfidf],
        }, f, ensure_ascii=False, indent=2)
    print(f"  저장: {OUTPUT_DIR / 'paper_tfidf.json'}")

    with open(OUTPUT_DIR / 'keyword_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(keyword_analysis, f, ensure_ascii=False, indent=2)
    print(f"  저장: {OUTPUT_DIR / 'keyword_analysis.json'}")


def main():
    print("\n" + "#" * 60)
    print("#  Phase 2: 형태소 분석 + TF-IDF 분석")
    print("#" * 60)

    init_dirs()

    news_docs, news_counter = extract_and_normalize_news()
    paper_docs, paper_counter = extract_and_normalize_papers()

    print("\n" + "=" * 50)
    print("TF-IDF 계산 중...")
    print("=" * 50)

    news_tfidf, news_df = calculate_tfidf(news_docs, news_counter, NEWS_TFIDF_TOP_N)
    paper_tfidf, paper_df = calculate_tfidf(paper_docs, paper_counter, PAPER_TFIDF_TOP_N)

    print_top_keywords(news_tfidf, "뉴스", 100)
    print_top_keywords(paper_tfidf, "논문", 100)

    keyword_analysis = find_common_and_unique(
        news_tfidf, paper_tfidf, news_counter, paper_counter
    )

    save_results(news_tfidf, paper_tfidf, news_counter, paper_counter, keyword_analysis)

    print("\n" + "#" * 60)
    print("#  Phase 2 완료!")
    print("#" * 60)


if __name__ == '__main__':
    main()
