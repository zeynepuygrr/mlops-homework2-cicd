VENV=.venv
PY=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip

.PHONY: install sanity streaming predict all clean test lint smoke-test

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

sanity:
	$(PY) src/sanity_check.py

streaming:
	$(PY) src/train_streaming.py

predict:
	$(PY) src/predict.py

test:
	$(PY) -m pytest tests/ -v

test-unit:
	$(PY) -m pytest tests/test_feature_utils.py -v

test-integration:
	$(PY) -m pytest tests/test_api_integration.py -v

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --statistics

smoke-test:
	$(PY) scripts/smoke_test_api.py

all: sanity streaming predict

clean:
	rm -rf models metrics
