"""
Phase 5 시각화: 키워드 조합별 맥락 워드클라우드
- 각 키워드 조합이 뉴스/논문에서 등장한 문서의 제목, 카테고리, 주요 키워드 등 텍스트를 유의어 전처리 후 워드클라우드로 시각화
"""

import json
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from config import normalize_keyword, VIZ_DIR, OUTPUT_DIR, init_dirs

# 분석 대상 키워드 쌍
TARGET_PAIRS = [
    ('인공지능', '혁신'),
    ('인공지능', '청년'),
    ('플랫폼', '혁신'),
    ('여성', '인공지능'),
]

# 파일 경로
JSON_PATH = OUTPUT_DIR / 'phase5_keyword_pair_mentions.json'


def preprocess_text(items, fields, exclude=None):
    """문서 리스트에서 지정 필드 텍스트를 유의어 정규화 후 합침 (불용어 제외)"""
    texts = []
    exclude = set(exclude or [])
    for item in items:
        for field in fields:
            value = item.get(field, '')
            if field == 'keywords':
                keywords = [normalize_keyword(k.strip()) for k in value.split(',') if k.strip()]
                texts.extend([k for k in keywords if k not in exclude])
            else:
                texts.append(str(value))
    return ' '.join(texts)


def visualize_wordcloud(text, title, save_path):
    wc = WordCloud(font_path='malgun.ttf', width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main():
    init_dirs()

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for pair in TARGET_PAIRS:
        pair_str = f'{pair[0]}-{pair[1]}'
        for source in ['news', 'paper']:
            items = data[source].get(pair_str, [])
            if not items:
                continue
            # 제목, 카테고리, 키워드 등 텍스트 합침
            fields = ['title', 'category', 'keywords', 'authors']
            # 조합 키워드를 불용어로 제외
            text = preprocess_text(items, fields, exclude=list(pair))
            save_path = VIZ_DIR / f'wordcloud_{source}_{pair_str}.png'
            title = f'{source.upper()} | {pair_str} 문서 맥락 워드클라우드'
            visualize_wordcloud(text, title, save_path)
            print(f'{save_path} 저장 완료')

if __name__ == '__main__':
    main()
