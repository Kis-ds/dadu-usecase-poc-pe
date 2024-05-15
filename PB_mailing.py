import sys
sys.path.append('C:/Users/Administrator/PycharmProjects/datasolution_news_3_8')

import time
import polars as pl
import pandas as pd
import win32com.client as win32
from datetime import datetime, timedelta, date
from pbproject.common.pb_make_excel import pb_make_excel

##### make excel file

pb_make_excel()
time.sleep(10)

def PB_monitoring_email(pb_rec_address, pb_cc_address):


    today_date = datetime.now().strftime("%Y-%m-%d")

    # Outlook Application 객체 생성
    outlook = win32.Dispatch('Outlook.Application')

    # 이메일 객체 생성
    email_send = outlook.CreateItem(0)


    email_send.Subject = f"★★데일리 모니터링- {today_date}★★"

    for recipient in pb_rec_address:
        email_send.Recipients.Add(recipient)

    for cc_email in pb_cc_address:
        recipient = email_send.Recipients.Add(cc_email)
        recipient.Type = 2  # Type 2는 CC

    # 이메일 본문 설정
    body = f"""
        {today_date} 데일리 모니터링 송부드립니다.
        """
    email_send.Body = body

    attachment_path = fr"C:\Users\Administrator\PycharmProjects\datasolution_news_3_8\pbproject\final_output\PB전략부_데일리모니터링_{today_date}.xlsx"
    email_send.Attachments.Add(attachment_path)

    # 이메일 전송
    email_send.Send()

    print("이메일 전송 완료")


pb_rec_address = ['110419@koreainvestment.com', 'ljs@koreainvestment.com', 'seokjaem@koreainvestment.com', '107916@koreainvestment.com', '108485@koreainvestment.com' ]
pb_cc_address = ['112247@koreainvestment.com', '112523@koreainvestment.com']

sent_email = PB_monitoring_email(pb_rec_address, pb_cc_address)


