# GitHub Actions Pipeline - Adım Adım Rehber

Bu rehber, GitHub Actions pipeline'ını çalıştırıp screenshot almak için gerekli tüm adımları içerir.

## 📋 Ön Hazırlık

### 1. Git Repository Kontrolü

Önce repository'nin GitHub'da olduğundan emin olun:

```bash
# Git remote'u kontrol et
git remote -v

# Eğer remote yoksa veya yanlışsa:
# git remote add origin https://github.com/KULLANICI_ADINIZ/REPO_ADI.git
```

### 2. Dosyaları Commit ve Push Et

```bash
# Tüm değişiklikleri stage'e al
git add .

# Commit et
git commit -m "feat: implement CI/CD pipeline for Homework 2"

# GitHub'a push et
git push origin main
# veya
git push origin master
```

---

## 🚀 Adım Adım: Pipeline'ı Çalıştırma ve Screenshot Alma

### ADIM 1: GitHub Repository'yi Aç

1. Web tarayıcınızda GitHub'a gidin: https://github.com
2. Repository'nize gidin (örn: `https://github.com/KULLANICI_ADINIZ/REPO_ADI`)

### ADIM 2: Actions Sekmesine Git

1. Repository sayfasında üst menüden **"Actions"** sekmesine tıklayın
   - Yer: Repository ana sayfasında, "Code", "Issues", "Pull requests" yanında

2. İlk kez Actions kullanıyorsanız:
   - GitHub Actions'ı etkinleştirmek isteyip istemediğiniz sorulabilir
   - "I understand my workflows, go ahead and enable them" butonuna tıklayın

### ADIM 3: Workflow'u İncele

1. Actions sayfasında solda workflow listesini göreceksiniz
2. **"MLOps CI/CD Pipeline"** workflow'unu bulun
3. Workflow'a tıklayın

### ADIM 4: Pipeline'ın Otomatik Çalışmasını Bekle

**Not:** Pipeline otomatik olarak çalışır çünkü:
- `push` event'i tetiklenir (main/master branch'e push ettiğinizde)
- `pull_request` event'i tetiklenir (PR oluşturduğunuzda)

Pipeline şu adımları çalıştıracak:

1. **Commit Stage (CI)**
   - Checkout code
   - Setup Python
   - Install dependencies
   - Lint with flake8
   - Run unit tests
   - Run component/integration tests

2. **Deployment Stage (CD)**
   - Build Docker image
   - Run smoke test

### ADIM 5: Pipeline'ı İzle (İsteğe Bağlı)

1. Workflow run'ına tıklayın (en üstteki run, yeşil veya sarı/turuncu olabilir)
2. Her stage'in çalışmasını izleyebilirsiniz
3. Log'ları görmek için stage'lere tıklayabilirsiniz

---

## 📸 Screenshot Alma Rehberi

### SCREENSHOT 1: Pipeline Configuration (Workflow Dosyası)

**Ne zaman:** Repository'de, kod dosyası olarak

**Nasıl:**

1. GitHub repository sayfasında `.github/workflows/ci.yml` dosyasına gidin
2. Dosyaya tıklayın
3. Ekran görüntüsü alın (Windows: `Win + Shift + S`, Mac: `Cmd + Shift + 4`)
4. **Önemli:** Dosyanın tamamını gösteren bir screenshot alın
   - İdeal: İlk 50-70 satır (name, on, jobs kısmı)
   - Veya tüm dosyayı scroll ederek birkaç screenshot

**Ne Göstermeli:**
- ✅ `name: MLOps CI/CD Pipeline`
- ✅ `on:` (push, pull_request)
- ✅ `jobs:` (commit-stage, deployment-stage)
- ✅ Stage'ler: lint, unit tests, integration tests, build, smoke test

### SCREENSHOT 2: Pipeline Overview (Workflow Run Listesi)

**Ne zaman:** Actions sayfasında, workflow run'ları listelenirken

**Nasıl:**

1. GitHub repository'de **"Actions"** sekmesine gidin
2. **"MLOps CI/CD Pipeline"** workflow'una tıklayın
3. Workflow run listesini göreceksiniz
4. En üstteki (en yeni) run'ı bulun
5. Ekran görüntüsü alın

**Ne Göstermeli:**
- ✅ Workflow ismi: "MLOps CI/CD Pipeline"
- ✅ Run durumu: ✅ (yeşil checkmark) veya ❌ (kırmızı X)
- ✅ Commit mesajı
- ✅ Branch adı (main/master)
- ✅ Zaman damgası

### SCREENSHOT 3: Success Evidence - Green Build (Evidence A)

**Ne zaman:** Pipeline başarıyla tamamlandıktan sonra

**Nasıl:**

1. Actions sayfasında **"MLOps CI/CD Pipeline"** workflow'una gidin
2. En üstteki (başarılı) run'a tıklayın
3. Run detay sayfasında:
   - **Sol tarafta:** Stage listesi (commit-stage, deployment-stage)
   - **Sağ tarafta:** Her stage'in durumu
4. Ekran görüntüsü alın

**Ne Göstermeli:**
- ✅ **commit-stage** - ✅ (yeşil checkmark)
  - ✅ Lint with flake8 - ✅
  - ✅ Run unit tests - ✅
  - ✅ Run component/integration tests - ✅
- ✅ **deployment-stage** - ✅ (yeşil checkmark)
  - ✅ Build Docker image - ✅
  - ✅ Run smoke test - ✅

**İpucu:** Her stage'i genişletip (tıklayarak) detayları da görebilirsiniz

