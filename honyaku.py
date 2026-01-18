import streamlit as st
import requests
import json
import urllib.parse

# --- 設定（GASのURLをここに貼る） ---
GAS_URL = "https://script.google.com/macros/s/AKfycbyCRsqwZpnj2M_ullXFJJXCeZGlhaQpeNnWnIabNdNC1wh9RJ4_s099hE_q4avvWbPkOg/exec"

st.set_page_config(page_title="翻訳保存メモ", page_icon="🎤")
st.title("🎤 翻訳メモ（最終安定版）")

# 言語選択
option = st.selectbox('翻訳先を選んでください', ('インドネシア語', '英語'))
lang_code = 'id' if option == 'インドネシア語' else 'en'

st.write("### 1. 日本語を話す（または入力）")
text_input = st.text_area("ここをタップしてマイクで話してください", height=100)

if text_input:
    st.write("---")
    st.write("### 2. 翻訳結果")
    
    # Google翻訳のページへのリンクを表示（確実なバックアップ）
    encoded_text = urllib.parse.quote(text_input)
    google_url = f"https://translate.google.com/?sl=ja&tl={lang_code}&text={encoded_text}&op=translate"
    
    st.markdown(f"[👉 もし表示されない場合はこちらで翻訳]({google_url})")

    # 簡易的な翻訳表示（GASに翻訳を任せる仕組み）
    if st.button(f"✅ スプレッドシートへ保存"):
        if GAS_URL != "あなたのGASのURLをここに貼る":
            # GAS側で翻訳も行うようにデータを送る
            data = {"ja": text_input, "lang": lang_code}
            requests.post(GAS_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            st.balloons()
            st.success("スプレッドシートに送信しました！")
        else:
            st.warning("GASのURLを設定してください")

st.divider()
st.caption("PC: Windowsキー + H / Mac: fnキー2回 で音声入力")
