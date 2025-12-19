import os
import asyncio
import discord
from discord.ext import commands
import subprocess
import uuid

TOKEN = os.getenv("DISCORD_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")
MUSIC_DIR = "music"
YTDLP = "/usr/local/bin/yt-dlp"

os.makedirs(MUSIC_DIR, exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

current_file = None

@bot.event
async def on_ready():
    print(f"Giriş yapıldı: {bot.user}")
    if PROXY_URL:
        safe_proxy = PROXY_URL.split("@")[-1] if "@" in PROXY_URL else "Ayarlı"
        print(f"Proxy devrede: ...@{safe_proxy}")

async def ses_kanalina_baglan(ctx):
    if ctx.voice_client:
        return ctx.voice_client
    if not ctx.author.voice:
        await ctx.send("❌ Önce bir ses kanalına girmen gerekiyor.")
        return None
    return await ctx.author.voice.channel.connect()

def youtube_download(url: str) -> str:
    out_file = os.path.join(MUSIC_DIR, f"{uuid.uuid4()}.mp3")

    cmd = [
        YTDLP,
        "--no-playlist",
        "-f", "bestaudio/best",
        "-x",
        "--audio-format", "mp3",
        "--force-ipv4",
        "--no-check-certificate",
        "--extractor-args", "youtube:player_client=android",
        "-o", out_file,
        url
    ]

    if PROXY_URL:
        cmd.insert(1, "--proxy")
        cmd.insert(2, PROXY_URL)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Hata Logu: {result.stderr}")
        raise RuntimeError("İndirme başarısız")

    if not os.path.exists(out_file):
        raise RuntimeError("Dosya indirilemedi")

    return out_file

@bot.command(name="katıl")
async def katil(ctx):
    await ses_kanalina_baglan(ctx)

@bot.command(name="git")
async def git(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@bot.command(name="kes")
async def kes(ctx):
    global current_file
    if ctx.voice_client:
        ctx.voice_client.stop()
    if current_file and os.path.exists(current_file):
        try: os.remove(current_file)
        except: pass
        current_file = None

@bot.command(name="çal")
async def cal(ctx, kaynak: str):
    global current_file
    vc = await ses_kanalina_baglan(ctx)
    if not vc: return

    if vc.is_playing() or vc.is_paused():
        vc.stop()
        await asyncio.sleep(0.5)

    if current_file and os.path.exists(current_file):
        try: os.remove(current_file)
        except: pass
        current_file = None

    yerel_dosya = os.path.join(MUSIC_DIR, kaynak)
    if os.path.exists(yerel_dosya):
        current_file = yerel_dosya
        vc.play(discord.FFmpegPCMAudio(yerel_dosya))
        await ctx.send(f"🎵 Çalıyor: {kaynak}")
        return

    url = kaynak
    if not kaynak.startswith("http"):
        url = f"https://www.youtube.com/watch?v={kaynak}"

    await ctx.send("🎵 Müzik hazırlanıyor...")
    try:
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, youtube_download, url)
    except Exception:
        await ctx.send("❌ Müzik açılamadı.")
        return
        
    current_file = file_path
    vc.play(discord.FFmpegPCMAudio(file_path))

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN eksik!")

bot.run(TOKEN)