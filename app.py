import streamlit as st
import os
import subprocess
from yt_dlp import YoutubeDL
from openai import OpenAI

st.set_page_config(page_title="Ghost-Reels Factory", layout="wide")

# --- INTERFACE ---
st.title("🏭 Ghost-Reels Factory")

with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Nouvelle Chasse")
    url = st.text_input("Lien de la vidéo source")
    style = st.selectbox("Style IA", ["Viral", "Mystérieux", "Éducatif"])
    lancer = st.button("Lancer la Transformation")

if lancer and url and api_key:
    client = OpenAI(api_key=api_key)
    
    with st.status("L'agent travaille...") as s:
        # 1. Téléchargement
        s.write("📥 Capture de la vidéo...")
        ydl_opts = {'outtmpl': 'input.mp4', 'format': 'best'}
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # 2. IA
        s.write("🧠 Création du titre viral...")
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Fais un titre de 3 mots pour cette vidéo : {url}"}]
        )
        titre = res.choices[0].message.content

        # 3. Montage Ghost (Anti-Copyright)
        s.write("🎬 Application du montage Ghost...")
        cmd = [
            'ffmpeg', '-y', '-i', 'input.mp4',
            '-vf', f"hflip,setpts=0.95*PTS,scale=1.1*iw:-1,crop=iw/1.1:ih/1.1,drawtext=text='{titre}':fontcolor=yellow:fontsize=40:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.5",
            '-c:a', 'copy', 'output.mp4'
        ]
        subprocess.run(cmd)
        
    with col2:
        st.subheader("✅ Résultat")
        st.video("output.mp4")
        st.success(f"Titre : {titre}")
        with open("output.mp4", "rb") as f:
            st.download_button("📥 Sauvegarder sur Tablette", f, file_name="video_finale.mp4")
