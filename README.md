# Discord Müzik Botu (Proxy & Anti-Bot Destekli)

Bu proje, Python ve `discord.py` kullanılarak geliştirilmiş; YouTube engellemelerini aşmak için **Proxy** ve **Android İstemci** modunu kullanan gelişmiş bir Discord müzik botudur. Hem tam bağlantıları hem de video ID'lerini destekler.

📂 **Repo:** [https://github.com/MertWA/DiscordBot](https://github.com/MertWA/DiscordBot)

## 🚀 Özellikler

* **Akıllı Link Algılama:** Sadece video ID'si girilse bile (örn: `qxHAeMDXn0Y`) otomatik olarak algılar ve çalar.
* **Gelişmiş YouTube Entegrasyonu:** `yt-dlp` ve Android istemci taklidi kullanarak bot korumalarını aşar.
* **Proxy Desteği:** IP engellemelerini (429/Sign-in hataları) aşmak için HTTP/HTTPS proxy desteği sunar.
* **Yerel Çalma:** `music/` klasörüne eklenen ses dosyalarını doğrudan oynatabilir.
* **Otomatik Temizlik:** Müzik bittiğinde veya durdurulduğunda geçici dosyalar otomatik silinir.
* **Gizlilik:** Kullanıcıya teknik detayları yansıtmaz, sadece "Müzik hazırlanıyor" bilgisini verir.

## 🛠️ Gereksinimler

Botun sorunsuz çalışması için sunucunuzda şunlar yüklü olmalıdır:

* **Python 3.8+**
* **FFmpeg:** Ses işleme için gereklidir (Sistem PATH'ine eklenmiş olmalıdır).
* **yt-dlp (Nightly):** YouTube'un son güncellemelerine karşı en güncel sürüm şarttır.
* **Proxy (Önerilen):** YouTube engellerini aşmak için Residential (Ev Tipi) Proxy önerilir.

## 📦 Kurulum

1.  Projeyi indirin:
    ```bash
    git clone [https://github.com/MertWA/DiscordBot.git](https://github.com/MertWA/DiscordBot.git)
    cd DiscordBot
    ```

2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install discord.py python-dotenv
    # yt-dlp'nin en güncel sürümünü yüklemek zorunludur:
    pip install -U --pre "yt-dlp[default]"
    ```

## ⚙️ Yapılandırma

Botun çalışması için ana dizinde bir **`.env`** dosyası oluşturun ve aşağıdaki bilgileri doldurun:

**`.env` Dosyası Örneği:**
```env
DISCORD_TOKEN=BURAYA_TOKEN_GELECEK
PROXY_URL=http://kullaniciadi:sifre@ip_adresi:port
```

### Değişkenler Hakkında
* **DISCORD_TOKEN:** Discord Developer Portal'dan alacağınız bot tokeni (Zorunlu).
* **PROXY_URL:** `http://kullanici:sifre@ip:port` formatında proxy adresi. (Opsiyonel ama VPS için önerilir).
* **YTDLP (Opsiyonel):** Varsayılan yol: `/usr/local/bin/yt-dlp`. Farklıysa `bot.py` içinden güncellenebilir.

## ▶️ Kullanım

Ayarlar `.env` dosyasından otomatik çekileceği için tek bir komutla başlatabilirsiniz:

### Linux / Mac
```bash
python bot.py
```

### Windows

```python bot.py```

### 💬 Komutlar
Botun desteklediği komutlar:

Katıl	!katıl	Botu bulunduğunuz ses kanalına çağırır.
Çal (URL)	!çal https://youtu.be/...	YouTube linkini indirir ve çalar.
Çal (ID)	!çal qxHAeMDXn0Y	Sadece YouTube video ID'si ile çalar.
Çal (Yerel)	!çal sarki.mp3	music/ klasöründeki dosyayı çalar.
Kes	!kes	Müziği durdurur ve geçici dosyayı siler.
Git	!git	Bot ses kanalından ayrılarak çıkış yapar.

### ⚠️ Sorun Giderme
Botu kullanırken karşılaşabileceğiniz yaygın hatalar ve çözümleri:

🔴 429 Too Many Requests / HTTP Error 429
Sebep: Kullandığınız Proxy IP adresi YouTube tarafından çok fazla istek gönderdiği için geçici olarak engellenmiştir.

Çözüm: Proxy sağlayıcınızdan farklı bir IP adresi seçerek .env dosyasındaki PROXY_URL değişkenini güncelleyin.

🔴 Müzik Açılamadı / Sign in required
Sebep: YouTube, trafiğin bir sunucudan (Datacenter) geldiğini algılamıştır veya yt-dlp sürümü eskidir.

Çözüm: 1. yt-dlp kütüphanesini güncelleyin: pip install -U --pre "yt-dlp[default]" 2. .env dosyasındaki Proxy adresini Residential (Ev tipi) bir proxy ile değiştirin.
