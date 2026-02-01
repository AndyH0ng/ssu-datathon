"""
분석 설정 파일 (config.py)
모든 상수, 설정값, 매핑을 한 곳에서 관리
"""

from pathlib import Path

# ============================================================
# 1. 경로 설정
# ============================================================

# 데이터 파일
NEWS_FILES = ['data/news_data.xlsx']
PAPER_FILE = 'data/datathon_data.json'

# 뉴스 카테고리 필터링 (통합 분류1 기준, 제외할 카테고리)
NEWS_EXCLUDE_CATEGORIES = [
    '정치>국회_정당',
    '정치>청와대',
    '정치>선거',
    '정치>외교',
    '정치>행정_자치',
    '사회>사건_사고',
]

# 출력 경로
OUTPUT_DIR = Path('output')
VIZ_DIR = Path('visualizations')
DOCS_DIR = Path('docs')


# ============================================================
# 2. 추출/분석 설정
# ============================================================

# TF-IDF 분석
NEWS_TFIDF_TOP_N = 500      # 뉴스 TF-IDF 상위 N개 키워드 추출
PAPER_TFIDF_TOP_N = 500     # 논문 TF-IDF 상위 N개 키워드 추출

# 공통 키워드 분석
COMMON_KEYWORD_TOP_N = 300  # 공통 키워드 비교 시 상위 N개 기준

# 간극 분석
GAP_NEWS_MIN_FREQ = 100     # 블루오션 판정 시 뉴스 최소 빈도
GAP_PAPER_MIN_FREQ = 50     # 학술선도 판정 시 논문 최소 빈도
GAP_BLUE_OCEAN_THRESHOLD = 5    # 블루오션 간극 지수 기준 (이상)
GAP_ACADEMIC_THRESHOLD = -1     # 학술선도 간극 지수 기준 (이하)

# 시각화
VIZ_TOP_N = 20              # 시각화에 표시할 상위 N개


# ============================================================
# 3. 동의어 매핑 (영어 → 한국어 통합)
# ============================================================

