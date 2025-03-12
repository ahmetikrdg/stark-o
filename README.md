# Stark-O Duygu Analizi Modeli 🚀

## **Stark-O ile Müşteri Geri Bildirimlerini Anlamlandırın!** 📊🤖

**Stark-O, müşteri yorumlarını analiz eden ve online öğrenme desteğiyle sürekli güncellenebilen bir Türkçe duygu analizi modelidir.** API üzerinden kullanılabilir veya yerel olarak çalıştırılabilir. 300K+ e-ticaret yorumu ile eğitilmiş olan bu model, metinleri **olumlu, olumsuz veya tarafsız** olarak değerlendirebilir.

🔗 **Modeli Hugging Face UI üzerinden deneyin:**  
[Hugging Face Stark-O UI](https://huggingface.co/spaces/ahmetikrdg/stark-o)

---

## 💡 **Nasıl Çalışır?**

1. Kullanıcı tarafından girilen metin temizlenir ve işlenir.
2. Model, 300K+ e-ticaret yorumu ile eğitilmiştir.
3. Sonuçlar **olumlu, olumsuz veya tarafsız** olarak değerlendirilir ve olasılık yüzdeleriyle sunulur.

### **Örnek Çıktı:**
```json
{
  "sentiment": "OLUMLU",
  "probabilities": {
    "OLUMLU": 0.85,
    "OLUMSUZ": 0.10,
    "TARAFSIZ": 0.05
  }
}
```

---

## 🎯 **Kullanım Alanları**

✅ **E-Ticaret:** Müşteri yorumlarını analiz ederek trendleri belirleme.  
✅ **Şirketler:** Ürün ve hizmet geri bildirimlerini otomatik değerlendirme.  
✅ **Sosyal Medya Analizi:** Kullanıcı duyarlılığı üzerine raporlama ve analiz.  

---

## 1️⃣ **API Üzerinden Kullanım**

Modeli doğrudan aşağıdaki API endpoint'i aracılığıyla kullanabilirsiniz:

### 🔗 **Endpoint:**
```
https://ahmetikrdg-stark-o-api.hf.space/predict
```

### 📌 **Örnek Kullanım:**
```python
import requests

url = "https://ahmetikrdg-stark-o-api.hf.space/predict"  
data = {"comment": "Bu ürün harika, çok beğendim!"}

response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
try:
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Error: API returned an empty response")
```

Bu endpoint'e bir yorum göndererek modelin tahminini alabilirsiniz.

---

## 2️⃣ **Model Dosyalarını İndirerek Kullanım**

Modeli kendi projenizde kullanmak için **sgd_model.pkl** ve **tfidf_vectorizer.pkl** dosyalarını indirerek lokal olarak çalıştırabilirsiniz.

### 📌 **Örnek Python Kullanımı:**
```python
import joblib
import re

vectorizer = joblib.load("tfidf_vectorizer.pkl")
model = joblib.load("sgd_model.pkl")

label_mapping = {0: "OLUMLU", 1: "OLUMSUZ", 2: "TARAFSIZ"}

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def predict_sentiment(comment):
    cleaned_comment = clean_text(comment)
    comment_vector = vectorizer.transform([cleaned_comment])
    prediction = model.predict(comment_vector)[0]
    proba = model.predict_proba(comment_vector)[0]
    return label_mapping[int(prediction)], {label_mapping[i]: float(proba[i]) for i in range(len(proba))}
```

Bu yöntemle modelinizi Python projelerinize entegre edebilirsiniz.

---

## 3️⃣ **Online Learning ile Modeli Özelleştirme**

### 1️⃣ **Model Dosyalarını İndirin**
Öncelikle aşağıdaki bağlantıdan **sgd_model.pkl** ve **tfidf_vectorizer.pkl** dosyalarını indirerek projenize ekleyin:

🔗 **[Model Dosyaları](https://huggingface.co/spaces/ahmetikrdg/stark-o-api/tree/main)**

### 2️⃣ **Kaynak Kodları İndirin ve Kurun**
Modeli kendi sisteminizde çalıştırmak için öncelikle Github reposunu indirmeniz gerekmektedir.

🔗 **[Stark-O Github](https://github.com/ahmetikrdg/stark-o)**

### 3️⃣ **Kendi Verilerinizle Eğitin**
Projeyi indirdikten sonra **data.xlsx** dosyasına kendi etiketli yorumlarınızı ekleyebilirsiniz. Model, bu verilerle **online learning** yöntemiyle güncellenir.

Alternatif olarak **/excel-upload** endpoint'ini kullanarak verilerinizi API üzerinden yükleyebilirsiniz:
```json
{
    "comments": ["Bu bir test yorumudur.", "İkinci bir test yorumu."],
    "labels": ["OLUMLU", "OLUMSUZ"]
}
```

Bu veriler **data.xlsx** dosyasına kaydedilecek ve model güncellenecektir.

---

## 3️⃣.1️⃣ **Yeni Yorumları Online Learning ile Analiz Etme**

🔗 **Endpoint:**
```
POST /analyze-comment
```

📌 **Örnek Request:**
```json
{
    "comment": "Selam, kullandığım filtre başka sonuç veriyor. Yeni yapıyı hiç beğenmedik.",
    "learning": false
}
```

Eğer `learning: true` gönderirseniz, model bu yorumdan öğrenerek gelecekteki tahminlerini güncelleyebilir.

---

## 3️⃣.2️⃣ **Modelin Güncel Raporunu Alma**

Modelin performans raporunu almak için aşağıdaki endpoint’i kullanabilirsiniz:

🔗 **GET /generate-report**

Bu işlem sonucunda modelin performansına dair bir PDF raporu alabilirsiniz.

---

## 3️⃣.3️⃣ **Modelin Başlangıç Modunu Seçme**

📌 **Endpoint:**
```
POST /set-start-model
```

📌 **Örnek Request:**
```json
{
    "startModel": false
}
```

Eğer `startModel: false` olarak gönderirseniz, model mevcut pkl dosyaları ile başlar. `true` gönderirseniz, model sıfırdan eğitilir.

---

## 🚀 **Modeli Prod Ortamına Deploy Etme**

1. Modelinizi bir API olarak çalıştırmak için FastAPI veya Flask gibi framework'leri kullanabilirsiniz.
2. Modelinizi bir sunucuya (AWS, Google Cloud, Hugging Face Spaces, vb.) deploy edebilirsiniz.
3. Modeli bir Docker container içinde çalıştırarak ölçeklenebilir hale getirebilirsiniz.
4. CI/CD süreçleri ile model güncellemelerini otomatikleştirebilirsiniz.

---

## 🚀 **Sonuç**

Stark-O, hem API hem de yerel kullanım seçenekleriyle **esnek ve güçlü bir duygu analizi modelidir**. Online learning desteği sayesinde zamanla daha da iyileştirilebilir. Kendi verilerinizle eğitebilir, mevcut modeli API üzerinden kullanabilir veya projelerinize entegre edebilirsiniz! 🚀🔥

