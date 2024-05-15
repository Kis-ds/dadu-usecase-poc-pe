


import OpenDartReader
api_key='2f9794910c7c7ded3d8e1b44b2d04894ff87f908'
dart = OpenDartReader(api_key)



corp_code = dart.corp_codes

from datar.all import *
import pandas as pd
#corp_code_stock = pd.DataFrame(corp_code >> filter_(f.stock_code != ' ')).reset_index(drop = True)


corp_code_stock = corp_code.query("stock_code != ' ' ")

targetfirm = ["베셀","라이프시멘틱스","큐리언트","엠젠솔루션","일진전기","애니젠","대한전선","유니슨"
    ,"케이에스피", "후성", "다원시스", "STX","삼성제약", "가온전선", "LG디스플레이", "KR모터스", "진원생명과학"
    ,"누리플랜", "아미코젠", "메드팩토", "삼화전자공업", "알체라", "드림라인", "이엠티", "세기상사", "HSD엔진",
                "진양화학", "노바렉스", "카이노스메드", "에어부산", "파라텍", "에스디생명공학", "퓨쳐켐",
              '자이에스앤디','다원시스','메디콕스','DL','이지홀딩스', '마니커에프앤지', '한화시스템', '하이브', '비디아이','휴맥스', '판타지오'
    ,'엔젤로보틱스',' 케이엔알시스템']

target_corps = corp_code_stock[corp_code_stock['corp_name'].isin(targetfirm)].reset_index(drop = True)

#corp_code = target_corps['corp_code'][0]



reports = pd.DataFrame()

for i in range(len(target_corps)):
    name = target_corps.iloc[i]['corp_name']
    reports0 = dart.list(corp=name, start='20100101', end='20240415')
    reports = pd.concat([reports0, reports], axis = 0)
    print(i, reports)

reports = pd.DataFrame(reports).reset_index(drop = True)


reports_target = reports.query("report_nm == '[발행조건확정]증권신고서(지분증권)'")

reports_target['recent'] = reports_target.groupby(['corp_code'])['rcept_no'].transform('max')

reports_target_confirmed = reports_target.query("recent == rcept_no")


reports_target2 = reports.query('report_nm.str.contains("\[기재정정\]증권신고서\(지분증권\)")')
#reports_target3 = reports.query('report_nm.str.contains("\[첨부정정\]증권신고서\(지분증권\)")')

#    filter_(f.report_nm.str.contains("\[기재정정\]증권신고서\(지분증권\)")|
#            f.report_nm.str.contains("\[첨부정정\]증권신고서\(지분증권\)"))).reset_index(drop = True)


reports_target_all = pd.concat([reports_target, reports_target2], axis = 0).reset_index(drop = True)


##list
reports_target_all = reports_target_confirmed.reset_index(drop = True)

reports_target_all.to_excel("xml_list_30.xlsx")




#### 원본파일 가져오기 #####



rcept_nos = reports_target2.rcept_no.to_list()

for i in range(len(rcept_nos)):
    print(i)
    try:
        doc_id = rcept_nos[i]
        xml_text = dart.document(doc_id)
        file_path = fr'C:/Users/Administrator/PycharmProjects/datasolution_news_3_8/{doc_id}.xml'
        # 파일 쓰기 모드로 열고, xml_text의 내용을 파일에 쓴 후 파일을 닫습니다.
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(xml_text)
        print(f'{i}, doc_id, File saved successfully at {file_path}')
    except Exception as e:
        print(f"An error occurred: {e}")


































reports_list = reports_target_all['rcept_no']

for i in range(len(reports_list)):

    try:
        doc_id = reports_list[i]
        xml_text = dart.document(doc_id)

        # XML 파일로 저장하고자 하는 파일명과 경로
        file_path = fr'C:/Users/Administrator/PycharmProjects/datasolution_news_3_8/{doc_id}.xml'
        # 파일 쓰기 모드로 열고, xml_text의 내용을 파일에 쓴 후 파일을 닫습니다.
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(xml_text)
        print(f'{i}, doc_id, File saved successfully at {file_path}')
    except Exception as e:
    print(f"An error occurred: {e}")












