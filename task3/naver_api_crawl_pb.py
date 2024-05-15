import pandas as pd
from datetime import datetime
from datetime import datetime, timedelta, date
from polars import col, when, from_pandas, concat, count
from tqdm import tqdm
import os
import requests
import re
import urllib.parse
import json
import html

def naver_api_crawl(client_id, client_secret, keyword_data, enddate, naver_api_disp, naver_sort_cri):
    today_st = enddate
    tyear, tmonth, tday = today_st.split('.')
    date = datetime.strptime(today_st, '%Y.%m.%d')
    date -= timedelta(days=1)
    ydat_st = date.strftime('%Y.%m.%d')
    yyear, ymonth, yday = ydat_st.split('.')

    recent_crawl_dt = re.sub(r'\.', '-', today_st)

    #keyword_data = pd.DataFrame(keyword_data)
    stocks = keyword_data.select('Code').unique().to_series()
    news_today_pd1 = pd.DataFrame()
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    #for i in tqdm(range(len(stocks))):

    for i in (range(len(stocks))):
        stock = stocks[i]
        keyword_row = keyword_data.filter(col('Code') == stock)
        keyword = keyword_row.select('Name').item()
        news_today_pd0 = pd.DataFrame()
        encText = urllib.parse.quote(keyword)
        url = f"https://openapi.naver.com/v1/search/news?query={encText}&display={naver_api_disp}&start=1&sort={naver_sort_cri}"  # JSON 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            response = response_body.decode('utf-8')
            parsed_json = json.loads(response)

            try:
                # 데이터프레임으로 변환
                df = pd.DataFrame(parsed_json["items"])
                head_df = df.head()
                print([i, keyword, head_df])
                if len(df) == 0:
                    print("no news")

                df.rename(
                    columns={'description': 'content', 'pubDate': 'press_date', 'originallink': 'article_url'},
                    inplace=True)
                df['keyword'] = keyword
                df['recent_crawl_dt'] = recent_crawl_dt
                df['recent_crawl_dt'] = pd.to_datetime(df['recent_crawl_dt'], format='%Y-%m-%d')
                #df['press_date'] = pd.to_datetime(df['press_date']).dt.tz_localize(None)

                df['press_date'] = pd.to_datetime(df['press_date'], format='%a, %d %b %Y %H:%M:%S %z')
                df['press_date'] = df['press_date'].dt.tz_localize(None)

                df['pyear'] = df['press_date'].dt.year
                df['pmonth'] = df['press_date'].dt.month
                df['pday'] = df['press_date'].dt.day
                df['phour'] = df['press_date'].dt.hour
                df['title'] = df['title'].apply(lambda x: re.sub('<.*?>', '', x))
                df['content'] = df['content'].apply(lambda x: re.sub('<.*?>', '', x))
                df['title'] = df['title'].apply(lambda x: html.unescape(x))
                df['content'] = df['content'].apply(lambda x: html.unescape(x))

                df['tyear'] = int(tyear)
                df['tmonth'] = int(tmonth)
                df['tday'] = int(tday)
                df['yyear'] = int(yyear)
                df['ymonth'] = int(ymonth)
                df['yday'] = int(yday)

                df['press_name'] = df['article_url'].apply(
                    lambda url: re.sub(r'http[s]?://', '', url).split('/')[0])

                #df_yday_tday = df[
                #    ((df['pyear'] == df['tyear']) & (df['pmonth'] == df['tmonth']) & (df['pday'] == df['tday'])) |
                #    ((df['pyear'] == df['yyear']) & (df['pmonth'] == df['ymonth']) & (
                #            df['pday'] == df['yday']))].reset_index(drop=False)

                # 11PM에 돌리므로 오늘데이터만 추출
                #df_tday = df[((df['pyear'] == df['tyear']) & (df['pmonth'] == df['tmonth']) & (df['pday'] == df['tday']))].reset_index(drop=False)


                news_today_pd0 = pd.concat([news_today_pd0, df], axis=0)
            except KeyError:
                print("No items found in response for keyword:", keyword)
                continue  # 다음 루프로 이동

        else:
            print("Error Code:" + str(rescode))

        news_today_pd0['stock'] = stock
        news_today_pd1 = pd.concat([news_today_pd1, news_today_pd0], axis=0)

    news_today_pd1.reset_index(drop = False, inplace = True)
    news_today_pd = news_today_pd1[
        ['stock', "keyword", "index", "press_name", "press_date", "title", "content", "article_url", "recent_crawl_dt", "link"]]
    news_today_pd["article"] = None
    news_today_pd = news_today_pd[news_today_pd['press_date'].dt.date == today.date()].reset_index(drop=True)

    print(news_today_pd['press_date'].dt.date.unique())

    #news_today_pd.reset_index(drop=True, inplace=True)

    current_dt = date.today().strftime('%y_%m_%d')
    news_today_pd.to_csv(f"news_today_pd_{current_dt}.csv", index = False, encoding = 'utf-8-sig')
    news_today_pl = from_pandas(news_today_pd)

    return news_today_pd, news_today_pl


#a,b = naver_api_crawl(client_id, client_secret, keyword_data, enddate, naver_api_disp, naver_sort_cri)