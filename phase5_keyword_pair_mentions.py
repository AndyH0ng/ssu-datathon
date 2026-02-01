"""
Phase 5: 특정 키워드 조합별 문서 발췌 및 정리
- 대상 키워드 조합: '인공지능-혁신', '인공지능-청년', '플랫폼-혁신', '여성-인공지능'
- 각 조합이 뉴스/논문 데이터에서 어디서 언급되는지 발췌
- 동의어 정규화 적용
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import json
from config import NEWS_FILES, PAPER_FILE, normalize_keyword

# 분석 대상 키워드 쌍
TARGET_PAIRS = [
    ('인공지능', '혁신'),
    ('인공지능', '청년'),
    ('플랫폼', '혁신'),
    ('여성', '인공지능'),
]


def extract_news_mentions():
    """뉴스 데이터에서 키워드 조합이 함께 언급된 문서 발췌"""
    results = {pair: [] for pair in TARGET_PAIRS}
    for file in NEWS_FILES:
        df = pd.read_excel(file)
        for idx, row in df.iterrows():
            keywords = [normalize_keyword(k.strip()) for k in str(row['키워드']).split(',') if k.strip()]
            keywords = set(keywords)
            for pair in TARGET_PAIRS:
                if pair[0] in keywords and pair[1] in keywords:
                    results[pair].append({
                        'index': idx,
                        'title': row.get('제목', ''),
                        'keywords': ', '.join(keywords),
                        'category': row.get('통합 분류1', ''),
                    })
    return results


def extract_paper_mentions():
    """논문 데이터에서 키워드 조합이 함께 언급된 문서 발췌"""
    results = {pair: [] for pair in TARGET_PAIRS}
    with open(PAPER_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for idx, item in enumerate(data['NODE_LIST']):
        kywd = item.get('KYWD', '')
        keywords = [normalize_keyword(k.strip()) for k in str(kywd).split(',') if k.strip()]
        keywords = set(keywords)
        for pair in TARGET_PAIRS:
            if pair[0] in keywords and pair[1] in keywords:
                results[pair].append({
                    'index': idx,
                    'title': item.get('TITLE', ''),
                    'keywords': ', '.join(keywords),
                    'authors': item.get('AUTHORS', ''),
                })
    return results


def main():
    print("Phase 5: 키워드 조합별 문서 발췌 및 정리")
    news_mentions = extract_news_mentions()
    paper_mentions = extract_paper_mentions()

    # 결과 요약 출력
    for pair in TARGET_PAIRS:
        print(f"\n{'='*60}\n키워드 조합: {pair[0]} - {pair[1]}")
        print(f"[뉴스 데이터] {len(news_mentions[pair])}건")
        for item in news_mentions[pair][:5]:  # 최대 5건 샘플
            print(f"  - 제목: {item['title']} | 카테고리: {item['category']} | 키워드: {item['keywords']}")
        print(f"[논문 데이터] {len(paper_mentions[pair])}건")
        for item in paper_mentions[pair][:5]:
            print(f"  - 제목: {item['title']} | 저자: {item['authors']} | 키워드: {item['keywords']}")

    # 결과 저장
    # tuple key를 문자열로 변환
    def tuple_key_to_str(d):
        return {f'{k[0]}-{k[1]}': v for k, v in d.items()}

    output = {
        'news': tuple_key_to_str(news_mentions),
        'paper': tuple_key_to_str(paper_mentions)
    }
    with open('phase5_keyword_pair_mentions.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n결과 저장 완료: phase5_keyword_pair_mentions.json")


if __name__ == '__main__':
    main()
