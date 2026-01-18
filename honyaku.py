import sys
import streamlit as st


# がめんの　せってい
st.set_page_config(page_title="TalkLog", layout="wide")


st.components.v1.html(
    """
    <html>
    <body style="font-family: sans-serif; background-color: #f4f7f6; padding: 10px;">
        <div style="max-width: 800px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
           
            <h1 style="color: #333; font-size: 24px; margin-bottom: 5px;">おはなしメモ</h1>
            <p style="color: #888; font-size: 14px; margin-bottom: 20px;">しゃべった　ことばを　「きろく」　します</p>


            <div style="background: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #eee;">
                <div style="margin-bottom: 10px;">
                    <label style="font-size: 14px; font-weight: bold;">やりかた：</label>
                    <select id="modeSelect" style="padding: 8px; font-size: 14px; border-radius: 4px; border: 1px solid #ccc;">
                        <option value="trans" selected>ほんやく　をつける</option>
                        <option value="mono">にほんご　だけ</option>
                    </select>
                </div>
               
                <div id="langSettings">
                    <label style="font-size: 14px; font-weight: bold;">ほんやくの　ことば：</label>
                    <select id="langSelect" style="padding: 8px; font-size: 14px; border-radius: 4px; border: 1px solid #ccc;">
                        <option value="id" selected>インドネシアご（尼）</option>
                        <option value="en">えいご</option>
                        <option value="zh-CN">ちゅうごくご</option>
                        <option value="vi">ベトナムご</option>
                    </select>
                </div>
               
                <div style="margin-top: 15px; font-size: 14px; color: #555; border-top: 1px solid #eee; padding-top: 10px;">
                    いままでの　もじすう： <span id="charCount" style="font-weight: bold; color: #007bff; font-size: 18px;">0</span> もじ
                </div>
            </div>


            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <button id="btn" style="flex: 2; background-color: #007bff; color: white; padding: 18px; border-radius: 8px; border: none; font-size: 18px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 0 #0056b3;">
                    ききとりを　はじめる
                </button>
                <button id="downloadBtn" style="flex: 1; background-color: white; color: #333; border: 2px solid #333; padding: 18px; border-radius: 8px; cursor: pointer; font-weight: bold;">
                    ほぞんする
                </button>
            </div>


            <div id="status" style="color: #007bff; font-size: 13px; margin-bottom: 15px; font-weight: bold; text-align: center;">ボタンを　おすと　うごきます</div>
           
            <div id="log" style="height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: #fff; display: flex; flex-direction: column-reverse; gap: 12px; line-height: 1.6;">
                </div>
        </div>


        <script>
        const btn = document.getElementById('btn');
        const downloadBtn = document.getElementById('downloadBtn');
        const modeSelect = document.getElementById('modeSelect');
        const langSelect = document.getElementById('langSelect');
        const langSettings = document.getElementById('langSettings');
        const log = document.getElementById('log');
        const status = document.getElementById('status');
        const charCountDisp = document.getElementById('charCount');
       
        let totalChars = 0;
        let fullLog = "おはなしメモ　きろく\\n\\n";


        modeSelect.onchange = () => {
            langSettings.style.display = (modeSelect.value === 'trans') ? 'block' : 'none';
        };


        const Speech = window.SpeechRecognition || window.webkitSpeechRecognition;


        if (Speech) {
            const rec = new Speech();
            rec.lang = 'ja-JP';
            rec.continuous = true;
            let active = false;


            btn.onclick = () => {
                if (!active) {
                    rec.start();
                    btn.innerText = "ストップ";
                    btn.style.backgroundColor = "#ff4d4f";
                    btn.style.boxShadow = "0 4px 0 #b33637";
                    status.innerText = "おはなしを　きいています...";
                    active = true;
                } else {
                    rec.stop();
                    btn.innerText = "ききとりを　はじめる";
                    btn.style.backgroundColor = "#007bff";
                    btn.style.boxShadow = "0 4px 0 #0056b3";
                    status.innerText = "とまっています";
                    active = false;
                }
            };


            rec.onresult = async (e) => {
                const jaText = e.results[e.results.length - 1][0].transcript;
                const mode = modeSelect.value;
                const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
               
                totalChars += jaText.length;
                charCountDisp.innerText = totalChars;


                let entryHtml = `<div style="padding: 10px; border-left: 4px solid #007bff; background: #f8f9ff;">
                                    <span style="font-size: 11px; color: #999;">${time}</span><br>
                                    <div style="font-size: 15px; color: #333; margin-top: 4px;">${jaText}</div>`;
                let logText = `[${time}] ${jaText}\\n`;


                if (mode === 'trans') {
                    const targetLang = langSelect.value;
                    const targetName = langSelect.options[langSelect.selectedIndex].text.split('（')[0];
                   
                    try {
                        const res = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=ja&tl=${targetLang}&dt=t&q=${encodeURIComponent(jaText)}`);
                        const data = await res.json();
                        const transText = data[0][0][0];
                       
                        entryHtml += `<div style="color: #007bff; margin-top: 8px; font-weight: bold; border-top: 1px dashed #d0d0d0; padding-top: 5px;">${transText}</div>`;
                        logText += `(${targetName}) ${transText}\\n`;
                    } catch (err) { console.error(err); }
                }
               
                entryHtml += `</div>`;
                fullLog += logText + "\\n";
               
                const div = document.createElement('div');
                div.innerHTML = entryHtml;
                log.appendChild(div);
            };


            rec.onend = () => { if (active) rec.start(); };


            downloadBtn.onclick = () => {
                const blob = new Blob([fullLog], {type: 'text/plain'});
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `おはなしメモ_${new Date().toLocaleDateString()}.txt`;
                a.click();
            };
        }
        </script>
    </body>
    </html>
    """,
    height=850,
)