# 회사의 고유번호(CORP_CODE)를 찾습니다. (여기서는 예시로 '005930'을 사용합니다. 삼성전자의 고유번호입니다.)
corp_code = '005930'  # 케이에스피(KSP)의 고유번호로 변경해야 합니다.

# 증권신고서(공시보고서) 조회: 'A001'은 증권신고서의 종류 코드입니다.
# 시작일과 종료일을 지정하여 해당 기간 동안의 증권신고서를 조회합니다.
reports = dart.regstate('073010', '지분증권', start=None, end=None)
reports = dart.regstate('177350', '지분증권', start=None, end=None)

dart.document('20240102000211')


import OpenDartReader


dart.list_date_ex('2022-10-03')


list = dart.regstate('케이에스피', '지분증권')


reports = dart.report(corp= '073010', bgn_de='20200101', pblntf_ty='A001', page_count=100)



dart.regstate(corp, key_word, start=None, end=None)

report = dart.report('005930', '사업보고서', 2020)


# rcp_no를 이용하여 보고서 다운로드
rcp_no = '20240102000211'
xmlfile = dart.document(rcp_no)


xml_text = dart.document('20220816001711')


xmlfile = dart.document(rcp_no, dir_path = '여기에_저장할_경로를_입력하세요')

# XML 파일로 저장하고자 하는 파일명과 경로
file_path = fr'C:/Users/Administrator/PycharmProjects/datasolution_news_3_8/{rcp_no}.xml'

# 파일 쓰기 모드로 열고, xml_text의 내용을 파일에 쓴 후 파일을 닫습니다.
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(xmlfile)

print(f'File saved successfully at {file_path}')

xmlfile



# 증권신고서 다운로드를 위한 함수 정의
def download_report(corp_code, bgn_de, end_de, report_type='A001'):
    """
    corp_code: 회사의 고유 코드
    bgn_de: 조회 시작 일자 (예: '20200101')
    end_de: 조회 종료 일자 (예: '20201231')
    report_type: 보고서의 종류 ('A001'은 증권신고서)
    """
    # 해당 기간 동안의 증권신고서 목록 조회
    reports = dart.report(corp_code, bgn_de=bgn_de, end_de=end_de, pblntf_ty=report_type)

    # 조회된 각 보고서에 대하여
    for idx, report in reports.iterrows():
        # 보고서의 고유 번호(rcp_no)를 사용하여 PDF 다운로드 URL 생성
        url = dart.sub_docs(rcp_no=report['rcept_no'], match='pdf')

        # 다운로드 URL이 존재하는 경우
        if url:
            # 첫 번째 PDF 문서 URL 사용
            pdf_url = url[0]
            # PDF 파일 다운로드
            dart.download(url=pdf_url, path='./', filename=f"{report['rcept_no']}.pdf")
            print(f"Downloaded {report['rcept_no']}.pdf")


# 예시: '005930'은 삼성전자의 corp_code가 아니라 예시일 뿐, 실제 corp_code로 대체 필요
download_report(corp_code='005930', bgn_de='20200101', end_de='20201231')

177350
dart.company_by_name('베셀')
dart.regstate('케이에스피', '지분증권')

dart.sub_docs(rcp_no)
rcp_no = '20240102000211'
dart.sub_docs(rcp_no)


dart.company('177350')


from langchain_community.document_loaders import UnstructuredXMLLoader

loader = UnstructuredXMLLoader(

)
docs = loader.load()
docs[0]

loader = UnstructuredXMLLoader(
    r"C:\Users\Administrator\PycharmProjects\datasolution_news_3_8\20240109000342.xml"
)


docs = loader.load()


docs[0]





from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)

xml_text = dart.document('20240109000342')



# XML 파일로 저장하고자 하는 파일명과 경로
file_path = r'C:/Users/Administrator/PycharmProjects/datasolution_news_3_8/20240109000342.xml'

