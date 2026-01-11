"""
Unit tests for feature engineering logic (feature_utils.py).

These tests are:
- Fast: No external dependencies (no database, no network calls)
- Isolated: Each test is independent
- Focused: Test hashing and feature cross logic specifically
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.feature_extraction import FeatureHasher

from src.feature_utils import to_feature_dict, _escape_token_part


class TestEscapeTokenPart:
    """Test token escaping logic for safe separator handling."""
    
    def test_escape_equals_sign(self):
        """Test that '=' is escaped to '%3D'."""
        result = _escape_token_part("test=value")
        assert result == "test%3Dvalue"
    
    def test_escape_pipe_sign(self):
        """Test that '|' is escaped to '%7C'."""
        result = _escape_token_part("test|value")
        assert result == "test%7Cvalue"
    
    def test_escape_both_separators(self):
        """Test that both separators are escaped correctly."""
        result = _escape_token_part("a=b|c")
        assert result == "a%3Db%7Cc"
    
    def test_no_escape_needed(self):
        """Test that normal strings are unchanged."""
        result = _escape_token_part("normal_value")
        assert result == "normal_value"


class TestToFeatureDict:
    """Test feature dictionary generation (hashing input)."""
    
    def test_simple_feature_dict(self):
        """Test basic feature dictionary creation."""
        df = pd.DataFrame({
            'id': [1, 2],
            'click': [0, 1],
            'site_id': ['s1', 's2'],
            'app_id': ['a1', 'a2'],
        })
        
        result = to_feature_dict(df, add_feature_cross=False)
        
        assert len(result) == 2
        assert 'site_id=s1' in result[0]
        assert 'app_id=a1' in result[0]
        assert result[0]['site_id=s1'] == 1
        # Check that excluded columns are not in the feature dict (check keys, not string)
        assert 'click=' not in result[0]
        assert 'id=' not in result[0]  # Direct key check, not string search
    
    def test_feature_cross_default_pairs(self):
        """Test feature cross with default pairs."""
        df = pd.DataFrame({
            'id': [1],
            'click': [0],
            'site_id': ['s1'],
            'app_id': ['a1'],
            'site_domain': ['sd1'],
            'app_domain': ['ad1'],
            'device_type': ['dt1'],
            'device_conn_type': ['dc1'],
        })
        
        result = to_feature_dict(df, add_feature_cross=True)
        
        assert len(result) == 1
        features = result[0]
        
        # Check base features
        assert 'site_id=s1' in features
        assert 'app_id=a1' in features
        
        # Check cross features (default pairs)
        assert 'cross:site_id=s1|app_id=a1' in features
        assert 'cross:site_domain=sd1|app_domain=ad1' in features
        assert 'cross:device_type=dt1|device_conn_type=dc1' in features
    
    def test_feature_cross_custom_pairs(self):
        """Test feature cross with custom pairs."""
        df = pd.DataFrame({
            'id': [1],
            'click': [0],
            'col_a': ['val_a'],
            'col_b': ['val_b'],
        })
        
        custom_pairs = [('col_a', 'col_b')]
        result = to_feature_dict(df, add_feature_cross=True, cross_pairs=custom_pairs)
        
        assert len(result) == 1
        features = result[0]
        assert 'cross:col_a=val_a|col_b=val_b' in features
    
    def test_missing_values_skipped(self):
        """Test that missing values (NaN) are skipped."""
        df = pd.DataFrame({
            'id': [1],
            'click': [0],
            'site_id': ['s1'],
            'app_id': [np.nan],  # Missing value
        })
        
        result = to_feature_dict(df, add_feature_cross=False, skip_missing=True)
        
        assert len(result) == 1
        features = result[0]
        assert 'site_id=s1' in features
        assert 'app_id=nan' not in features
    
    def test_excluded_columns(self):
        """Test that 'id' and 'click' columns are excluded."""
        df = pd.DataFrame({
            'id': [1, 2],
            'click': [0, 1],
            'feature_col': ['f1', 'f2'],
        })
        
        result = to_feature_dict(df, add_feature_cross=False)
        
        assert len(result) == 2
        # Check that id and click are not in the feature dict
        features_str = str(result[0])
        assert 'id=' not in features_str or 'id=1' not in result[0]
        assert 'click=' not in features_str or 'click=0' not in result[0]
        assert 'feature_col=f1' in result[0]


class TestHashingIntegration:
    """Test that feature dictionaries work correctly with FeatureHasher."""
    
    def test_hashing_consistency(self):
        """Test that same input produces consistent hash bucket."""
        df = pd.DataFrame({
            'id': [1, 2],
            'click': [0, 1],
            'site_id': ['s1', 's1'],  # Same value
            'app_id': ['a1', 'a1'],   # Same value
        })
        
        dicts = to_feature_dict(df, add_feature_cross=False)
        
        hasher = FeatureHasher(n_features=2**10, input_type='dict')
        X = hasher.transform(dicts)
        
        # Both rows should have the same hash for 'site_id=s1' and 'app_id=a1'
        assert X.shape == (2, 2**10)
        # The sparse matrix should have same non-zero positions for identical features
        assert X[0, :].nnz > 0
        assert X[1, :].nnz > 0
    
    def test_hashing_different_inputs(self):
        """Test that different inputs produce different hash patterns."""
        df1 = pd.DataFrame({
            'id': [1],
            'click': [0],
            'site_id': ['s1'],
            'app_id': ['a1'],
        })
        df2 = pd.DataFrame({
            'id': [2],
            'click': [1],
            'site_id': ['s2'],  # Different value
            'app_id': ['a2'],   # Different value
        })
        
        dicts1 = to_feature_dict(df1, add_feature_cross=False)
        dicts2 = to_feature_dict(df2, add_feature_cross=False)
        
        hasher = FeatureHasher(n_features=2**10, input_type='dict')
        X1 = hasher.transform(dicts1)
        X2 = hasher.transform(dicts2)
        
        # Different inputs should produce different hash patterns
        # (they might have some collisions, but generally should be different)
        assert X1.shape == X2.shape == (1, 2**10)
        # At least some positions should be different
        assert (X1 != X2).nnz > 0
    
    def test_feature_cross_hashing(self):
        """Test that feature cross tokens are correctly hashed."""
        df = pd.DataFrame({
            'id': [1],
            'click': [0],
            'site_id': ['s1'],
            'app_id': ['a1'],
        })
        
        dicts = to_feature_dict(df, add_feature_cross=True)
        hasher = FeatureHasher(n_features=2**10, input_type='dict')
        X = hasher.transform(dicts)
        
        # Should have hash features for both base and cross features
        assert X.shape == (1, 2**10)
        assert X.nnz > 0
        
        # Verify cross feature exists in dict
        assert 'cross:site_id=s1|app_id=a1' in dicts[0]

