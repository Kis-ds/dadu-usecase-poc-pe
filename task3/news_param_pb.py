import os
import pandas as pd
from datetime import datetime, timedelta, date
import xlwings as xw

directory = os.getcwd()


enddates = ''
if enddates == '':
    today = datetime.today().date()
    enddates = [str(today.year) + "." + str(today.month).zfill(2) + "." + str(today.day).zfill(2)]
else:
    enddates


enddates = ['2023.3.27']


crawl_numdays_naver = 2
naver_api_disp = 50
naver_sort_cri = 'sim'
duration = 5
article_col = 'no'
sim_thresh = 0.6
jw_thresh = 0.6


remove_press_url = ["fashion","newsen",'fomos','basket','besteleven','golf','spotv','maniareport','jumpball','sportal','mydaily','xports','sports','sport','xportsnews','osen','tvreport','sports','asiatoday','newswatch','opinionnews','football','skyedaily','game','starnews','star','spotv','fourfourtwo']
remove_press =["패션","fashion","newsen",'스포츠','마이데일리','스타뉴스','osen','스포탈코리아','sportalkorea','점프볼','jumpball','마니아','스포티비','풋볼','골프','낚시','베스트일레븐','besteleven','바스켓','포모스']
keywords_list = ['M&A','m&a','인수','합병','제품출시','제품 출시','출시','신제품', '신약', '신약개발' ,'신약 개발', '원자재가격' ,'원자재', '가격', '규제승인' ,'규제', '승인' ,'파트너십' ,'파트너쉽' , '법적합의' ,'법적 합의' , '정부정책' ,'정부 정책' ,'대주주 지분거래', '대주주 지분 거래' , '지분거래']


remove_press_url = '|'.join([word.replace(',', '') for word in remove_press_url])
remove_press = '|'.join([word.replace(',', '') for word in remove_press])
keywords = '|'.join([word.replace(',', '') for word in keywords_list])


########API keys#############

my_api_key = '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' #신용카드 바꿀것
client_id = '9h0qInsUO939znd_s5uF'
client_secret='Ls0XXMVVwZ'

apikeys = [my_api_key,client_id,client_secret]


