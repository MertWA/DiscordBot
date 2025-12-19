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

###💬 Komutlar

!katıl	Botu bulunduğunuz ses kanalına çağırır.
!çal <url>	Belirtilen YouTube bağlantısını indirir ve çalar.
!çal <dosya>	music/ klasöründeki yerel dosyayı çalar (örn: !çal sarki.mp3).
!kes	Çalan müziği durdurur ve indirilen geçici dosyayı siler.
!git	Bot ses kanalından ayrılır.
