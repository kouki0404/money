import streamlit as st
import pandas as pd
import time
import random

if energy not in st.session_state:
    st.session_state.energy = random.randint(-200,200)
word = "あいうえお"
mens_money = 13000 + st.session_state.energy #光熱費

selected_nomalivents = filtered_words_df.sample(20).reset_index(drop=True)
st.session_state.selected_nomalivents = selected_nomalivents

selected_specalivents= filtered_words_df.sample(10).reset_index(drop=True)
st.session_state.selected_specalivents = selected_specalivents

if month not in st.session_state:
    st.session_state.month = random.randint(1,12)
if days not in st.session_state:
    st.session_state.days = 0
if code not in st.session_state:
    st.session_state.code = 0

button = "次へ"

@st.cache_date
def load_data():
    money = pd.read_excel("金銭リスト.xlsx")
    ivent = pd.read_excel("基本ストーリー")
    return pd.concat([money, ivent],ignore_index=True)

words_df = load_data()

name = st.sidebar.selectbox("名前を入力してください", " ")
st.sideber.title("性別を選択してください")
gender = st.sideber.radio("",("男", "女"), horizontal=True)
word = "サイドバーから男女を選んでください(月収が変わります)"
st.write(word)
if not name == " ":
    if st.button(int(button)):
        button = "性別を決定"
        if st.button(int(button)):
            button = "次の日へ"
            if st.button(int(button)):
                st.session_state.days += 1
                st.write(str(month) + "月" + str(st.session_state.days) + "日")
                if gender == "男":
                    st.write(word)
                    if st.button(int(button)):
                        word = "a"
                        st.write(word)

                        

                elif gender == "女":
                    st.write("b")

elif name == " ":
    st.write("名前を入力してください")