# DeepScan Image Forensics

DeepScan Image Forensics, dijital görüntüler üzerinde manipülasyon (photoshop, sahtecilik vb.) olup olmadığını tespit etmek için tasarlanmış web tabanlı bir analiz aracıdır. Proje, görüntülerin orijinal olup olmadığını belirlemek için **Hata Seviyesi Analizi (Error Level Analysis - ELA)** yöntemini ve matematiksel istatistikleri kullanır.

## Özellikler

- **Hata Seviyesi Analizi (ELA):** Görüntüdeki bölgesel sıkıştırma farklılıklarını tespit ederek sonradan yapılan oynamaları (montaj, photoshop vb.) ortaya çıkarır.
- **Kullanıcı Dostu Web Arayüzü:** Flask tabanlı web arayüzü sayesinde kullanıcılar kolayca resim yükleyip analiz sonuçlarını görebilir.
- **Detaylı Analiz Skorlaması:** Standart sapma, ortalama ve 99. yüzdelik (percentile) değerlerini hesaba katan gelişmiş bir algoritma ile ELA skoru üretilir.
- **Ön İşleme (Preprocessing):** Görüntüler analiz öncesinde gri tonlamaya çevrilir, yeniden boyutlandırılır ve normalize edilir.
- **Türkçe Karakter Desteği:** Dosya yollarında ve isimlerinde Türkçe karakterlerden kaynaklı oluşabilecek hatalara karşı önlemler alınmıştır.

## Teknolojiler

- **Python 3.x**
- **Flask** (Web Framework)
- **OpenCV (cv2)** (Görüntü İşleme)
- **NumPy** (Matematiksel Hesaplamalar ve Veri Analizi)
- **Werkzeug** (Güvenli dosya işlemleri)

## Kurulum

Projeyi yerel ortamınızda (lokalde) çalıştırmak için aşağıdaki adımları izleyin:

1. **Projeyi Klonlayın veya İndirin:**
   ```bash
   git clone <repo-url>
   cd "image ön işleme adımları"
   ```

2. **Gerekli Kütüphaneleri Yükleyin:**
   Python ortamınızda aşağıdaki paketlerin yüklü olduğundan emin olun (Sanal ortam - virtual environment kullanmanız önerilir):
   ```bash
   pip install Flask opencv-python numpy werkzeug
   ```

## Kullanım

Projeyi çalıştırmak için ana dizinde `server.py` dosyasını başlatmanız yeterlidir:

```bash
python server.py
```

Uygulama varsayılan olarak `http://127.0.0.1:5000/` adresinde çalışmaya başlayacaktır.

1. Tarayıcınızı açın ve `http://127.0.0.1:5000/` adresine gidin.
2. Analiz etmek istediğiniz görüntüyü seçin ve yükleyin.
3. Sistem görüntüyü işleyecek ve size bir **Analiz Sonucu (Sahte/Gerçek)**, **Güven Skoru (%)** ve manipülasyonları belirginleştiren **ELA Görüntüsünü** sunacaktır.

## Proje Yapısı

```
.
├── server.py              # Flask web sunucusu ve API rotaları
├── model.py               # ELA analiz algoritması ve skorlama
├── preprocess.py          # Görüntü ön işleme adımları (Gri tonlama, boyutlandırma vb.)
├── templates/
│   └── index.html         # Web arayüzü (Kullanıcı etkileşimi)
├── static/
│   ├── uploads/           # Kullanıcı tarafından yüklenen resimlerin kaydedildiği klasör
│   └── results/           # İşlenmiş ve analiz edilmiş (Gri & ELA) görüntü çıktılarının kaydedildiği klasör
```

## Algoritma Hakkında (ELA)

**Error Level Analysis (ELA)**, bir JPEG görüntüsünün bilerek yeniden sıkıştırılması ve orijinal görüntü ile sıkıştırılmış versiyon arasındaki farkın alınması mantığına dayanır. Orijinal bir görüntüde sıkıştırma oranı genel olarak homojendir. Ancak sonradan eklenmiş veya oynanmış bir bölge varsa, o bölge farklı bir sıkıştırma seviyesine sahip olacağından ELA görüntüsünde parlak veya belirgin olarak ortaya çıkacaktır.
Bu proje, sadece basit bir ELA almakla kalmayıp, bu fark matrisi üzerinden istatistiksel (mean, std, percentile) hesaplamalar yaparak otomatik bir "Gerçek/Sahte" sınıflandırması yapmaktadır.
