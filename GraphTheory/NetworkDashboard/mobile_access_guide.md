# Telefon veya Tabletten Nasıl Erişilir?

Kız arkadaşınızın telefonundan uygulamayı açması için iki yolunuz var. 

Bilinmesi gereken önemli nokta: **Telefon bu kodu (Python) çalıştıramaz.** Kodu sizin bilgisayarınız (veya bir sunucu) çalıştırır, telefon sadece *ekran* olarak bağlanır.

## Yöntem 1: Aynı Evdeyseniz (Wi-Fi)
Eğer ikiniz de aynı modeme bağlıysanız en kolayı budur.

1.  Bilgisayarınızda uygulamayı çalıştırın (`run_dashboard.bat` ile).
2.  Siyah terminal penceresinde **Network URL** diye bir adres göreceksiniz.
    *   Örnek: `http://192.168.1.105:8501` (Sizinki farklı olabilir).
3.  Kız arkadaşınızın telefonundaki tarayıcıyı (Chrome/Safari) açın.
4.  Adres çubuğuna bu numarayı aynen yazın.
5.  Eğer açılmazsa, bilgisayarınızın **Güvenlik Duvarını (Firewall)** geçici olarak kapatıp tekrar deneyin.

## Yöntem 2: Farklı Yerlerdeyseniz (İnternet Üzerinden)
Eğer o başka bir evdeyse veya şehirdeyse, uygulamanızı **internete yüklemeniz** gerekir. Bu işlem tamamen ücretsizdir ve profesyonel görünür.

### Adım Adım Streamlit Cloud Yüklemesi

1.  **GitHub Hesabı Açın:** Eğer yoksa [github.com](https://github.com) adresinden ücretsiz bir hesap açın.
2.  **Repository Oluşturun:** GitHub'da "New Repository" diyip bir isim verin (örn: `graph-dashboard`).
3.  **Dosyaları Yükleyin:**
    *   Bu klasördeki tüm dosyaları (`app.py`, `requirements.txt`, `data` klasörü vb.) oraya sürükleyip bırakın (veya Git kullanarak yükleyin).
4.  **Streamlit Cloud'a Bağlanın:**
    *   [streamlit.io/cloud](https://streamlit.io/cloud) adresine gidin.
    *   GitHub ile giriş yapın.
    *   "New App" butonuna basın.
    *   Listeden az önce oluşturduğunuz Repository'yi (`graph-dashboard`) seçin.
    *   "Deploy!" butonuna basın.
5.  **Sonuç:** Size `https://graph-dashboard.streamlit.app` gibi şık bir link verecek. Bu linki WhatsApp’tan atın, dünyanın her yerinden girebilir!

> **Öneri:** Eğer bu proje ciddi bir hal alırsa, Yöntem 2'yi (Streamlit Cloud) kesinlikle tavsiye ederim. Hem telefon hem bilgisayardan sorunsuz açılır ve bilgisayarınızın açık kalmasına gerek olmaz.
