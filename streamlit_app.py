import os
import yt_dlp
import whisper
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
from deep_translator import GoogleTranslator

# ========== SETTINGS ==========
TARGET_LANG = "te"  # Telugu (change to "hi" for Hindi, etc.)
OUTPUT_NAME = "translated_video.mp4"

# ========== STREAMLIT GUI ==========
st.title("🎬 YouTube Video Voice Translator")
st.write("Translate YouTube videos into any language (ex: Telugu) for free!")

url = st.text_input("Enter YouTube video URL:")
target_lang = st.text_input("Target language code (example: te for Telugu)", TARGET_LANG)

if st.button("Start Translation"):
    if not url:
        st.error("Please enter a YouTube video link.")
    else:
        try:
            st.info("📥 Downloading video...")
            ydl_opts = {'outtmpl': 'video.mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            st.success("Video downloaded successfully!")

            st.info("🎵 Extracting audio...")
            os.system("ffmpeg -y -i video.mp4 -q:a 0 -map a audio.mp3")
            st.success("Audio extracted.")

            st.info("🗣️ Transcribing audio using Whisper model...")
            model = whisper.load_model("base")
            result = model.transcribe("audio.mp3")
            text = result["text"]

            with open("original_text.txt", "w", encoding="utf-8") as f:
                f.write(text)

            st.success("Transcription complete!")

            st.info(f"🌐 Translating text into {target_lang} ...")
            translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
            with open("translated_text.txt", "w", encoding="utf-8") as f:
                f.write(translated)

            st.success("Translation done!")

            st.info("🔊 Generating new audio...")
            tts = gTTS(translated, lang=target_lang)
            tts.save("voice.mp3")

            st.success("Voice created successfully!")

            st.info("🎬 Merging new audio with video...")
            video = VideoFileClip("video.mp4")
            new_audio = AudioFileClip("voice.mp3")
            final_video = video.set_audio(new_audio)
            final_video.write_videofile(OUTPUT_NAME, codec="libx264", audio_codec="aac")

            st.video(OUTPUT_NAME)
            st.success("✅ Translation complete! You can now play or download your video.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