SYNONYM_MAP = {
    # 인공지능 관련
    'Artificial Intelligence': '인공지능',
    'Artificial intelligence': '인공지능',
    'artificial intelligence': '인공지능',
    'Artificial Intelligence(AI)': '인공지능',
    'Artificial Intelligence (AI)': '인공지능',
    'artificial intelligence (AI)': '인공지능',
    'AI': '인공지능',
    '인공지능(AI)': '인공지능',
    'Generative AI': '생성형AI',
    'generative AI': '생성형AI',
    'Generative Artificial Intelligence': '생성형AI',
    '생성형 인공지능': '생성형AI',
    '생성 AI': '생성형AI',
    'ChatGPT': '생성형AI',
    '챗GPT': '생성형AI',
    'Machine Learning': '머신러닝',
    'Machine learning': '머신러닝',
    'machine learning': '머신러닝',
    '기계학습': '머신러닝',
    'Deep Learning': '딥러닝',
    'deep learning': '딥러닝',
    'Deep learning': '딥러닝',
    'Big Data': '빅데이터',
    'Big data': '빅데이터',
    'big data': '빅데이터',
    '빅 데이터': '빅데이터',
    'Metaverse': '메타버스',
    'metaverse': '메타버스',
    '메타버스(Metaverse)': '메타버스',
    'Blockchain': '블록체인',
    'blockchain': '블록체인',
    'Blockchain Technology': '블록체인',
    'Digital Transformation': '디지털전환',
    'digital transformation': '디지털전환',
    'Digital transformation': '디지털전환',
    '디지털 전환': '디지털전환',
    '디지털 트랜스포메이션': '디지털전환',
    'DX': '디지털전환',
    'Digitalization': '디지털전환',
    '디지털화': '디지털전환',
    '4차 산업혁명': '4차산업혁명',
    '4th Industrial Revolution': '4차산업혁명',
    'Fourth Industrial Revolution': '4차산업혁명',
    'The Fourth Industrial Revolution': '4차산업혁명',
    'fourth industrial revolution': '4차산업혁명',
    '4th industrial revolution': '4차산업혁명',
    'Industry 4.0': '4차산업혁명',

    # 기후/환경 관련
    'climate crisis': '기후위기',
    'Climate Crisis': '기후위기',
    'Climate Change': '기후변화',
    'Climate change': '기후변화',
    'climate change': '기후변화',
    '기후 변화': '기후변화',
    'Climate Justice': '기후정의',
    'Climate justice': '기후정의',
    'Carbon Neutrality': '탄소중립',
    'Carbon neutrality': '탄소중립',
    'carbon neutrality': '탄소중립',
    'Green Growth': '녹색성장',
    'Renewable Energy': '재생에너지',
    'Environment': '환경',
    'Sustainability': '지속가능성',
    'sustainability': '지속가능성',
    'Sustainable Management': '지속가능경영',
    'ESG Management': 'ESG',
    'ESG management': 'ESG',
    'ESG 경영': 'ESG',
    'ESG경영': 'ESG',
    'ESG Rating': 'ESG등급',
    'ESG 등급': 'ESG등급',

    # 코로나19 관련
    'COVID-19': '코로나19',
    'Covid-19': '코로나19',
    'covid-19': '코로나19',
    'COVID19': '코로나19',
    '코로나 19': '코로나19',
    '코로나-19': '코로나19',
    '코로나바이러스감염증-19': '코로나19',
    '코로나': '코로나19',
    'Pandemic': '팬데믹',
    'pandemic': '팬데믹',
    'COVID-19 pandemic': '팬데믹',

    # 국가/지역
    'China': '중국',
    'Chinese': '중국',
    '中国': '중국',
    'Taiwan': '대만',
    'Korea': '한국',
    'South Korea': '한국',
    'North Korea': '북한',
    'Japan': '일본',
    '日本': '일본',
    'Russia': '러시아',
    'USA': '미국',
    'US': '미국',
    'U.S.': '미국',
    'United States': '미국',
    'the United States': '미국',
    'The United States': '미국',
    'the U.S.': '미국',
    'India': '인도',
    'Vietnam': '베트남',
    'EU': '유럽연합',
    'European Union': '유럽연합',
    '유럽연합(EU)': '유럽연합',
    'Africa': '아프리카',
    'Ukraine': '우크라이나',
    'Ukraine War': '우크라이나전쟁',
    '우크라이나 전쟁': '우크라이나전쟁',
    'Central Asia': '중앙아시아',
    'Latin America': '중남미',

    # 인구/사회
    'Depression': '우울',
    'depression': '우울',
    '우울감': '우울',
    '우울증': '우울',
    'Depressive Symptoms': '우울',
    'Satisfaction': '만족도',
    'satisfaction': '만족도',
    'Job Satisfaction': '직무만족',
    'job satisfaction': '직무만족',
    'Job satisfaction': '직무만족',
    '직무만족도': '직무만족',
    '직무 만족': '직무만족',
    '직무 만족도': '직무만족',
    'Life Satisfaction': '삶의만족도',
    'life satisfaction': '삶의만족도',
    'Life satisfaction': '삶의만족도',
    '삶의 만족도': '삶의만족도',
    '삶의 만족': '삶의만족도',
    '생활만족도': '삶의만족도',
    '생활만족': '삶의만족도',
    'Self-Efficacy': '자기효능감',
    'Self-efficacy': '자기효능감',
    'self-efficacy': '자기효능감',
    '자기 효능감': '자기효능감',
    '자아효능감': '자기효능감',
    'Self-Esteem': '자아존중감',
    'Self-esteem': '자아존중감',
    'self-esteem': '자아존중감',
    'Trust': '신뢰',
    'trust': '신뢰',
    'Happiness': '행복',
    'happiness': '행복',
    '행복감': '행복',
    'Empathy': '공감',
    'Resilience': '회복탄력성',
    'resilience': '회복탄력성',
    '리질리언스': '회복탄력성',
    '레질리언스': '회복탄력성',
    '적응유연성': '회복탄력성',
    'Grit': '그릿',
    'grit': '그릿',
    'Gender': '젠더',
    'gender': '젠더',
    'Youth': '청년',
    'youth': '청년',
    'Young Adults': '청년',
    'young adults': '청년',
    'Young adults': '청년',
    '청년층': '청년',
    '청년세대': '청년',
    'Young people': '청년',
    'young people': '청년',
    'Elderly': '노인',
    'elderly': '노인',
    'Older Adults': '노인',
    'Older adults': '노인',
    'older adults': '노인',
    '고령자': '노인',
    'Adolescents': '청소년',
    'adolescents': '청소년',
    'adolescent': '청소년',
    'Adolescent': '청소년',
    'Adolescence': '청소년',
    'MZ generation': 'MZ세대',
    'MZ Generation': 'MZ세대',
    'Generation MZ': 'MZ세대',
    'MZ generations': 'MZ세대',
    'Women': '여성',
    'women': '여성',
    'Female': '여성',
    'female': '여성',
    'Woman': '여성',
    'Social Support': '사회적지지',
    'social support': '사회적지지',
    'Social support': '사회적지지',
    '사회적 지지': '사회적지지',
    'Social Capital': '사회적자본',
    '사회적 자본': '사회적자본',
    'Quality of Life': '삶의 질',
    'Quality of life': '삶의 질',
    'Social Isolation': '사회적고립',
    '사회적 고립': '사회적고립',
    'Suicidal Ideation': '자살생각',
    'Aging': '고령화',
    'aging': '고령화',
    'aging population': '고령화',
    'aging society': '고령화',
    'population aging': '고령화',
    'Population Aging': '고령화',
    'ageing': '고령화',
    'Age Discrimination': '연령차별',
    'Disabled': '장애인',
    'People with Disabilities': '장애인',
    'people with disabilities': '장애인',
    'Persons with Disabilities': '장애인',
    'Persons with disabilities': '장애인',
    'The Disabled': '장애인',
    'Disabilities': '장애인',
    'disability': '장애인',
    'disabled person': '장애인',
    'disabled people': '장애인',
    'Individuals with Disabilities': '장애인',
    'Disability Acceptance': '장애수용',
    'Mental Health': '정신건강',
    'mental health': '정신건강',
    'Mental health': '정신건강',
    'Local Extinction': '지방소멸',
    'local extinction': '지방소멸',
    'Local extinction': '지방소멸',
    'Local Shrinking': '지방소멸',
    'Population Decline': '인구감소',
    'population decline': '인구감소',
    'Urban Regeneration': '도시재생',
    'urban regeneration': '도시재생',
    'Urban regeneration': '도시재생',
    'Balanced Regional Development': '지역균형발전',
    'Inequality': '불평등',
    'inequality': '불평등',
    'Fairness': '공정성',
    'Equality': '평등',
    'Human Rights': '인권',
    'human rights': '인권',
    'Human rights': '인권',
    'Human right': '인권',
    'fundamental rights': '기본권',
    'Freedom of Expression': '표현의자유',
    'freedom of expression': '표현의자유',
    'Freedom of expression': '표현의자유',
    'Freedom of Speech': '표현의자유',
    'freedom of speech': '표현의자유',
    'Freedom of speech': '표현의자유',
    '언론의 자유': '표현의자유',
    '표현의 자유': '표현의자유',
    'Defamation': '명예훼손',
    'defamation': '명예훼손',
    'Hate Speech': '혐오표현',
    'Populism': '포퓰리즘',
    'populism': '포퓰리즘',
    'Autocracy': '권위주의',
    'Rule of Law': '법치주의',
    'rule of law': '법치주의',

    # 경영/경제
    'Organizational Commitment': '조직몰입',
    'organizational commitment': '조직몰입',
    'Organizational commitment': '조직몰입',
    'Turnover Intention': '이직의도',
    'turnover intention': '이직의도',
    'Turnover intention': '이직의도',
    '이직 의도': '이직의도',
    'Purchase Intention': '구매의도',
    'Purchase intention': '구매의도',
    'Repurchase Intention': '재구매의도',
    'Behavioral intention': '행동의도',
    'Behavioral Intention': '행동의도',
    'Customer Satisfaction': '고객만족',
    'Customer satisfaction': '고객만족',
    'customer satisfaction': '고객만족',
    'Service Quality': '서비스품질',
    '서비스 품질': '서비스품질',
    'Innovative Behavior': '혁신행동',
    'Financial Performance': '재무성과',
    'Corporate Social Responsibility': '기업의 사회적 책임',
    '사회적 책임': '기업의 사회적 책임',
    'CSR': '기업의 사회적 책임',
    'SMEs': '중소기업',
    'SME': '중소기업',
    'Small and Medium-sized Enterprises (SMEs)': '중소기업',
    'Small and Medium Enterprises': '중소기업',
    'small and medium-sized enterprises': '중소기업',
    'Small and Medium-sized Enterprises(SMEs)': '중소기업',
    'Firm Value': '기업가치',
    'firm value': '기업가치',
    'Firm value': '기업가치',
    'Corporate Value': '기업가치',
    'corporate value': '기업가치',
    '기업 가치': '기업가치',
    'Tobin’s Q': '기업가치',
    'Corporate Governance': '지배구조',
    'Governance': '거버넌스',
    'governance': '거버넌스',
    'Innovation': '혁신',
    'innovation': '혁신',
    'Entrepreneurship': '기업가정신',
    'entrepreneurship': '기업가정신',
    '기업가 정신': '기업가정신',
    'Entrepreneurial Intention': '창업의도',
    '창업의지': '창업의도',
    'Startup': '스타트업',
    'Startups': '스타트업',
    'startup': '스타트업',
    'Start-up': '스타트업',
    'startups': '스타트업',
    'Venture Capital': '벤처캐피탈',
    'Venture capital': '벤처캐피탈',
    '벤처캐피털': '벤처캐피탈',
    'Platform': '플랫폼',
    'platform': '플랫폼',
    'Platforms': '플랫폼',
    'platforms': '플랫폼',
    'Youtube': '유튜브',
    '유튜브(YouTube)': '유튜브',
    'Influencer': '인플루언서',
    'Influencers': '인플루언서',
    'Netflix': '넷플릭스',
    'OTT 서비스': 'OTT',
    'Job Stress': '직무스트레스',
    'Job stress': '직무스트레스',
    'job stress': '직무스트레스',
    'Burnout': '소진',
    'burnout': '소진',
    '직무소진': '소진',
    'Emotional Labor': '감정노동',
    'Emotional labor': '감정노동',
    'Public Service Motivation': '공공봉사동기',
    'Dynamic Capabilities': '동적역량',
    'Smart Contract': '스마트계약',
    'smart contract': '스마트계약',
    'Smart contract': '스마트계약',
    'Cryptocurrency': '암호화폐',
    'Virtual Assets': '가상자산',
    'NFT': 'NFT',
    'Kim Jong-un': '김정은',
    'Kim Jong Un': '김정은',
    'Kim Il-sung': '김일성',
    'Korean Peninsula': '한반도',

    # 연구방법
    'Mediating Effect': '매개효과',
    'Moderating Effect': '조절효과',
    'Case Study': '사례연구',
    'case study': '사례연구',
    'Text Mining': '텍스트마이닝',
    'Text mining': '텍스트마이닝',
    'text mining': '텍스트마이닝',
    '텍스트 마이닝': '텍스트마이닝',
    'Topic Modeling': '토픽모델링',
    'topic modeling': '토픽모델링',
    'Topic modeling': '토픽모델링',
    '토픽 모델링': '토픽모델링',
    'Semantic Network Analysis': '의미연결망분석',
    'Semantic network analysis': '의미연결망분석',
    '의미연결망 분석': '의미연결망분석',
    'CONCOR analysis': 'CONCOR분석',
    'CONCOR 분석': 'CONCOR분석',
    'Sentiment Analysis': '감성분석',
    'Latent Class Analysis': '잠재계층분석',
    'latent profile analysis': '잠재프로파일분석',
    '잠재프로파일': '잠재프로파일분석',

    # 기타
    'Social Media': '소셜미디어',
    'Media': '미디어',
    'Education': '교육',
    'Autonomy': '자율성',
    'Perceived Value': '지각된가치',
    'perceived value': '지각된가치',
    'Perceived value': '지각된가치',
    '지각된 가치': '지각된가치',
    'Perceived Usefulness': '지각된유용성',
    '지각된 유용성': '지각된유용성',
    'Risk Perception': '위험인식',
    '위험지각': '위험인식',
    'Income': '소득',
    'income': '소득',
    'health': '건강',
    'Copyright': '저작권',
    'Decentralization': '탈중앙화',
    'Transparency': '투명성',
    'AI ethics': 'AI윤리',
    'AI 윤리': 'AI윤리',
    'Instructional Design': '교수설계',
    'AI Education': 'AI교육',
    '인공지능 교육': 'AI교육',
    'AI literacy': 'AI리터러시',
    'AI 리터러시': 'AI리터러시',
    'Elementary Education': '초등교육',
    'information quality': '정보품질',
    'Interactivity': '상호작용성',
    'Flow': '플로우',
    'Parental mediation': '부모중재',
    'Self-regulation': '자율규제',
    'Platform Labor': '플랫폼노동',
    '플랫폼 노동자': '플랫폼노동자',
    'Platform Workers': '플랫폼노동자',
    'Business Model': '비즈니스모델',
    'Regulation': '규제',
    '국가규제': '규제',
    'Export': '수출',
    'Firm Size': '기업규모',
    'Market Orientation': '시장지향성',
    'Performance': '성과',
    '기업성과': '경영성과',
    'Government Support': '정부지원',
    'Early Childhood Teacher': '유아교사',
    'social workers': '사회복지사',
    '항공사 승무원': '객실승무원',
    'Customer Orientation': '고객지향성',
    'Social Connectedness': '사회적연결감',
    '사회적 연결감': '사회적연결감',
    'Team Trust': '팀신뢰',
    'Communication': '의사소통',
    'Military Life Satisfaction': '군생활만족',
    '군 생활 만족': '군생활만족',
    'Organizational Justice': '조직공정성',
    'Proactive Personality': '주도적성향',
    'MZ Generation Soldiers': 'MZ세대장병',
    'Characteristics of MZ Generation': 'MZ세대특성',
    'Mental Force': '정신전력',
    'Transformational Leadership': '변혁적리더십',
    '변혁적 리더십': '변혁적리더십',
    'Authoritarian Leadership': '권위주의적리더십',
    'Leader Ability': '리더능력',
    'Task Performance': '과업성과',
    'Creativity': '창의성',
    'Defense Artificial Intelligence': '국방인공지능',
    '국방 인공지능': '국방인공지능',
    'Intelligent Robot': '지능형로봇',
    'role conception': '역할인식',
    'image': '이미지',
    'ROK-US alliance': '한미동맹',
    'alliance conflict': '동맹갈등',
    'WMD Elimination': 'WMD제거',
    'Biological Weapons': '생물무기',
    'OR': 'OR기법',
    'M&S': 'M&S',
    'Combat Victory Factors': '전투승리요인',
    'Brigade-Level KCTC Bigdata': '여단급KCTC빅데이터',
    'Factor Analysis': '요인분석',
    'Offensive Operation': '공격작전',
    'Regression Analysis': '회귀분석',
    'Behavioral Economics': '행동경제학',
    'Heuristic': '휴리스틱',
    'Prospect Theory': '전망이론',
    'SMART NAVY': '스마트해군',
    'military organization culture': '군조직문화',
    'interaction effect': '상호작용효과',
    'mine action': '지뢰대응행동',
    'national mine action authority': '국가지뢰정책감독기구',
    'mine action center': '지뢰행동센터',
    'UCAVs': '무인전투기',
    'Concept of Operations': '작전운용개념',
    'Operation Object': '운용대상',
    'Purpose of Operation': '운용목적',
    'Mission Priority': '임무우선순위',
    'Brexit': '브렉시트',
    'Global Britain': '글로벌브리튼',
    'AUKUS': '오커스',
    'Foreign Policy': '외교정책',
    'Fake News on North Korea': '북한관련가짜뉴스',
    'Fake News Discernment': '가짜뉴스식별력',
    'Right Wing Authoritarianism': '우익권위주의',
    'Social Dominance Orientation': '사회지배지향성',
    'System Justification': '체제정당화',
    'Symbolic Ideology': '상징적이념',
    'Revolution in Military Affairs': '군사혁신',
    'Modern War': '현대전',
    'Total War': '총력전',
    'Defense Science and Technology': '국방과학기술',
    'Military R&D': '군사R&D',
    'The transition period': '전환기',
    'Security environment': '안보환경',
    'National defense policy': '국방정책',
    'Roh Taewoo administration': '노태우정부',
    'Kim Youngsam administration': '김영삼정부',
    'Total Force': '총체전력',
    'Reserve Forces': '예비전력',
    'Mobilization Division': '동원사단',
    'Selected Reserves': '선발예비군',
    'Army Mobilization Force Command': '육군동원전력사령부',
    'Hard Power': '하드파워',
    'Soft Power': '소프트파워',
    'Smart Power': '스마트파워',
    'the Effectiveness and Roles of Aircraft Carriers': '항공모함의유용성과역할',
    'Korea-U.S. Combined command structure': '한미연합지휘구조',
    'transfer of wartime OPCON': '전작권전환',
    'autonomy-security trade-off theory': '자율성안보교환이론',
    'future CFC': '미래연합사',
    'Korea joint force command': '합동군사령부',
    'Migrants as the Threat of Terrorism': '테러위협으로서의이주민',
    'Perception on migrants': '이주민인식',
    'National Sentiment': '국민정서',
    'National security': '국가안보',
    'Logistic regression': '로지스틱회귀분석',
    'Syrian Civil War': '시리아내전',
    'war termination': '전쟁종결',
    'prolonging of wars': '전쟁장기화',
    'veto players': '거부권자',
    'Indo-Pakistan Rivalry': '인도파키스탄갈등',
    'US-Soviet Union Rivalry': '미소갈등',
    'Sino-US Rapprochement': '미중화해',
    'Nuclear Proliferation': '핵확산',
    'Independence of Bangladesh': '방글라데시독립',
    'Neorealism': '신현실주의',
    'Balance of Power': '세력균형',
    'Distribution of Capability': '능력분포',
    'Perception': '인식',
    'Kenneth N. Waltz': '케네스월츠',
    'National crisis management systems': '국가위기관리체계',
    'Event-related policy change model': '사건중심정책변동모형',
    'focusing events': '초점사건',
    'Visibility': '가시성',
    'Government responsibility': '정부책임성',
    'New Space': '뉴스페이스',
    'Space Security': '우주안보',
    'Space Development Promotion Act': '우주개발진흥법',
    'Defense Acquisition Act': '방위사업법',
    'Integrated Defense Act': '통합방위법',
    'Unmanned Aerial Vehicle': '무인항공기',
    'Unmanned Aerial Systems': '무인항공시스템',
    'Drone': '드론',
    'Export Control': '수출통제',
    'Export Policy': '수출정책',
    'MTCR': '미사일기술통제체제',
    'digital literacy': '디지털리터러시',
    '디지털 리터러시': '디지털리터러시',
    'leadership': '리더십',
    'risk-taking tendency': '위험감수성향',
    'Strategic Culture': '전략문화',
    'Identity': '정체성',
    'Threat Perception': '위협인식',
    'Security Policy': '안보정책',
    'Strategic Choice': '전략적선택',
    'Identity of Korean People’s Army': '조선인민군정체성',
    'Formation and change of the identity of North Korean military': '북한군정체성형성및변화',
    'KPA Identity from the Perspective of Constructivism': '구성주의관점에서의인민군정체성',
    'ROK-US Alliance': '한미동맹',
    'Comprehensive Strategic Alliance': '포괄적전략동맹',
    'Integrated Alliance': '통합동맹',
    'Alliance Coherence': '동맹견고성',
    'New Generation Artificial Intelligence Development Plan': '차세대인공지능발전규획',
    'Central-Local Relations': '중앙지방관계',
    'Bottom Up Innovation': '상향식혁신',
    'RMA': '군사혁신',
    'Korean RMA': '한국군사혁신',
    'Discourse Analysis': '담론분석',
    'Structural Topic Model': '구조토픽모델',
    'National defense reform': '국방개혁',
    'Defense innovation 4.0': '국방혁신4.0',
    'Reserve war power': '예비전력',
    'Regular army': '상비전력',
    'Mobilization war power': '동원전력',
    'Refine reserve war power': '예비전력정예화'
}


