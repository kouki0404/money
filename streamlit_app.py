import streamlit as st
import pandas as pd
import random
from PIL import Image
import sqlite3
import hashlib
import os

# 画像をロードする関数
def load_images():
    images = {
        'beef': Image.open('牛肉.png'),
        'pork': Image.open('豚肉.png'),
        'chicken': Image.open('鶏肉.png'),
        'hamburger': Image.open('合いびき肉.png'),
        'carrot': Image.open('人参.png'),
        'potato': Image.open('じゃがいも.png'),
        'onion': Image.open('玉ねぎ.png'),
        'cabbage': Image.open('キャベツ.png'),
        'lettuce': Image.open('レタス.png'),
        'tomato': Image.open('トマト.png'),
        'cucumber': Image.open('きゅうり.png'),
        'shiitake': Image.open('しいたけ.png'),
        'gobo': Image.open('ごぼう.png'),
        'broccoli': Image.open('ブロッコリー.png'),
        'green_onion': Image.open('ネギ.png'),
        'nira': Image.open('ニラ.png'),
        'garlic': Image.open('にんにく.png'),
        'green_pepper': Image.open('ピーマン.png'),
        'ginger': Image.open('生姜.png'),
        'green_peas': Image.open('グリーンピース.png'),
        'bamboo_shoot': Image.open('筍.png'),
        'salt': Image.open("塩.png"),
        'sugar': Image.open("砂糖.png"),
        'soy_sauce': Image.open("醤油.png"),
        'miso': Image.open("みそ.png"),
        'salad_oil': Image.open("サラダ油.png"),
        'rice': Image.open("米.png"),
        'egg': Image.open("卵.png"),
        'saba': Image.open("さば.png"),
        'soba': Image.open("そば.png"),
        'pasta': Image.open("パスタ.png"),
        'butter': Image.open("バター.png"),
        'bacon': Image.open("ベーコン.png"),
        'shrimp': Image.open("海老.png"),
        'tofu': Image.open("豆腐.png")
    }
    return images

# セッションステートの初期化
if 'energy' not in st.session_state:
    st.session_state.energy = random.randint(-700, 700)
if 'month' not in st.session_state:
    st.session_state.month = random.randint(1, 12)
if 'days' not in st.session_state:
    st.session_state.days = 1
if 'code' not in st.session_state:
    st.session_state.code = 0
if 'username' not in st.session_state:
    st.session_state.username = ""

# 曜日設定
youbi_list = ["月", "火", "水", "木", "金", "土", "日"]
youbi = youbi_list[st.session_state.days % 7]

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

# 基本的な金額設定
mens_money = 13000 + st.session_state.energy
mens_total = 270400
womans_total = 208000

# SQLiteデータベース接続
def create_user_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_data(username TEXT PRIMARY KEY, text_content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS study_data(username TEXT, date TEXT, study_hours REAL, score INTEGER, subject TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS goals(username TEXT PRIMARY KEY, goal TEXT)''')
    conn.commit()

def add_user(conn, username):
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username) VALUES (?)', (username,))
    conn.commit()

# メイン関数
def main():
    # データベースに接続
    conn = sqlite3.connect('database.db')
    create_user_table(conn)
    
    # アイテム選択
    item_date = ["牛肉 100g 400円", "豚肉 100g 200円", "鶏肉 100g 150円", "卵 1パック 200円", "米 5kg 2500円", "大根 1本 200円", "キャベツ 1玉 300円", "みそ 1パック 300円", "合いびき肉 100g 200円"]
    
    # 性別選択
    gender = st.selectbox("性別を選んでください", ["性別を選択してください", "男", "女"])
    
    # 名前決定ボタン
    if st.button("名前、性別を決定"):
        if gender == "性別を選んでください" or not st.session_state.username:
            st.write("性別を選択、または名前を設定してください")
        else:
            st.write(f"ようこそ、{st.session_state.username}さん！")
    
    # アイテム選択
    selected_item = st.sidebar.selectbox("基本値段", item_date)

    # ユーザー名の入力
    if 'username' in st.session_state and st.session_state.username:
        username = st.session_state['username']
        choose = st.sidebar.radio("", ("ゲーム画面", "肉類", "野菜", "調味料", "その他"), horizontal=True)
        
        # ゲーム画面
        if choose == "ゲーム画面":
            st.write(f"{st.session_state.month}月 {st.session_state.days}日 {youbi}曜日")
            st.write(f"初期金額 {mens_total} 円 (光熱費が引かれています)")
            
            # 食費の処理（仮）
            food_expense = 1500
            remaining_balance = mens_total - food_expense
            st.write(f"残金: {remaining_balance} 円")
            
            # Chatbot iframe
            st.markdown("""
            <iframe src="https://www.chatbase.co/chatbot-iframe/nVm1Yf2i4qWPwWDlr9itc" width="100%" style="height: 100%; min-height: 700px" frameborder="0"></iframe>
            """, unsafe_allow_html=True)
        
        # 肉類、野菜、調味料、その他の選択
        images = load_images()
        if choose == "肉類":
            st.image(images['beef'])
            st.image(images['pork'])
            st.image(images['chicken'])
            st.image(images['hamburger'])
        elif choose == "野菜":
            st.image(images['carrot'])
            st.image(images['potato'])
            st.image(images['onion'])
            st.image(images['cabbage'])
            st.image(images['lettuce'])
            st.image(images['tomato'])
            st.image(images['cucumber'])
            st.image(images['shiitake'])
            st.image(images['gobo'])
            st.image(images['broccoli'])
        elif choose == "調味料":
            st.image(images['salt'])
            st.image(images['sugar'])
            st.image(images['soy_sauce'])
            st.image(images['miso'])
            st.image(images['salad_oil'])
        elif choose == "その他":
            st.image(images['rice'])
            st.image(images['egg'])
            st.image(images['saba'])
            st.image(images['soba'])
            st.image(images['pasta'])
            st.image(images['butter'])
            st.image(images['bacon'])
