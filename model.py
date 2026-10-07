import cv2
import numpy as np
import os

def perform_ela(image_path, quality=90):
    try:
        img_array = np.fromfile(image_path, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except:
        img = None

    if img is None:
        return None, 0.0

    temp_filename = "temp_ela.jpg"
    is_success, encoded_img = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if is_success:
        with open(temp_filename, 'wb') as f:
            encoded_img.tofile(f)
    
    try:
        compressed_array = np.fromfile(temp_filename, dtype=np.uint8)
        compressed_img = cv2.imdecode(compressed_array, cv2.IMREAD_COLOR)
    except:
        compressed_img = None
    
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
        
    diff = cv2.absdiff(img, compressed_img)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    ela_score = np.mean(gray_diff)
    
    max_diff = np.max(gray_diff)
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    ela_image = cv2.convertScaleAbs(gray_diff, alpha=scale)
    
    return ela_image, ela_score

def analyze_image(image_path):
    ela_image, ela_score = perform_ela(image_path)
    
    if ela_image is None:
        return {"error": "Görüntü okunamadı veya bulunamadı."}
    
    is_fake = False
    confidence = 0.0
    threshold = 3.0 
    
    if ela_score > threshold:
        is_fake = True
        confidence = min(99.9, 50.0 + ((ela_score - threshold) / threshold) * 50)
    else:
        is_fake = False
        confidence = max(50.0, 100.0 - ((ela_score / threshold) * 50))
        
    return {
        "status": "Sahte/Manipüle Edilmiş" if is_fake else "Gerçek/Orijinal",
        "confidence": round(confidence, 2),
        "ela_score": round(ela_score, 4),
        "ela_image": ela_image
    }
