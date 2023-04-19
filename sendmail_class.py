###########################################################################################################
################################# 출력된 HTML 파일을 뉴스레터로 보내는 코딩##################################
###########################################################################################################
import os
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
from PIL import Image
import imghdr
import base64
import io
import configparser

class NewsletterSend:
    def __init__(self):
        self.SMTP_SERVER = 'smtp.gmail.com'
        self.SMTP_PORT = 465
        self.SMTP_USER = 'jjangsy0904@gmail.com'  # 각 개인의 이메일 아이디
        self.SMTP_PASSWORD = 'wjcoidrrhsbbpimc'  # 각 개인이 설정한 SMTP 비밀번호 입력
        self.to_users = ['miou35@naver.com']
        self.subject = '/^o^/ 취준레터가 도착했습니다! /^o^/'

    def send_newsletter(self):
        file_path_base = './news/output_test_'
        file_extension = '.html'
        i = 0
        while os.path.exists(f"{file_path_base}{i}{file_extension}"):
            file_path_3 = f"{file_path_base}{i}{file_extension}"
            i += 1

        target_addr = ','.join(self.to_users)
        # 이메일 송신인 / 수신인 / 제목 / 본문내용 생성
        msg = MIMEMultipart('related')  # mixed가 아닌 related로 설정해도 별첨화일을 송부할 수 있다.

        msg['From'] = self.SMTP_USER   #MIMEMultipart객체의 송신인 필드에 값을 넣어준 것임
        msg['To'] = target_addr   #MIMEMultipart객체의 수신인 필드에 값을 넣어준 것임
        msg['Subject'] = self.subject  #MIMEMultipart객체의 제목 필드에 값을 넣어준 것임

        # 이메일에 첨부할 html 파일 추가
        #'output_test_01.html'파일명과 경로를 ' file_path_3 '에 이미 할당해 놓았기 때문에 
        # os.path.basename()메서드로 연결시켜서 'output_test_01.html'파일명을 2번 써 줄 필요가 없도록 코딩(실수가능성차단)  
        with open(file_path_3, 'r', encoding='utf-8') as f:
            file_data = f.read()

        # 기사요약 으로 출력한 output_test_01.html파일의 내용을 기사본문에 붙이는 코딩이다.
        html = MIMEText(file_data, 'html')
        msg.attach(html)


        smtp = smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT)
        smtp.login(self.SMTP_USER, self.SMTP_PASSWORD)
        smtp.sendmail(self.SMTP_USER, self.to_users, msg.as_string())
        smtp.close()
