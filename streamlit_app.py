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
mens_money = 3000 + st.session_state.energy
mens_total = 61000
womans_total = 47000

# パスワードをハッシュ化する関数
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
 
def delete_study_data(conn, username, date):
    c = conn.cursor()
    c.execute('DELETE FROM study_data WHERE username = ? AND date = ?', (username, date))
    conn.commit()
 
# ハッシュ化されたパスワードをチェックする関数
def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text
def create_tables(con):
    cc = con.cursor()
    cc.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    con.commit()
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
    conn.commit()
#新しいユーザーを追加する関数
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
 
# ユーザーをログインさせる関数
def login_user(conn, username, password):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    user = c.fetchone()
    if user and check_hashes(password, user[1]):  # user[1] はハッシュ化されたパスワード
        return user  # ユーザー情報を返す
    return None
@st.cache_data
def load_data():
    main = pd.read_excel("基本ストーリー.xlsx")
    special = pd.read_excel("金銭リスト.xlsx")
    cook = pd.read_excel("栄養・材料の量の内訳.xlsx")
    swich = pd.read_excel("Nextday.xlsx")
    return pd.concat([main, special], ignore_index=True)

words_df = load_data()
# メイン関数
def main():
    # データベースに接続
    conn = sqlite3.connect('database.db')
    create_user_table(conn)
    menu = ["アカウント作成","ログイン","ゲーム画面"]
    choose = st.sidebar.selectbox("",menu)
    # アイテム選択
    item_date = ["牛肉 100g 400円", "豚肉 100g 200円", "鶏肉 100g 150円", "卵 1パック 200円", "米 5kg 2500円", "大根 1本 200円", "キャベツ 1玉 300円", "みそ 1パック 300円", "合いびき肉 100g 200円"]

    # ユーザー名の入力
    if 'username' in st.session_state and st.session_state.username:
        username = st.session_state['username']
        foods = ["ホーム","肉類","野菜","調味料","その他"]
        reizouko = st.sidebar.selectbox("冷蔵庫",foods)

        # ゲーム画面
        selected_item = st.sidebar.selectbox("基本値段", item_date)
        if choose == "ゲーム画面" and reizouko == "ホーム":
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
        if reizouko == "肉類":
            st.image(images['beef'])
            st.image(images['pork'])
            st.image(images['chicken'])
            st.image(images['hamburger'])
        elif reizouko == "野菜":
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
        elif reizouko == "調味料":
            st.image(images['salt'])
            st.image(images['sugar'])
            st.image(images['soy_sauce'])
            st.image(images['miso'])
            st.image(images['salad_oil'])
        elif reizouko == "その他":
            st.image(images['rice'])
            st.image(images['egg'])
            st.image(images['saba'])
            st.image(images['soba'])
            st.image(images['pasta'])
            st.image(images['butter'])
            st.image(images['bacon'])

    if choose == "ログイン":
        st.subheader("ログイン画面です")
        username = st.sidebar.text_input("ユーザー名を入力してください")
        password = st.sidebar.text_input("パスワードを入力してください", type='password')
 
        if st.sidebar.button("ログイン"):
            user_info = login_user(conn, username, make_hashes(password))
 
            if user_info:
                st.session_state['username'] = username
                st.success("{}さんでログインしました".format(username))
                st.success('ホーム画面に移動して下さい')
 
                # データ削除のオプション
            else:
                st.warning("ユーザー名かパスワードが間違っています")
    elif choose == "アカウント作成":
        st.subheader("新しいアカウントを作成します")
        new_user = st.text_input("ユーザー名を入力してください")
        new_password = st.text_input("パスワードを入力してください", type='password')
        gender = st.selectbox("性別を選んでください", ["性別を選択してください", "男", "女"])
 
        if st.button("サインアップ"):
            if check_user_exists(conn, new_user):
                st.error("このユーザー名は既に使用されています。別のユーザー名を選んでください。")
            else:
                try:
                    add_user(conn, new_user, make_hashes(new_password))
                    st.success("アカウントの作成に成功しました")
                    st.info("ログイン画面からログインしてください")
                except Exception as e:
                    st.error(f"アカウントの作成に失敗しました: {e}")

 
            if username == "sky0404":
                st.success("こんにちは、北山さん！")
 
                if st.button("すべてのユーザーのデータを削除"):
                    if delete_all_users(conn):
                        st.success("すべてのユーザーのデータが削除されました。")
                    else:
                        st.error("データの削除に失敗しました。")
if __name__ == '__main__':
    main()