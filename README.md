# Discord Müzik Botu (Proxy & Anti-Bot Destekli)

Bu proje, Python ve `discord.py` kullanılarak geliştirilmiş; YouTube engellemelerini aşmak için **Proxy** ve **Android İstemci** modunu kullanan gelişmiş bir Discord müzik botudur. Ayrıca sunucudaki yerel dosyaları da oynatabilir.

📂 **Repo:** [https://github.com/MertWA/DiscordBot](https://github.com/MertWA/DiscordBot)

## 🚀 Özellikler

* **Gelişmiş YouTube Entegrasyonu:** `yt-dlp` ve Android istemci taklidi kullanarak bot korumalarını aşar.
* **Proxy Desteği:** IP engellemelerini (429/Sign-in hataları) aşmak için HTTP/HTTPS proxy desteği sunar.
* **Yerel Çalma:** `music/` klasörüne eklenen ses dosyalarını doğrudan oynatabilir.
* **Otomatik Temizlik:** Müzik bittiğinde veya durdurulduğunda geçici dosyalar (UUID ile isimlendirilir) otomatik silinir.
* **Cookies Gerektirmez:** Karmaşık çerez dosyalarıyla uğraşmanıza gerek kalmaz.

## 🛠️ Gereksinimler

Botun sorunsuz çalışması için sunucunuzda şunlar yüklü olmalıdır:

* **Python 3.8+**
* **FFmpeg:** Ses işleme için gereklidir (Sistem PATH'ine eklenmiş olmalıdır).
* **yt-dlp (Nightly):** YouTube'un son güncellemelerine karşı `yt-dlp`'nin en güncel geliştirici sürümü gereklidir.
* **Proxy (Önerilen):** VPS/Datacenter IP'leri YouTube tarafından engellendiği için çalışan bir Residential (Ev Tipi) Proxy önerilir.

## 📦 Kurulum

1.  Projeyi indirin:
    ```bash
    git clone [https://github.com/MertWA/DiscordBot.git](https://github.com/MertWA/DiscordBot.git)
    cd DiscordBot
    ```

2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install discord.py
    # yt-dlp'nin en güncel sürümünü yüklemek zorunludur:
    pip install -U --pre "yt-dlp[default]"
    ```

## ⚙️ Yapılandırma

Botu çalıştırmadan önce ortam değişkenlerini (Environment Variables) ayarlamalısınız.

### 1. Discord Token
Botun çalışabilmesi için `DISCORD_TOKEN` gereklidir.

### 2. Proxy Ayarı (Önemli)
Sunucu IP'niz YouTube tarafından engelliyse (Sign in / 429 hatası), `PROXY_URL` tanımlamalısınız.
**Format:** `http://kullaniciadi:sifre@ip_adresi:port`

### 3. yt-dlp Yolu
Kod varsayılan olarak `/usr/local/bin/yt-dlp` yolunu kullanır. Farklıysa `bot.py` içindeki `YTDLP` değişkenini güncelleyin.

## ▶️ Kullanım

Botu başlatmak için terminalde aşağıdaki komutları kullanın:

### Linux / Mac

```
export DISCORD_TOKEN="DISCORD_TOKENINIZ_BURAYA"
export PROXY_URL="http://kullanici:sifre@ip:port"  # Proxy yoksa bu satırı atlayın

python bot.py
```
### Windows 

```
$env:DISCORD_TOKEN="DISCORD_TOKENINIZ_BURAYA"
$env:PROXY_URL="http://kullanici:sifre@ip:port"

python bot.py
```

## 💬 Komutlar

Botun desteklediği komutlar ve açıklamaları aşağıdadır:

| Komut | Kullanım Şekli | Açıklama |
| :--- | :--- | :--- |
| **Katıl** | `!katıl` | Botu bulunduğunuz ses kanalına çağırır. |
| **Çal (URL)** | `!çal <youtube_linki>` | Belirtilen YouTube bağlantısını Proxy üzerinden indirir ve çalar. |
| **Çal (Yerel)**| `!çal <dosya_adi.mp3>` | `music/` klasörüne attığınız yerel dosyayı çalar. |
| **Kes** | `!kes` | Çalan müziği anında durdurur ve geçici dosyayı siler. |
| **Git** | `!git` | Bot ses kanalından ayrılarak çıkış yapar. |

## ⚠️ Sorun Giderme

Botu kullanırken karşılaşabileceğiniz yaygın hatalar ve çözümleri:

### 🔴 429 Too Many Requests / HTTP Error 429
* **Sebep:** Kullandığınız Proxy IP adresi YouTube tarafından çok fazla istek gönderdiği için geçici olarak engellenmiştir.
* **Çözüm:** Webshare panelinizden farklı bir Proxy IP adresi seçerek `PROXY_URL` değişkenini güncelleyin.

### 🔴 Sign in to confirm / Login required
* **Sebep:** YouTube, trafiğin bir sunucudan veya bottan geldiğini algılamıştır.
* **Çözüm:** "Datacenter Proxy" yerine "Residential (Ev Tipi) Proxy" kullanmayı deneyin. Kodun **Android Modu** çalıştığından emin olun.

### 🔴 Dosya İndirilemedi / Format Hataları
* **Sebep:** `yt-dlp` kütüphanesi güncelliğini yitirmiş olabilir.
* **Çözüm:** Sunucuda şu komutu çalıştırarak güncelleyin:
    ```bash
    pip install -U --pre "yt-dlp[default]"
    ```
