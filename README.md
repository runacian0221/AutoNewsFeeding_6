## 프로젝트 제목
실시간 뉴스 요약 메일링 프로그램 구축
<br>
<br>

## 📆프로젝트 기간
2023.3.17 ~ 2023.4.19
<br>
<br>

## 목차
1. [프로젝트 소개](#프로젝트-소개)
2. [기술 스택](#기술-스택)
3. [인사이트](#인사이트)
4. [프로세스](#프로세스)
<br>

## 프로젝트 소개 
다음 경제뉴스를 대상 1시간 주기로 실시간 뉴스를 크롤링하고, 수집한 기사데이터의 유사도 계산을 통해<br>
3줄 요약 후 이메일 자동 발송
<br>
<br>
## 📚기술 스택
| Python |   Beautifulsoup   |   Gensim   |   Pandas   |  Scikit_learn   |   Konlpy   |
| :--------: | :------: | :------: | :-----: | :-----: |  :-----: |
|   <img src="https://user-images.githubusercontent.com/123911214/222653423-27f43572-8729-4fa1-be32-95e7b439c46a.png" width="200" height="50"/>   |   <img src="https://user-images.githubusercontent.com/123911214/232716532-48519665-430b-422d-ad33-102cc5c5b95c.png" width="150" height="50"/>   |   <img src="https://user-images.githubusercontent.com/123911214/232717251-f45d3653-4238-4efb-abba-cd7f5acfc5c8.png" width="150" height="100"/>   | <img src="https://user-images.githubusercontent.com/123911214/232713662-5fdf38b5-355c-4de0-a9d2-4d105e137d82.png" width="100" height="100"/> | <img src="https://user-images.githubusercontent.com/123911214/232714129-f0f6392b-3d85-4cf7-83d7-545092eac345.png" width="100" height="50"/> | <img src="https://user-images.githubusercontent.com/123911214/232715045-ebabb5b7-5f06-4aef-934b-ca6d1b209098.png" width="100" height="100"/> | 
<br>

## 🎞인사이트
● 출·퇴근길 간단하게 뉴스를 보기 위해, 다음 뉴스데이터 정보를 수집하고 요약한 자료를<br>
  &nbsp;&nbsp;이메일로 자동 발송하는 시스템을 구축<br>
● 요약된 뉴스 기사를 이용하여 보다 쉽고 빠르게 기사의 중요 내용을 확인 할 수 있을<br> &nbsp;&nbsp;것으로 기대됨<br>
<br>

## 💻프로세스
<img src="https://user-images.githubusercontent.com/123911214/232953934-48957ebc-1267-42e0-be62-051af47acdf0.png" width="600" height="300"/>
1. Beautifulsoup을 이용해 다음 경제뉴스기사 클롤링<br>
2. Multiprocessing으로 90일치의 데이터를 추출하고 csv파일로 저장<br>
3. Cleansing 코드를 작성하고, 작성한 코드를 이용하여 뉴스의 불필요한 특수기호, 불용어를 처리<br>
4. Nltk를 이용해 기사문서 tokenize, Konlpy의 mecab으로 품사태깅 tagging(동사, 명사)<br>
5. Gensim의 corpora를 이용해 단어의 출현 빈도를 계산하고, 단어마다 index 부여<br>
6. Gensim의 LDA를 이용해 뉴스기사의 토픽키워드 기준으로 순위를 매겨 top3문장으로 기사요약<br>
7. HTML 문서에 요약한 뉴스기사 데이터를 삽입<br>
8. Email로 메일을 전송<br>
9. Crontab을 이용하여 자동화 스케쥴링
<br>
