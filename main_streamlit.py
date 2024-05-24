import streamlit as st
from streamlit_option_menu import option_menu
from st_files_connection import FilesConnection
from datetime import date
import pandas as pd
import warnings

### API 및 라이브러리 관련 세팅 ###
warnings.filterwarnings(action='ignore')
API_KEY = 'd7d1be298b9cac1558eab570011f2bb40e2a6825'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept-Encoding': '*', 'Connection': 'keep-alive'}

st.set_page_config(layout='wide')
conn = st.connection('s3', type=FilesConnection)
left_mg = 0
right_mg = 10
top_mg = 0
btm_mg = 10
DT = date.today().strftime('%y_%m_%d')

### 화면 ###

st.header('PB 뉴스 수집')

### S3에서 결과파일 가져오기 ###
df_news = conn.read("kis-duda-usecase-poc-2/poc_mzn/news_ai/news_today_pd_multi_{}.csv".format(DT), input_format="csv", ttl=600)
st.datarframe(df_news)