# ============================================================
# 4. 불용어 목록
# ============================================================

STOPWORDS = {
    '대통령', '이재명', '윤석열', '한덕수', '이준석', '안철수', '재판', 'A씨', 'B씨',
    '살해', '살인', '폭행', '치사', '항소', '특검', '더불어민주당', '민주당', '국민의힘', '국힘', '여야',
    '매개효과', '조절효과', '조절된 매개효과', '근거이론', '질적 연구', '질적연구',
    '사례연구', '메타분석', '내용분석', '현상학적 연구', 'AHP', 'IPA',
    '잠재프로파일분석', '군집분석', '네트워크 분석', '연구동향', 'research trends',
    '중국', '미국', '일본', '러시아', '북한', '유럽연합',
}


# ============================================================
# 5. 분석 대상 키워드 (동시 출현 분석용)
# ============================================================

TOPIC_KEYWORDS = [
    # 기술/트렌드
    '인공지능', '기후변화', 'ESG', '메타버스', '디지털전환', '블록체인',
    '코로나19', '탄소중립', '4차산업혁명', '빅데이터', '머신러닝', '생성형AI',

    # 인구/세대
    '노인', '청년', '청소년', 'MZ세대', '고령화', '여성', '젠더', '장애인',

    # 심리/복지
    '우울', '정신건강', '행복', '삶의만족도', '회복탄력성', '자기효능감',
    '직무만족', '이직의도', '직무스트레스', '소진',

    # 경제/경영
    '중소기업', '스타트업', '기업가치', '기업가정신', '혁신',
    '플랫폼', '유튜브', 'OTT',

    # 사회/정치
    '민주주의', '인권', '표현의자유', '불평등', '도시재생', '지방소멸',
]