# 파일 쓰기 모드로 열고, xml_text의 내용을 파일에 쓴 후 파일을 닫습니다.
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(xml_text)

print(f'File saved successfully at {file_path}')







from langchain_community.document_loaders import PyPDFLoader
import openai
loader = PyPDFLoader(r"C:\Users\Administrator\Downloads\[오상헬스케어][정정]증권신고서(지분증권)(2024.02.29).pdf")
#pages = loader.load_and_split()


from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
texts = text_splitter.split_documents(documents)


from langchain.llms import OpenAI




embeddings = OpenAIEmbeddings(openai_api_key="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")
db = FAISS.from_documents(texts, embeddings)

retriever = db.as_retriever()

from langchain_openai import OpenAI
llm = OpenAI(openai_api_key="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", model_name = 'gpt-4-0125-preview')

from langchain.chains import RetrievalQA


retriever = db.as_retriever()

qa = RetrievalQA.from_chain_type(

    llm = llm,
    chain_type = "stuff",
    retriever = retriever

)

# 이미 설정된 LLM(언어 모델)과 retriever 객체를 사용
qa = RetrievalQA.from_chain_type(
    llm=llm,  # LLM 객체 예: OpenAI GPT 모델
    chain_type="stuff",  # 사용할 체인 유형
    retriever=retriever  # 이전 단계에서 생성된 retriever 객체
)

query = "Which company's securities report is this document?"

# `invoke` 메서드를 사용하여 질문 처리, 이 때 'input' 파라미터에 질문을 포함시킵니다.
result = qa.invoke(method_name="run", input={"query": query})

# 결과 출력
print(result['answer'])

query = "Which company's securities report is this document?"
result = qa({"query":query})
print(result['result'])


result = chain.invoke({"question": question})



from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI talking to human"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])


memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=80,
    memory_key="chat_history",
    return_messages=True,
)


def load_memory(input):
    print(input)
    return memory.load_memory_variables({})["chat_history"]


from langchain_openai import OpenAI
llm = OpenAI(openai_api_key="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", model_name = 'gpt-4-0125-preview')

chain = RunnablePassthrough.assign(chat_history=load_memory) | prompt | llm

def invoke_chain(question):
    result = chain.invoke({"question": question})
    memory.save_context(
        {"input": question},
        {"output": result.content},
    )
    print(result)



invoke_chain(query)
















# XML 데이터 문자열
xml_data = '''
<DOCUMENT xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="dart3.xsd">
    <DOCUMENT-NAME ACODE="10001">증권신고서(지분증권)</DOCUMENT-NAME>
    <FORMULA-VERSION ADATE="20231229">3.7</FORMULA-VERSION>
    <COMPANY-NAME AREGCIK="00328191">(주)케이에스피</COMPANY-NAME>
    <BODY>
        <LIBRARY>
            <CORRECTION>
                <TITLE ATOC="Y" AASSOCNOTE="CORRECTION">정 정 신 고 (보고)</TITLE>
                <TABLE ACLASS="NORMAL" AFIXTABLE="N" WIDTH="600" BORDER="0">
                    <COLGROUP>
                        <COL WIDTH="591"></COL>
                    </COLGROUP>
                    <TBODY>
                        <TR ACOPY="Y" ADELETE="Y">
                            <TD WIDTH="600" HEIGHT="30"></TD>
                        </TR>
                        <TR ACOPY="Y" ADELETE="Y">
                            <TD ALIGN="RIGHT" WIDTH="600" HEIGHT="30">2024 년 01 월 02 일</TD>
                        </TR>
                    </TBODY>
                </TABLE>
                <P></P>
                <P></P>
                <P USERMARK="F-14">1. 정정대상 공시서류 : 증권신고서(지분증권)</P>
                ...
                <TABLE BORDER="1" WIDTH="611" ACLASS="NORMAL" AFIXTABLE="N">
                    <COLGROUP>
                        <COL WIDTH="158"></COL>
                        <COL WIDTH="259"></COL>
                        <COL WIDTH="167"></COL>
                    </COLGROUP>
                    <THEAD ALIGN="LEFT" VALIGN="TOP">
                        <TR ACOPY="Y" ADELETE="Y">
                            <TH WIDTH="167" VALIGN="MIDDLE" ALIGN="CENTER" ACOPYCOL="Y" ADELETECOL="Y" AMOVECOL="N" HEIGHT="30">제출일자</TH>
                            <TH WIDTH="268" VALIGN="MIDDLE" ALIGN="CENTER" ACOPYCOL="Y" ADELETECOL="Y" AMOVECOL="N" HEIGHT="30">문서명</TH>
                            <TH WIDTH="176" VALIGN="MIDDLE" ALIGN="CENTER" ACOPYCOL="Y" ADELETECOL="Y" AMOVECOL="N" HEIGHT="30">비고</TH>
                        </TR>
                    </THEAD>
                    ...
                </TABLE>
                ...
            </CORRECTION>
        </LIBRARY>
    </BODY>
</DOCUMENT>
'''

