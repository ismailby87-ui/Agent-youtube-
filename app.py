import streamlit as st
import os
import subprocess
from yt_dlp import YoutubeDL
from openai import OpenAI

st.set_page_config(page_title="Ghost-Reels Factory", layout="wide")

st.title("🏭 Ghost-Reels Factory")

with st.sidebar:
    st.header("🔑 Configuration")
    api_key_input = st.text_input("OpenAI API Key", type="password", key="my_api_key")
    st.info("Si TikTok bloque (Erreur 403), utilise l'option 'Upload Manuel' ci-dessous.")

# --- CHOIX DE LA SOURCE ---
mode = st.radio("Choisis ta source :", ["Lien automatique (TikTok/Insta)", "Upload Manuel (Plus fiable)"])

with st.form("main_form"):
    if mode == "Lien automatique (TikTok/Insta)":
        url_input = st.text_input("Colle le lien de la vidéo")
        uploaded_file = None
    else:
        uploaded_file = st.file_opener = st.file_uploader("Choisis la vidéo depuis ta tablette", type=["mp4", "mov"])
        url_input = None
        
    submit_button = st.form_submit_button("🚀 LANCER LA GÉNÉRATION")

if submit_button:
    if not api_key_input:
        st.error("⚠️ Ajoute ta clé OpenAI !")
    else:
        try:
            client = OpenAI(api_key=api_key_input)
            raw_video = "input.mp4"

            # --- ETAPE 1 : ACQUISITION ---
            with st.status("Étape 1 : Récupération de la vidéo...") as status:
                if os.path.exists("input.mp4"): os.remove("input.mp4")
                
                if mode == "Lien automatique (TikTok/Insta)" and url_input:
                    ydl_opts = {
                        'outtmpl': 'input.mp4',
                        'format': 'best',
                        'nocheckcertificate': True,
                        'quiet': True,
                        'addheader': [('User-Agent', 'Mozilla/5.0')],
                    }
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url_input])
                elif uploaded_file:
                    with open("input.mp4", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                else:
                    st.error("Donne un lien ou un fichier !")
                    st.stop()
                st.write("✅ Vidéo prête !")

            # --- ETAPE 2 : IA ---
            with st.status("Étape 2 : Intelligence Artificielle...") as status:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": "Donne moi un titre viral de 3 mots. Réponds juste le titre."}]
                )
                titre = res.choices[0].message.content
                st.write(f"✅ Titre généré : {titre}")

            # --- ETAPE 3 : MONTAGE GHOST ---
            with st.status("Étape 3 : Montage Anti-Copyright...") as status:
                if os.path.exists("output.mp4"): os.remove("output.mp4")
                # Montage puissant : Miroir + Vitesse + Zoom
                cmd = f'ffmpeg -y -i input.mp4 -vf "hflip,setpts=0.95*PTS,scale=1.2*iw:-1,crop=iw/1.2:ih/1.2" -c:a copy output.mp4'
                subprocess.run(cmd, shell=True, capture_output=True)
                st.write("✅ Montage terminé !")

            # --- ETAPE 4 : RESULTAT ---
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.video("output.mp4")
            with c2:
                st.success(f"🔥 Titre : {titre}")
                with open("output.mp4", "rb") as f:
                    st.download_button("📥 SAUVEGARDER SUR TABLETTE", f, file_name="video_finale.mp4")

        except Exception as e:
            st.error(f"💥 Erreur : {str(e)}")
            st.info("Conseil : Si c'est une erreur 403, télécharge la vidéo sur ta tablette et utilise le 'Upload Manuel'.")
