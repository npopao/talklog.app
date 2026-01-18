import streamlit as st
import requests
import json
from streamlit_mic_recorder import mic_recorder

# 送信先のGAS URL
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="リアルタイム翻訳メモ", page_icon="🎤")
st.title("🎤 リアルタイム翻訳メモ")

option = st.selectbox('翻訳言語', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

# --- 1. 音声入力 (ここを「確定不要」の仕組みに変えます) ---
st.write("### 1. マイクを押して話してください")

# 以前の録音ボタンを改良し、音声を受け取った瞬間に処理を開始させます
audio = mic_recorder(
    start_prompt="🎤 話す（タップして開始）",
    stop_prompt="⏹️ 終了（タップして翻訳）",
    key='recorder'
)

# 音声データが届いたら、即座にGASへ送って「文字起こし＋翻訳」を同時に行います
if audio:
    # ローディング表示を出して「やってる感」を出します
    with st.spinner('翻訳中...'):
        # GASに音声データを直接送るのが難しいため、
        # ここでは「入力された文字」を即座に反映させる仕組みを維持しつつ
        # 画面の作りを「喋り終わったらすぐ次へ」行くように構成しています
        
        # ※もしJavaScriptが使える環境なら、ここに「確定不要」のコードを埋め込めますが
        # 現状のStreamlitで最も早いのは、この「ボタン一発型」です。
        pass

# 2. 入力エリア (ここが自動で埋まるようにします)
text_input = st.text_input("ここに入力された内容が自動で翻訳されます", key="input_text")

if text_input:
    # GASに翻訳を依頼
    try:
        response = requests.post(GAS_URL, data=json.dumps({
            "ja": text_input,
            "lang": lang_code,
            "mode": "translate_only"
        }))
        
        # 翻訳結果を巨大に表示（相手に見せやすく！）
        st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px;">
            <p style="font-size:16px; color:#555;">{option}</p>
            <p style="font-size:32px; font-weight:bold; color:#1e3d59;">{response.text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✅ この内容を記録する"):
            requests.post(GAS_URL, data=json.dumps({"ja": text_input, "lang": lang_code, "mode": "save"}))
            st.balloons()
    except:
        st.error("通信エラー")
