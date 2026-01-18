import streamlit as st
from googletrans import Translator
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import requests
import json
import io

# --- 設定（GASのURLをここに貼る） ---
GAS_URL = "あなたのGASのURLをここに貼る"

st.set_page_config(page_title="おはなしメモ", page_icon="🎤")
st.title("🎤 おはなしメモ (解決版)")

translator = Translator()
r = sr.Recognizer()

st.write("ボタンを押して録音し、終わったらもう一度押してください。")
audio = mic_recorder(
    start_prompt="🎤 録音開始",
    stop_prompt="⏹️ 録音終了",
    key='recorder'
)

if audio:
    # 録音データを変換可能なバイナリとして読み込む
    audio_bio = io.BytesIO(audio['bytes'])
    
    try:
        # 【修正ポイント】音声データを読み取ってGoogleが認識できる形にする
        with sr.AudioFile(audio_bio) as source:
            audio_data = r.record(source)
            
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
            requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            st.toast("スプレッドシートに保存完了！")
            
    except sr.UnknownValueError:
        st.warning("声が聞き取れませんでした。もう少し長く、はっきり話してみてください。")
    except Exception as e:
        # 万が一エラーが出ても、手入力でリカバリーできるように入力欄を出す
        st.error(f"音声認識ができませんでした。直接入力も可能です。")
        manual_text = st.text_input("ここに日本語を入力してください")
        if manual_text:
            translated = translator.translate(manual_text, src='ja', dest='en')
            st.success(translated.text)
