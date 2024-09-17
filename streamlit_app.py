import streamlit as st
import pandas as pd
import random

# セッションステートの初期化
if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-200, 200)

if 'month' not in st.session_state:
    st.session_state.month = random.randint(1, 12)
if 'days' not in st.session_state:
    st.session_state.days = 0
if 'code' not in st.session_state:
    st.session_state.code = 0

# ボタンのラベルを文字列として設定
button_label = "次へ"

@st.cache
def load_data():
    money = pd.read_excel("金銭リスト.xlsx")
    ivent = pd.read_excel("基本ストーリー.xlsx")
    return pd.concat([money, ivent], ignore_index=True)

# データの読み込み
words_df = load_data()

# サイドバーの設定
name = st.sidebar.text_input("名前を入力してください", "")
st.sidebar.title("性別を選択してください")
gender = st.sidebar.radio("", ("男", "女"), horizontal=True)

# 光熱費の計算
mens_money = 13000 + st.session_state.energy

# 表示するテキスト
word = "サイドバーから男女を選んでください(月収が変わります)"
st.write(word)

if name != "":
    if st.button(button_label):
        button_label = "性別を決定"
        if st.button(button_label):
            button_label = "次の日へ"
            if st.button(button_label):
                st.session_state.days += 1
                st.write(f"{st.session_state.month}月{st.session_state.days}日")
                if gender == "男":
                    st.write("男の場合の処理")
                    if st.button(button_label):
                        word = "a"
                        st.write(word)
                elif gender == "女":
                    st.write("女の場合の処理")
else:
    st.write("名前を入力してください")
