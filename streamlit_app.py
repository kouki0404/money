import streamlit as st
import pandas as pd
import numpy as np
import random
import plotly.graph_objects as go
from PIL import Image
import sqlite3
import hashlib
import os
import plotly.express as px

# 画像をロードする関数
def load_images():
    images = {
        'beef': Image.open('牛肉.png'),#niku
        'pork': Image.open('豚肉.png'),#buta
        'chicken': Image.open('鶏肉.png'),#tori
        'hamburger': Image.open('合いびき肉.png'),#aibiki
        'carrot': Image.open('人参.png'),#ninnjinn
        'potato': Image.open('じゃがいも.png'),#jaga
        'onion': Image.open('玉ねぎ.png'),#tama
        'cabbage': Image.open('キャベツ.png'),#cabb
        'lettuce': Image.open('レタス.png'),#lett
        'tomato': Image.open('トマト.png'),#tomato
        'cucumber': Image.open('きゅうり.png'),#cucu
        'shiitake': Image.open('しいたけ.png'),#shiitake
        'gobo': Image.open('ごぼう.png'),#gobo
        'broccoli': Image.open('ブロッコリー.png'),#broc
        'green_onion': Image.open('ネギ.png'),#negi
        'nira': Image.open('ニラ.png'),#nira
        'garlic': Image.open('にんにく.png'),#garl
        'green_pepper': Image.open('ピーマン.png'),#pepp
        'ginger': Image.open('生姜.png'),#ging
        'green_peas': Image.open('グリーンピース.png'),#peas
        'bamboo_shoot': Image.open('筍.png'),#bamboo
        'salt': Image.open("塩.png"),#salt
        'sugar': Image.open("砂糖.png"),#sugar
        'soy_sauce': Image.open("醤油.png"),#soy
        'miso': Image.open("みそ.png"),#miso
        'salad_oil': Image.open("サラダ油.png"),#sala
        'rice': Image.open("米.png"),#rice
        'egg': Image.open("卵.png"),#egg
        'saba': Image.open("さば.png"),#saba
        'soba': Image.open("そば.png"),#soba
        'pasta': Image.open("パスタ.png"),#pasta
        'butter': Image.open("バター.png"),#butt
        'bacon': Image.open("ベーコン.png"),#bacon
        'shrimp': Image.open("海老.png"),#ebi
        'tofu': Image.open("豆腐.png")#tofu
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
if 'days_zone' not in st.session_state:
    st.session_state.days_zone = 0
if 'total_money' not in st.session_state:
    st.session_state.total_money = 100000
if 'total_niku' not in st.session_state:
    st.session_state.total_niku = 0
if 'total_buta' not in st.session_state:
    st.session_state.total_buta = 0
if 'total_tori' not in st.session_state:
    st.session_state.total_tori = 0
if 'total_aibiki' not in st.session_state:
    st.session_state.total_aibiki = 0
if 'total_ninnjinn' not in st.session_state:
    st.session_state.total_ninnjinn = 0
if 'total_jaga' not in st.session_state:
    st.session_state.total_jaga = 0
if 'total_tama' not in st.session_state:
    st.session_state.total_tama = 0
# 曜日設定
youbi_list = ["月", "火", "水", "木", "金", "土", "日"]
youbi = youbi_list[st.session_state.days % 7]
total_days = 7

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

# セッション状態の初期化
def initialize_session_state():
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

# DB接続
conn = sqlite3.connect('user_data.db')
# パスワードをハッシュ化する関数
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# ハッシュ化されたパスワードをチェックする関数
def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# ユーザーテーブルとその他のテーブルを作成する関数
def create_user_table(conn):
    c = conn.cursor()
    # ユーザー情報を格納するテーブル
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS user_score(username TEXT PRIMARY KEY, score INTEGER)')
def delete_all_users(conn, username):
    c = conn.cursor()
    c.execute('DELETE FROM user_score WHERE username = ?', (username,))
    conn.commit()

# ユーザーをデータベースに追加する関数
def add_user(conn, username, password):
    try:
        # パスワードをハッシュ化
        hashed_password = make_hashes(password)

        # カーソルを作成
        c = conn.cursor()
        
        # ユーザーを追加するSQL文
        c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, hashed_password))
        
        # コミットして変更を保存
        conn.commit()
        
        # 成功した場合にTrueを返す
        return True
    except sqlite3.IntegrityError as e:
        # ユーザー名が重複している場合など、IntegrityErrorをキャッチ
        st.error(f"エラーが発生しました: {e}")
        return False
    except Exception as e:
        # 他のエラーに対応するための一般的な例外処理
        st.error(f"予期しないエラーが発生しました: {e}")
        return False

