"""
Phase 1: 데이터 전처리 - 뉴스/논문 키워드 추출 및 정제
"""

import pandas as pd
import json
from collections import Counter

# config에서 설정 import
from config import NEWS_FILES, PAPER_FILE, OUTPUT_DIR, NEWS_EXCLUDE_CATEGORIES, init_dirs


def extract_news_keywords():
    """뉴스 데이터에서 키워드 추출"""
    print("=" * 50)
    print("뉴스 키워드 추출 중...")
    print("=" * 50)

    all_keywords = []
    keywords_per_article = []

    for file in NEWS_FILES:
        print(f"  처리 중: {file}")
        df = pd.read_excel(file)

        # 카테고리 필터링
        original_count = len(df)
        df = df[~df['통합 분류1'].isin(NEWS_EXCLUDE_CATEGORIES)]
        filtered_count = len(df)
        print(f"    카테고리 필터링: {original_count:,} → {filtered_count:,} ({original_count - filtered_count:,}건 제외)")

        for kw in df['키워드'].dropna():
            # 쉼표로 분리 후 정제
            keywords = [k.strip() for k in str(kw).split(',') if k.strip()]
            all_keywords.extend(keywords)
            keywords_per_article.append(set(keywords))

    # 빈도수 계산
    keyword_counter = Counter(all_keywords)

    print(f"\n[뉴스 결과]")
    print(f"  총 키워드 수 (중복 포함): {len(all_keywords):,}")
    print(f"  고유 키워드 수: {len(keyword_counter):,}")
    print(f"  기사 수: {len(keywords_per_article):,}")

    return keyword_counter, keywords_per_article


def extract_paper_keywords():
    """논문 데이터에서 키워드 추출"""
    print("\n" + "=" * 50)
    print("논문 키워드 추출 중...")
    print("=" * 50)

    with open(PAPER_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    node_list = data['NODE_LIST']

    all_keywords = []
    keywords_per_paper = []

    for item in node_list:
        kywd = item.get('KYWD')
        if kywd:
            # 쉼표로 분리 후 정제
            keywords = [k.strip() for k in str(kywd).split(',') if k.strip()]
            all_keywords.extend(keywords)
            keywords_per_paper.append(set(keywords))

    # 빈도수 계산
    keyword_counter = Counter(all_keywords)

    print(f"\n[논문 결과]")
    print(f"  총 키워드 수 (중복 포함): {len(all_keywords):,}")
    print(f"  고유 키워드 수: {len(keyword_counter):,}")
    print(f"  논문 수 (키워드 보유): {len(keywords_per_paper):,}")

    return keyword_counter, keywords_per_paper


def find_common_keywords(news_counter, paper_counter, top_n=1000):
    """뉴스와 논문의 공통 키워드 찾기"""
    print("\n" + "=" * 50)
    print(f"공통 키워드 분석 (상위 {top_n}개 기준)")
    print("=" * 50)

    news_top = set(dict(news_counter.most_common(top_n)).keys())
    paper_top = set(dict(paper_counter.most_common(top_n)).keys())

    common = news_top & paper_top

    # 공통 키워드를 논문 빈도 기준으로 정렬
    common_with_freq = []
    for kw in common:
        news_freq = news_counter.get(kw, 0)
        paper_freq = paper_counter.get(kw, 0)
        common_with_freq.append({
            'keyword': kw,
            'news_freq': news_freq,
            'paper_freq': paper_freq,
            'gap': news_freq - paper_freq  # 간극 (양수: 뉴스에서 더 많이 언급)
        })

    common_with_freq.sort(key=lambda x: x['paper_freq'], reverse=True)

    print(f"  공통 키워드 수: {len(common)}개\n")
    print(f"{'키워드':<20} | {'뉴스 빈도':>12} | {'논문 빈도':>10}")
    print("-" * 50)
    for item in common_with_freq[:30]:
        print(f"{item['keyword']:<20} | {item['news_freq']:>12,} | {item['paper_freq']:>10,}")

    return common_with_freq


def print_top_keywords(counter, name, top_n=200):
    """상위 키워드 출력"""
    print(f"\n{'=' * 50}")
    print(f"{name} 상위 {top_n}개 키워드")
    print("=" * 50)

    for i, (kw, cnt) in enumerate(counter.most_common(top_n), 1):
        print(f"{i:3}. {kw}: {cnt:,}")


def save_results(news_counter, paper_counter, common_keywords):
    """결과 저장"""
    print("\n" + "=" * 50)
    print("결과 저장 중...")
    print("=" * 50)

    # 뉴스 키워드 저장
    news_output = {
        'total_unique': len(news_counter),
        'keyword_freq': dict(news_counter.most_common(1000))
    }
    with open(OUTPUT_DIR / 'news_keywords.json', 'w', encoding='utf-8') as f:
        json.dump(news_output, f, ensure_ascii=False, indent=2)
    print(f"  저장: {OUTPUT_DIR / 'news_keywords.json'}")

    # 논문 키워드 저장
    paper_output = {
        'total_unique': len(paper_counter),
        'keyword_freq': dict(paper_counter.most_common(1000))
    }
    with open(OUTPUT_DIR / 'paper_keywords.json', 'w', encoding='utf-8') as f:
        json.dump(paper_output, f, ensure_ascii=False, indent=2)
    print(f"  저장: {OUTPUT_DIR / 'paper_keywords.json'}")

    # 공통 키워드 저장
    with open(OUTPUT_DIR / 'common_keywords.json', 'w', encoding='utf-8') as f:
        json.dump(common_keywords, f, ensure_ascii=False, indent=2)
    print(f"  저장: {OUTPUT_DIR / 'common_keywords.json'}")


def main():
    print("\n" + "#" * 60)
    print("#  Phase 1: 데이터 전처리 - 키워드 추출 및 정제")
    print("#" * 60)

    init_dirs()

    # 1. 뉴스 키워드 추출
    news_counter, news_per_article = extract_news_keywords()

    # 2. 논문 키워드 추출
    paper_counter, paper_per_doc = extract_paper_keywords()

    # 3. 상위 키워드 출력
    print_top_keywords(news_counter, "뉴스", 200)
    print_top_keywords(paper_counter, "논문", 200)

    # 4. 공통 키워드 분석
    common_keywords = find_common_keywords(news_counter, paper_counter)

    # 5. 결과 저장
    save_results(news_counter, paper_counter, common_keywords)

    print("\n" + "#" * 60)
    print("#  Phase 1 완료!")
    print("#" * 60)


if __name__ == '__main__':
    main()