# BeautifulSoup 객체 생성
soup = BeautifulSoup(xml_data, 'xml')

# <TITLE>, <TH>, <TD> 태그 찾기
tags_of_interest = soup.find_all(['TITLE', 'TH', 'TD'])

# 각 태그와 그 텍스트 추출
for tag in tags_of_interest:
    print(f"{tag}")

from bs4 import BeautifulSoup

# BeautifulSoup 객체 생성, 이 예제에서는 'html.parser'를 사용했습니다.
# 실제 상황에서는 'xml' 파서를 사용하셔도 됩니다.
soup = BeautifulSoup(xml_data, 'xml')


def extract_and_preserve(soup):
    text_parts = []  # 최종 텍스트를 저장할 리스트

    # 모든 텍스트와 <table> 태그를 찾아서 처리
    for content in soup.contents:
        if content.name == 'TITLE':
            # <table> 태그는 그대로 문자열로 변환하여 추가
            text_parts.append(str(content))
        elif not content.name:
            # NavigableString 객체라면, 텍스트로 간주하고 추가
            text_parts.append(content.strip())
        else:
            # 그 외의 태그 내용도 재귀적으로 처리
            text_parts.append(extract_and_preserve(content))

    # 모든 부분을 공백으로 연결하여 반환
    return ' '.join(filter(None, text_parts))


soup = BeautifulSoup(xml_data, 'xml')
text_with_preserved_tables = extract_and_preserve(soup)
print(text_with_preserved_tables)












from bs4 import BeautifulSoup, NavigableString

def extract_with_specific_tags_preserved(element):
    result = []  # 최종 문자열을 저장할 리스트

    # 재귀적으로 모든 요소 순회
    for content in element.descendants:
        if isinstance(content, NavigableString):
            parent_tag = content.parent.name
            if parent_tag in ['title', 'tr', 'td']:
                # <title>, <tr>, <td> 태그의 텍스트는 태그와 함께 보존
                result.append(str(content.parent))
            else:
                # 그 외의 텍스트는 태그 없이 추가
                result.append(content.strip())
        elif content.name in ['title', 'tr', 'td']:
            # 이미 처리된 <title>, <tr>, <td> 태그는 중복으로 추가하지 않음
            continue

    # 결과 리스트의 아이템들을 공백으로 구분하여 하나의 문자열로 합침
    return ' '.join(filter(None, result))

# 예제 XML 데이터
xml_data = '''
<DOCUMENT xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="dart3.xsd">
    ...
    <TITLE ATOC="Y" AASSOCNOTE="CORRECTION">정 정 신 고 (보고)</TITLE>
    ...
    <TR ACOPY="Y" ADELETE="Y">
        <TD ALIGN="RIGHT" WIDTH="600" HEIGHT="30">2024 년 01 월 02 일</TD>
    </TR>
    ...
</DOCUMENT>
'''

soup = BeautifulSoup(xml_data, 'xml')
text_with_preserved_elements = extract_with_specific_tags_preserved(soup)
print(text_with_preserved_elements)