# ============================================================
# 6. 카테고리 분류 (시각화용)
# ============================================================

KEYWORD_CATEGORIES = {
    '기술/트렌드': ['인공지능', '메타버스', '블록체인', '빅데이터', '생성형AI', '디지털전환', '4차산업혁명'],
    '인구/세대': ['청년', '노인', '청소년', 'MZ세대', '여성', '장애인', '고령화', '젠더'],
    '심리/복지': ['우울', '행복', '정신건강', '직무만족', '회복탄력성', '자기효능감', '이직의도', '직무스트레스', '소진', '삶의만족도'],
    '환경/지속가능': ['기후변화', 'ESG', '탄소중립'],
    '경제/경영': ['중소기업', '스타트업', '기업가치', '기업가정신', '혁신', '플랫폼', '유튜브', 'OTT'],
    '사회/정치': ['민주주의', '인권', '표현의자유', '불평등', '도시재생', '지방소멸'],
    '국제': ['미국', '중국', '일본', '북한', '러시아', '유럽연합'],
}

CATEGORY_COLORS = {
    '기술/트렌드': '#3498db',
    '인구/세대': '#2ecc71',
    '심리/복지': '#9b59b6',
    '환경/지속가능': '#1abc9c',
    '경제/경영': '#f1c40f',
    '사회/정치': '#e67e22',
    '국제': '#e74c3c',
}


