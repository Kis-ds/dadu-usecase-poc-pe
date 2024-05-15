
#pip install openai==0.28

import polars as pl
from polars import col, when, from_pandas, concat, count, lit
import pandas as pd
from pandas import to_pickle
import numpy as np
import itertools
import json

import time
from datetime import timedelta, date
import traceback
from tqdm import tqdm
import os
import requests
import re
import html
from pytz import timezone

from bs4 import BeautifulSoup
import textdistance
import urllib.parse


import openai
import random
import schedule
import win32com.client as win32
import xlwings as xw

from pbproject.task3.news_param_pb import apikeys

#from datar.all import *
#from konlpy.tag import Okt
# from konlpy.tag import Komoran
# komoran = Komoran()


#from PyKomoran import *
#komoran = Komoran("EXP")
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import Select


##############################################################
###############################################################
############################# 함수 #############################
###############################################################
################################################################


########API keys#############

#my_api_key = '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' #신용카드 바꿀것
#client_id = '9h0qInsUO939znd_s5uF'
#client_secret='Ls0XXMVVwZ'
#apikeys = [my_api_key,client_id,client_secret]


#### openai reponse
def chatfunc(prompt):
    model_engine = "gpt-3.5-turbo"
    # 맥스 토큰
    # max_tokens = 2048
    messages = [{"role": "system", "content": "You are a helpful assistant."}
        , {"role": "user", "content": prompt}]

    chat = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
        temperature=0.2)

    reply = chat.choices[0].message.content
    usage = chat.usage

    return reply, usage


##################################################
############## 기준에 따른 필터링 함수들##############
#################################################

###########JW 계산 및 필터링#############

def categorize(today_news_sel_pl):

    openai.api_key = apikeys[0]
    news_pl0 = today_news_sel_pl.with_row_count()
    news_pl = news_pl0.with_columns(lit("NA").alias('category'))

    cat_cond = (col('category') == "Partnership Conclusion") | \
               (col('category') == "M&A") | \
               (col('category') == "New Product Launch") | \
               (col('category') == "New Drug Development") | \
               (col('category') == "Regulatory Approval") | \
               (col('category') == "Legal Agreement") | \
               (col('category') == "Policy Related") | \
               (col('category') == "Shareholder Equity Transactions")

    trans_cond = ( when(col('카테고리') == "Partnership Conclusion").then("파트너쉽")
                  .when(col('카테고리') == "M&A").then("인수합병")
                  .when(col('카테고리') == "New Product Launch").then("신제품출시")
                  .when(col('카테고리') == "New Drug Development").then("신약개발")
                  .when(col('카테고리') == "Regulatory Approval").then("규제승인")
                  .when(col('카테고리') == "Legal Agreement").then("법적합의")
                  .when(col('카테고리') == "Policy Related").then("규제관련")
                  .when(col('카테고리') == "Shareholder Equity Transactions").then("대주주지분거래")
                  .otherwise("기타"))

    for i in tqdm(range(len(news_pl))):
        title = news_pl.select('title').to_series()[i]
        attempts = 0

        while attempts < 5:
            try:
                prompt_all = fr'''
                Forget all your previous instructions.\
    
                Classify each news headline into the following topics: \
                M&A, New Product Launch, Sales Outlook, Stock Market Outlook, New Drug Development, Raw Material Price, Regulatory Approval, Partnership Conclusion, Legal Agreement, Government Policy Related, Major Shareholder Equity Transactions. \
                Say "Other" if you do not fall into the above categories.                
    
                Headline: {title}
    
                Warnings: Never explain anything, just tell me the type.
                '''
                reply, usage = chatfunc(prompt_all)
                time.sleep(3)

                news_pl = \
                    news_pl. \
                        with_columns(
                        when(col("row_nr") == i).then(reply)
                        .otherwise(col('category'))
                        .alias('category'))

                print([i, title, reply])
                break  # 성공적으로 완료되면 반복문을 종료

            except Exception as e:
                traceback.print_exc()
                attempts += 1  # 에러 발생 시 시도 횟수 증가
                time.sleep(75)  # 에러 대기 시간, 필요에 따라 조정 가능

        if attempts == 5:
            print(f"Maximum attempts reached for index {i} with title: {title}")

    news_sel_pl = news_pl.filter(cat_cond)

    news_sel_major_press_pl = \
    news_sel_pl.\
        with_columns(when(col('link').str.contains('naver')).then(1).otherwise(0).alias('naver')).\
        with_columns(when( (col('naver').sum().over(['keyword', 'code', 'category'])) > 1 ).then(1).otherwise(0).alias('naverhave')).\
        with_columns(lit(1).alias('one')).\
        with_columns(col('one').cumsum().over(['keyword', 'code', 'category']).alias('r')).\
        filter( ( (col('naverhave') == 1) & (col('r') == 1) ) | ( (col('naverhave') == 0) & (col('r') == 1) ) ).\
        select('code', 'keyword', 'press_name', 'press_date', 'title', 'content', 'link', 'category' ).\
        rename({"code":"종목코드", "keyword":"종목명" , "press_name":"언론사URL" , "press_date":"작성일자"
                ,"title":"제목" ,"content":"기사부분",  'link':'네이버링크', 'category':'카테고리'}).\
        with_columns(trans_cond.alias('카테고리')).\
        sort(['카테고리', '종목명']).\
        drop(['기사부분'])


    news_sel_major_press_pd = news_sel_major_press_pl.to_pandas()

    current_dt = date.today().strftime('%y%m%d')
    news_sel_major_press_pd.to_csv(f'pb_news_{current_dt}.csv', index=False, encoding="utf-8-sig")

    return news_sel_major_press_pd, news_sel_major_press_pl