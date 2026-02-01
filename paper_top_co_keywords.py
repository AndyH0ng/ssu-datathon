"""
논문(paper) 데이터에서 '인공지능', '청년', '여성' 키워드와 함께 많이 언급된 키워드 분석 및 시각화
- 각 키워드별로 동시 등장 빈도 상위 키워드 집계
- bar plot으로 시각화
"""


import json
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from collections import Counter
from config import PAPER_FILE, normalize_keyword

# 한글 폰트 설정 (malgun.ttf가 같은 폴더에 있어야 함)
import os
font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'malgun.ttf')
if os.path.exists(font_path):
    plt.rcParams['font.family'] = font_manager.FontProperties(fname=font_path).get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    print('경고: malgun.ttf 폰트 파일이 없으면 한글이 깨질 수 있습니다.')

TARGET_KEYWORDS = ['인공지능', '청년', '여성']


def load_paper_docs():
    with open(PAPER_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    docs = []
    for item in data['NODE_LIST']:
        kywd = item.get('KYWD', '')
        keywords = [normalize_keyword(k.strip()) for k in str(kywd).split(',') if k.strip()]
        docs.append(set(keywords))
    return docs


def get_co_keywords(docs, target):
    counter = Counter()
    for doc in docs:
        if target in doc:
            for kw in doc:
                if kw != target:
                    counter[kw] += 1
    return counter


def plot_top_keywords(counter, target, top_n=15):
    most_common = counter.most_common(top_n)
    if not most_common:
        print(f"'{target}'와 함께 등장한 키워드가 없습니다.")
        return
    labels, values = zip(*most_common)
    plt.figure(figsize=(10, 5))
    plt.barh(labels[::-1], values[::-1], color='skyblue')
    plt.title(f"논문에서 '{target}'와 함께 많이 등장한 키워드")
    plt.xlabel('동시 등장 문서 수')
    plt.tight_layout()
    plt.savefig(f'paper_top_co_keywords_{target}.png')
    plt.close()
    print(f"paper_top_co_keywords_{target}.png 저장 완료")


def main():
    docs = load_paper_docs()
    for target in TARGET_KEYWORDS:
        counter = get_co_keywords(docs, target)
        print(f"\n'{target}'와 함께 많이 등장한 키워드 TOP 15:")
        for kw, cnt in counter.most_common(15):
            print(f"  {kw}: {cnt}회")
        plot_top_keywords(counter, target)

if __name__ == '__main__':
    main()
