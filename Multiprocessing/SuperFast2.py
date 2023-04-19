import os
import sys
import grequests
import requests
import json
import pandas as pd
import multiprocessing
import concurrent.futures
from bs4 import BeautifulSoup
import re

# 재귀 최대 깊이를 바꾸었다.
sys.setrecursionlimit(10000)

class DaumNewsCrawler:
    # 카테고리 탐색을 위한 변수이다.
    CATEGORIES = {
        'economic': ['경제', {
            'finance': '금융',
            'industry': '기업산업',
            'employ': '취업직장인',
            'others': '경제일반',
            'autos': '자동차',
            'stock': '주식',
            'stock/market': '시황분석',
            'stock/publicnotice': '공시',
            'stock/world': '해외증시',
            'stock/bondsfutures': '채권선물',
            'stock/fx': '외환',
            'stock/others': '주식일반',
            'estate': '부동산',
            'consumer': '생활경제',
            'world': '국제경제'
        }],
        'digital': ['IT', {
            'internet': '인터넷',
            'science': '과학',
            'game': '게임',
            'it': '휴대폰통신',
            'device': 'IT기기',
            'mobile': '통신_모바일',
            'software': '소프트웨어',
            'others': 'Tech일반'
        }],
        'culture': ['문화', {
            'health': '건강',
            'life': '생활정보',
            'art': '공연/전시',
            'book': '책',
            'leisure': '여행레져',
            'others': '문화생활일반',
            'weather': '날씨',
            'fashion': '뷰티/패션',
            'home': '가정/육아',
            'food': '음식/맛집',
            'religion': '종교'
        }]
    }

    # 클래스 생성과 동시에 메인 카테고리, 서브 카테고리, 날짜를 초기화 하는 함수이다.
    def __init__(self, main_category, sub_category, date):
        self.base_url = f"https://news.daum.net/breakingnews/{main_category}/{sub_category}?regDate={date}&page="
        self.last_page = 0
        self.page_list = []
        self.news_list = []
        self.index = 0
        self.main_category = main_category
        self.sub_category = sub_category
        self.date = date
        self.data_df = pd.DataFrame(columns=[
                                    'platform', 'main_category', 'sub_category',
                                    'title', 'content', 'writer', 'writed_at', 'url', 'news_agency', 'sentiment'])
        self.params = {}

    # 마지막 페이지 번호를 찾기 위한 함수이다.
    def find_last_page(self):
        last_url = self.base_url + "9999"
        response = requests.get(last_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tmp_page = soup.select_one('.inner_paging em').text
        self.last_page = int(tmp_page.replace('현재 페이지', '').strip())

    # 뉴스 URL을 추출하기 위한 함수이다.
    def search(self):
        for date in range(1, self.last_page+1):
            self.page_list.append(self.base_url + str(date))

        reqs = (grequests.get(link) for link in self.page_list)
        resp = grequests.map(reqs)

        for r in resp:
            soup = BeautifulSoup(r.text, 'lxml')
            news_list = soup.select('.list_allnews')
            news_list = news_list[0].select('.tit_thumb')

            for news in news_list:
                link = news.find('a')
                self.news_list.append(link.attrs['href'])

    # 추출한 뉴스 게시글 URL에서 정보를 수집한다.
    def crawling(self):
        print('crawling')
        reqs = (grequests.get(link) for link in self.news_list)
        resp = grequests.map(reqs)

        for r in resp:
            data = []
            soup = BeautifulSoup(r.text, 'lxml')
            url = r.url
            title = soup.select_one('.head_view > .tit_view').text
            writer = soup.select('.head_view > .info_view > .txt_info')[0].text
            writer = writer.split()[0]
            if '입력' in writer:
                writer = '익명'
            if not writer:
                writer = '익명'
            writed_at = soup.select_one(
                '.head_view > .info_view .num_date').text
            content = soup.select_one('.news_view > .article_view').text.strip().replace('\n',' ')
            if not content:
                content = "내용 없음"
            content = ' '.join(content.split())
            news_agency = soup.select_one('#kakaoServiceLogo').text

            news_id = r.url.split('/')[-1]
            base_url_sticker = 'https://action.daum.net/apis/v1/reactions/home?itemKey={}'
            sticker_url = base_url_sticker.format(news_id)

            header = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "referer": sticker_url,
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb3J1bV9rZXkiOiJuZXdzIiwidXNlcl92aWV3Ijp7ImlkIjotOTE3MDQyMTUsImljb24iOiJodHRwczovL3QxLmRhdW1jZG4ubmV0L3Byb2ZpbGUvbDl0QlVMeW82X0EwIiwicHJvdmlkZXJJZCI6IkRBVU0iLCJkaXNwbGF5TmFtZSI6IuyImCJ9LCJncmFudF90eXBlIjoiYWxleF9jcmVkZW50aWFscyIsInNjb3BlIjpbXSwiZXhwIjoxNjgwMTQ5NDQxLCJhdXRob3JpdGllcyI6WyJST0xFX0lOVEVHUkFURUQiLCJST0xFX0RBVU0iLCJST0xFX0lERU5USUZJRUQiLCJST0xFX1VTRVIiXSwianRpIjoiMzI0ZTliMjktMjNiOC00ZTk2LTg3YTktZTZkODQ4MzBkZWFmIiwiZm9ydW1faWQiOi05OSwiY2xpZW50X2lkIjoiMjZCWEF2S255NVdGNVowOWxyNWs3N1k4In0.KL6vzQI3b9C7Zrtlspe5e2oW01as2SAg4Cp5NfGKZA4'}
            raw = requests.get(sticker_url, headers=header)

            s_jsonData = json.loads(raw.text)
            s_jsonData
 
            sentiment = {"추천해요" : 0, "좋아요" : 0, "감동이에요" : 0, "화나요" : 0, "슬퍼요" : 0}
 
            sentiment['좋아요'] = s_jsonData['item']['stats']['LIKE']
            sentiment['감동이에요'] = s_jsonData['item']['stats']['IMPRESS']
            sentiment['슬퍼요'] = s_jsonData['item']['stats']['SAD']
            sentiment['화나요'] = s_jsonData['item']['stats']['ANGRY']
            sentiment['추천해요'] = s_jsonData['item']['stats']['RECOMMEND']
            content = re.sub(f'{news_agency}')
            data += '다음', self.CATEGORIES[self.main_category][0], \
                self.CATEGORIES[self.main_category][1][self.sub_category], \
                title, content, writer, writed_at, url, news_agency, sentiment
            self.data_df.loc[self.index] = data
            self.index += 1

    # 수집한 정보를 csv로 저장하는 함수이다.
    def save(self):
        print('def save')
        self.data_df.to_csv(
            f'./{self.CATEGORIES[self.main_category][0]}_{self.CATEGORIES[self.main_category][1][self.sub_category]}_{self.date}.csv')

    # 위의 모든 함수를 한번에 실행하는 함수이다.
    def start(self):
        self.find_last_page()
        self.search()
        self.crawling()
        self.save()
        return None

# 해당 기간의 날짜 리스트를 반환하는 함수이다.
def get_date_list(start, end):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    date_list = pd.date_range(start=start, end=end, freq='D')
    date_list = date_list.strftime('%Y%m%d')
    return date_list

# 현재 폴더의 모든 csv를 합치는 함수이다.
def combine_all_csv():
    csv_list = []
    files = os.listdir(os.getcwd())

    for file in files:
        name, ext = os.path.splitext(file)
        if ext == '.csv':
            csv_list.append(file)

    total_csv = pd.DataFrame(columns=[
        'platform', 'main_category', 'sub_category',
        'title', 'content', 'writer', 'writed_at', 'url', 'news_agency', 'sentiment'
    ])
    for csv in csv_list:
        df = pd.read_csv(csv, index_col=0)
        total_csv = pd.concat([total_csv, df], ignore_index=True)

    total_csv.to_csv('./total.csv')

    for csv in csv_list:
        os.remove(csv)


# 처음 실행되는 메인 함수이다.
if __name__ == '__main__':
    # 날짜 리스트를 가져온다.
    date_list = get_date_list('20230201', '20230316')
    # 카테고리 확인을 위한 인스턴스를 생성한다.
    sample = DaumNewsCrawler('economic', 'finance', '20230201')
    # 크롤링을 위해 생성된 인스턴스를 저장할 리스트
    class_list = []

    # 원하는 크롤러 인스턴스를 생성 후 리스트에 저장
    for date in date_list:
        for category in sample.CATEGORIES['economic'][1].keys():
            class_list.append(DaumNewsCrawler('economic', category, date))

    # 멀티 프로세싱을 위한 작업공간
    pool = concurrent.futures.ProcessPoolExecutor(
        max_workers=multiprocessing.cpu_count()*2)

    # 작업 저장을 위한 리스트
    procs = []

    # 인스턴스를 프로세스에 할당
    for dnc in class_list:
        procs.append(pool.submit(dnc.start))

    # 모든 프로세스가 완료되었는지 확인
    concurrent.futures.wait(procs)

    # 만들어진 csv 파일 통합 후 삭제
    combine_all_csv()