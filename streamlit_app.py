import streamlit as st
import pandas as pd
import random
from PIL import Image
import os
import altair as alt
import numpy as np
#肉
imagea = Image.open('牛肉.png')
imageb = Image.open('豚肉.png')
imagec = Image.open('鶏肉.png')
imaged = Image.open('合いびき肉.png')
#野菜
imagef = Image.open('人参.png')
imageg = Image.open('じゃがいも.png')
imagei = Image.open('玉ねぎ.png')
imagej = Image.open('キャベツ.png')
imagek = Image.open('レタス.png')
imagel = Image.open('トマト.png')
imagem = Image.open('きゅうり.png')
imagen = Image.open('しめじ.png')
imageo = Image.open('しいたけ.png')
imagep = Image.open('ごぼう.png')
imageq = Image.open('ブロッコリー.png')
imager = Image.open('ネギ.png')
images = Image.open('ニラ.png')
imaget = Image.open('にんにく.png')
imageu = Image.open('ピーマン.png')
imagev = Image.open('生姜.png')
imagew = Image.open('グリーンピース.png')
imagex = Image.open('筍.png')

# セッションステートの初期化
if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-200, 200)
if 'month' not in st.session_state:
    st.session_state.month = random.randint(1, 12)
if 'days' not in st.session_state:
    st.session_state.days = 1
if 'code' not in st.session_state:
    st.session_state.code = 0
if 'xx' not in st.session_state:
    st.session_state.xx = 0
if 'number' not in st.session_state:
    st.session_state.number = 1

# 月に応じた条件設定
month_serrect = ""
if 3 <= st.session_state.month <= 5:
    month_serrect = "3~5"
elif 6 <= st.session_state.month <= 8:
    month_serrect = "6~8"
elif 9 <= st.session_state.month <= 11:
    month_serrect = "9~11"
elif st.session_state.month == 12 or st.session_state.month in (1, 2):
    month_serrect = "12~2"

mens_money = 13000 + st.session_state.energy
mens_total = 270400
womans_total = 208000

totalcount_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
total_days = totalcount_days[st.session_state.month]

@st.cache_data
def load_data():
    main = pd.read_excel("基本ストーリー.xlsx")
    special = pd.read_excel("金銭リスト.xlsx")
    cook = pd.read_excel("栄養・材料の量の内訳.xlsx")
    return pd.concat([main, special], ignore_index=True)

words_df = load_data()

item_date = ["卵 1パック 300円", "米 5kg 2500円", "大根 1本 200円", "豚肉 100g 200円", "キャベツ 1玉 200円"]
st.sidebar.title("性別を選択してください")
gender = st.sidebar.radio("", ("以下から選択してください", "男", "女"), horizontal=True)
selected_item = st.sidebar.selectbox("基本値段", item_date)

if gender == "以下から選択してください":
    st.write("サイドバーから男女を選んでください(月収が変わります)")
else:
    st.session_state.app_started = True
    st.session_state.finished = False
    st.write(f"{st.session_state.month}月 {st.session_state.days}日")

    if gender == "男":
        st.session_state.current_total = mens_total - mens_money
    else:
        st.session_state.current_total = womans_total

    choose = st.sidebar.radio("", ("ゲーム画面", "肉類", "野菜", "調味料", "その他"), horizontal=True)

    if choose == "ゲーム画面":
        st.write(f"初期金額 {st.session_state.current_total} 円 (光熱費が引かれています)")
        if st.button("次の日へ"): 
            st.session_state.days += 1
            st.session_state.code += 1
            st.session_state.current_total -= 500
        st.write(f"現在の合計金額: {st.session_state.current_total}円")

    elif choose in ["肉類", "野菜", "調味料", "その他"]:
        # 画像を2カラムに表示
        col1, col2 = st.columns(2)
        images_to_show = []

        if choose == "肉類":
            st.image(imagea)
            #仮
            a = 100
            st.subtitle("残り" + str(a) + "g")
            st.image(imageb)
            st.image(imagec)
            st.image(imaged)
        elif choose == "野菜":
            images_to_show = images_yasai
        elif choose == "調味料":
            images_to_show = images_choumiryou
        elif choose == "その他":
            images_to_show = images_other

    if gender == "女":
        st.write(f"残金 {womans_total} 円")
