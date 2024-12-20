import streamlit as st
import pandas as pd
import numpy as np
import random
from PIL import Image
import sqlite3
import hashlib
import os

# 画像をロードする関数
def load_images():
    # 各食材や調味料に対応する画像をロード
    images = {
        '牛肉': Image.open('牛肉.png'),
        '豚肉': Image.open('豚肉.png'),
        '鶏肉': Image.open('鶏肉.png'),
        '合いびき肉': Image.open('合いびき肉.png'),
        '人参': Image.open('人参.png'),
        'じゃがいも': Image.open('じゃがいも.png'),
        '玉ねぎ': Image.open('玉ねぎ.png'),
        'キャベツ': Image.open('キャベツ.png'),
        'レタス': Image.open('レタス.png'),
        'トマト': Image.open('トマト.png'),
        'きゅうり': Image.open('きゅうり.png'),
        'しいたけ': Image.open('しいたけ.png'),
        'ごぼう': Image.open('ごぼう.png'),
        'ブロッコリー': Image.open('ブロッコリー.png'),
        'ネギ': Image.open('ネギ.png'),
        'ニラ': Image.open('ニラ.png'),
        'にんにく': Image.open('にんにく.png'),
        'ピーマン': Image.open('ピーマン.png'),
        '生姜': Image.open('生姜.png'),
        'グリーンピース': Image.open('グリーンピース.png'),
        '筍': Image.open('筍.png'),
        '塩': Image.open("塩.png"),
        '砂糖': Image.open("砂糖.png"),
        '醤油': Image.open("醤油.png"),
        'みそ': Image.open("みそ.png"),
        'サラダ油': Image.open("サラダ油.png"),
        '米': Image.open("米.png"),
        '卵': Image.open("卵.png"),
        'さば': Image.open("さば.png"),
        'そば': Image.open("そば.png"),
        'パスタ': Image.open("パスタ.png"),
        'バター': Image.open("バター.png"),
        'ベーコン': Image.open("ベーコン.png"),
        '海老': Image.open("海老.png"),
        '豆腐': Image.open("豆腐.png")
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
if 'total_cabb' not in st.session_state:
    st.session_state.total_cabb = 0
if 'total_lett' not in st.session_state:
    st.session_state.total_lett = 0
if 'total_tomato' not in st.session_state:
    st.session_state.total_tomato = 0
if 'total_cucu' not in st.session_state:
    st.session_state.total_cucu = 0
if 'total_shiitake' not in st.session_state:
    st.session_state.total_shiitake = 0
if 'total_gobo' not in st.session_state:
    st.session_state.total_gobo = 0
if 'total_broc' not in st.session_state:
    st.session_state.total_broc = 0
if 'total_negi' not in st.session_state:
    st.session_state.total_negi = 0
if 'total_nira' not in st.session_state:
    st.session_state.total_nira = 0
if 'total_garl' not in st.session_state:
    st.session_state.total_garl = 0
if 'total_pepp' not in st.session_state:
    st.session_state.total_pepp = 0
if 'total_ging' not in st.session_state:
    st.session_state.total_ging = 0
if 'total_peas' not in st.session_state:
    st.session_state.total_peas = 0
if 'total_bamboo' not in st.session_state:
    st.session_state.total_bamboo = 0
if 'total_salt' not in st.session_state:
    st.session_state.total_salt = 0
if 'total_suger' not in st.session_state:
    st.session_state.total_suger = 0
if 'total_soy' not in st.session_state:
    st.session_state.total_soy = 0
if 'total_miso' not in st.session_state:
    st.session_state.total_miso = 0
if 'total_sala' not in st.session_state:
    st.session_state.total_sala = 0
if 'total_rice' not in st.session_state:
    st.session_state.total_rice = 0
if 'total_egg' not in st.session_state:
    st.session_state.total_egg = 0
if 'total_saba' not in st.session_state:
    st.session_state.total_saba = 0
if 'total_soba' not in st.session_state:
    st.session_state.total_soba = 0
if 'total_pasta' not in st.session_state:
    st.session_state.total_pasta = 0
if 'total_butt' not in st.session_state:
    st.session_state.total_butt = 0
if 'total_bacon' not in st.session_state:
    st.session_state.total_bacon = 0
if 'total_ebi' not in st.session_state:
    st.session_state.total_ebi = 0
if 'total_tofu' not in st.session_state:
    st.session_state.total_tofu = 0
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
        username = st.text_input("ユーザー")
        password = st.text_input("パスワード")
        if username == "sky_kk" and password == "Kita4127":
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
            times = ["朝", "昼", "夜"]
            days_total = st.session_state.days // 3 + 1
            st.write(f"{st.session_state.month}月 {st.session_state.days}日 {youbi}曜日{times[st.session_state.days_zone]}")
            st.write(f"残金: {st.session_state.total_money} 円")

            st.session_state.current_dish += 1
            if st.session_state.days < 9:
                if 'test_started' in st.session_state and not st.session_state.finished:
                    ryouri_name = ['チキンカレーライス','肉じゃが','とんかつ','卵かけご飯','ハンバーグ','ロールキャベツ','かけそば','オムライス','チャーハン','牛丼','唐揚げ','生姜焼き','団子汁','春巻き','鯖の塩焼き','マカロニグラタン','クリームシチュー','ポトフ','親子丼','冷やし中華','麻婆豆腐','回鍋肉','ペペロンチーノ','鯛のカルパッチョ','お好み焼き','ゴーヤチャンプル','プルコギ','きんぴらごぼう','筑前煮','すき焼き']
                    choice_ryouri = st.selectbox("",ryouri_name)
                    if st.button("決定"):
                        if choice_ryouri == "チキンカレーライス":
                            if st.session_state.total_tori < 35 or st.session_state.total_jaga < 40 or st.session_state.total_ninnjinn < 45 or st.session_state.total_rice < 180:
                                st.error("材料が足りません")
                            else:
                                st.session_state.days_zone += 1
                                if st.session_state.days_zone > 2:
                                    st.session_state.days_zone = 0
                                    st.session_state.days += 1
                else:
                    st.session_state.finished = True

            else:
                if 'test_started' in st.session_state and st.session_state.finished:
                    display_results()    
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