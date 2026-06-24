# --- PHASE 1 : TÉLÉCHARGEMENT (Version Spéciale TikTok) ---
            with st.status("Étape 1 : Téléchargement...") as status:
                if os.path.exists("video.mp4"): os.remove("video.mp4")
                
                ydl_opts = {
                    'outtmpl': 'video.mp4',
                    'format': 'best',
                    'quiet': True,
                    'no_warnings': True,
                    # Ces lignes aident à contourner le blocage TikTok :
                    'nocheckcertificate': True,
                    'ignoreerrors': False,
                    'logtostderr': False,
                    'addheader': [
                        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'),
                        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                        ('Accept-Language', 'en-US,en;q=0.5'),
                    ],
                }
                
                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url_input])
                    st.write("✅ Vidéo capturée !")
                except Exception as e:
                    st.error("❌ TikTok bloque la connexion. Essaie de copier le lien d'une autre vidéo ou d'une autre plateforme (Insta/YouTube) pour tester.")
                    st.stop()
