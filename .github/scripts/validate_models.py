#!/usr/bin/env python3
"""Validate model submissions to OctoFaceHub."""

import os
import json
import sys
import glob
import jsonschema
import requests

# Define schema for metadata.json files
METADATA_SCHEMA = {
    "type": "object",
    "required": ["name", "description", "author", "tags", "ipfs_cid", "created_at"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "description": {"type": "string"},
        "author": {"type": "string", "minLength": 1},
        "tags": {"type": "array", "items": {"type": "string"}},
        "ipfs_cid": {"type": "string", "minLength": 1},
        "size_mb": {"type": "number", "minimum": 0},
        "created_at": {"type": "string", "format": "date-time"}
    }
}

def validate_metadata_files(base_dir="."):
    """Validate all metadata.json files in the models directory."""
    metadata_files = glob.glob(os.path.join(base_dir, "models/*/metadata.json"))
    
    if not metadata_files:
        print("No model metadata files found.")
        return True
    
    all_valid = True
    
    for metadata_file in metadata_files:
        model_dir = os.path.dirname(metadata_file)
        model_name = os.path.basename(model_dir)
        
        print(f"Validating {metadata_file}...")
        
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            
            # Validate against schema
            jsonschema.validate(metadata, METADATA_SCHEMA)
            
            # Check for README.md
            readme_path = os.path.join(model_dir, "README.md")
            if not os.path.exists(readme_path):
                print(f"Error: README.md missing for {model_name}")
                all_valid = False
            
            # Check IPFS CID is valid by trying to access it
            ipfs_cid = metadata.get("ipfs_cid")
            if ipfs_cid:
                try:
                    # Just check if the IPFS gateway responds with a success status
                    response = requests.head(f"https://w3s.link/ipfs/{ipfs_cid}", timeout=5)
                    if response.status_code >= 400:
                        print(f"Error: IPFS CID {ipfs_cid} is not accessible (status {response.status_code})")
                        all_valid = False
                except requests.RequestException as e:
                    print(f"Warning: Could not verify IPFS CID {ipfs_cid}: {str(e)}")
            
            print(f"✅ {model_name} is valid")
            
        except json.JSONDecodeError:
            print(f"Error: {metadata_file} is not valid JSON")
            all_valid = False
        except jsonschema.exceptions.ValidationError as e:
            print(f"Error: {metadata_file} failed validation: {e}")
            all_valid = False
        except Exception as e:
            print(f"Error validating {metadata_file}: {str(e)}")
            all_valid = False
    
    return all_valid

def validate_model_map(base_dir="."):
    """Validate that the model-map.json is up to date and contains all models."""
    try:
        model_dirs = glob.glob(os.path.join(base_dir, "models/*/"))
        model_names = [os.path.basename(os.path.dirname(d)) for d in model_dirs]
        # Remove any dot directories like .github
        model_names = [name for name in model_names if not name.startswith(".")]
        
        # Skip if no models
        if not model_names:
            return True
        
        # Skip model-map.json if it exists in the model_names
        model_names = [name for name in model_names if name != "model-map.json"]
        
        # Load the model map
        model_map_path = os.path.join(base_dir, "models/model-map.json")
        if not os.path.exists(model_map_path):
            print(f"Error: Model map file not found at {model_map_path}")
            return False
            
        with open(model_map_path, "r") as f:
            model_map = json.load(f)
        
        if "models" not in model_map or not isinstance(model_map["models"], list):
            print("Error: models/model-map.json is missing the 'models' array")
            return False
        
        # Get model names from the map
        map_model_names = [model.get("name", "").lower().replace(" ", "-") for model in model_map["models"]]
        
        # Check if all models in directories are in the map
        missing_models = []
        for model_name in model_names:
            if model_name not in map_model_names:
                missing_models.append(model_name)
        
        if missing_models:
            print(f"Error: The following models are missing from models/model-map.json: {', '.join(missing_models)}")
            return False
        
        return True
    
    except Exception as e:
        print(f"Error validating model-map.json: {str(e)}")
        return False

def main():
    """Main function to validate all models."""
    print("Validating OctoFaceHub model submissions...")
    
    metadata_valid = validate_metadata_files()
    map_valid = validate_model_map()
    
    if metadata_valid and map_valid:
        print("✅ All validations passed!")
        return 0
    else:
        print("❌ Validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 