import streamlit as st
import yt_dlp
import os
import re

# Page Configuration
st.set_page_config(page_title="Video Downloader", page_icon="📥", layout="centered")

# Custom CSS for UI
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📥 Social Media Downloader")
st.write("Download high-quality videos from YouTube, Instagram, X, and Facebook.")

url = st.text_input("", placeholder="Paste your video link here...")

if url:
    try:
        # 1. Setup Options for Extraction
        extract_opts = {
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

        with st.spinner("Fetching video details..."):
            with yt_dlp.YoutubeDL(extract_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            # UI Layout for Preview
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(info.get('thumbnail', ''), use_container_width=True)
            with col2:
                st.write(f"**Title:** {info.get('title', 'Unknown Title')[:50]}...")
                st.write(f"**Source:** {info.get('extractor_key', 'Unknown')}")

            # 2. Download Logic
            if st.button("Download Video"):
                if not os.path.exists('downloads'):
                    os.makedirs('downloads')
                
                file_path = f"downloads/{info['id']}.mp4"
                
                # Setup Download Options with 403 Bypass Headers
                dl_opts = {
                    'format': 'best', # Using 'best' to avoid FFmpeg issues for now
                    'outtmpl': file_path,
                    'noplaylist': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'referer': 'https://www.google.com/',
                }

                with yt_dlp.YoutubeDL(dl_opts) as ydl:
                    ydl.download([url])

                with open(file_path, "rb") as f:
                    st.download_button(
                        label="✅ Save to Device",
                        data=f,
                        file_name=f"video_{info['id']}.mp4",
                        mime="video/mp4"
                    )
                    
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.divider()
st.caption("Note: For high-resolution (1080p+) merging, ensure FFmpeg is installed on the server.")
