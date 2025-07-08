# =============================================================================
# config.py - Configuration and constants
# =============================================================================

import os

class Config:
    UPLOAD_DIR = "uploads"
    OUTPUT_DIR = "exports"
    
    # Required fields for validation
    REQUIRED_FIELDS = [
        "titre", "projet", "code_projet", "client", 
        "type_doc", "numero_doc", "annee_doc"
    ]
    
    @classmethod
    def setup_directories(cls):
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
