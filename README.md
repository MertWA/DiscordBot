# Discord Müzik Botu

Bu proje, Python ve `discord.py` kullanılarak geliştirilmiş; YouTube bağlantılarını indirip çalabilen veya sunucudaki yerel dosyaları oynatabilen bir Discord müzik botudur.

📂 **Repo:** [https://github.com/MertWA/DiscordBot](https://github.com/MertWA/DiscordBot)

## 🚀 Özellikler

* **YouTube Entegrasyonu:** `yt-dlp` kullanarak YouTube bağlantılarındaki sesi indirir ve çalar.
* **Yerel Çalma:** `music/` klasörüne eklenen ses dosyalarını doğrudan oynatabilir.
* **Çerez (Cookies) Desteği:** YouTube yaş kısıtlaması veya bot korumalarını aşmak için `cookies.txt` kullanır.
* **Otomatik Temizlik:** Yeni bir şarkıya geçildiğinde veya müzik durdurulduğunda geçici indirilen dosyalar silinir.

## 🛠️ Gereksinimler

Botun sorunsuz çalışması için sunucunuzda aşağıdaki araçların yüklü olması gerekir:

* **Python 3.8+**
* **FFmpeg:** Ses işleme ve dönüştürme için gereklidir (Sistem PATH'ine eklenmiş olmalıdır).
* **yt-dlp:** YouTube videolarını indirmek için gereklidir.
* **Node.js:** `yt-dlp`'nin JavaScript çalışma zamanı (js-runtimes) argümanı için gereklidir.

## 📦 Kurulum

1.  Projeyi bilgisayarınıza indirin:
    ```bash
    git clone [https://github.com/MertWA/DiscordBot.git](https://github.com/MertWA/DiscordBot.git)
    cd DiscordBot
    ```

2.  Gerekli Python kütüphanesini yükleyin:
    ```bash
    pip install discord.py
    ```

## ⚙️ Yapılandırma

Botu çalıştırmadan önce aşağıdaki adımları tamamlamanız gerekir:

### 1. Discord Token
Botun çalışabilmesi için `DISCORD_TOKEN` ortam değişkeni (environment variable) tanımlanmalıdır.

### 2. Cookies Dosyası
Bot, YouTube indirmeleri için proje ana dizininde **`cookies.txt`** dosyasına ihtiyaç duyar.
* Tarayıcınızdan YouTube çerezlerini "Netscape formatında" dışa aktarın.
* Dosyayı `cookies.txt` adıyla `bot.py` ile aynı dizine kaydedin.

### 3. yt-dlp Yolu
Eğer `yt-dlp` sisteminizde farklı bir konumdaysa, kod içerisindeki `YTDLP` değişkenini kendi yolunuza göre güncelleyin. Varsayılan: `/usr/local/bin/yt-dlp`

## ▶️ Kullanım

Botu başlatmak için terminalde şu komutu kullanın:

**Linux/Mac:**
```bash
export DISCORD_TOKEN="TOKEN_BURAYA"
python bot.py
```

**Windows (Powershell):**
```powershell
$env:DISCORD_TOKEN="TOKEN_BURAYA"
python bot.py
```

### 💬 Komutlar

| Komut | Açıklama |
| :--- | :--- |
| `!katıl` | Botu bulunduğunuz ses kanalına çağırır. |
| `!çal <url>` | Belirtilen YouTube bağlantısını indirir ve çalar. |
| `!çal <dosya>` | `music/` klasöründeki belirtilen dosyayı çalar (örn: `!çal sarki.mp3`). |
| `!kes` | Çalan müziği durdurur ve indirilen geçici dosyayı siler. |
| `!git` | Bot ses kanalından ayrılır. |

## ⚠️ Notlar
* Bot, indirilen YouTube dosyalarını MP3 formatına çevirerek `music/` klasörüne geçici bir isimle (UUID) kaydeder.
* `!kes` komutu kullanıldığında veya yeni bir şarkı açıldığında eski dosya otomatik olarak silinir.
