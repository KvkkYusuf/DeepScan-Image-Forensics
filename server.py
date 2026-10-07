import os
import sys
import cv2
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# Klasör adındaki Türkçe karakterlerden dolayı oluşan import hatasını engellemek için:
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocess import process_image
from model import analyze_image

app = Flask(__name__)

# Gerekli klasörleri oluştur
os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)
os.makedirs(os.path.join('static', 'results'), exist_ok=True)

@app.route('/')
def index():
    # templates/index.html dosyasını render eder
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'Lütfen bir resim yükleyin.'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Resim seçilmedi.'}), 400
        
    import uuid
    # Güvenli dosya adı oluştur
    filename = secure_filename(file.filename)
    # Eğer dosya adında sadece Türkçe karakter varsa filename boş kalabilir, bu durumu önleyelim:
    if not filename or filename.startswith('.'):
        filename = str(uuid.uuid4()) + ".jpg"
        
    filepath = os.path.join('static', 'uploads', filename)
    file.save(filepath)
    
    # 1. Ön İşleme Adımı (preprocess.py)
    preprocess_result = process_image(filepath)
    if not preprocess_result:
        return jsonify({'error': 'Ön işleme başarısız. Görüntü okunamadı (Dosya yolu hatası olabilir).'}), 500
    
    _, gray_img = preprocess_result
    gray_filename = f'gray_{filename}'
    gray_path = os.path.join('static', 'results', gray_filename)
    
    # cv2.imwrite yerine Türkçe karakter destekli kaydetme:
    is_success, encoded_gray = cv2.imencode(".jpg", gray_img)
    if is_success:
        with open(gray_path, "wb") as f:
            encoded_gray.tofile(f)
    
    # 2. Analiz Adımı (model.py)
    analysis_result = analyze_image(filepath)
    if "error" in analysis_result:
         return jsonify({'error': analysis_result['error']}), 500
         
    ela_filename = f'ela_{filename}'
    ela_path = os.path.join('static', 'results', ela_filename)
    
    is_success, encoded_ela = cv2.imencode(".jpg", analysis_result['ela_image'])
    if is_success:
        with open(ela_path, "wb") as f:
            encoded_ela.tofile(f)
    
    # Sonuçları JSON olarak HTML arayüzüne gönder
    return jsonify({
        'status': analysis_result['status'],
        'confidence': analysis_result['confidence'],
        'ela_score': analysis_result['ela_score'],
        'original_url': f'/static/uploads/{filename}',
        'gray_url': f'/static/results/{gray_filename}',
        'ela_url': f'/static/results/{ela_filename}'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