soup = BeautifulSoup(xml_contents, 'xml')

def extract_text_with_selected_tags(soup, tags_to_preserve):
    output_texts = []  # 최종 결과를 저장할 리스트

    for element in soup.descendants:
        # 해당 element가 NavigableString이고, 부모 태그가 보존 대상 태그 중 하나일 경우
        if isinstance(element, NavigableString) and element.parent.name in tags_to_preserve:
            output_texts.append(str(element.parent))
        # 해당 element가 NavigableString이지만, 부모 태그가 보존 대상 태그에 속하지 않는 경우
        elif isinstance(element, NavigableString):
            output_texts.append(element.strip())
        # 해당 element 자체가 보존 대상 태그 중 하나이고, 바로 상위의 NavigableString이 아닐 경우
        elif element.name in tags_to_preserve and not isinstance(element, NavigableString):
            output_texts.append(str(element))

    # 중복 제거
    output_texts = list(dict.fromkeys(output_texts))
    return ' '.join(output_texts)

tags_to_preserve = ['title', 'td', 'th']
extracted_text = extract_text_with_selected_tags(soup, tags_to_preserve)
print(extracted_text)
















from bs4 import BeautifulSoup, NavigableString

def extract_with_specific_tags_preserved(element):
    result = []  # 최종 문자열을 저장할 리스트

    # 재귀적으로 모든 요소 순회
    for content in element.descendants:
        if isinstance(content, NavigableString):
            parent_tag = content.parent.name
            if parent_tag in ['title', 'tr', 'td']:
                # <title>, <tr>, <td> 태그의 텍스트는 태그와 함께 보존
                result.append(str(content.parent))
            else:
                # 그 외의 텍스트는 태그 없이 추가
                result.append(content.strip())
        elif content.name in ['title', 'tr', 'td']:
            # 이미 처리된 <title>, <tr>, <td> 태그는 중복으로 추가하지 않음
            continue

    # 결과 리스트의 아이템들을 공백으로 구분하여 하나의 문자열로 합침
    return ' '.join(filter(None, result))

# 예제 XML 데이터
xml_data = '''
<DOCUMENT xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="dart3.xsd">
    ...
    <TITLE ATOC="Y" AASSOCNOTE="CORRECTION">정 정 신 고 (보고)</TITLE>
    ...
    <TR ACOPY="Y" ADELETE="Y">
        <TD ALIGN="RIGHT" WIDTH="600" HEIGHT="30">2024 년 01 월 02 일</TD>
    </TR>
    ...
</DOCUMENT>
'''

soup = BeautifulSoup(xml_data, 'xml')
text_with_preserved_elements = extract_with_specific_tags_preserved(soup)
print(text_with_preserved_elements)
















# XML/HTML 예제 데이터
xml_content = '''
<root>
    <p>This is outside the table.</p>
    <table><tr><td>Inside table</td></tr></table>
    <p>Also outside the table.</p>
</root>
'''

# 함수 호출
soup = BeautifulSoup(xml_content, 'html.parser')
extracted_text = extract_and_preserve(soup)
print(extracted_text)




















from bs4 import BeautifulSoup, NavigableString

xml_data = '''<?xml version="1.0" encoding="utf-8"?>
<DOCUMENT xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="dart3.xsd">
... (여기에 XML 데이터를 삽입) ...
</DOCUMENT>'''


xml_short = xmlfile[0:10000]

soup = BeautifulSoup(xml_short, 'xml')


def remove_attributes(tag):
    """태그에서 모든 속성을 제거합니다."""
    for attribute in list(tag.attrs):
        del tag[attribute]


def extract_text_and_remove_attributes(soup, tags_to_preserve):
    output_texts = []

    for element in soup.descendants:
        if isinstance(element, NavigableString) and element.parent.name in tags_to_preserve:
            # 부모 태그의 속성을 제거합니다.
            parent = element.parent
            remove_attributes(parent)
            output_texts.append(str(parent))
        elif isinstance(element, NavigableString):
            output_texts.append(element.strip())
        elif element.name in tags_to_preserve:
            # 해당 태그의 속성을 제거합니다.
            remove_attributes(element)
            output_texts.append(str(element))

    # 중복 제거
    output_texts = list(dict.fromkeys(output_texts))
    return ' '.join(output_texts)


