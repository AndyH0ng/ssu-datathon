"""
상위 5개 키워드 간 동시 출현 분석
- Paper 상위 5개: 코로나19, 인공지능, ESG, 직무만족, 우울
- News 상위 5개: 인공지능, 여성, 청년, 혁신, 플랫폼
"""

import pandas as pd
import json
from collections import Counter, defaultdict

# config에서 설정 import
from config import (
    NEWS_FILES, PAPER_FILE, OUTPUT_DIR,
    NEWS_EXCLUDE_CATEGORIES,
    normalize_keyword, init_dirs
)


# 분석 대상 키워드 정의
PAPER_TOP5 = ['코로나19', '인공지능', 'ESG', '직무만족', '우울']
NEWS_TOP5 = ['인공지능', '여성', '청년', '혁신', '플랫폼']

# 통합 키워드 목록 (중복 제거)
ALL_KEYWORDS = list(set(PAPER_TOP5 + NEWS_TOP5))


def extract_docs_with_keywords(source='news'):
    """문서별 키워드 추출 (동의어 정규화 적용)"""
    all_docs = []

    if source == 'news':
        for file in NEWS_FILES:
            df = pd.read_excel(file)
            # 카테고리 필터링
            df = df[~df['통합 분류1'].isin(NEWS_EXCLUDE_CATEGORIES)]
            for kw in df['키워드'].dropna():
                # 동의어 정규화 적용
                keywords = [normalize_keyword(k.strip()) for k in str(kw).split(',') if k.strip()]
                keywords = list(set(keywords))  # 중복 제거
                if keywords:
                    all_docs.append(keywords)
    else:  # paper
        with open(PAPER_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data['NODE_LIST']:
            kywd = item.get('KYWD')
            if kywd:
                # 동의어 정규화 적용
                keywords = [normalize_keyword(k.strip()) for k in str(kywd).split(',') if k.strip()]
                keywords = list(set(keywords))  # 중복 제거
                if keywords:
                    all_docs.append(keywords)

    return all_docs


def calculate_cooccurrence_matrix(docs, target_keywords):
    """
    대상 키워드 간의 동시 출현 매트릭스 계산

    Returns:
        matrix: dict[keyword1][keyword2] = count (동시 출현 문서 수)
        keyword_freq: dict[keyword] = count (개별 출현 문서 수)
    """
    matrix = defaultdict(lambda: defaultdict(int))
    keyword_freq = Counter()

    for doc in docs:
        doc_set = set(doc)

        # 각 키워드의 개별 출현 빈도 계산
        for kw in target_keywords:
            if kw in doc_set:
                keyword_freq[kw] += 1

        # 대상 키워드 간 동시 출현 계산
        for kw1 in target_keywords:
            if kw1 in doc_set:
                for kw2 in target_keywords:
                    if kw2 in doc_set and kw1 != kw2:
                        matrix[kw1][kw2] += 1

    return matrix, keyword_freq


def print_cooccurrence_analysis(source_name, docs, target_keywords, top5_label, top5_keywords):
    """동시 출현 분석 결과 출력"""
    print(f"\n{'=' * 70}")
    print(f"{source_name} 데이터에서 {top5_label} 상위 5개 키워드 동시 출현 분석")
    print('=' * 70)
    print(f"총 문서 수: {len(docs):,}")

    matrix, keyword_freq = calculate_cooccurrence_matrix(docs, target_keywords)

    # 개별 키워드 출현 빈도
    print(f"\n[{top5_label} 상위 5개 키워드 개별 출현 빈도]")
    print("-" * 50)
    for kw in top5_keywords:
        freq = keyword_freq.get(kw, 0)
        ratio = freq / len(docs) * 100 if docs else 0
        print(f"  {kw}: {freq:,}회 ({ratio:.2f}%)")

    # 동시 출현 매트릭스 출력
    print(f"\n[{top5_label} 상위 5개 키워드 간 동시 출현 매트릭스]")
    print("-" * 70)

    # 헤더 출력
    header = f"{'키워드':<12}"
    for kw in top5_keywords:
        header += f" {kw:>10}"
    print(header)
    print("-" * 70)

    # 각 행 출력
    for kw1 in top5_keywords:
        row = f"{kw1:<12}"
        for kw2 in top5_keywords:
            if kw1 == kw2:
                row += f" {'-':>10}"
            else:
                count = matrix[kw1][kw2]
                row += f" {count:>10,}"
        print(row)

    return matrix, keyword_freq


def analyze_cross_occurrence(docs, source_name):
    """모든 대상 키워드 간 동시 출현 분석"""
    print(f"\n{'=' * 70}")
    print(f"{source_name} 데이터: 전체 주요 키워드 간 동시 출현 분석")
    print('=' * 70)

    matrix, keyword_freq = calculate_cooccurrence_matrix(docs, ALL_KEYWORDS)

    # 개별 출현 빈도
    print(f"\n[전체 주요 키워드 개별 출현 빈도]")
    print("-" * 50)
    sorted_keywords = sorted(ALL_KEYWORDS, key=lambda x: keyword_freq.get(x, 0), reverse=True)
    for kw in sorted_keywords:
        freq = keyword_freq.get(kw, 0)
        ratio = freq / len(docs) * 100 if docs else 0
        source_label = ""
        if kw in PAPER_TOP5 and kw in NEWS_TOP5:
            source_label = "[Paper+News]"
        elif kw in PAPER_TOP5:
            source_label = "[Paper]"
        else:
            source_label = "[News]"
        print(f"  {kw:<10} {source_label:<15}: {freq:,}회 ({ratio:.2f}%)")

    # 동시 출현 상세 분석
    print(f"\n[키워드별 동시 출현 상세]")
    for kw1 in sorted_keywords:
        if keyword_freq.get(kw1, 0) == 0:
            continue
        print(f"\n▶ {kw1} (출현: {keyword_freq.get(kw1, 0):,}회)")
        cooccur_list = []
        for kw2 in ALL_KEYWORDS:
            if kw1 != kw2 and matrix[kw1][kw2] > 0:
                cooccur_list.append((kw2, matrix[kw1][kw2]))
        cooccur_list.sort(key=lambda x: x[1], reverse=True)

        if cooccur_list:
            for kw2, count in cooccur_list:
                # kw1이 출현한 문서 중 kw2도 함께 출현한 비율
                ratio = count / keyword_freq.get(kw1, 1) * 100
                print(f"   - {kw2}: {count:,}회 (동시출현률: {ratio:.1f}%)")
        else:
            print("   (동시 출현 없음)")

    return matrix, keyword_freq


def create_summary_table(paper_docs, news_docs):
    """요약 테이블 생성"""
    print("\n" + "=" * 80)
    print("동시 출현 분석 요약 테이블")
    print("=" * 80)

    # Paper 분석
    paper_matrix, paper_freq = calculate_cooccurrence_matrix(paper_docs, ALL_KEYWORDS)
    # News 분석
    news_matrix, news_freq = calculate_cooccurrence_matrix(news_docs, ALL_KEYWORDS)

    results = []
    for kw1 in ALL_KEYWORDS:
        for kw2 in ALL_KEYWORDS:
            if kw1 < kw2:  # 중복 방지
                paper_count = paper_matrix[kw1][kw2]
                news_count = news_matrix[kw1][kw2]
                results.append({
                    '키워드1': kw1,
                    '키워드2': kw2,
                    'Paper동시출현': paper_count,
                    'News동시출현': news_count,
                    'Paper키워드1빈도': paper_freq.get(kw1, 0),
                    'Paper키워드2빈도': paper_freq.get(kw2, 0),
                    'News키워드1빈도': news_freq.get(kw1, 0),
                    'News키워드2빈도': news_freq.get(kw2, 0),
                })

    # 정렬: Paper 동시출현 기준 내림차순
    results.sort(key=lambda x: (x['Paper동시출현'] + x['News동시출현']), reverse=True)

    # 출력
    print(f"\n{'키워드1':<10} | {'키워드2':<10} | {'Paper동시출현':>12} | {'News동시출현':>12}")
    print("-" * 55)
    for r in results:
        if r['Paper동시출현'] > 0 or r['News동시출현'] > 0:
            print(f"{r['키워드1']:<10} | {r['키워드2']:<10} | {r['Paper동시출현']:>12,} | {r['News동시출현']:>12,}")

    return results


def main():
    """메인 실행"""
    init_dirs()

    print("=" * 70)
    print("상위 5개 키워드 동시 출현 분석")
    print("=" * 70)
    print(f"\nPaper 상위 5개: {PAPER_TOP5}")
    print(f"News 상위 5개: {NEWS_TOP5}")
    print(f"통합 키워드: {ALL_KEYWORDS}")

    # 데이터 로드
    print("\n[데이터 로드 중...]")
    paper_docs = extract_docs_with_keywords(source='paper')
    news_docs = extract_docs_with_keywords(source='news')

    print(f"  Paper 문서 수: {len(paper_docs):,}")
    print(f"  News 문서 수: {len(news_docs):,}")

    # 1. Paper 데이터에서 Paper 상위 5개 키워드 분석
    print_cooccurrence_analysis("Paper", paper_docs, PAPER_TOP5, "Paper", PAPER_TOP5)

    # 2. News 데이터에서 News 상위 5개 키워드 분석
    print_cooccurrence_analysis("News", news_docs, NEWS_TOP5, "News", NEWS_TOP5)

    # 3. Paper 데이터에서 전체 주요 키워드 분석
    analyze_cross_occurrence(paper_docs, "Paper")

    # 4. News 데이터에서 전체 주요 키워드 분석
    analyze_cross_occurrence(news_docs, "News")

    # 5. 요약 테이블
    summary = create_summary_table(paper_docs, news_docs)

    # 결과 저장
    output_file = OUTPUT_DIR / 'top5_cooccurrence_analysis.json'

    # Paper/News 매트릭스 저장
    paper_matrix, paper_freq = calculate_cooccurrence_matrix(paper_docs, ALL_KEYWORDS)
    news_matrix, news_freq = calculate_cooccurrence_matrix(news_docs, ALL_KEYWORDS)

    output_data = {
        'paper_top5': PAPER_TOP5,
        'news_top5': NEWS_TOP5,
        'all_keywords': ALL_KEYWORDS,
        'paper': {
            'doc_count': len(paper_docs),
            'keyword_freq': dict(paper_freq),
            'cooccurrence': {k1: dict(v) for k1, v in paper_matrix.items()}
        },
        'news': {
            'doc_count': len(news_docs),
            'keyword_freq': dict(news_freq),
            'cooccurrence': {k1: dict(v) for k1, v in news_matrix.items()}
        },
        'summary': summary
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n\n결과 저장 완료: {output_file}")


if __name__ == '__main__':
    main()
