import streamlit as st
import os
import subprocess
from yt_dlp import YoutubeDL
from openai import OpenAI

# Configuration de la page
st.set_page_config(page_title="Ghost-Reels Factory", layout="wide")

st.title("🏭 Ghost-Reels Factory")

# --- BARRE LATERALE ---
with st.sidebar:
    st.header("🔑 Configuration")
    api_key_input = st.text_input("OpenAI API Key", type="password", key="my_api_key")
    st.info("Colle ta clé 'sk-...' ici.")

# --- FORMULAIRE PRINCIPAL ---
with st.form("main_form"):
    url_input = st.text_input("Lien de la vidéo (TikTok, Insta, YouTube)")
    submit_button = st.form_submit_button("🚀 LANCER LA GÉNÉRATION")

# --- LOGIQUE DE TRAVAIL ---
if submit_button:
    if not api_key_input or not url_input:
        st.error("⚠️ Remplis la clé API et l'URL !")
    else:
        try:
            client = OpenAI(api_key=api_key_input)
            
            # 1. TÉLÉCHARGEMENT
            with st.status("Étape 1 : Téléchargement...") as status:
                if os.path.exists("video.mp4"): os.remove("video.mp4")
                
                ydl_opts = {
                    'outtmpl': 'video.mp4',
                    'format': 'best',
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'addheader': [
                        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'),
                    ],
                }
                
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                st.write("✅ Vidéo capturée !")

            # 2. INTELLIGENCE ARTIFICIELLE
            with st.status("Étape 2 : Création du titre IA...") as status:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": "Donne moi un titre viral de 3 mots max. Réponds juste le titre."}]
                )
                titre = res.choices[0].message.content
                st.write(f"✅ Titre : {titre}")

            # 3. MONTAGE GHOST
            with st.status("Étape 3 : Montage Anti-Copyright...") as status:
                if os.path.exists("output.mp4"): os.remove("output.mp4")
                # Commande FFmpeg simplifiée (Miroir + Zoom + Vitesse)
                cmd = f'ffmpeg -y -i video.mp4 -vf "hflip,setpts=0.95*PTS,scale=1.1*iw:-1,crop=iw/1.1:ih/1.1" -c:a copy output.mp4'
                subprocess.run(cmd, shell=True, capture_output=True)
                st.write("✅ Montage terminé !")

            # 4. AFFICHAGE DES RESULTATS
            st.divider()
            col_left, col_right = st.columns(2)
            
            with col_left:
                if os.path.exists("output.mp4"):
                    st.video("output.mp4")
            
            with col_right:
                st.success(f"🔥 **Titre généré :** {titre}")
                st.write("Vidéo prête pour YouTube Shorts / TikTok")
                with open("output.mp4", "rb") as f:
                    st.download_button("📥 SAUVEGARDER SUR TABLETTE", f, file_name="video_finale.mp4")

        except Exception as e:
            st.error(f"💥 Erreur : {str(e)}")
