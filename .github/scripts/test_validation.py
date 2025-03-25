#!/usr/bin/env python3
"""Test the model validation script."""

import os
import json
import tempfile
import shutil
import unittest
from datetime import datetime
from . import validate_models


class TestValidation(unittest.TestCase):
    """Test the model validation script."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.models_dir = os.path.join(self.test_dir, "models")
        os.makedirs(self.models_dir)
        
        # Create model-map.json
        self.model_map = {
            "models": []
        }
        with open(os.path.join(self.models_dir, "model-map.json"), "w") as f:
            json.dump(self.model_map, f)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_validate_empty_repo(self):
        """Test validation of an empty repo."""
        # Should pass with empty models directory
        self.assertTrue(validate_models.validate_metadata_files(self.test_dir))
        self.assertTrue(validate_models.validate_model_map(self.test_dir))
    
    def test_schema_validation(self):
        """Test schema validation."""
        # Test that valid metadata passes
        model_dir = os.path.join(self.models_dir, "test-model")
        os.makedirs(model_dir)
        
        # Create a valid metadata.json
        metadata = {
            "name": "Test Model",
            "description": "A test model",
            "author": "testuser",
            "tags": ["test", "model"],
            "ipfs_cid": "bafybeih2qqh6rfmgrrggvkwsve7yuru72tm66vmp2cc5q7nmhytnovq7dm",
            "size_mb": 10.5,
            "created_at": datetime.now().isoformat()
        }
        
        with open(os.path.join(model_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f)
        
        # Create README.md
        with open(os.path.join(model_dir, "README.md"), "w") as f:
            f.write("# Test Model\n\nA test model.")
        
        # Update model-map.json
        self.model_map["models"].append({
            "name": "Test Model",
            "author": "testuser",
            "description": "A test model",
            "tags": ["test", "model"],
            "ipfs_cid": "bafybeih2qqh6rfmgrrggvkwsve7yuru72tm66vmp2cc5q7nmhytnovq7dm",
            "size_mb": 10.5,
            "created_at": metadata["created_at"],
            "path": "models/test-model"
        })
        
        with open(os.path.join(self.models_dir, "model-map.json"), "w") as f:
            json.dump(self.model_map, f)
        
        # Run validation using the test directory
        self.assertTrue(validate_models.validate_metadata_files(self.test_dir))
        self.assertTrue(validate_models.validate_model_map(self.test_dir))


if __name__ == "__main__":
    unittest.main() 