### SCREENSHOT 4: Stage Detayları (İsteğe Bağlı - Daha Detaylı)

**Ne zaman:** Her stage'in detaylarını göstermek istediğinizde

**Nasıl:**

1. Başarılı workflow run'ında bir stage'e tıklayın (örn: "Run unit tests")
2. Log'ları göreceksiniz
3. Test sonuçlarını gösteren kısmı screenshot alın

**Örnek:**
- Unit tests: "12 passed"
- Integration tests: "9 passed"
- Linting: "0 errors"

### SCREENSHOT 5: Failure Evidence - Stop the Line (Evidence B)

**Ne zaman:** Sabotage test yaptıktan sonra (kasıtlı bug ekleyip push ettikten sonra)

**Nasıl:**

1. **Önce kasıtlı bug ekleyin:**
   ```bash
   # src/feature_utils.py dosyasını açın
   # Satır 56'yı bulun:
   # for row in df[feature_cols].itertuples(index=False, name=None):
   
   # Syntax error ekleyin (':' kaldırın):
   # for row in df[feature_cols].itertuples(index=False, name=None)  # Eksik ':'
   ```

2. **Commit ve push edin:**
   ```bash
   git add src/feature_utils.py
   git commit -m "test: sabotage test - intentional syntax error"
   git push origin main
   ```

3. **Actions sayfasına gidin:**
   - **"MLOps CI/CD Pipeline"** workflow'una tıklayın
   - En üstteki (başarısız) run'a tıklayın

4. **Screenshot alın:**
   - ❌ **commit-stage** - ❌ (kırmızı X) veya ⚠️ (sarı warning)
   - ❌ **deployment-stage** - ⏭️ Skipped (atlandı çünkü commit-stage başarısız oldu)

**Ne Göstermeli:**
- ❌ Hangi stage'de durduğu (genellikle "Lint with flake8" veya "Run unit tests")
- ❌ Error mesajı (tıklayarak log'ları görebilirsiniz)
- ⏭️ deployment-stage'in skipped olduğu (kırmızı çizgi ile)

**İpucu:** Hata mesajını görmek için başarısız stage'e tıklayın ve log'larda hata mesajını screenshot alın

---

## 🖼️ Screenshot Alma İpuçları

### Windows:
- **Windows + Shift + S**: Ekran kesme aracı
- **PrtScn**: Tüm ekran
- **Alt + PrtScn**: Aktif pencere

### Mac:
- **Cmd + Shift + 4**: Seçilen alan
- **Cmd + Shift + 3**: Tüm ekran
- **Cmd + Shift + 4 + Space**: Pencere

### Chrome/Edge Eklentisi:
- **Awesome Screenshot**: Uzun sayfalar için
- **Full Page Screen Capture**: Scroll ederek tüm sayfayı alır

---

## 📝 PDF Raporu İçin Screenshot Düzeni

### 1. Pipeline Configuration Screenshot
- `.github/workflows/ci.yml` dosyasının görüntüsü
- İlk 50-70 satır yeterli
- Veya dosyanın tamamı (birkaç screenshot)

### 2. Evidence A (Success) - Green Build
- Actions sayfasında workflow run detayları
- Tüm stage'lerin ✅ (yeşil) olduğunu gösteren görsel
- İdeal: Sol tarafta stage listesi, sağ tarafta detaylar

### 3. Evidence B (Failure) - Stop the Line
- Actions sayfasında başarısız workflow run
- ❌ (kırmızı X) işaretini gösteren görsel
- Hangi stage'de durduğu
- deployment-stage'in skipped olduğu
- Error log'u (isteğe bağlı ama önerilir)

---

## ✅ Kontrol Listesi

- [ ] GitHub repository hazır
- [ ] Dosyalar commit ve push edildi
- [ ] Actions sayfasına erişim var
- [ ] Workflow çalıştı (otomatik veya manuel)
- [ ] Success screenshot alındı (Evidence A)
- [ ] Sabotage test yapıldı
- [ ] Failure screenshot alındı (Evidence B)
- [ ] Pipeline configuration screenshot alındı
- [ ] Tüm screenshot'lar PDF'e eklendi

---

## 🆘 Sorun Giderme

### Problem: Actions sekmesi görünmüyor
**Çözüm:** 
- Repository'nin public olması veya GitHub Pro/Team hesabına sahip olmanız gerekebilir
- Repository settings'den Actions'ı kontrol edin

### Problem: Pipeline çalışmıyor
**Çözüm:**
- `.github/workflows/ci.yml` dosyasının doğru yerde olduğundan emin olun
- YAML syntax hatası olabilir, kontrol edin
- Branch adının `main` veya `master` olduğundan emin olun

### Problem: Docker build başarısız
**Çözüm:**
- `Dockerfile` dosyasının doğru olduğundan emin olun
- GitHub Actions'da Docker support aktif olmalı
- Model dosyası (`artifacts/model.joblib`) repository'de olmalı

### Problem: Smoke test başarısız
**Çözüm:**
- Container'ın başlaması için yeterli zaman verin
- Port conflict olabilir (workflow'da 8000 portu kullanılıyor)
- API endpoint'lerinin doğru olduğundan emin olun

---

## 📚 Ek Kaynaklar

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Docker Actions](https://docs.github.com/en/actions/using-containerized-services/about-service-containers)

---

**Not:** Bu rehberi adım adım takip ederek tüm gerekli screenshot'ları alabilirsiniz. Herhangi bir sorunla karşılaşırsanız yukarıdaki sorun giderme bölümüne bakabilirsiniz.

