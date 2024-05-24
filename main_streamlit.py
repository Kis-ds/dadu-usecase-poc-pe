import streamlit as st
from streamlit_option_menu import option_menu
from st_files_connection import FilesConnection
import plotly.graph_objects as go
import cufflinks as cf
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from itertools import product
import warnings
import os
import pickle
import pe_func

### API 및 라이브러리 관련 세팅 ###
warnings.filterwarnings(action='ignore')
API_KEY = 'd7d1be298b9cac1558eab570011f2bb40e2a6825'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept-Encoding': '*', 'Connection': 'keep-alive'}

st.set_page_config(layout='wide')
conn = st.connection('s3', type=FilesConnection)
cf.go_offline()
dir_path = os.path.dirname(os.path.abspath(__file__))
left_mg = 0
right_mg = 10
top_mg = 0
btm_mg = 10
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            .font{font-size:10px;}
            .col_heading {text-align: center !important}
            </style>
            """

### 화면 ###

st.header('주식연계채권 발행내역')
tab1, tab2 = st.tabs(['💰발행내역', '📈대시보드'])
with tab1:
    all_yn = st.radio('검색 유형', ('전체 검색', '회사별 검색'), horizontal=True)

    with st.form(key='form1'):
        if all_yn == '회사별 검색':
            ### S3에서 결과파일 가져오기 ###
            df_mzn = conn.read("kis-duda-usecase-poc-2/poc_mzn/pickle/Mezzanine_new.pkl", input_format="csv", ttl=600)
            df_mzn['발행사'] = df_mzn['발행사'].str.replace('주식회사', '').str.replace('(주)', '').str.replace('㈜', '').str.replace(
                '(','').str.replace(')', '').str.strip()
            corp_nm_list = df_mzn.sort_values('발행사')['발행사'].unique()
            corp_nm = st.selectbox('기업명을 입력하세요', corp_nm_list)
        else:
            corp_nm = ''

        knd = st.multiselect('채권 종류', ('전환사채권', '신주인수권부사채권', '교환사채권'))
        c1, c2 = st.columns(2)
        with c1:
            start_dt = st.date_input('시작일')
        with c2:
            end_dt = st.date_input('종료일')  # , min_value=start_dt)
        c3, c4 = st.columns(2)

        with c3:
            intr_ex_min = st.number_input('표면이자율(%) MIN', min_value=0, max_value=100, value=0)
        with c4:
            intr_ex_max = st.number_input('표면이자율(%) MAX', min_value=0, max_value=100, value=10)
        c5, c6 = st.columns(2)
        with c5:
            intr_sf_min = st.number_input('만기이자율(%) MIN', min_value=0, max_value=100, value=0)
        with c6:
            intr_sf_max = st.number_input('만기이자율(%) MAX', min_value=0, max_value=100, value=10)

        form1_bt = st.form_submit_button('조회')

    if form1_bt:
        df = pe_func.get_mezn_data(knd, corp_nm, start_dt, end_dt, intr_ex_min, intr_ex_max, intr_sf_min, intr_sf_max)
        pe_func.set_df(df, "mezzanine", start_dt.strftime('%Y%m%d'), end_dt.strftime('%Y%m%d'))
        
with tab2:
    ### S3에서 결과파일 가져오기 ###
    df_mzn = conn.read("kis-duda-usecase-poc-2/poc_mzn/pickle/Mezzanine_new.pkl", input_format="csv", ttl=600)
    df_mzn = pe_func.cleansing_mzn_df(df_mzn)

    st.markdown('<h4 style = "color:#1B5886;">| 통합 현황 분석</h4>', unsafe_allow_html=True)
    c_total_1, c_total_2 = st.columns(2, gap="large")
    with c_total_1:
        start_year, end_year = st.select_slider('> 발행연도',
                                                options=sorted(df_mzn['발행연도'].unique().tolist()),
                                                value=(2018, 2022))
    st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
    c_total_3, c_total_4, c_total_5 = st.columns(3, gap="large")
    with c_total_3:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: grey">TOP5 발행사</div>',
            unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        knd = st.radio('채권 종류', ('교환사채권', '신주인수권', '전환사채권'), horizontal=True)
        knd = '신주인수권부사채권' if (knd == '신주인수권') else knd
        mzn_cnt = df_mzn[(df_mzn['발행연도'] >= start_year) & (df_mzn['발행연도'] <= end_year) & (df_mzn['종류'] == knd)].shape[0]
        mzn_amt = '{0:,.0f}'.format(round(df_mzn[(df_mzn['발행연도'] >= start_year) & (df_mzn['발행연도'] <= end_year) & (df_mzn['종류'] == knd)]['권면총액'].sum()))
        df_top5 = df_mzn[(df_mzn['발행연도'] >= start_year) & (df_mzn['발행연도'] <= end_year) & (df_mzn['종류'] == knd)].groupby(['종류', '발행사'])[
            ['권면총액']].agg(sum).sort_values('권면총액',
                                           ascending=False).reset_index().head()
        df_top5_temp = pd.DataFrame(data=[1, 2, 3, 4, 5], columns=['#'], index=range(0, 5))
        df_top5 = pd.concat([df_top5_temp, df_top5], axis=1)
        df_top5 = df_top5[['#', '발행사', '권면총액']].fillna('-')
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        if (df_top5['권면총액']!='-').all():
            st.table(df_top5.style.format({'권면총액': '{:,.0f}'}))
        st.markdown(f"(총 발행건수: {mzn_cnt}건,  총 발행금액: {mzn_amt}원)")

    with c_total_4:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: grey">연도별 발행규모</div>',
            unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        df_pivot = pd.pivot_table(df_mzn[(df_mzn['발행연도'] >= start_year) & (df_mzn['발행연도'] <= end_year)], index='발행연도', columns='종류',
                                  values='권면총액', aggfunc='sum').fillna(0)
        fig_amt = df_pivot.iplot(kind='bar', barmode='stack', asFigure=True, dimensions=(400, 400),
                                 colors=('#828e84', '#e2725b', '#38618c')) # #92b0d2, '#2f8bcc', '#019875', '#dc9094'
        fig_amt.update_layout(margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg,
                              plot_bgcolor='white', paper_bgcolor='white',
                              legend=dict(bgcolor='white', yanchor='top', y=-0.1, xanchor='left', x=0.01, orientation='h'))
        st.plotly_chart(fig_amt, use_container_width=True)

    with c_total_5:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: grey">월별 평균 이자율</div>',
            unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        df_pivot = df_mzn[(df_mzn['발행연도'] >= start_year) & (df_mzn['발행연도'] <= end_year)].groupby(['발행연도', '발행월'])[
            ['표면이자율(%)', '만기이자율(%)']].agg(['mean']).reset_index()
        df_temp = pd.DataFrame(list(product(list(range(start_year, end_year)), list(range(1, 13)))),
                               columns=['발행연도', '발행월'])
        df_pivot = pd.merge(df_pivot, df_temp, how='outer', on=['발행연도', '발행월']).fillna(0).sort_values(['발행연도', '발행월'])
        df_pivot = df_pivot.set_index(['발행연도', '발행월'])
        fig_int = df_pivot.iplot(kind='scatter', y=['표면이자율(%)', '만기이자율(%)'], asFigure=True, dimensions=(400, 400),
                                 colors=('#38618c', '#e2725b'), line_shape='spline')
        fig_int.update_layout(margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg,
                              plot_bgcolor='white', paper_bgcolor='white',
                              legend=dict(bgcolor='white', yanchor='top', y=-0.2, xanchor='left', x=0.01, orientation='h'))
        st.plotly_chart(fig_int, use_container_width=True)

    st.markdown('<h4 style = "color:#1B5886;">| 발행사별 현황 분석</h4>', unsafe_allow_html=True)
    c_corp_1, c_corp_2, c_corp_3 = st.columns(3, gap="large")
    with c_corp_1:
        corp_nm_list = df_mzn.sort_values('발행사')['발행사'].unique()
        corp_nm = st.selectbox('발행사명', corp_nm_list)
    with c_corp_2:
        corp_start_dt = st.date_input('시작일(발행일 기준)', value=datetime.date(2018, 1, 1), key='corp_start_dt', label_visibility="visible")
    with c_corp_3:
        corp_end_dt = st.date_input('종료일(발행일 기준)', key='corp_end_dt', label_visibility="visible")
    df_corp = df_mzn[(df_mzn['발행일'] >= corp_start_dt.strftime('%Y%m%d')) & (df_mzn['발행일'] <= corp_end_dt.strftime('%Y%m%d'))]
    df_corp = df_corp.sort_values('발행일')

    st.markdown('<h1 style="text-align:center">   </h1>', unsafe_allow_html=True)
    c_corp_4, c_corp_5 = st.columns([1, 2], gap='small')
    with c_corp_4:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: grey">이자율 요약</div>',
            unsafe_allow_html=True)
    with c_corp_5:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: grey">타사대비 이자율/권면총액/주식수</div>',
            unsafe_allow_html=True)
    c_corp_6, c_corp_7, c_corp_8, c_corp_9 = st.columns([1.5, 1, 1, 1], gap='small')
    with c_corp_6:
        # st.markdown('<h6 style="text-align:center">이자율 요약</h6>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        df_corp_itr = df_corp[df_corp['발행사'] == corp_nm]
        df_corp_itr = df_corp_itr.groupby('종류')[['표면이자율(%)', '만기이자율(%)']].agg(['count', 'min', 'mean', 'max'])

        df_corp_itr_A = df_corp_itr[['표면이자율(%)']].reset_index()
        df_corp_itr_A.columns = ['TYPE', 'CNT', 'MIN', 'AVG', 'MAX']
        st.caption('표면이자율(%)')
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df_corp_itr_A.style.format({'MIN': '{:.2f}', 'AVG': '{:.2f}', 'MAX': '{:.2f}'}))

        df_corp_itr_B = df_corp_itr[['만기이자율(%)']].reset_index()
        df_corp_itr_B.columns = ['TYPE', 'CNT', 'MIN', 'AVG', 'MAX']
        st.caption('만기이자율(%)')
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df_corp_itr_B.style.format({'MIN': '{:.2f}', 'AVG': '{:.2f}', 'MAX': '{:.2f}'}))
    with c_corp_7:
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        df_corp_melt = pd.melt(df_corp, id_vars=['종류', '발행사', '공시일', '회차'], value_vars=['표면이자율(%)', '만기이자율(%)'])
        fig_bx_1 = go.Figure(go.Box(x=df_corp_melt['variable'], y=df_corp_melt['value'], marker=dict(color='#828e84')))
        fig_bx_1.add_trace(go.Scatter(x=['표면이자율(%)', '만기이자율(%)'],
                                      y=[df_corp_melt.loc[
                                             (df_corp_melt['발행사'] == corp_nm) & (df_corp_melt['variable'] == '표면이자율(%)')][
                                             'value'].mean(),
                                         df_corp_melt.loc[
                                             (df_corp_melt['발행사'] == corp_nm) & (df_corp_melt['variable'] == '만기이자율(%)')][
                                             'value'].mean()],
                                      mode='markers', marker=dict(symbol='diamond', color='red', size=10),
                                      showlegend=False))
        fig_bx_1.update_layout(showlegend=False, template='seaborn', height=350, width=300,
                               margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg)
        st.plotly_chart(fig_bx_1, use_container_width=True)
    with c_corp_8:
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        df_corp_melt = pd.melt(df_corp, id_vars=['종류', '발행사', '공시일', '회차'], value_vars=['권면총액'])
        df_corp_melt = df_corp_melt[df_corp_melt['value'] < np.percentile(df_corp_melt['value'], 95)]
        fig_bx_2 = go.Figure()
        fig_bx_2.add_trace(go.Box(x=df_corp_melt['variable'], y=df_corp_melt['value'], marker=dict(color='#828e84')))
        fig_bx_2.add_trace(go.Scatter(x=['권면총액'],
                                      y=[df_corp_melt.loc[df_corp_melt['발행사'] == corp_nm]['value'].mean()],
                                      mode='markers', marker=dict(symbol='diamond', color='red', size=10),
                                      showlegend=False))
        fig_bx_2.update_layout(showlegend=False, template='seaborn', height=350, width=300,
                               margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg)
        st.plotly_chart(fig_bx_2, use_container_width=True)
    with c_corp_9:
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        df_corp_melt = pd.melt(df_corp, id_vars=['종류', '발행사', '공시일', '회차'], value_vars=['주식수'])
        df_corp_melt = df_corp_melt[df_corp_melt['value'] < np.percentile(df_corp_melt['value'], 95)]
        fig_bx_3 = go.Figure(go.Box(x=df_corp_melt['variable'], y=df_corp_melt['value'], marker=dict(color='#828e84')))
        fig_bx_3.add_trace(go.Scatter(x=['주식수'],
                                      y=[df_corp_melt.loc[df_corp_melt['발행사'] == corp_nm]['value'].mean()],
                                      mode='markers', marker=dict(symbol='diamond', color='red', size=10),
                                      showlegend=False))
        fig_bx_3.update_layout(showlegend=False, template='seaborn', height=350, width=300,
                               margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg)
        st.plotly_chart(fig_bx_3, use_container_width=True)
        st.markdown('<div style = "color:red; font-size: 10px; text-align:right;">(발행사 위치: ◆)&nbsp;&nbsp;&nbsp;</div>',
                    unsafe_allow_html=True)

    st.markdown('<h1 style="text-align:center">   </h1>', unsafe_allow_html=True)
    st.markdown('<h4 style = "color:#1B5886;">| 조건별 현황 분석</h4>', unsafe_allow_html=True)
    c_con_1, c_con_2, c_con_3, c_con_4, c_con_5 = st.columns([1, 0.8, 0.8, 1.2, 1.2], gap='small')
    with c_con_1:
        con_nm = st.radio('기준명', ('권면총액', '주식수'), horizontal=True)
    with c_con_2:
        con_st_value = st.number_input('최소값', value=1000000000, min_value=0)
    with c_con_3:
        con_end_value = st.number_input('최대값', value=10000000000, min_value=0)
    with c_con_4:
        con_st_dt = st.date_input('시작일(발행일 기준)', value=datetime.date(2018, 1, 1))
    with c_con_5:
        con_end_dt = st.date_input('종료일(발행일 기준)')

    st.markdown('<h1 style="text-align:center">   </h1>', unsafe_allow_html=True)
    c_con_6, c_con_7= st.columns([1,2], gap='large')
    with c_con_6:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: grey">이자율 요약</div>',
            unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        df_con = df_mzn[(df_mzn['발행일'] >= con_st_dt.strftime('%Y%m%d')) & (df_mzn['발행일'] <= con_end_dt.strftime('%Y%m%d')) & (df_mzn[con_nm]>=con_st_value) & (df_mzn[con_nm]<=con_end_value)]
        df_con_itr = df_con.groupby('종류')[['표면이자율(%)', '만기이자율(%)']].agg(['count', 'min', 'mean', 'max'])

        df_con_itr_A = df_con_itr[['표면이자율(%)']].reset_index()
        df_con_itr_A.columns = ['TYPE', 'CNT', 'MIN', 'AVG', 'MAX']
        st.caption('표면이자율(%)')
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df_con_itr_A.style.format({'MIN': '{:.2f}', 'AVG': '{:.2f}', 'MAX': '{:.2f}'}))

        df_con_itr_B = df_con_itr[['만기이자율(%)']].reset_index()
        df_con_itr_B.columns = ['TYPE', 'CNT', 'MIN', 'AVG', 'MAX']
        st.caption('만기이자율(%)')
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df_con_itr_B.style.format({'MIN': '{:.2f}', 'AVG': '{:.2f}', 'MAX': '{:.2f}'}))

    with c_con_7:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: grey">채권종류별 만기 이자율 분포</div>',
            unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        fig_dot = df_con.iplot(kind='scatter', x='만기기간', y='만기이자율(%)', asFigure=True, mode='markers',
                               colors=('#828e84', '#e2725b', '#38618c'), categories='종류',
                               xTitle='만기기간(년)', yTitle='만기이자율(%)', text='발행사')  # , size='권면총액')
        fig_dot.update_layout(margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg,
                              plot_bgcolor='white', paper_bgcolor='white',
                              legend=dict(bgcolor='white', yanchor='top', y=-0.2, xanchor='left', x=0.01,
                                          orientation='h'))
        fig_dot.update_traces(marker=dict(size=8, line=dict(width=0)),
                              hovertemplate=('만기기간:%{x}년<br>' + '만기이자율:%{y}%<br>' + '발행사:%{text}'))
        st.plotly_chart(fig_dot, use_container_width=True)