# ============================================================
# 7. 유틸리티 함수
# ============================================================

def normalize_keyword(keyword):
    """키워드 정규화 (동의어 매핑 적용)"""
    kw = keyword.strip()
    return SYNONYM_MAP.get(kw, kw)


def is_valid_keyword(keyword):
    """유효한 키워드인지 확인"""
    if not keyword or len(keyword) < 2:
        return False
    if keyword in STOPWORDS:
        return False
    if keyword.isdigit():
        return False
    if len(keyword) > 30:
        return False
    return True


def init_dirs():
    """출력 디렉토리 생성"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    VIZ_DIR.mkdir(exist_ok=True)
    DOCS_DIR.mkdir(exist_ok=True)


# ============================================================
# 8. 설정 요약 출력
# ============================================================

def print_config():
    """현재 설정 출력"""
    print("=" * 60)
    print("분석 설정 (config.py)")
    print("=" * 60)
    print(f"\n[데이터]")
    print(f"  뉴스 파일: {NEWS_FILES}")
    print(f"  논문 파일: {PAPER_FILE}")

    print(f"\n[추출/분석 설정]")
    print(f"  TF-IDF 상위 추출: 뉴스 {NEWS_TFIDF_TOP_N}개 / 논문 {PAPER_TFIDF_TOP_N}개")
    print(f"  공통 키워드 비교 기준: 상위 {COMMON_KEYWORD_TOP_N}개")
    print(f"  시각화 표시 개수: {VIZ_TOP_N}개")

    print(f"\n[간극 분석 기준]")
    print(f"  블루오션 판정: 뉴스 빈도 > {GAP_NEWS_MIN_FREQ}, 간극 지수 > {GAP_BLUE_OCEAN_THRESHOLD}")
    print(f"  학술선도 판정: 논문 빈도 > {GAP_PAPER_MIN_FREQ}, 간극 지수 < {GAP_ACADEMIC_THRESHOLD}")

    print(f"\n[키워드 처리]")
    print(f"  동의어 매핑: {len(SYNONYM_MAP)}개")
    print(f"  불용어: {len(STOPWORDS)}개")
    print(f"  분석 대상 키워드: {len(TOPIC_KEYWORDS)}개")
    print(f"  카테고리: {len(KEYWORD_CATEGORIES)}개")
    print("=" * 60)


if __name__ == '__main__':
    print_config()
