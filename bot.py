import os
import asyncio
import discord
from discord.ext import commands
import subprocess
import uuid
from dotenv import load_dotenv
import shutil

# .env yüklemesi
load_dotenv()

# --- AYARLAR ---
TOKEN = os.getenv("DISCORD_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")
MUSIC_DIR = "music"
COOKIES_FILE = "cookies.txt"

# yt-dlp yolunu bulamazsa sistemdekini kullan
YTDLP = shutil.which("yt-dlp") or "/usr/local/bin/yt-dlp"

# --- KONTROLLER ---
if not TOKEN:
    raise RuntimeError("HATA: .env dosyasında DISCORD_TOKEN bulunamadı!")

os.makedirs(MUSIC_DIR, exist_ok=True)

# --- BOT KURULUMU ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# --- GLOBAL DEĞİŞKENLER ---
music_queue = [] 
current_track_info = None 
current_file_path = None

# --- YARDIMCI FONKSİYONLAR ---
def create_embed(title, description, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=description, color=color)
    return embed

def get_proxy_args():
    args = []
    # Cookies dosyasının varlığını ve doluluğunu kontrol et
    if os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 0:
        args.extend(["--cookies", COOKIES_FILE])
    
    if PROXY_URL:
        args.extend(["--proxy", PROXY_URL])
    return args

def youtube_download(query: str) -> str:
    out_file = os.path.join(MUSIC_DIR, f"{uuid.uuid4()}.mp3")
    
    url = query
    if not query.startswith("http"):
        url = f"ytsearch1:{query}"

    cmd = [
        YTDLP,
        # --- EKLENEN KISIM: JS MOTORU ---
        "--js-runtimes", "node", 
        
        "--no-playlist",
        "-f", "bestaudio/best",
        "-x",
        "--audio-format", "mp3",
        "--force-ipv4",
        "--no-check-certificate",
        
        # Web Tarayıcısı Taklidi (Güncel Chrome)
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        
        "-o", out_file,
        url
    ]

    # Proxy ve Cookies argümanlarını araya ekle
    # (Sabit parametrelerden sonra, URL'den önce)
    extra_args = get_proxy_args()
    insert_pos = len(cmd) - 1 
    for arg in reversed(extra_args):
        cmd.insert(insert_pos, arg)

    # İndirme işlemini başlat
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"DL Hata Detayı: {result.stderr}") 
        
        # Hata Analizi
        if "cookies are no longer valid" in result.stderr:
             raise RuntimeError("Cookies dosyası geçersiz oldu. Lütfen yenileyin.")
        if "Sign in" in result.stderr:
            raise RuntimeError("YouTube botu engelledi. Cookies veya Proxy yenilenmeli.")
            
        raise RuntimeError("İndirme servisinde hata oluştu.")

    if not os.path.exists(out_file):
        raise RuntimeError("Dosya oluşturulamadı.")

    return out_file

# --- OYNATMA MANTIĞI ---

async def play_next(ctx):
    global current_track_info, current_file_path
    
    if len(music_queue) == 0:
        current_track_info = None
        await ctx.send(embed=create_embed("Sıra Bitti", "🎵 Liste tamamlandı.", discord.Color.gold()))
        return

    track = music_queue.pop(0)
    current_track_info = track
    
    try:
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, youtube_download, track['query'])
        current_file_path = file_path

        vc = ctx.voice_client
        if not vc: return 

        vc.play(
            discord.FFmpegPCMAudio(file_path), 
            after=lambda e: bot.loop.create_task(song_finished(ctx, e, file_path))
        )
        
        await ctx.send(embed=create_embed("Şimdi Çalıyor", f"💿 **{track['query']}**\n👤 İsteyen: {track['requester']}", discord.Color.green()))

    except Exception as e:
        print(f"Oynatma hatası: {e}")
        # Hata mesajını kullanıcıya gösterelim ki ne olduğunu bilsinler
        err_msg = str(e) if "Cookies" in str(e) else "Teknik bir hata oluştu."
        await ctx.send(embed=create_embed("Hata", f"❌ '{track['query']}' çalınamadı: {err_msg}", discord.Color.red()))
        await play_next(ctx)

async def song_finished(ctx, error, file_path):
    if file_path and os.path.exists(file_path):
        try: os.remove(file_path)
        except: pass
    await play_next(ctx)

# --- EVENTLER ---
@bot.event
async def on_ready():
    print(f"✅ Giriş yapıldı: {bot.user}")
    
    safe_proxy = PROXY_URL.split("@")[-1] if PROXY_URL and "@" in PROXY_URL else "Yok"
    cookies_status = "Var" if os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 0 else "Yok/Boş"
    
    print(f"ℹ️ Sistem: Proxy={safe_proxy} | Cookies={cookies_status}")

# --- KOMUTLAR ---

@bot.command(name="baglan", aliases=["katıl", "join"])
async def baglan(ctx):
    if ctx.voice_client: return ctx.voice_client
    if not ctx.author.voice:
        await ctx.send(embed=create_embed("Uyarı", "❌ Önce bir ses kanalına katılmalısın.", discord.Color.red()))
        return None
    await ctx.author.voice.channel.connect()
    return ctx.voice_client

