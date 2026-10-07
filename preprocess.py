import cv2
import os
import numpy as np

def process_image(image_path):
    """
    Görüntüyü alır, gri tonlamaya çevirir ve temel ön işleme adımlarını uygular.
    """
    # Görüntünün var olup olmadığını kontrol et
    if not os.path.exists(image_path):
        print(f"Hata: {image_path} bulunamadı. Lütfen görüntüyü bu klasöre ekleyin.")
        return None

    # Görüntüyü oku (Türkçe karakterleri desteklemesi için np kullanıyoruz)
    try:
        img_array = np.fromfile(image_path, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Okuma hatası: {e}")
        return None
        
    if img is None:
         print(f"Hata: {image_path} okunamadı. Dosya formatının desteklendiğinden emin olun.")
         return None
    
    # 1. Adım: Görüntüyü gri tonlamaya çevir (İsteğiniz üzerine)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Adım: Yeniden boyutlandırma (Modeller genellikle sabit boyut bekler, örn: 224x224)
    resized_img = cv2.resize(gray_img, (224, 224))
    
    # 3. Adım: Normalizasyon (Piksel değerlerini 0-255 aralığından 0-1 aralığına çeker)
    normalized_img = resized_img / 255.0
    
    return normalized_img, gray_img

if __name__ == "__main__":
    # Test için örnek bir kullanım (görüntünüzün adını 'ornek_resim.jpg' olarak varsayıyoruz)
    test_image_path = "ornek_resim.jpg" 
    
    print("Görüntü ön işleme adımları başlatılıyor...")
    result = process_image(test_image_path)
    
    if result is not None:
        normalized, gray = result
        print("İşlem başarılı! Görüntü gri tonlamaya çevrildi ve ön işleme tamamlandı.")
        
        # Test amaçlı gri tonlamalı hali kaydedelim
        cv2.imwrite("gri_sonuc.jpg", gray)
        print("Gri tonlamalı görüntü 'gri_sonuc.jpg' olarak çalışma dizinine kaydedildi.")
