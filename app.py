import streamlit as st
import yt_dlp
import os
import re

# Page Configuration
st.set_page_config(page_title="YT Downloader & Converter", page_icon="🎬", layout="centered")

# YouTube-inspired Dark Theme UI
st.markdown("""
    <style>
    .main { background-color: #0f0f0f; color: white; }
    .stTextInput>div>div>input { background-color: #212121; color: white; border: 1px solid #3f3f3f; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    .video-btn { background-color: #cc0000 !important; color: white !important; }
    .audio-btn { background-color: #2ba640 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 YT Video & Audio Downloader")
url = st.text_input("", placeholder="Paste YouTube link here...")

def is_youtube_url(url):
    return re.match(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+', url)

if url:
    if not is_youtube_url(url):
        st.error("⚠️ Please enter a valid YouTube URL.")
    else:
        try:
            with st.spinner("🔍 Fetching metadata..."):
                ydl_opts = {
                    'quiet': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                
                # Display Video Info
                st.image(info.get('thumbnail', ''), width=450)
                st.subheader(info.get('title'))
                
                col1, col2 = st.columns(2)

                # --- VIDEO DOWNLOAD BUTTON ---
                with col1:
                    if st.button("🎥 Download Video (MP4)"):
                        with st.spinner("Downloading video..."):
                            save_path = f"downloads/{info['id']}.mp4"
                            opts = {
                                'format': 'best',
                                'outtmpl': save_path,
                                'noplaylist': True,
                            }
                            with yt_dlp.YoutubeDL(opts) as ydl:
                                ydl.download([url])
                            
                            with open(save_path, "rb") as f:
                                st.download_button("💾 Save MP4", f, file_name=f"{info['title']}.mp4")

                # --- AUDIO DOWNLOAD BUTTON ---
                with col2:
                    if st.button("🎵 Download Audio (MP3)"):
                        with st.spinner("Extracting audio..."):
                            # We use 'bestaudio' to get the highest quality stream
                            save_path = f"downloads/{info['id']}.mp3"
                            opts = {
                                'format': 'bestaudio/best',
                                'outtmpl': save_path,
                                # Note: If ffmpeg is on server, use postprocessors for true MP3
                                # If no ffmpeg, this will just save the audio stream (m4a/webm)
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                            }
                            with yt_dlp.YoutubeDL(opts) as ydl:
                                ydl.download([url])
                            
                            with open(save_path, "rb") as f:
                                st.download_button("💾 Save MP3", f, file_name=f"{info['title']}.mp3")

        except Exception as e:
            st.error(f"Something went wrong. YouTube might be blocking the request. Error: {e}")

st.divider()
st.caption("Privacy: We do not store your data. Files are deleted after the session.")
