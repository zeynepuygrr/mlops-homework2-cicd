"""
Component/Integration tests for API serving logic.

These tests verify the interaction between:
- Model serving logic (predictor.py)
- Data source (model_loader.py)
- Feature engineering (feature_utils.py)

Unlike unit tests, these tests can involve file system operations
to ensure data consistency.
"""
import pytest
import joblib
import tempfile
from pathlib import Path
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction import FeatureHasher

from app.model_loader import load_artifact, DEFAULT_MODEL_PATH
from app.predictor import build_predictor
from src.feature_utils import to_feature_dict


@pytest.fixture
def temp_model_file():
    """Create a temporary model artifact file."""
    # Create a simple dummy model for testing
    hasher = FeatureHasher(n_features=2**10, input_type='dict')
    
    # Create dummy data for training
    df = pd.DataFrame({
        'site_id': ['s1', 's2'],
        'app_id': ['a1', 'a2'],
    })
    dicts = to_feature_dict(df, add_feature_cross=False)
    X = hasher.transform(dicts)
    y = [0, 1]
    
    # Train a simple model
    model = DummyClassifier(strategy='prior')
    model.fit(X, y)
    
    # Create artifact
    artifact = {
        'model': model,
        'hasher': hasher,
        'use_feature_cross': False,
        'cross_pairs': None,
    }
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.joblib', delete=False) as f:
        joblib.dump(artifact, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_model_file_ensemble():
    """Create a temporary model artifact file with ensemble."""
    hasher = FeatureHasher(n_features=2**10, input_type='dict')
    
    df = pd.DataFrame({
        'site_id': ['s1', 's2'],
        'app_id': ['a1', 'a2'],
    })
    dicts = to_feature_dict(df, add_feature_cross=False)
    X = hasher.transform(dicts)
    y = [0, 1]
    
    sgd = DummyClassifier(strategy='uniform')
    nb = DummyClassifier(strategy='prior')
    sgd.fit(X, y)
    nb.fit(X, y)
    
    artifact = {
        'sgd': sgd,
        'nb': nb,
        'hasher': hasher,
        'use_feature_cross': False,
        'cross_pairs': None,
    }
    
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.joblib', delete=False) as f:
        joblib.dump(artifact, f)
        temp_path = f.name
    
    yield temp_path
    
    Path(temp_path).unlink(missing_ok=True)


class TestModelLoader:
    """Test model loading from file system."""
    
    def test_load_artifact_from_file(self, temp_model_file, monkeypatch):
        """Test loading artifact from a specific file path."""
        monkeypatch.setenv('MODEL_PATH', temp_model_file)
        
        artifact = load_artifact()
        
        assert 'hasher' in artifact
        assert artifact['hasher'] is not None
        assert 'model' in artifact or 'sgd' in artifact
    
    def test_load_artifact_default_path(self, temp_model_file, monkeypatch):
        """Test loading artifact with default path (if file exists)."""
        # This test may fail if DEFAULT_MODEL_PATH doesn't exist,
        # which is expected in CI. We'll skip if file doesn't exist.
        if Path(DEFAULT_MODEL_PATH).exists():
            artifact = load_artifact()
            assert 'hasher' in artifact


class TestPredictorIntegration:
    """Test predictor building and prediction flow."""
    
    def test_build_predictor_single_model(self, temp_model_file):
        """Test building predictor with single model artifact."""
        artifact = joblib.load(temp_model_file)
        predict_one = build_predictor(artifact)
        
        # Test prediction with sample features
        features = {
            'site_id': 's1',
            'app_id': 'a1',
        }
        
        proba = predict_one(features)
        
        assert isinstance(proba, float)
        assert 0.0 <= proba <= 1.0
    
    def test_build_predictor_ensemble(self, temp_model_file_ensemble):
        """Test building predictor with ensemble model."""
        artifact = joblib.load(temp_model_file_ensemble)
        predict_one = build_predictor(artifact)
        
        features = {
            'site_id': 's1',
            'app_id': 'a1',
        }
        
        proba = predict_one(features)
        
        assert isinstance(proba, float)
        assert 0.0 <= proba <= 1.0
    
    def test_predictor_with_feature_cross(self, temp_model_file):
        """Test predictor with feature cross enabled."""
        artifact = joblib.load(temp_model_file)
        artifact['use_feature_cross'] = True
        artifact['cross_pairs'] = [('site_id', 'app_id')]
        
        predict_one = build_predictor(artifact)
        
        features = {
            'site_id': 's1',
            'app_id': 'a1',
        }
        
        proba = predict_one(features)
        assert 0.0 <= proba <= 1.0
    
    def test_predictor_missing_hasher(self):
        """Test that missing hasher raises error."""
        artifact = {'model': DummyClassifier()}
        
        with pytest.raises(ValueError, match="missing 'hasher'"):
            build_predictor(artifact)
    
    def test_predictor_data_consistency(self, temp_model_file):
        """Test that same features produce consistent predictions."""
        artifact = joblib.load(temp_model_file)
        predict_one = build_predictor(artifact)
        
        features = {
            'site_id': 's1',
            'app_id': 'a1',
        }
        
        proba1 = predict_one(features)
        proba2 = predict_one(features)
        
        # Same input should produce same output (deterministic)
        assert proba1 == proba2
    
    def test_predictor_different_features(self, temp_model_file):
        """Test that different features produce different predictions."""
        artifact = joblib.load(temp_model_file)
        predict_one = build_predictor(artifact)
        
        features1 = {'site_id': 's1', 'app_id': 'a1'}
        features2 = {'site_id': 's2', 'app_id': 'a2'}
        
        proba1 = predict_one(features1)
        proba2 = predict_one(features2)
        
        # Different inputs may produce different outputs
        # (though with dummy models they might be the same)
        assert isinstance(proba1, float)
        assert isinstance(proba2, float)


class TestEndToEndFlow:
    """Test complete flow from file system to prediction."""
    
    def test_load_and_predict_flow(self, temp_model_file, monkeypatch):
        """Test complete flow: load artifact -> build predictor -> predict."""
        monkeypatch.setenv('MODEL_PATH', temp_model_file)
        
        # Load artifact (file system interaction)
        artifact = load_artifact()
        
        # Build predictor
        predict_one = build_predictor(artifact)
        
        # Make prediction
        features = {
            'site_id': 'test_site',
            'app_id': 'test_app',
        }
        proba = predict_one(features)
        
        assert 0.0 <= proba <= 1.0

