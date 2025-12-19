# 🎵 Discord Music Bot (yt-dlp)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0%2B-5865F2?style=for-the-badge&logo=discord)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green?style=for-the-badge&logo=ffmpeg)

A lightweight, self-hosted Discord music bot capable of playing audio directly from YouTube links using `yt-dlp` and `ffmpeg`.  
It supports cookie-based authentication to bypass YouTube restrictions.

> **Note:** This project includes setups for both English and Turkish speakers.  
> 🇹🇷 **Türkçe dokümantasyon için [aşağı kaydırın](#-discord-müzik-botu-türkçe).**

---

## 🇺🇸 Features

- **YouTube Playback:** Downloads and streams audio from YouTube URLs  
- **Local File Support:** Plays files located in the `music/` directory  
- **Cookie Support:** Uses `cookies.txt` to handle age-restricted or premium content  
- **Clean Management:** Auto-deletes temporary files after playback or when skipped  

---

## 🛠️ Installation & Setup

### 1. Prerequisites

Ensure you have the following installed:

- Python **3.8+**
- **FFmpeg** (must be added to system PATH)
- **yt-dlp** (binary executable)

### 2. Clone the Repository

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
3. Install Dependencies
bash
Kodu kopyala
pip install -r requirements.txt
4. Configuration
Bot Token (Environment Variable):

bash
Kodu kopyala
export DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
Cookies:

Place your cookies.txt (Netscape format) in the root directory

Required for age-restricted or premium content

yt-dlp Path:

Default path: /usr/local/bin/yt-dlp

Update bot.py if different

🚀 Usage
Run the bot:

bash
Kodu kopyala
python3 bot.py
Commands (Turkish-based)
!katıl → Summons the bot to your voice channel

!çal <url> → Plays audio from a YouTube link

!kes → Stops playback and clears queue

!git → Disconnects the bot

🇹🇷 Discord Müzik Botu (Türkçe)
yt-dlp ve ffmpeg altyapısını kullanarak YouTube üzerinden yüksek kaliteli müzik çalan, kendi sunucunuzda barındırabileceğiniz basit ve güçlü bir Discord botu.

✨ Özellikler
YouTube Oynatma: Linkleri indirip anında oynatır

Çerez Desteği: cookies.txt sayesinde yaş kısıtlamalarını aşar

Otomatik Temizlik: Şarkı bitince geçici dosyaları siler

🛠️ Kurulum
1. Gereksinimler
Python 3.8+

FFmpeg (PATH’e ekli olmalı)

yt-dlp (/usr/local/bin altında veya yol düzenlenmeli)

2. Kütüphanelerin Yüklenmesi
bash
Kodu kopyala
pip install -r requirements.txt
3. Ayarlamalar
Bot Token:

bash
Kodu kopyala
export DISCORD_TOKEN="TOKEN_BURAYA"
Cookies:

YouTube cookies içeren cookies.txt dosyasını ana dizine ekleyin

Olmazsa indirme işlemi hata verir

🚀 Kullanım
bash
Kodu kopyala
python3 bot.py
Komutlar
!katıl → Botu ses kanalına çağırır

!çal <link> → YouTube linkini indirir ve çalar

!kes → Müziği durdurur ve dosyayı siler

!git → Bot kanaldan ayrılır

⚠️ Disclaimer / Yasal Uyarı
This bot is for educational purposes only.
Downloading copyrighted content may violate YouTube Terms of Service.

Bu bot yalnızca eğitim amaçlıdır.
YouTube’dan telifli içerik indirmek Hizmet Koşulları’na aykırı olabilir.