soup = BeautifulSoup(xml_short, 'xml')
tags_to_preserve = ['TITLE', 'TD', 'TH']
extracted_text = extract_text_and_remove_attributes(soup, tags_to_preserve)
print(extracted_text)





from bs4 import BeautifulSoup, NavigableString

def clear_attributes(tag):
    """태그에서 모든 속성을 제거합니다."""
    for attribute in list(tag.attrs):
        del tag[attribute]

def extract_text_preserving_headers_and_title(soup):
    result_texts = []
    # <title> 태그의 내용을 포함
    for title in soup.find_all('title'):
        clear_attributes(title)
        result_texts.append(str(title))

    # 모든 <table> 태그를 처리
    for table in soup.find_all('table'):
        # <th> 태그가 있는 테이블인지 확인
        if table.find('th'):
            # <th> 태그의 내용을 포함
            for th in table.find_all('th'):
                clear_attributes(th)
                result_texts.append(str(th))
            # 해당하는 <td> 태그의 내용을 포함
            for td in table.find_all('td'):
                clear_attributes(td)
                result_texts.append(str(td))
        else:
            # <th> 태그가 없으면, <td> 태그의 텍스트만 추출
            for td in table.find_all('td'):
                result_texts.append(td.get_text(strip=True))

    # 테이블과 타이틀을 제외한 나머지 텍스트 추출
    for content in soup.find_all(text=True):
        if content.parent.name not in ['title', 'table', 'th', 'td']:
            result_texts.append(content.strip())

    return ' '.join(filter(None, set(result_texts)))  # 중복 제거 및 결과 결합

# XML 데이터
xml_data = '''... 여기에 XML 데이터를 삽입 ...'''
soup = BeautifulSoup(xml_short, 'xml')
extracted_text = extract_text_preserving_headers_and_title(soup)
print(extracted_text)




soup = BeautifulSoup(xml_short, 'html.parser')


def extract_tables_and_text(soup):
    output = []

    # <title> 태그 처리
    for title in soup.find_all('title'):
        title.clear()
        output.append(str(title))

    # <table> 태그 처리
    for table in soup.find_all('table'):
        if table.find('th'):  # <th> 태그가 있는 경우에만 처리
            # <th> 태그 내용 보존
            for th in table.find_all('th'):
                th.clear()
                output.append(str(th))
            # <td> 태그 내용 보존
            for td in table.find_all('td'):
                td.clear()
                output.append(str(td))
        else:
            # <th> 태그가 없는 경우, 텍스트만 추출
            output.append(table.get_text(separator=" ", strip=True))

    # 테이블 밖의 텍스트 추출
    for content in soup.find_all(text=True):
        if content.parent.name not in ['html', 'body', 'table', 'th', 'td', 'title']:
            output.append(content.strip())

    return ' '.join(filter(None, output))

extracted_text = extract_tables_and_text(soup)











def extract_text_with_selected_tags(soup, tags_to_preserve):
    output_texts = []  # 최종 결과를 저장할 리스트

    for element in soup.descendants:
        # 해당 element가 NavigableString이고, 부모 태그가 보존 대상 태그 중 하나일 경우
        if isinstance(element, NavigableString) and element.parent.name in tags_to_preserve:
            output_texts.append(str(element.parent))
        # 해당 element가 NavigableString이지만, 부모 태그가 보존 대상 태그에 속하지 않는 경우
        elif isinstance(element, NavigableString):
            output_texts.append(element.strip())
        # 해당 element 자체가 보존 대상 태그 중 하나이고, 바로 상위의 NavigableString이 아닐 경우
        elif element.name in tags_to_preserve and not isinstance(element, NavigableString):
            output_texts.append(str(element))

    # 중복 제거
    output_texts = list(dict.fromkeys(output_texts))
    return ' '.join(output_texts)

