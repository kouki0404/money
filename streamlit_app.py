import streamlit as st
import pandas as pd
import random

if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-200,200)
if 'xx' not in st.session_state:
    st.session_state.xx = 0
mens_money = 13000 + st.session_state.energy #光熱費
mens_total = 270400 #男の平均月給
womans_total = 208000 #女の平均月給

if 'month' not in st.session_state:
    st.session_state.month = random.randint(1,12)
if 'days' not in st.session_state:
    st.session_state.days = 1
if 'code' not in st.session_state:
    st.session_state.code = 0
item_date = ["卵 1パック 300円","米 5kg 2500円","大根 1本200円","豚肉 100g 200円","キャベツ 1玉200円"]
totalcount_days = [0,31,28,31,30,31,30,31,31,30,31,30,31]
total_days = totalcount_days[st.session_state.month]
st.sidebar.title("性別を選択してください")
gender = st.sidebar.radio("",("以下から選択してください","男", "女"), horizontal=True)
word = "サイドバーから男女を選んでください(月収が変わります)"
st.write(word)

st.write(str(st.session_state.month) + "月" + str(st.session_state.days) + "日")
if gender == "男":
    st.session_state.started = True
    st.session_state.finished = False
    st.write("初期金額" + str(mens_total - mens_money) + "円(光熱費が引かれています)")
    mens_wallet = mens_total - mens_money
    for option in st.session_state.options:
        if st.button(option, key=f"{st.session_state.current_question}-{option}"):
            update_question(option)
            st.experimental_rerun()
    if st.button("次の日へ"):
        st.session_state.days += 1
        if  st.session_state.days <= total_days:
            word = "a" #この部分もexcelで出力
            words = [" ","牛肉200g 500円","豚肉300g 450円"]
            key = st.selectbox("何を買う？",words)
            if key == "牛肉200g 500円":
                mens_total -= 500
                st.session_state.xx += 1
                st.write("残金 " + str(mens_wallet) + "円")
        
        else:
            st.session_state.finished = True
            def display_results():
                st.write("終了！残金" + str(mens_total) + "円")
elif gender == "女":
    st.write("残金 " + str(womans_total) + "円")

