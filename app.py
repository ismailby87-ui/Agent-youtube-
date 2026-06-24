import streamlit as st
import os
import subprocess
from yt_dlp import YoutubeDL
from openai import OpenAI

st.set_page_config(page_title="Ghost-Reels Factory", layout="wide")

st.title("🏭 Ghost-Reels Factory")

# Utilisation des "secrets" de Streamlit ou saisie manuelle
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    st.info("Astuce : Si rien ne se passe, vérifie que ta clé OpenAI est active.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Source")
    url = st.text_input("Colle le lien ici (TikTok, Insta, YouTube)")
    lancer = st.button("🚀 LANCER LA GÉNÉRATION")

if lancer:
    if not api_key or not url:
        st.warning("⚠️ Remplis la clé API et l'URL d'abord.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            # --- PHASE 1 : TÉLÉCHARGEMENT ---
            with st.status("Étape 1 : Téléchargement...") as status:
                if os.path.exists("video.mp4"): os.remove("video.mp4")
                
                ydl_opts = {
                    'outtmpl': 'video.mp4',
                    'format': 'best[ext=mp4]/best',
                    'quiet': True,
                    'no_warnings': True
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                if os.path.exists("video.mp4"):
                    st.write("✅ Vidéo capturée !")
                else:
                    st.error("❌ Le téléchargement a échoué.")
                    st.stop()

            # --- PHASE 2 : IA ---
            with st.status("Étape 2 : Intelligence Artificielle...") as status:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": "Donne moi un titre viral de 3 mots max pour une vidéo courte. Réponds juste le titre."}]
                )
                titre = res.choices[0].message.content
                st.write(f"✅ Titre généré : {titre}")

            # --- PHASE 3 : MONTAGE GHOST ---
            with st.status("Étape 3 : Montage Ghost...") as status:
                if os.path.exists("output.mp4"): os.remove("output.mp4")
                
                # Commande FFmpeg simplifiée au maximum pour éviter les bugs de police
                # On fait : Miroir + Zoom + Vitesse
                cmd = (
                    f'ffmpeg -y -i video.mp4 '
                    f'-vf "hflip,setpts=0.95*PTS,scale=1.1*iw:-1,crop=iw/1.1:ih/1.1" '
                    f'-c:a copy output.mp4'
                )
                
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if os.path.exists("output.mp4"):
                    st.write("✅ Montage terminé !")
                else:
                    st.error("❌ Erreur montage : " + result.stderr)
                    st.stop()

            # --- PHASE 4 : AFFICHAGE ---
            with col2:
                st.subheader("🎬 Résultat Final")
                st.video("output.mp4")
                st.success(f"Titre : {titre}")
                with open("output.mp4", "rb") as f:
                    st.download_button("📥 SAUVEGARDER SUR TABLETTE", f, file_name="ghost_video.mp4")

        except Exception as e:
            st.error(f"💥 Erreur globale : {str(e)}")
