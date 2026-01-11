# Pipeline Failure - Çözüm Rehberi

## 🔴 Sorun

GitHub Actions pipeline'ı başarısız oldu (kırmızı X).

## 🔍 Olası Nedenler

### 1. Model Dosyası Eksik (En Olası) ✅ DÜZELTİLDİ

**Sorun:** `.gitignore` dosyasında `*.joblib` var, bu yüzden `artifacts/model.joblib` dosyası Git'e commit edilmemiş.

**Çözüm:** 
- ✅ `.gitignore` dosyasına exception eklendi: `!artifacts/model.joblib`
- ✅ `artifacts/model.joblib` dosyası force add edildi

**Yapılacaklar:**
```bash
git add .gitignore
git commit -m "fix: add artifacts/model.joblib exception to gitignore"
git push origin main
```

### 2. Test Hatası

Eğer commit-stage'de başarısız olduysa:
- Unit testler başarısız olmuş olabilir
- Integration testler başarısız olmuş olabilir
- Linting hatası olabilir

**Kontrol:**
- GitHub Actions'da hangi stage'de durduğuna bakın
- Log'ları okuyun (stage'e tıklayın)

### 3. Docker Build Hatası

Eğer deployment-stage'de başarısız olduysa:
- Dockerfile hatası olabilir
- Model dosyası eksik (yukarıdaki çözüm)
- Bağımlılık hatası olabilir

### 4. Smoke Test Hatası

Eğer smoke test'te başarısız olduysa:
- Container başlamadı
- API endpoint'leri yanlış
- Port conflict

---

## ✅ Adım Adım Çözüm

### ADIM 1: Hangi Stage'de Başarısız Olduğunu Kontrol Et

1. GitHub Actions sayfasına gidin
2. Başarısız run'a tıklayın (kırmızı X)
3. Hangi stage'de durduğunu göreceksiniz:
   - ❌ **commit-stage** → Linting/Test hatası
   - ❌ **deployment-stage** → Docker build/Smoke test hatası

### ADIM 2: Log'ları Okuyun

1. Başarısız stage'e tıklayın
2. Log'lara bakın
3. Hata mesajını okuyun

### ADIM 3: Soruna Göre Çözüm Uygulayın

#### Model Dosyası Eksik (En Olası) ✅

**Çözüm uygulandı! Şimdi yapılacaklar:**

```bash
# 1. Değişiklikleri commit et
git add .gitignore
git commit -m "fix: add artifacts/model.joblib exception to gitignore"

# 2. Model dosyasını ekle (eğer yoksa)
git add -f artifacts/model.joblib
git commit -m "fix: add model file for Docker build"

# 3. Push et
git push origin main
```

#### Test Hatası

**Yerel olarak test et:**

```bash
# Unit testler
python -m pytest tests/test_feature_utils.py -v

# Integration testler
python -m pytest tests/test_api_integration.py -v

# Linting
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

**Sorun varsa düzelt ve tekrar push et.**

#### Docker Build Hatası

**Yerel olarak test et:**

```bash
docker build -t avazu-ctr-api:latest .
```

**Sorun varsa:**
- Dockerfile'ı kontrol et
- Model dosyasının varlığını kontrol et
- Bağımlılıkları kontrol et

---

## 📋 Kontrol Listesi

- [ ] Hangi stage'de başarısız olduğunu kontrol ettim
- [ ] Log'ları okudum
- [ ] Model dosyası exception'ı eklendi (✅)
- [ ] Model dosyası force add edildi (✅)
- [ ] Değişiklikler commit edildi
- [ ] GitHub'a push edildi
- [ ] Pipeline tekrar çalıştırıldı
- [ ] Başarılı oldu mu kontrol ettim

---

## 🆘 Hala Başarısız mı?

Eğer yukarıdaki çözümler işe yaramadıysa:

1. **GitHub Actions log'larını detaylı okuyun**
   - Hangi step'te başarısız olduğunu bulun
   - Hata mesajını okuyun
   - Stack trace varsa inceleyin

2. **Yerel olarak test edin**
   - Aynı komutları local'de çalıştırın
   - Hata tekrarlanıyor mu kontrol edin

3. **Workflow dosyasını kontrol edin**
   - `.github/workflows/ci.yml` dosyasında syntax hatası var mı?
   - YAML formatı doğru mu?

4. **Repository durumunu kontrol edin**
   - Tüm dosyalar commit edilmiş mi?
   - Branch adı doğru mu (main/master)?

---

## 📝 Notlar

- Model dosyası (`artifacts/model.joblib`) büyük olabilir, bu normaldir
- GitHub'da dosya boyutu limiti vardır (100MB), ama genellikle model dosyaları bundan küçüktür
- Eğer model dosyası çok büyükse, Git LFS kullanmayı düşünebilirsiniz (şimdilik gerekli değil)