tags_to_preserve = ['TITLE', 'TD', 'TH']
extracted_text = extract_text_with_selected_tags(soup, tags_to_preserve)
print(extracted_text)

from bs4 import BeautifulSoup


def process_xml(xml_data):
    soup = BeautifulSoup(xml_data, 'html.parser')

    # Remove all attributes from specific tags
    for tag in soup.find_all(['title', 'th', 'td']):
        tag.attrs = {}

    # Extract and preserve <TITLE> and <TH> text with tags
    titles_and_headers = ''.join(str(tag) for tag in soup.find_all(['title', 'th']))

    # Extract and preserve <TD> text with tags only if it corresponds to <TH>
    data_cells = ''
    for table in soup.find_all('table'):
        th_tags = table.find_all('th')
        if th_tags:  # Process only if <TH> exists
            td_tags = table.find_all('td')[:len(th_tags)]  # Match corresponding <TD>s
            data_cells += ''.join(str(tag) for tag in td_tags)

    # For the rest, remove tags and just extract text
    # Remove handled tags to avoid duplicating their text
    for tag in soup.find_all(['title', 'th', 'td', 'table']):
        tag.decompose()

    # Extract remaining text
    remaining_text = soup.get_text(separator=' ', strip=True)

    # Combine all parts
    extracted_content = titles_and_headers + data_cells + remaining_text
    return extracted_content



processed_text = process_xml(xml_short)
print(processed_text)


def remove_attributes(tag):
    """태그에서 모든 속성을 제거합니다."""
    for attribute in list(tag.attrs):
        del tag[attribute]


def extract_text_and_remove_attributes(soup, tags_to_preserve):
    output_texts = []

    for table in soup.find_all('TABLE'):
        # 각 테이블의 <TH> 태그의 개수 파악
        th_tags = table.find_all('TH')
        num_th = len(th_tags)

        # <TH> 태그 처리
        for th in th_tags:
            remove_attributes(th)
            output_texts.append(str(th))

        # 상응하는 <TD> 태그 처리
        td_tags = table.find_all('TD')[:num_th]
        for td in td_tags:
            remove_attributes(td)
            output_texts.append(str(td))

    # <TITLE>, <TH>, <TD> 외의 나머지 텍스트 추출
    for content in soup.find_all(text=True):
        if content.parent.name not in ['TABLE', 'TH', 'TD', 'TITLE']:
            output_texts.append(content.strip())

    return ' '.join(filter(None, set(output_texts)))



soup = BeautifulSoup(xml_short, 'xml')
tags_to_preserve = ['TITLE', 'TH', 'TD']
extracted_text = extract_text_and_remove_attributes(soup, tags_to_preserve)
print(extracted_text)












def remove_attributes_and_extract_matched_td(soup):
    output_texts = []

    # 모든 태그의 속성 제거 및 필요한 태그 추출
    for element in soup.descendants:
        if isinstance(element, NavigableString):
            parent = element.parent
            if parent.name in ['TITLE', 'TH', 'TD']:
                remove_attributes(parent)
                if parent.name in ['TITLE', 'TH']:
                    output_texts.append(str(parent))
                elif parent.name == 'TD' and parent.find_previous_siblings('TH'):
                    output_texts.append(str(parent))
            else:
                output_texts.append(element.strip())

    # 중복 제거 및 결합
    return ' '.join(sorted(set(output_texts), key=output_texts.index))

soup = BeautifulSoup(xml_short, 'xml')
extracted_text = remove_attributes_and_extract_matched_td(soup)
print(extracted_text)





