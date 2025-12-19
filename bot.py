import os
import asyncio
import discord
from discord.ext import commands
import subprocess
import uuid

TOKEN = os.getenv("DISCORD_TOKEN")
# PROXY_URL terminalden alınacak
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
        # Güvenlik için şifreyi gizleyerek yazdıralım
        safe_proxy = PROXY_URL.split("@")[-1] if "@" in PROXY_URL else "Ayarlı"
        print(f"🌍 Proxy devrede: ...@{safe_proxy}")
    else:
        print(f"⚠️ Proxy YOK! Bu sunucu banlanabilir.")

async def ses_kanalina_baglan(ctx):
    if ctx.voice_client:
        return ctx.voice_client
    if not ctx.author.voice:
        await ctx.send("❌ Önce bir ses kanalına girmen gerekiyor.")
        return None
    return await ctx.author.voice.channel.connect()

def youtube_download(url: str) -> str:
    out_file = os.path.join(MUSIC_DIR, f"{uuid.uuid4()}.mp3")

    # GÜNCELLENMİŞ KOMUT YAPISI
    cmd = [
        YTDLP,
        "--no-playlist",
        "-f", "bestaudio/best",
        "-x",
        "--audio-format", "mp3",
        "--force-ipv4",
        "--no-check-certificate", # SSL hatalarını bazen proxy yüzünden verir, yok sayalım.
        
        # iOS yerine Android kullanıyoruz, PO Token istemez.
        "--extractor-args", "youtube:player_client=android",
        
        "-o", out_file,
        url
    ]

    # Proxy varsa ekle
    if PROXY_URL:
        cmd.insert(1, "--proxy")
        cmd.insert(2, PROXY_URL)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"⚠️ Hata Logu: {result.stderr}")
        
        if "Too Many Requests" in result.stderr or "429" in result.stderr:
             raise RuntimeError("Bu Proxy IP'si YouTube tarafından geçici limitlendi (429). Lütfen farklı bir Proxy IP'si deneyin.")
        
        if "Sign in" in result.stderr:
             raise RuntimeError("YouTube erişim reddetti. Proxy çalışmıyor olabilir.")
        
        raise RuntimeError(f"İndirme başarısız.")

    if not os.path.exists(out_file):
        raise RuntimeError("Dosya indirilemedi.")

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

    if kaynak.startswith("http"):
        await ctx.send("⬇️ Proxy ile indiriliyor...")
        try:
            loop = asyncio.get_event_loop()
            file_path = await loop.run_in_executor(None, youtube_download, kaynak)
        except Exception as e:
            await ctx.send(f"❌ Hata: {str(e)}")
            return
        current_file = file_path
        vc.play(discord.FFmpegPCMAudio(file_path))
        return

    dosya = os.path.join(MUSIC_DIR, kaynak)
    if not os.path.exists(dosya):
        await ctx.send("❌ Dosya bulunamadı.")
        return

    current_file = dosya
    vc.play(discord.FFmpegPCMAudio(dosya))
    await ctx.send(f"🎵 Çalıyor: {kaynak}")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN eksik!")

bot.run(TOKEN)