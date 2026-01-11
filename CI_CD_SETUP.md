# CI/CD Pipeline Setup - Homework 2 Deliverables

Bu döküman, MLOps CI/CD Pipeline implementasyonunun özetini içermektedir.

## Pipeline Yapısı

```
Commit Stage (CI)
├── Checkout Code
├── Setup Python
├── Install Dependencies
├── Lint with flake8        ← Code quality check
├── Run Unit Tests          ← Fast, isolated tests
└── Run Component Tests     ← Integration tests

Deployment Stage (CD)
├── Build Docker Image      ← Package once
└── Run Smoke Test          ← Deployment verification
```

## Deliverables

### 1. Pipeline Configuration

**Dosya:** `.github/workflows/ci.yml`

Pipeline aşağıdaki stage'leri içerir:
- **Build** → Python environment setup
- **Unit Test** → Feature engineering logic tests
- **Lint** → Code style and syntax checks
- **Package** → Docker image build
- **Smoke Test** → API deployment verification

### 2. Unit Tests (Fast, Isolated)

**Dosya:** `tests/test_feature_utils.py`

**Neden "Fast":**
- External dependency yok (database, network yok)
- Sadece in-memory operations
- FeatureHasher ile integration testleri dahil

**Test Coverage:**
- Token escaping logic (`_escape_token_part`)
- Feature dictionary generation (`to_feature_dict`)
- Feature cross functionality
- Missing value handling
- Hashing consistency

### 3. Component/Integration Tests

**Dosya:** `tests/test_api_integration.py`

**Neden "Integration":**
- File system interaction (model loading)
- Component interaction (model_loader + predictor + feature_utils)
- Data consistency verification

**Test Coverage:**
- Model loading from file system
- Predictor building
- Single model and ensemble support
- Feature cross integration
- End-to-end prediction flow

### 4. Smoke Test (Deployment Verification)

**Dosya:** `scripts/smoke_test_api.py`

**Neden "End-to-end":**
- Full stack test (API endpoint → model → response)
- Real container deployment
- Network interaction (HTTP requests)
- User perspective verification

**Test Steps:**
1. Health check (`/health` endpoint)
2. Prediction request (`/predict` endpoint)
3. Response validation (status code, data format, value ranges)

### 5. Build Scripts

**Dosyalar:**
- `scripts/build.sh` (Linux/Mac)
- `scripts/build.bat` (Windows)

**Principle:** "Only build your binaries once"

### 6. Linting Configuration

**Dosya:** `.flake8`

- Max line length: 127
- Max complexity: 10
- Syntax error detection
- Style warnings

## Test Execution

### Local Testing

```bash
# Unit tests
pytest tests/test_feature_utils.py -v

# Integration tests
pytest tests/test_api_integration.py -v

# All tests
pytest tests/ -v

# Linting
flake8 .

# Smoke test (API must be running)
python scripts/smoke_test_api.py
```

### CI/CD Pipeline Testing

Pipeline otomatik olarak şu durumlarda çalışır:
- Push to `main`/`master` branch
- Pull request to `main`/`master` branch

## Sabotage Test (Stop the Line)

Detaylar için `SABOTAGE_TEST.md` dosyasına bakın.

**Özet:**
1. Kasıtlı bug ekle (syntax error, logic error, vb.)
2. Commit ve push et
3. Pipeline failure'ı gözlemle
4. Bug'ı düzelt
5. Success'i doğrula

## Evidence Collection

Pipeline çalıştıktan sonra şu evidence'ları toplayın:

1. **Pipeline Configuration Screenshot**
   - `.github/workflows/ci.yml` dosyasının screenshot'ı
   - GitHub Actions UI'dan workflow görseli

2. **Success Evidence (Green Build)**
   - Tüm testlerin passed olduğu screenshot
   - Linting passed
   - Docker build successful
   - Smoke test passed

3. **Failure Evidence (Stop the Line)**
   - Sabotage test'te pipeline failure screenshot'ı
   - Hangi stage'de durduğunu gösteren görsel
   - Error message'ı gösteren görsel

4. **Test Code**
   - `tests/test_feature_utils.py` (Unit test kodu)
   - `scripts/smoke_test_api.py` (Smoke test kodu)
   - Test açıklamaları (neden "fast" ve "end-to-end")

## Pipeline Stages Explained

### Build Stage
- Code checkout
- Python environment setup
- Dependency installation

### Unit Test Stage
- **Fast:** No external dependencies
- **Isolated:** Each test independent
- Tests feature engineering logic specifically

### Lint Stage
- Syntax error detection (E9, F63, F7, F82)
- Style warnings
- Complexity checks

### Package Stage
- Docker image build
- Artifact packaging
- Single build principle

### Smoke Test Stage
- Container startup
- Service health check
- Single prediction request
- Response validation
- **End-to-end:** Full user journey simulation

