import streamlit as st
import pandas as pd
import random
from PIL import Image
import os
import altair as alt
import numpy as np
import sqlite3
import hashlib
import streamlit.components.v1 as components
import os
#文字のフォント変更
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
#調味料
imagey = Image.open("塩.png")
imagez = Image.open("砂糖.png")
imageaa = Image.open("醤油.png")
imageab = Image.open("みそ.png")
imageac = Image.open("サラダ油.png")
#その他
imagead = Image.open("米.png")
imageae = Image.open("卵.png")
imageaf = Image.open("さば.png")
imageag = Image.open("そば.png")
imageah = Image.open("パスタ.png")
imageai = Image.open("バター.png")
imageaj = Image.open("ベーコン.png")
imageak = Image.open("海老.png")
imageal = Image.open("豆腐.png")
# セッションステートの初期化
if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-700, 700)
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
youbi_list = [0,"月","火","水","木","金","土","日"]
youbi = youbi_list[st.session_state.days]
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
# テーブルを作成（存在しない場合）
def create_user_table(conn):
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS user_data(username TEXT PRIMARY KEY, text_content TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS study_data(username TEXT, date TEXT, study_hours REAL, score INTEGER, subject TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS class_data(username TEXT PRIMARY KEY, class_grade TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS goals(username TEXT PRIMARY KEY, goal TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS projects(username TEXT, project_name TEXT, progress REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS events(username TEXT, date TEXT, description TEXT)')
# 新しいユーザーを追加する関数
def add_user(conn, username, password):
    hashed_password = make_hashes(password)
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
# ユーザー名の存在を確認する関数
def check_user_exists(conn, username):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    return c.fetchone() is not None
# 学習データを保存する関数
def save_study_data(conn, username, date, study_hours, score, subject):
    c = conn.cursor()
    c.execute('INSERT INTO study_data(username, date, study_hours, score, subject) VALUES (?, ?, ?, ?, ?)',
              (username, date, study_hours, score, subject))
    conn.commit()
# ユーザーの学習データを取得する関数
def get_study_data(conn, username):
    c = conn.cursor()
    c.execute('SELECT date, study_hours, score, subject FROM study_data WHERE username = ?', (username,))
    return c.fetchall()

@st.cache_data
def load_data():
    main = pd.read_excel("基本ストーリー.xlsx")
    special = pd.read_excel("金銭リスト.xlsx")
    cook = pd.read_excel("栄養・材料の量の内訳.xlsx")
    return pd.concat([main, special], ignore_index=True)

words_df = load_data()

item_date = ["牛肉 100g 400円", "豚肉 100g 200円", "鶏肉 100g 150円", "卵 1パック 200円", "米 5kg 2500円", "大根 1本 200円", "キャベツ 1玉 300円", "みそ 1パック 300円", "合いびき肉 100g 200円"]
st.sidebar.title("性別を選択してください")
gender = st.selectbox("", ("以下から選択してください", "男", "女"), horizontal=True)
selected_item = st.sidebar.selectbox("基本値段", item_date)

if st.button("名前、性別を決定"):
    if gender == "以下から選択してください":
        st.write("サイドバーから男女を選んでください(月収が変わります)")
    else:
        st.session_state.app_started = True
        st.session_state.finished = False
        choose = st.sidebar.radio("", ("ゲーム画面", "肉類", "野菜", "調味料", "その他"), horizontal=True)
        while st.session_state.days <= 7:
            if gender == "男":
                st.session_state.current_total = mens_total - mens_money
            if choose == "ゲーム画面":
                st.write(f"{st.session_state.month}月 {st.session_state.days}日{youbi}曜日")
                st.write(f"初期金額 {st.session_state.current_total} 円 (光熱費が引かれています)")
                #食費1日1500円
                # Chatbot iframe を "ゲーム画面" の選択時に表示
                st.markdown("""
                <iframe
                    src="https://www.chatbase.co/chatbot-iframe/nVm1Yf2i4qWPwWDlr9itc"
                    width="100%" 
                    style="height: 100%; min-height: 700px"
                    frameborder="0">
                </iframe>
                """, unsafe_allow_html=True)

            elif choose in ["肉類", "野菜", "調味料", "その他"]:
                # 画像を2カラムに表示
                col1, col2 = st.columns(2)
                images_to_show = []

                if choose == "肉類":
                    st.image(imagea)
                    #仮
                    a = 100
                    st.subheader("残り" + str(a) + "g")
                    st.image(imageb)
                    st.image(imagec)
                    st.image(imaged)
                elif choose == "野菜":
                    st.image(imagef)
                    st.image(imageg)
                    st.image(imagei)
                    st.image(imagej)
                    st.image(imagek)
                    st.image(imagel)
                    st.image(imagem)
                    st.image(imagen)
                    st.image(imageo)
                    st.image(imagep)
                    st.image(imageq)
                    st.image(imager)
                    st.image(images)
                    st.image(imaget)
                    st.image(imageu)
                    st.image(imagev)
                    st.image(imagew)
                    st.image(imagex)
                elif choose == "調味料":
                    st.image(imagey)
                    st.image(imagez)
                    st.image(imageaa)
                    st.image(imageab)
                    st.image(imageac)
                elif choose == "その他":
                    st.image(imagead)
                    st.image(imageae)
                    st.image(imageaf)
                    st.image(imageag)
                    st.image(imageah)
                    st.image(imageai)
                    st.image(imageaj)
                    st.image(imageak)
                    st.image(imageal)
            if gender == "女":
                st.write(f"残金 {womans_total} 円")

        st.title("終了！")
        st.write("残金" + int(st.session_state.current_total) + "円")