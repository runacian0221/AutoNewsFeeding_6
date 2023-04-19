import os
os.chdir('/home/ubuntu/workspace/news_team_6')
print(os.path.abspath('.'))
import datetime
from datetime import timedelta
import pandas as pd
import concurrent.futures
import multiprocessing
from datetime import timedelta
from SuperFast2 import DaumNewsCrawler,get_date_list,combine_all_csv
from summary import Summary
from sendmail_class import NewsletterSend

if not os.path.exists('news'):
        os.mkdir('news')

#처음 실행되는 메인 함수이다.
## 크롤링 부분 ##
if __name__ == '__main__':
    # 날짜 리스트를 가져온다.
    date_list = get_date_list((datetime.datetime.now() - timedelta(hours=1)).strftime('%Y%m%d%H%M'), datetime.datetime.now().strftime('%Y%m%d%H%M'))
    # 카테고리 확인을 위한 인스턴스를 생성한다.
    sample = DaumNewsCrawler('economic', 'finance', '20230201')
    # 크롤링을 위해 생성된 인스턴스를 저장할 리스트
    class_list = []

    # 원하는 크롤러 인스턴스를 생성 후 리스트에 저장
    for date in date_list:
        for category in sample.CATEGORIES['digital'][1].keys():
            class_list.append(DaumNewsCrawler('digital', category, date))

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

    ## 요약부분 ##
    df = pd.read_csv('./total.csv')
    summarizer = Summary()
    summarizer.stopword()
    summarizer.generate_html(df)

    os.remove('./total.csv')

    ## 이메일 보내는부분 ##
    sender = NewsletterSend()
    sender.send_newsletter()