# 🎵 Gelişmiş Discord Müzik Botu (Proxy & Anti-Bot Destekli)

Bu proje, Python ve `discord.py` kullanılarak geliştirilmiş; YouTube engellemelerini aşmak için **Proxy**, **Cookies** ve **User-Agent** taklidi kullanan gelişmiş bir müzik botudur.

Standart botların aksine; **Sıra (Queue) Yönetimi**, **Akıllı Link Algılama** ve **Gelişmiş Hata Yönetimi** özelliklerine sahiptir. Kullanıcıya teknik detayları yansıtmaz, şık **Embed** mesajları ile yanıt verir.

📂 **Repo:** [https://github.com/MertWA/DiscordBot](https://github.com/MertWA/DiscordBot)

## 🚀 Özellikler

* **🎧 Sıra Yönetimi:** Şarkılar bittiğinde otomatik olarak sıradakine geçer. Araya şarkı eklenebilir veya listeden silinebilir.
* **🛡️ Anti-Bot Koruması:** `yt-dlp` ile Proxy ve Cookies kullanarak "Sign in" ve "429 Too Many Requests" hatalarını minimize eder.
* **⚡ Akıllı Arama:** Sadece şarkı adı veya video ID'si girilse bile (örn: `qxHAeMDXn0Y`) otomatik bulur ve çalar.
* **🎨 Şık Arayüz:** Kullanıcı dostu, renkli ve emojili Embed mesajları.
* **📂 Yerel Çalma:** `music/` klasörüne atılan dosyaları doğrudan oynatabilir.
* **🧹 Otomatik Temizlik:** Çalan dosyalar işi bitince sunucudan otomatik silinir, disk dolmaz.

## 🛠️ Gereksinimler

Botun sorunsuz çalışması için sunucunuzda (VPS/VDS) şunlar yüklü olmalıdır:

* **Python 3.8+**
* **FFmpeg:** Ses işleme için zorunludur.
* **Node.js:** `yt-dlp`'nin karmaşık YouTube şifrelemelerini çözmesi için gereklidir.
* **Proxy (Önerilen):** YouTube engellerini aşmak için Residential (Ev Tipi) Proxy önerilir.

## 📦 Kurulum

1.  **Projeyi indirin:**
```bash
git clone https://github.com/MertWA/DiscordBot.git
cd DiscordBot
```

2.  **Sistem paketlerini yükleyin (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install -y ffmpeg nodejs npm
```

3.  **Python kütüphanelerini yükleyin:**
```bash
pip install discord.py python-dotenv
# yt-dlp'nin en güncel sürümünü yüklemek zorunludur:
pip install -U --pre "yt-dlp[default]"
```

## ⚙️ Yapılandırma (.env)

Botun çalışması için ana dizinde bir **`.env`** dosyası oluşturun ve bilgilerinizi aşağıdaki formatta girin:

```env
DISCORD_TOKEN=BURAYA_TOKEN_GELECEK
PROXY_URL=http://kullaniciadi:sifre@ip_adresi:port
```

> **Not:** `cookies.txt` dosyanız varsa, `bot.py` ile aynı dizine atmanız yeterlidir. Bot otomatik algılar.

### Değişkenler Hakkında
* **DISCORD_TOKEN:** Discord Developer Portal'dan alacağınız bot tokeni (Zorunlu).
* **PROXY_URL:** `http://kullanici:sifre@ip:port` formatında proxy adresi. (Zorunlu değil ama önerilir).
    * *Önemli:* Proxy adresinin sonundaki `:port` numarasını yazdığınızdan emin olun! (Örn: `:6641`)

## ▶️ Kullanım

Ayarlar `.env` dosyasından otomatik çekileceği için tek komutla başlatabilirsiniz:

### Linux / Mac / Windows
```bash
python bot.py
```

## 💬 Komutlar

Bot, profesyonel bir DJ gibi yönetilebilir. İşte komut listesi:

| Komut | Kısayollar | Açıklama |
| :--- | :--- | :--- |
| **`!oynat <isim/url>`** | `!çal`, `!p`, `!play` | Şarkıyı çalar veya sıraya ekler. |
| **`!durdur`** | `!pause`, `!dur` | Müziği geçici olarak duraklatır. |
| **`!devam`** | `!resume` | Duraklatılan müziği devam ettirir. |
| **`!gec`** | `!skip`, `!s` | Sıradaki şarkıya geçer. |
| **`!gec <sayı>`** | `!atla` | Belirtilen sıraya atlar (aradaki şarkıları siler). |
| **`!sira`** | `!queue`, `!q`, `!list` | Müzik listesini ve o an çalanı gösterir. |
| **`!cikar <sayı>`** | `!remove`, `!sil` | Listeden belirtilen sıradaki şarkıyı siler. |
| **`!temizle`** | `!clear` | Tüm listeyi boşaltır. |
| **`!kapat`** | `!stop`, `!bitir` | Müziği kapatır, listeyi siler ve dosyaları temizler. |
| **`!baglan`** | `!katıl`, `!join` | Botu ses kanalına çağırır. |
| **`!ayril`** | `!git`, `!leave` | Bot ses kanalından ayrılır. |

## ⚠️ Sorun Giderme

### 🔴 Connection Refused / Bağlantı Reddedildi
* **Sebep:** `.env` dosyasındaki `PROXY_URL` hatalı girilmiş.
* **Çözüm:** Proxy port numarasını (örn: `:6641`) yazdığınızdan emin olun. Varsayılan 80 portu genellikle yanlıştır.

### 🔴 Sign in to confirm / Login required
* **Sebep:** YouTube, Proxy IP'nizi veya Cookies dosyanızı güvenli bulmadı.
* **Çözüm:**
    1.  `cookies.txt` dosyanızı **Gizli Sekme** kullanarak yenileyin.
    2.  `yt-dlp` kütüphanesini güncelleyin: `pip install -U --pre "yt-dlp[default]"`

### 🔴 No supported JavaScript runtime
* **Sebep:** Sunucuda Node.js eksik.
* **Çözüm:** `sudo apt install nodejs` komutu ile yükleyin.
