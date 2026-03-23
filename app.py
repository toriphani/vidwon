import streamlit as st
import yt_dlp
import os
import re

# Page Configuration
st.set_page_config(page_title="Universal Video Downloader", page_icon="📥", layout="centered")

# Custom CSS for a "Clean & Professional" look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📥 Social Media Downloader")
st.subheader("Download from YouTube, Instagram, X (Twitter), and Facebook")

url = st.text_input("", placeholder="Paste your video link here...")

def get_video_info(url):
    ydl_opts = {
    'format': 'best',
    'quiet': True,
    'no_warnings': True,
    # Forces IPv4 to avoid common IPv6 blocks on cloud servers
    'source_address': '0.0.0.0', 
    # Mimics a real Windows Chrome browser
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'add_header': [
        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language: en-US,en;q=0.9',
    ],
    'nocheckcertificate': True,
}
            with st.spinner("Fetching video details..."):
            info = get_video_info(url)
            
            # Display Video Preview
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(info.get('thumbnail', ''), use_container_width=True)
            with col2:
                st.write(f"**Title:** {info.get('title', 'Unknown Title')}")
                st.write(f"**Duration:** {info.get('duration_string', 'N/A')}")
                st.write(f"**Source:** {info.get('extractor_key', 'Unknown')}")

            # Download Logic
            # Note: For webapps, we download to a temporary buffer or file 
            # and then serve it to the user via st.download_button
            if st.button("Prepare Download"):
                file_path = f"downloads/{info['id']}.mp4"
                
                # Ensure directory exists
                if not os.path.exists('downloads'):
                    os.makedirs('downloads')

                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': file_path,
                    'noplaylist': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                with open(file_path, "rb") as f:
                    st.download_button(
                        label="🔥 Click to Save to Device",
                        data=f,
                        file_name=f"{re.sub(r'[^a-zA-Z0-9]', '_', info['title'])}.mp4",
                        mime="video/mp4"
                    )
                
                # Cleanup: Optional (remove file after download button is clicked)
                # os.remove(file_path)

    except Exception as e:
        st.error(f"Error: Make sure the URL is valid. ({str(e)})")

st.info("💡 **Note:** This tool is for personal use only. Please respect creators' copyrights.")
