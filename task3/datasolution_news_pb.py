import xlwings as xw
#from datar.all import *
from datetime import datetime
import polars as pl
from polars import col, when, from_pandas, lit
import pandas as pd
from pandas import to_pickle
import numpy as np
import itertools
import json
import time
import traceback
from tqdm import tqdm
import os
import requests
import re
from pytz import timezone
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
import textdistance
import urllib.parse
import openai
import random
import schedule
import win32com.client as win32

import FinanceDataReader as fdr
from pbproject.task3.news_param_pb import apikeys, enddates, crawl_numdays_naver, naver_api_disp, naver_sort_cri, duration, article_col, sim_thresh, jw_thresh, remove_press_url,remove_press, keywords
from pbproject.task3.naver_api_crawl_pb import naver_api_crawl
from pbproject.task3.news_categorize_chat_pb import chatfunc, categorize




def news_crawling_pb():

    krx_today_price_pd = fdr.StockListing('KRX')[['Code', 'Name', 'Market']]
    #stock_kospi_kosdaq = from_pandas(krx_today_price_pd).\
    #                        filter( (col("Market") == "KOSPI") | (col("Market") == "KOSDAQ"))[0:20,:]

    stock_kospi_kosdaq = from_pandas(krx_today_price_pd). \
                         filter( (col("Market") == "KOSPI") | (col("Market") == "KOSDAQ"))

    current_dt = date.today().strftime('%Y-%m-%d')
    ####################
    #######1. 종목뉴스 네이버 크롤링#########
    #####################################

    for i in range(len(enddates)):

        enddate = enddates[i]
        newsdata_pd, newsdata_pl = naver_api_crawl(apikeys[1], apikeys[2], stock_kospi_kosdaq, enddate, naver_api_disp, naver_sort_cri)


    ### 오늘 뉴스만 필터링 (naver_api_crawl안에서 되어야 하는데 이상함, 나중에 수정 필요)
    #today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    #newsdata_pd = newsdata_pd[newsdata_pd['press_date'].dt.date == today.date()].reset_index(drop=True)
    #newsdata_pl = from_pandas(newsdata_pd)
    ##########################################
    #######2-1. 중복제거 (코사인유사도)##########
    ########################################

    today_news_pl = newsdata_pl\
                            .with_columns(lit(1).alias('one'))\
                            .with_columns(col('one').cumsum().over("stock").alias('rn')) \
                            .with_columns(col('rn').max().over("stock").alias('mr')) \
                            .filter(~(col('title').is_null()) & (col('mr') > 1 )) \
                            .filter(~col('article_url').str.contains(remove_press_url)) \
                            .filter(~col('article_url').str.contains(remove_press)) \
                            .filter(~col('press_name').str.contains(remove_press))\
                            .drop(["mr",'rn'])\
                            .with_columns(col('one').cumsum().over(["stock", "title"]).alias('nrn'))\
                            .filter(col('nrn')==1)\
                            .drop(['nrn','one'])\
                            .rename({"stock":"code"})


    keyword_cond = col('title').str.contains(keywords)
    today_news_sel_pl = today_news_pl.filter(keyword_cond)

    news_sel_major_press_pd, news_sel_major_press_pl = categorize(today_news_sel_pl)

    news_sel_major_press_pd.to_pickle(r'C:\Users\Administrator\PycharmProjects\datasolution_news_3_8\pbproject\task3\task3.pkl')
    news_sel_major_press_pd.to_csv(fr'C:\Users\Administrator\PycharmProjects\datasolution_news_3_8\pbproject\task3\output\task3_news_{current_dt}.csv', encoding = 'utf-8-sig', index = False)

    return news_sel_major_press_pd, news_sel_major_press_pl

#aa, bb= news_crawling_pb()
#news_sel_major_press_pd, news_sel_major_press_pl = news_crawling_pb()

#news_cossim_rm_sel = cossim_rm(news_int,0.6)
#news_cossim_jw_rm_sel = jw_rm(news_cossim_rm_sel, 0.6).drop('row_nr').to_pandas()