# ユーザーが存在するかチェックする関数
def check_user_exists(conn, username):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    return c.fetchone() is not None

# ユーザーのログインを確認する関数
def login_user(conn, username, password):
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    user = c.fetchone()
    if user and check_hashes(password, user[1]):
        return user
    return None
def save_user_score(conn, username, score):
    c = conn.cursor()
    
    # ユーザーがすでに存在しているか確認
    c.execute('SELECT username FROM user_score WHERE username = ?', (username,))
    existing_user = c.fetchone()
    
    if existing_user:
        # すでにユーザーが存在する場合、スコアを更新
        c.execute('UPDATE user_score SET score = ? WHERE username = ?', (score, username))
    else:
        # ユーザーが存在しない場合、新しいユーザーのスコアを挿入
        c.execute('INSERT INTO user_score(username, score) VALUES (?, ?)', (username, score))
    
    conn.commit()
def load_data():
    # Excelファイルを読み込む
    df = pd.read_excel("Nextday.xlsx", header=0)
    df.columns = df.columns.astype(str).str.strip()
    return df
# データを読み込む
words_df = load_data()
print("Columns in words_df:", words_df.columns)

# 読み込まれた列数が予想通りか確認
expected_columns = ['No.', '材料', '料理名', '値段', 'タンパク質', '脂質', '炭水化物', '無機質', 'ビタミン']
if len(words_df.columns) != len(expected_columns):
    st.error(f"Expected {len(expected_columns)} columns, but found {len(words_df.columns)} columns.")
else:
    # 列名が一致した場合、列名を設定
    words_df.columns = expected_columns
dish_start = 1
dish_end = 252
# "No."列が dish_start から dish_end の範囲に含まれるデータをフィルタリングし、"No."列でソート
filtered_words_df = words_df[(words_df['No.'] >= dish_start) & (words_df['No.'] <= dish_end)].sort_values(by='No.')
print("Columns in words_df:", words_df.columns)
# メイン関数

