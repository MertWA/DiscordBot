import os
import asyncio
import discord
from discord.ext import commands
import subprocess
import uuid

TOKEN = os.getenv("DISCORD_TOKEN")
MUSIC_DIR = "music"
COOKIES_FILE = "cookies.txt"
YTDLP = "/usr/local/bin/yt-dlp"

os.makedirs(MUSIC_DIR, exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

current_file = None

@bot.event
async def on_ready():
    print(f"Giriş yapıldı: {bot.user}")

async def ses_kanalina_baglan(ctx):
    if ctx.voice_client:
        return ctx.voice_client
    if not ctx.author.voice:
        await ctx.send("❌ Önce bir ses kanalına girmen gerekiyor.")
        return None
    return await ctx.author.voice.channel.connect()

def youtube_download(url: str) -> str:
    if not os.path.exists(COOKIES_FILE):
        raise RuntimeError("cookies.txt bulunamadı")

    out_file = os.path.join(MUSIC_DIR, f"{uuid.uuid4()}.mp3")

    cmd = [
        YTDLP,
        "--js-runtimes", "node",
        "--cookies", COOKIES_FILE,
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--no-playlist",
        "-o", out_file,
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0 or not os.path.exists(out_file):
        raise RuntimeError(result.stderr.strip() or "YouTube indirilemedi")

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
        os.remove(current_file)
        current_file = None

@bot.command(name="çal")
async def cal(ctx, kaynak: str):
    global current_file
    vc = await ses_kanalina_baglan(ctx)
    if not vc:
        return

    if vc.is_playing() or vc.is_paused():
        vc.stop()
        await asyncio.sleep(0.5)

    if current_file and os.path.exists(current_file):
        os.remove(current_file)
        current_file = None

    if kaynak.startswith("http"):
        await ctx.send("⬇️ YouTube indiriliyor...")
        try:
            file_path = youtube_download(kaynak)
        except Exception as e:
            await ctx.send(f"❌ YouTube hatası:\n```{str(e)[:1500]}```")
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
    raise RuntimeError("DISCORD_TOKEN ortam değişkeni bulunamadı!")

bot.run(TOKEN)