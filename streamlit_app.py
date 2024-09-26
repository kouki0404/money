import streamlit as st
import pandas as pd
import random

if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-200,200)
mens_money = 13000 + st.session_state.energy #光熱費
mens_total = 270400 #男の平均月給
womans_total = 208000 #女の平均月給

if 'month' not in st.session_state:
    st.session_state.month = random.randint(1,12)
if 'days' not in st.session_state:
    st.session_state.days = 0
if 'code' not in st.session_state:
    st.session_state.code = 0
st.sidebar.title("性別を選択してください")
gender = st.sidebar.radio("",("男", "女"), horizontal=True)
word = "サイドバーから男女を選んでください(月収が変わります)"
st.write(word)

button_label = "性別を決定"
if st.button(button_label):
    button_label = "次の日へ"
    selected_days = filtered_words_df.sample(20).reset_index(drop=True)
    st.session_state.selected_days = selected_days
    st.session_state.total_days = len(selected_days)
    selected_ivents = filtered_words_df.sample(10).reset_index(drop=True)
    st.session_state.selected_ivents = selected_ivents
    st.session_state.total_ivents = len(selected_ivents)
    if st.button(button_label):
        st.session_state.days += 1
        st.write(str(month) + "月" + str(st.session_state.days) + "日")
        if gender == "男":
            st.write("残金 " + int(mens_total) + "円")
            st.write(word)
            if st.button(button_label):
                word = "a" #この部分もexcelで出力
                st.write(word)
                
        elif gender == "女":
            st.write("残金 " + int(womans_total) + "円")