def process_xml(xml_data):
    soup = BeautifulSoup(xml_data, 'xml')

    # Remove attributes and collect texts
    def clean_and_collect(tag):
        remove_attributes(tag)
        return str(tag)

    # Remove all attributes from a tag
    def remove_attributes(tag):
        for attribute in list(tag.attrs):
            del tag[attribute]

    output_texts = []

    # TITLE tags
    for title in soup.find_all('TITLE'):
        output_texts.append(clean_and_collect(title))

    # Process tables
    for table in soup.find_all('TABLE'):
        th_texts = [th.get_text() for th in table.find_all('TH')]
        if th_texts:  # If TH tags exist, process corresponding TD tags
            for tr in table.find_all('TR'):
                tds = tr.find_all('TD')
                for td in tds:
                    if td.get_text() in th_texts:
                        output_texts.append(clean_and_collect(td))
        else:  # If no TH tags, collect TD texts without tags
            for td in table.find_all('TD'):
                output_texts.append(td.get_text())

    # Collect remaining text not in TITLE/TH/TD
    for element in soup.find_all(True):
        if element.name not in ['HTML', 'BODY', 'TITLE', 'TH', 'TD', 'TABLE', 'TR', 'ROOT']:
            output_texts.append(element.get_text())

    return ' '.join(filter(None, output_texts))


print(process_xml(xml_short))


def remove_all_attributes(tag):
    for attribute in list(tag.attrs):
        del tag[attribute]


def process_and_extract(soup):
    # Keeping <TITLE> and <TH> tags and their texts, remove attributes
    for tag in soup.find_all(['TITLE', 'TH']):
        remove_all_attributes(tag)
        tag.string = tag.text

    # Handling <TD> tags
    td_texts = []  # To capture text for <TD>s not directly under a <TH>
    for table in soup.find_all('TABLE'):
        th_count = len(table.find_all('TH'))
        for tr in table.find_all('TR'):
            tds = tr.find_all('TD')
            for td in tds[:th_count]:
                remove_all_attributes(td)
                td.string = td.text
            for td in tds[th_count:]:
                td_texts.append(td.text)
                td.decompose()  # Remove <TD> not under <TH>

    # Extracting remaining text outside the specified tags
    for tag in soup.find_all():
        if tag.name not in ['TITLE', 'TH', 'TD']:
            td_texts.append(tag.text)
            tag.decompose()

    # Combine processed tags and remaining text
    processed_text = ''.join(str(tag) for tag in soup.find_all(['TITLE', 'TH', 'TD'])) + ' '.join(td_texts)
    return processed_text


soup = BeautifulSoup(xml_short, 'html.parser')
print(process_and_extract(soup))

from bs4 import BeautifulSoup

xml_data = '''
<root>
    <TITLE>Example Title</TITLE>
    <table>
        <tr>
            <TH>Header 1</TH><TH>Header 2</TH>
        </tr>
        <tr>
            <TD>Data 1</TD><TD>Data 2</TD>
        </tr>
        <tr>
            <TD>Extra Data 1</TD><TD>Extra Data 2</TD>
        </tr>
    </table>
    <p>Some other text here.</p>
</root>
'''


def process_xml(xml_data):
    soup = BeautifulSoup(xml_data, 'html.parser')

    # Function to remove all attributes from a tag
    def clear_attributes(tag):
        tag.attrs = {}

    # Collecting titles and headers with tags, removing attributes
    titles_and_headers = ''
    for title in soup.find_all('title'):
        clear_attributes(title)
        titles_and_headers += str(title)
    for th in soup.find_all('th'):
        clear_attributes(th)
        titles_and_headers += str(th)

    # Collecting corresponding <td>s, removing attributes
    corresponding_tds = ''
    for table in soup.find_all('table'):
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        if headers:
            for tr in table.find_all('tr'):
                tds = tr.find_all('td')
                for td in tds[:len(headers)]:
                    clear_attributes(td)
                    corresponding_tds += str(td)

    # Extracting other texts
    other_texts = ' '.join(soup.find_all(text=True))

    # Remove the texts already captured
    for tag in soup(['title', 'th', 'td', 'table', 'tr', 'td']):
        tag.decompose()

    # Combine everything
    result = titles_and_headers + corresponding_tds + ' ' + ' '.join(soup.stripped_strings)

    return result


processed_text = process_xml(xml_short)
print(processed_text)