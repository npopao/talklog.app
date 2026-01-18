import streamlit as st
from googletrans import Translator
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import requests
import json
import io

# --- 設定（ここにGASのURLを貼る） ---
GAS_URL = "あなたのGASのURLをここに貼る"

st.set_page_config(page_title="おはなしメモ", page_icon="🎤")
st.title("🎤 おはなしメモ (最終版)")

translator = Translator()
r = sr.Recognizer()

st.write("ボタンを押して録音し、終わったらもう一度押してください。")
audio = mic_recorder(
    start_prompt="🎤 録音開始",
    stop_prompt="⏹️ 録音終了",
    key='recorder'
)

if audio:
    # 録音データを処理可能な形式に変換
    audio_bio = io.BytesIO(audio['bytes'])
    
    with sr.AudioFile(audio_bio) as source:
        audio_data = r.record(source)
        try:
            # Googleの音声認識を実行
            text = r.recognize_google(audio_data, language='ja-JP')
            
            st.subheader("聞き取った内容:")
            st.info(text)
            
            # 翻訳実行
            translated = translator.translate(text, src='ja', dest='en')
            st.subheader("英語翻訳:")
            st.success(translated.text)
            
            # GASへの送信
            if GAS_URL != "あなたのGASのURLをここに貼る":
                data = {"ja": text, "trans": translated.text}
                requests.post(GAS_URL, data=json.dumps(data))
                st.toast("スプレッドシートに保存完了！")
                
        except sr.UnknownValueError:
            st.warning("声がうまく聞き取れませんでした。もう一度はっきり話してみてください。")
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.divider()
st.caption("※音声認識にはGoogleのサービスを利用しています。")
