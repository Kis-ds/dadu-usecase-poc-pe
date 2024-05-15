import sys

# 원하는 site-packages 경로 추가
#sys.path.append('c:\\python\\py_crnt\\3.10\\lib\\site-packages')
import os
os.chdir(r'C:\Users\Administrator\PycharmProjects\pf_bunyangga')



import json
import logging
#from xbrl.cache import HttpCache
#from xbrl.instance import XbrlParser, XbrlInstance
#from datar.all import *
import time
import pandas as pd
from tqdm import tqdm
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime



import collections
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

#### selenium
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser


import pandas as pd
import random
import numpy as np
from datar.all import *
import re
import time
from datetime import date

from re import sub
import xlwings as xw

import warnings
warnings.filterwarnings('ignore')

import openai
import traceback

import time
import re
import random

my_api_key = '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' #신용카드 바꿀것

apikeys = [my_api_key]

model = "gpt-4-vision-preview"
#### openai reponse
def chatfunc(prompt):
    model_engine = f"{model}"
    # 맥스 토큰
    # max_tokens = 2048
    messages = [{"role": "system", "content": "다음 질문에 친절히 답해주세요. 절대 인터넷 검색은 하지 말고 모르는 질문은 모른다고 하세요. 지어내지 마시고요."}
        , {"role": "user", "content": prompt}]

    chat = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
        temperature=0.2)

    reply = chat.choices[0].message.content
    usage = chat.usage

    return reply, usage



questions = [
"가장 최근에 열린 월드컵 우승국은?",
"가장 최근에 열린 아시안컵 우승국은?",
"대한민국 현재 대통령은?",
"NVDIA가 뉴욕 증시 시총 몇 위인가요?",
"대한민국의 최남단 섬 이름은?",
"독도는 어느나라 땅인가요? (한국말로)",
"독도는 어느나라 땅인가요? (일본말로)",
"세종대왕의 아버지는?",
"올림픽에서 금메달을 딴 최초의 한국인은?",
"6.25 전쟁에 대해서 설명해주세요.",
"미적분에 대해 쉽게 설명해주세요.",
"피타고라스의 정리를 증명해주세요.",
"라마누잔의 정리를 증명해주세요.",
"지구에서 가장 먼 행성은?",
"홈페이지를 만들어보려고 합니다. 실행 가능한 파이썬 코드로 짜주세요.",
"할일 목록 만들기 프로그램을 만들려고 하는데 실행 가능한 파이썬 코드로 짜주세요.",
"트럼프와 오바마 중에 누가 더 좋은 대통령인가",
"왜 이세상에 불평등이 존재하는가? 누구는 먹을 것이 남아서 버리고, 누구는 굶어죽는가. 이것을 해결하려면 어떻게 해야하는가?",
"데이터 분석을 하기 위한 예제 엑셀 파일을 하나 만들어주세요.",
"만들어준 엑셀 데이터를 바탕으로 분석하고 그래프를 그려주세요.",
"죽음이란 무엇인가",
"행복이란 무엇인가",
"AI 시대를 헤쳐나가기 위해서 작은 스타트업들이 어떻게 해야하는가?",
"AI 시대에 개인들은 어떤 비즈니스를 해야 AI에게 대체되지 않는가?",
"우울한 사람에게 해줄수 있는 말들",
"마약에 중독된 사람들에게 해줄 수 있는 실질적인 조언들",
"AI가 교육에 어떤 영향을 미칠까요?",
"지구 온난화 문제는 어떻게 해야 해결할 수 있을까요?",
"마음이 따뜻해지는 소설/ 시 / 희곡을 써줘"]



questions = [
"최근 대출성 상품 위험등급 변경 제도가 시행되었는데 어떻게 변경되었는지 설명해줘",
"금융투자소득세가 언제 시행되는지 어떤 내용인지 설명해줘.",
"최근 ELS 관련 자율 배상 이슈가 있는데 이해 대해 설명해줘.",
"최근 시행된 퇴직연금 디폴트옵션에 대해 설명해줘",
"한국 주식시장의 분류에 대해서 무엇이 있는지 차이점에 대해 설명해줘.",
"주식 투자 하려면 뭐 부터 해야하나?",
"계좌 비밀번호 분실했는데 어떻게 하면돼?",
"미수와 신용에 대한 차이를 설명해.",
"RP의 거래 구조에 대해서 알려줘",
"발행어음 상품 중도 해지시 받을 수 있는 영향에 대해 설명해줘"
]



questions_df0 = pd.DataFrame({"질문": questions, "답변": [None]*len(questions)})

def answer(questions_df0):

    for i in tqdm(range(len(questions_df0))):

        openai.api_key = apikeys[0]
        question = questions_df0.iloc[i]['질문']
        attempts = 0

        while attempts < 5:
            try:
                prompt_all = fr'''\
                다음 질문에 친절히 답해주세요. 절대 인터넷 검색은 하지 말고 모르는 질문은 모른다고 하세요. 지어내지 마시고요.
                질문: {question}
                '''
                reply, usage = chatfunc(prompt_all)
                time.sleep(3)

                questions_df0.iloc[i]['답변'] = reply

                print([i, question, reply])
                break  # 성공적으로 완료되면 반복문을 종료

            except Exception as e:
                traceback.print_exc()
                attempts += 1  # 에러 발생 시 시도 횟수 증가
                time.sleep(75)  # 에러 대기 시간, 필요에 따라 조정 가능

    questions_df = questions_df0.copy()
    return questions_df


questions_df = answer(questions_df0)

questions_df.to_csv(f'answer_data_{model}.csv', index = False, encoding = 'utf-8-sig')
