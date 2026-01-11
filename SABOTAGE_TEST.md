# Sabotage Test Senaryosu - "Stop the Line" Simulation

Bu döküman, CI/CD pipeline'ının kasıtlı olarak eklenen bug'ları yakalayıp deployment'ı durdurduğunu göstermek için hazırlanmıştır.

## Senaryo: Feature Engineering Bug'ı

### Adım 1: Kasıtlı Bug Ekleme

Aşağıdaki değişiklik `src/feature_utils.py` dosyasında yapılacaktır:

**Bug Tipi:** Syntax Error - Eksik döngü tanımlaması

`src/feature_utils.py` dosyasının 56. satırında:
```python
# Orijinal (doğru):
for row in df[feature_cols].itertuples(index=False, name=None):

# Sabotage (yanlış):
for row in df[feature_cols].itertuples(index=False, name=None)  # Eksik ':'
```

### Adım 2: Commit ve Push

Bu değişiklik commit edilip push edildiğinde:
1. **Linting Stage** - Flake8 syntax error'ı yakalayacak
2. **Pipeline FAILED** - Deployment durdurulacak
3. **Bad code production'a giremeyecek**

### Adım 3: Düzeltme

Bug düzeltilip tekrar commit edildiğinde pipeline başarıyla tamamlanacak.

## Test Senaryoları

### Senaryo A: Syntax Error
- **Dosya:** `src/feature_utils.py`
- **Bug:** Eksik ':' operatörü
- **Beklenen:** Linting stage'de failure

### Senaryo B: Logic Error
- **Dosya:** `src/feature_utils.py`
- **Bug:** Feature cross mantığında hata (ör: None yerine boş string döndürme)
- **Beklenen:** Unit test stage'de failure

### Senaryo C: Import Error
- **Dosya:** `app/predictor.py`
- **Bug:** Yanlış import path
- **Beklenen:** Import hatası, pipeline başlamadan failure

## Kullanım

1. Bir bug ekle (yukarıdaki senaryolardan biri)
2. Commit et: `git add . && git commit -m "test: sabotage test"`
3. Push et: `git push`
4. GitHub Actions'da pipeline'ı izle
5. Failure'ı doğrula
6. Bug'ı düzelt
7. Tekrar commit/push et ve success'i doğrula

