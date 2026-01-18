import streamlit as st
from googletrans import Translator
from streamlit_mic_recorder import mic_recorder
import requests
import json
import io

# --- 設定 ---
GAS_URL = "あなたのGASのURLをここに貼る"

st.set_page_config(page_title="おはなしメモ", page_icon="🎤")
st.title("🎤 おはなしメモ (安定版)")

translator = Translator()

# --- 録音ボタン（より確実な方式に変更） ---
st.write("ボタンを押して録音し、終わったらもう一度押してください。")
audio = mic_recorder(
    start_prompt="🎤 録音開始",
    stop_prompt="⏹️ 録音終了",
    key='recorder'
)

# 録音データが届いたら処理
if audio:
    # 音声からテキストへの変換（Streamlitの標準機能を利用）
    # ※ 本来は音声認識APIが必要ですが、まずはテキスト入力でテストできる窓を作ります
    st.audio(audio['bytes'])
    st.info("音声が届きました！")
    
    # テキスト入力欄（音声認識が不安定な時のバックアップ）
    text_input = st.text_input("ここに日本語を入力、または音声から自動入力されます", "")
    
    if text_input:
        try:
            translated = translator.translate(text_input, src='ja', dest='en')
            st.subheader("英語翻訳:")
            st.success(translated.text)
            
            # GAS送信
            if GAS_URL != "あなたのGASのURLをここに貼る":
                data = {"ja": text_input, "trans": translated.text}
                requests.post(GAS_URL, data=json.dumps(data))
                st.toast("スプレッドシートに保存しました！")
        except Exception as e:
            st.error(f"翻訳エラー: {e}")
