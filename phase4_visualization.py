"""
Phase 4: 시각화
- 간극 분석 차트
- 키워드 빈도 비교
- 산점도 (뉴스 vs 논문)
- 동시 출현 히트맵
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# config에서 설정 import
from config import (
    OUTPUT_DIR, VIZ_DIR,
    VIZ_TOP_N, KEYWORD_CATEGORIES, CATEGORY_COLORS,
    GAP_NEWS_MIN_FREQ, GAP_PAPER_MIN_FREQ,
    GAP_BLUE_OCEAN_THRESHOLD, GAP_ACADEMIC_THRESHOLD,
    TOPIC_KEYWORDS,
    init_dirs
)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    """분석 결과 로드"""
    with open(OUTPUT_DIR / 'gap_analysis.json', 'r', encoding='utf-8') as f:
        gap_data = json.load(f)

    with open(OUTPUT_DIR / 'news_tfidf.json', 'r', encoding='utf-8') as f:
        news_tfidf = json.load(f)

    with open(OUTPUT_DIR / 'paper_tfidf.json', 'r', encoding='utf-8') as f:
        paper_tfidf = json.load(f)

    with open(OUTPUT_DIR / 'news_cooccurrence.json', 'r', encoding='utf-8') as f:
        news_cooccur = json.load(f)

    with open(OUTPUT_DIR / 'paper_cooccurrence.json', 'r', encoding='utf-8') as f:
        paper_cooccur = json.load(f)

    return gap_data, news_tfidf, paper_tfidf, news_cooccur, paper_cooccur


def plot_gap_analysis(gap_data):
    """간극 분석 바 차트"""
    print("1. 간극 분석 차트 생성 중...")

    blue_ocean = [g for g in gap_data
                  if g['news_freq'] > GAP_NEWS_MIN_FREQ and g['gap_index'] > GAP_BLUE_OCEAN_THRESHOLD][:15]
    academic = [g for g in gap_data
                if g['paper_freq'] > GAP_PAPER_MIN_FREQ and g['gap_index'] < GAP_ACADEMIC_THRESHOLD]
    academic = sorted(academic, key=lambda x: x['gap_index'])[:15]

    combined = blue_ocean + academic
    combined = sorted(combined, key=lambda x: x['gap_index'], reverse=True)

    keywords = [d['keyword'] for d in combined]
    gaps = [d['gap_index'] for d in combined]
    colors = ['#2ecc71' if g > 0 else '#e74c3c' for g in gaps]

    fig, ax = plt.subplots(figsize=(12, 10))
    bars = ax.barh(keywords, gaps, color=colors)

    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.set_xlabel('간극 지수 (사회적 주목도 - 학술적 연구도)', fontsize=12)
    ax.set_title('블루오션 vs 학술선도 연구 주제\n(+: 사회적 주목도↑ 학술적 연구도↓ / -: 학술적 연구도↑ 사회적 주목도↓)', fontsize=14)

    for bar, gap in zip(bars, gaps):
        width = bar.get_width()
        label_x = width + 2 if width > 0 else width - 2
        ha = 'left' if width > 0 else 'right'
        ax.text(label_x, bar.get_y() + bar.get_height()/2,
                f'{gap:.1f}', ha=ha, va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(VIZ_DIR / '1_gap_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  저장: {VIZ_DIR / '1_gap_analysis.png'}")


def plot_scatter_comparison(gap_data):
    """산점도: 뉴스 비율 vs 논문 비율"""
    print("2. 산점도 생성 중...")

    valid = [g for g in gap_data if g['news_freq'] > 50 or g['paper_freq'] > 30]

    news_ratios = [g['news_ratio'] for g in valid]
    paper_ratios = [g['paper_ratio'] for g in valid]
    keywords = [g['keyword'] for g in valid]

    fig, ax = plt.subplots(figsize=(12, 10))
    scatter = ax.scatter(news_ratios, paper_ratios, alpha=0.6, s=100, c='steelblue')

    max_val = max(max(news_ratios), max(paper_ratios))
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, label='균형선')

    # config.py의 TOPIC_KEYWORDS 사용 (데이터 변경 시 자동 반영)
    for i, kw in enumerate(keywords):
        if kw in TOPIC_KEYWORDS:
            ax.annotate(kw, (news_ratios[i], paper_ratios[i]),
                       fontsize=9, ha='left', va='bottom',
                       xytext=(5, 5), textcoords='offset points')

    ax.set_xlabel('사회적 주목도 (1000 문서당 출현 수)', fontsize=12)
    ax.set_ylabel('학술적 연구도 (1000 문서당 출현 수)', fontsize=12)
    ax.set_title('사회적 주목도 vs 학술적 연구도\n(대각선 위: 학술 선도 / 대각선 아래: 블루오션)', fontsize=14)

    ax.fill_between([0, max_val], [0, max_val], [max_val, max_val],
                    alpha=0.1, color='green', label='학술 선도 영역')
    ax.fill_between([0, max_val], [0, 0], [0, max_val],
                    alpha=0.1, color='blue', label='블루오션 영역')

    ax.legend(loc='upper right')
    ax.set_xlim(0, None)
    ax.set_ylim(0, None)

    plt.tight_layout()
    plt.savefig(VIZ_DIR / '2_scatter_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  저장: {VIZ_DIR / '2_scatter_comparison.png'}")


def plot_tfidf_comparison(news_tfidf, paper_tfidf):
    """TF-IDF 상위 키워드 비교"""
    print("3. TF-IDF 비교 차트 생성 중...")

    fig, axes = plt.subplots(1, 2, figsize=(16, 10))

    news_top = news_tfidf['tfidf'][:VIZ_TOP_N]
    news_kw = [d['keyword'] for d in news_top]
    news_scores = [d['score'] / 1000 for d in news_top]

    axes[0].barh(news_kw[::-1], news_scores[::-1], color='steelblue')
    axes[0].set_xlabel('TF-IDF Score (×1000)', fontsize=11)
    axes[0].set_title(f'뉴스 TF-IDF 상위 {VIZ_TOP_N}', fontsize=13)

    paper_top = paper_tfidf['tfidf'][:VIZ_TOP_N]
    paper_kw = [d['keyword'] for d in paper_top]
    paper_scores = [d['score'] for d in paper_top]

    axes[1].barh(paper_kw[::-1], paper_scores[::-1], color='coral')
    axes[1].set_xlabel('TF-IDF Score', fontsize=11)
    axes[1].set_title(f'논문 TF-IDF 상위 {VIZ_TOP_N}', fontsize=13)

    plt.tight_layout()
    plt.savefig(VIZ_DIR / '3_tfidf_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  저장: {VIZ_DIR / '3_tfidf_comparison.png'}")


def plot_cooccurrence_heatmap(news_cooccur, paper_cooccur):
    """동시 출현 히트맵"""
    print("4. 동시 출현 히트맵 생성 중...")

    # config.py의 TOPIC_KEYWORDS에서 상위 10개 사용 (히트맵 가독성)
    main_keywords = TOPIC_KEYWORDS[:10]

    def build_matrix(cooccur_data, keywords):
        matrix = []
        for kw1 in keywords:
            row = []
            for kw2 in keywords:
                if kw1 == kw2:
                    row.append(cooccur_data.get(kw1, {}).get('freq', 0))
                elif kw1 in cooccur_data:
                    cooccur_list = cooccur_data[kw1].get('top_cooccur', [])
                    val = 0
                    for item in cooccur_list:
                        if item['keyword'] == kw2:
                            val = item['count']
                            break
                    row.append(val)
                else:
                    row.append(0)
            matrix.append(row)
        return matrix

    news_matrix = build_matrix(news_cooccur, main_keywords)
    paper_matrix = build_matrix(paper_cooccur, main_keywords)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    im1 = axes[0].imshow(news_matrix, cmap='Blues')
    axes[0].set_xticks(range(len(main_keywords)))
    axes[0].set_yticks(range(len(main_keywords)))
    axes[0].set_xticklabels(main_keywords, rotation=45, ha='right')
    axes[0].set_yticklabels(main_keywords)
    axes[0].set_title('뉴스 키워드 동시 출현\n(대각선: freq, 비대각선: count)', fontsize=13)
    cbar1 = plt.colorbar(im1, ax=axes[0], shrink=0.8)
    cbar1.set_label('동시 출현 수 (count)', fontsize=10)

    im2 = axes[1].imshow(paper_matrix, cmap='Oranges')
    axes[1].set_xticks(range(len(main_keywords)))
    axes[1].set_yticks(range(len(main_keywords)))
    axes[1].set_xticklabels(main_keywords, rotation=45, ha='right')
    axes[1].set_yticklabels(main_keywords)
    axes[1].set_title('논문 키워드 동시 출현\n(대각선: freq, 비대각선: count)', fontsize=13)
    cbar2 = plt.colorbar(im2, ax=axes[1], shrink=0.8)
    cbar2.set_label('동시 출현 수 (count)', fontsize=10)

    plt.tight_layout()
    plt.savefig(VIZ_DIR / '4_cooccurrence_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  저장: {VIZ_DIR / '4_cooccurrence_heatmap.png'}")


def plot_category_comparison(gap_data):
    """카테고리별 간극 비교"""
    print("5. 카테고리별 비교 차트 생성 중...")

    gap_dict = {g['keyword']: g for g in gap_data}

    fig, ax = plt.subplots(figsize=(14, 8))

    x_positions = []
    x_labels = []
    colors_list = []
    values = []
    pos = 0

    for cat, keywords in KEYWORD_CATEGORIES.items():
        for kw in keywords:
            if kw in gap_dict:
                x_positions.append(pos)
                x_labels.append(kw)
                values.append(gap_dict[kw]['gap_index'])
                colors_list.append(CATEGORY_COLORS[cat])
                pos += 1
        pos += 0.5

    bars = ax.bar(x_positions, values, color=colors_list, width=0.8)

    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('간극 지수', fontsize=12)
    ax.set_title('카테고리별 간극 분석\n(+: 블루오션 / -: 학술선도)', fontsize=14)

    legend_elements = [Patch(facecolor=CATEGORY_COLORS[cat], label=cat)
                       for cat in KEYWORD_CATEGORIES.keys()]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(VIZ_DIR / '5_category_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  저장: {VIZ_DIR / '5_category_comparison.png'}")


def plot_frequency_comparison(gap_data):
    """빈도 비교 (뉴스 vs 논문)"""
    print("6. 빈도 비교 차트 생성 중...")

    # config.py의 TOPIC_KEYWORDS 사용 (데이터에 있는 것만 필터링)
    gap_dict = {g['keyword']: g for g in gap_data}

    keywords = [kw for kw in TOPIC_KEYWORDS if kw in gap_dict]
    news_freq = [gap_dict[kw]['news_freq'] for kw in keywords]
    paper_freq = [gap_dict[kw]['paper_freq'] for kw in keywords]

    x = np.arange(len(keywords))
    width = 0.35

    fig, ax = plt.subplots(figsize=(14, 8))

    bars1 = ax.bar(x - width/2, news_freq, width, label='뉴스', color='steelblue')
    bars2 = ax.bar(x + width/2, paper_freq, width, label='논문', color='coral')

    ax.set_ylabel('문서 출현 수 (freq)', fontsize=12)
    ax.set_title('주요 키워드별 문서 출현 수 비교\n(뉴스: 사회적 주목도 / 논문: 학술적 연구도)', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(keywords, rotation=45, ha='right', fontsize=10)
    ax.legend()
    ax.set_yscale('log')

    plt.tight_layout()
    plt.savefig(VIZ_DIR / '6_frequency_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  저장: {VIZ_DIR / '6_frequency_comparison.png'}")


def main():
    print("\n" + "#" * 60)
    print("#  Phase 4: 시각화")
    print("#" * 60)

    init_dirs()

    print("\n데이터 로딩 중...")
    gap_data, news_tfidf, paper_tfidf, news_cooccur, paper_cooccur = load_data()

    print("\n시각화 생성 중...\n")

    plot_gap_analysis(gap_data)
    plot_scatter_comparison(gap_data)
    plot_tfidf_comparison(news_tfidf, paper_tfidf)
    plot_cooccurrence_heatmap(news_cooccur, paper_cooccur)
    plot_category_comparison(gap_data)
    plot_frequency_comparison(gap_data)

    print("\n" + "#" * 60)
    print("#  Phase 4 완료!")
    print(f"#  시각화 파일: {VIZ_DIR}/")
    print("#" * 60)


if __name__ == '__main__':
    main()
