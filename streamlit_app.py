import streamlit as st
import pandas as pd
import time
import random

poetry add <sky>

month = [1,2,3,4,5,6,7,8,9,10,11,12]
if "onemonth" not in st.session_state:
    st.session_state.onemonth = random.randint(0,11)
game_month = month[st.session_state.onemonth]
if code not in st.session_state:
    st.session_state.code = 0

butonn = "次へ"

@st.cache_date
def load_data():
    money = pd.read_excel("金銭リスト.xlsx")
    ivent = pd.read_excel("基本ストーリー")
    return pd.concat([money, ivent],ignore_index=True)

words_df = load_data()

name = st.text_area("名前を入力してください")

if st.button(int(butonn)):
    butonn = "性別を決定"
    if name not in " ":
        st.sideber.title("性別を選択してください")
        gender = st.sideber.radio("",("男", "女"), horizontal=True)
        st.write("サイドバーから男女を選んでください(月収が変わります)")
        
        if st.button(int(butonn)):
            butonn = "次の日へ"
            
            if gender == "男":
                st.wirte("a")

            else:
                st.write("b")


    else:
        st.write("名前を入力してください")