import streamlit as st
import requests
import json

# 送信先のGAS URL
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="おはなしメモ", page_icon="🎤")
st.title("🎤 おはなしメモ（PC安定版）")

# 言語選択
option = st.selectbox('翻訳したい言語を選んでください', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

st.write(f"現在は **{option}** 設定です。")

# 入力エリア
st.write("### 1. 日本語で話してください")
text_input = st.text_area("ここをクリックして [Windowsキー + H] で音声入力", height=150)

if text_input:
    st.write("---")
    st.write("### 2. スプレッドシートへ保存")
    st.info(f"「保存」を押すと、シート側で自動的に{option}に翻訳されて記録されます。")
    
    if st.button(f"✅ {option}に翻訳して保存する"):
        # 翻訳指示を含めてデータを送信
        data = {
            "ja": text_input,
            "lang": lang_code
        }
        
        try:
            # GASへ送信
            response = requests.post(GAS_URL, data=json.dumps(data))
            
            if response.status_code == 200:
                st.balloons()
                st.success("スプレッドシートに送信しました！")
            else:
                st.error(f"エラーが発生しました (Status: {response.status_code})")
        except Exception as e:
            st.error(f"送信エラー: {e}")

st.divider()
st.caption("※画面上に翻訳が出ないのは、動作を安定させるための仕様です。結果はスプレッドシートを確認してください。")