@bot.command(name="ayril", aliases=["git", "leave", "dc"])
async def ayril(ctx):
    global music_queue, current_track_info
    music_queue = []
    current_track_info = None
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send(embed=create_embed("Görüşürüz", "👋 Müzik sonlandırıldı.", discord.Color.orange()))

@bot.command(name="oynat", aliases=["çal", "play", "p"])
async def oynat(ctx, *, istek: str):
    vc = ctx.voice_client
    if not vc:
        if ctx.author.voice:
            vc = await ctx.author.voice.channel.connect()
        else:
            await ctx.send(embed=create_embed("Hata", "❌ Lütfen bir ses kanalına gir.", discord.Color.red()))
            return

    track = {'query': istek, 'requester': ctx.author.display_name}
    
    if not vc.is_playing() and not vc.is_paused():
        music_queue.append(track)
        await play_next(ctx) 
    else:
        music_queue.append(track)
        position = len(music_queue)
        await ctx.send(embed=create_embed("Sıraya Eklendi", f"📝 **{istek}**\n🔢 Sıradaki yeri: **{position}**", discord.Color.blue()))

@bot.command(name="sira", aliases=["queue", "list", "q"])
async def sira(ctx):
    if not music_queue and not current_track_info:
        await ctx.send(embed=create_embed("Sıra Boş", "📭 Şu an listede müzik yok.", discord.Color.greyple()))
        return

    desc = ""
    if current_track_info:
        desc += f"**💿 Şu An Çalıyor:** {current_track_info['query']} ({current_track_info['requester']})\n\n"
    
    if music_queue:
        desc += "**⏳ Bekleyenler:**\n"
        for i, track in enumerate(music_queue, 1):
            desc += f"`{i}.` {track['query']} _({track['requester']})_\n"
    else:
        desc += "\n_Sırada bekleyen başka şarkı yok._"

    await ctx.send(embed=create_embed("Müzik Listesi", desc, discord.Color.purple()))

@bot.command(name="durdur", aliases=["pause"])
async def durdur(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send(embed=create_embed("Duraklatıldı", "⏸️ Müzik geçici olarak durduruldu.", discord.Color.orange()))

@bot.command(name="devam", aliases=["resume"])
async def devam(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send(embed=create_embed("Devam", "▶️ Müzik kaldığı yerden devam ediyor.", discord.Color.green()))

@bot.command(name="gec", aliases=["skip", "s", "atla"])
async def gec(ctx, index: int = None):
    global music_queue
    vc = ctx.voice_client

    if not vc or (not vc.is_playing() and not vc.is_paused()):
        await ctx.send(embed=create_embed("Hata", "Şu an bir şey çalmıyor.", discord.Color.red()))
        return

    if index is not None:
        if 1 <= index <= len(music_queue):
            del music_queue[:index-1] 
            await ctx.send(embed=create_embed("Atlandı", f"⏭️ **{index}.** sıraya geçiliyor...", discord.Color.gold()))
            vc.stop() 
        else:
            await ctx.send(embed=create_embed("Hata", "❌ Geçersiz sıra numarası.", discord.Color.red()))
    else:
        await ctx.send(embed=create_embed("Geçildi", "⏭️ Şarkı geçildi.", discord.Color.gold()))
        vc.stop()

@bot.command(name="cikar", aliases=["remove", "sil"])
async def cikar(ctx, index: int):
    if 1 <= index <= len(music_queue):
        removed = music_queue.pop(index - 1)
        await ctx.send(embed=create_embed("Çıkarıldı", f"🗑️ **{removed['query']}** listeden silindi.", discord.Color.orange()))
    else:
        await ctx.send(embed=create_embed("Hata", "❌ Geçersiz numara.", discord.Color.red()))

@bot.command(name="temizle", aliases=["clear"])
async def temizle(ctx):
    global music_queue
    music_queue = []
    await ctx.send(embed=create_embed("Temizlendi", "🗑️ Liste boşaltıldı.", discord.Color.dark_grey()))

@bot.command(name="kapat", aliases=["stop", "bitir"])
async def kapat(ctx):
    global music_queue, current_track_info, current_file_path
    music_queue = []
    current_track_info = None
    if ctx.voice_client: ctx.voice_client.stop() 
    if current_file_path and os.path.exists(current_file_path):
        try: os.remove(current_file_path)
        except: pass
    await ctx.send(embed=create_embed("Bitti", "⏹️ Müzik kapatıldı.", discord.Color.red()))

@bot.command(name="yardim", aliases=["help"])
async def yardim(ctx):
    embed = discord.Embed(title="🎧 DJ Bot Komutları", color=discord.Color.purple())
    embed.add_field(name="▶️ !oynat <isim/link>", value="Çalar veya sıraya ekler.", inline=False)
    embed.add_field(name="📜 !sira", value="Listeyi gösterir.", inline=False)
    embed.add_field(name="⏭️ !gec <sayı>", value="Atlar.", inline=False)
    embed.add_field(name="🗑️ !cikar <sayı>", value="Listeden siler.", inline=False)
    embed.add_field(name="⏹️ !kapat", value="Kapatır.", inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)