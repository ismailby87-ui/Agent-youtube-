import streamlit as st
import os
import subprocess
from yt_dlp import YoutubeDL
from openai import OpenAI

st.set_page_config(page_title="Ghost-Reels Factory", layout="wide")

st.title("🏭 Ghost-Reels Factory")

# --- FORMULAIRE POUR FIXER LES DONNÉES SUR TABLETTE ---
with st.sidebar:
    st.header("🔑 Configuration")
    # On utilise une clé unique pour que la tablette s'en souvienne
    api_key_input = st.text_input("OpenAI API Key", type="password", key="my_api_key")

with st.container():
    st.subheader("📥 Lancement du Projet")
    
    # Création d'un formulaire : tout ce qui est dedans est envoyé d'un coup
    with st.form("main_form"):
        url_input = st.text_input("Colle le lien ici (TikTok, Insta, YouTube)", key="my_url")
        submit_button = st.form_submit_button("🚀 LANCER LA GÉNÉRATION")

# --- LOGIQUE DE TRAVAIL ---
if submit_button:
    # On vérifie si les cases sont vides
    if not api_key_input or not url_input:
        st.error("⚠️ Attention : Tu dois coller l'API et l'URL avant de cliquer sur le bouton.")
    else:
        try:
            client = OpenAI(api_key=api_key_input)
            
            # 1. TÉLÉCHARGEMENT
            with st.status("Étape 1 : Téléchargement...") as status:
                if os.path.exists("video.mp4"): os.remove("video.mp4")
                
                ydl_opts = {
                    'outtmpl': 'video.mp4',
                    'format': 'best[ext=mp4]/best',
                    'quiet': True,
                    'no_warnings': True
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                st.write("✅ Vidéo capturée !")

            # 2. IA
            with st.status("Étape 2 : Intelligence Artificielle...") as status:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": "Donne moi un titre viral de 3 mots max. Réponds juste le titre."}]
                )
                titre = res.choices[0].message.content
                st.write(f"✅ Titre : {titre}")

            # 3. MONTAGE GHOST
            with st.status("Étape 3 : Montage Ghost...") as status:
                if os.path.exists("output.mp4"): os.remove("output.mp4")
                
                # Montage simple pour tablette
                cmd = f'ffmpeg -y -i video.mp4 -vf "hflip,setpts=0.95*PTS,scale=1.1*iw:-1,crop=iw/1.1:ih/1.1" -c:a copy output.mp4'
                subprocess.run(cmd, shell=True, capture_output=True)
                st.write("✅ Montage terminé !")

            # 4. AFFICHAGE
            st.divider()
            col_v, col_t = st.columns([1,1])
            with col_v:
                st.video("output.mp4")
            with col_t:
                st.success(f"**Titre :** {titre}")
                with open("output.mp4", "rb") as f:
                    st.download_button("📥 SAUVEGARDER SUR TABLETTE", f, file_name="video_finale.mp4")

        except Exception as e:
            st.error(f"💥 Erreur : {str(e)}")