def main():
    # データベースに接続
    conn = sqlite3.connect('database.db')
    create_user_table(conn)
    menu = ["アカウント作成", "管理者用", "メイン画面"]
    choose = st.sidebar.selectbox("", menu)

    # 新規アカウント作成部分
    if choose == "アカウント作成":
        st.subheader("新しいアカウントを作成します")
        new_user = st.text_input("ユーザー名を入力してください")
        new_password = st.text_input("パスワードを入力してください", type='password')

        if st.button("サインアップ"):
            if check_user_exists(conn, new_user):
                st.error("このユーザー名は既に使用されています。別のユーザー名を選んでください。")
            else:
                # ユーザー名、ハッシュ化されたパスワードをデータベースに保存
                if add_user(conn, new_user, new_password):
                    st.session_state['username'] = new_user  # セッションにユーザー名を設定
                    st.success("アカウントの作成に成功しました")
                    st.info("ログイン画面からログインしてください")
                else:
                    st.error("アカウント作成に失敗しました。")
    # ログイン処理
    elif choose == "管理者用":
        st.subheader("管理者用")
        if username == "sky_kk":
            st.success("昊")
            if st.button("すべてのユーザーのデータを削除"):
                if delete_all_users(conn):
                    st.success("すべてのユーザーのデータが削除されました。")
                else:
                    st.error("データの削除に失敗しました。")
    if 'username' in st.session_state and st.session_state.username:
        username = st.session_state['username']
        foods = ["ホーム", "肉類", "野菜", "調味料", "その他"]
        reizouko = st.sidebar.selectbox("冷蔵庫", foods)
        item_date = ["牛肉 100g 900円", "豚肉 100g 200円", "鶏肉 100g 150円", "卵 1パック 200円", "米 5kg 2500円", "大根 1本 200円", "キャベツ 1玉 300円", "みそ 1パック 300円", "合いびき肉 100g 200円"]


        selected_item = st.sidebar.selectbox("基本値段", item_date)
        if choose == "メイン画面" and reizouko == "ホーム":
            st.session_state.update({
                'test_started': True,
                'correct_dish': 0,
                'current_dish': 0,
                'finished': False,
                'wrong_answers': [],
            })
            times = ["朝","昼","夜"]
            days_total = st.session_state.days//3 + 1
            st.write(f"{st.session_state.month}月 {days_total}日 {youbi}曜日{times[st.session_state.days_zone]}")
            st.write(f"残金: {st.session_state.total_money} 円")  # 修正: remaining_balance を直接mens_totalとして表示

            st.session_state.current_dish += 1
            if st.session_state.current_dish < 9:
                    if "selected_questions" not in st.session_state:
                      st.session_state.selected_questions = pd.DataFrame()  # 空のデータフレームで初期化

                    if "current_question" not in st.session_state:
                      st.session_state.current_question = 0  # 初期値を設定
                    if len(st.session_state.selected_dishes) >= 3:
                      options = list(st.session_state.selected_dishes['料理名'].sample(3))
                    options.append(st.session_state.current_question_data['料理名'])
                    np.random.shuffle(options)
                    st.session_state.options = options
                    st.session_state.answer = None
            else:
                    st.session_state.finished = True
            if 'test_started' in st.session_state and not st.session_state.finished:
                ryouri_name = ['']
                st.subheader(f"料理")
                st.subheader(f"{st.session_state.current_dish_data['料理名']}")

            else:
                if 'test_started' in st.session_state and st.session_state.finished:
                    display_results()    
            if st.button("決定"):
                st.session_state.days += 1
                st.session_state.days_zone += 1
                if st.session_state.days_zone == 2:
                    st.session_state.days_zone = 0
        # 冷蔵庫のアイテム選択
        images = load_images()
        if reizouko == "肉類":
            material = ["牛肉 100g900円", "豚肉 100g300円", "鶏肉 100g200円", "合いびき肉 100g200円"]
            choice = st.selectbox("", material)
            glam = st.number_input("購入する量", min_value=100, max_value=1000, step=100)
            if st.button("購入する"):
                if choice == "牛肉 100g900円":
                    total_niku += glam
                    st.session_state.total_money -= (900 // 100) * glam
                elif choice == "豚肉 100g300円":
                    total_buta += glam
                    st.session_state.total_money -= (300 // 100) * glam
                elif choice == "鶏肉 100g200円":
                    total_tori += glam
                    st.session_state.total_money -= (200 // 100) * glam
                else:
                    total_aibiki += glam 
                    st.session_state.total_money -= (200 // 100) * glam
            st.image(images['beef'])
            st.write(f"現在{total_niku}g")
            st.image(images['pork'])
            st.write(f"現在{total_buta}g")
            st.image(images['chicken'])
            st.write(f"現在{total_tori}g")
            st.image(images['hamburger'])
            st.write(f"現在{total_aibiki}g")
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

def display_results():
    #スコアリング方法　金額//100+1000*栄養観点
    correct_answers = st.session_state.correct_answers
    total_questions = st.session_state.total_questions
    wrong_answers = [wa for wa in st.session_state.wrong_answers if wa[0] in st.session_state.selected_questions['No.'].values]
    result = mens_total //100
    st.write(f"終了！スコア: {result}")
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()