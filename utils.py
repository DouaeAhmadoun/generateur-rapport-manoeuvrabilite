# =============================================================================
# utils.py - Utility functions
# =============================================================================

import streamlit as st
import json
import os
from io import BytesIO
from typing import Any, List
from config import Config

def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file and return path"""
    if uploaded_file is None:
        return ""
    
    Config.setup_directories()
    file_path = os.path.join(Config.UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def is_filled(value: Any) -> bool:
    """Check if value is not empty"""
    return value is not None and value != ""

def validate_report(data: dict) -> bool:
    """Validate if report has all required fields"""
    # Check metadata - NOUVELLE STRUCTURE
    metadata = data.get("metadonnees", {})  # Changé de "metadonnees_rapport" à "metadonnees"
    if not all(is_filled(metadata.get(field)) for field in ["titre", "projet"]):
        return False
    
    # Pas de code_document imbriqué - les champs sont maintenant directement dans metadonnees
    if not all(is_filled(metadata.get(field)) for field in ["code_projet", "client", "type", "numero", "annee"]):
        return False
    
    # Check introduction
    intro = data.get("introduction", {})
    if not all(is_filled(intro.get(field)) for field in ["guidelines", "objectifs"]):
        return False
    
    # Check has ships and simulations - STRUCTURE CORRIGÉE
    navires_data = data.get("donnees_navires", {}).get("navires", {}).get("navires", [])
    if not navires_data:
        return False
        
    simulations_data = data.get("simulations", {}).get("simulations", [])
    if not simulations_data:
        return False
    
    # Check conclusion
    if not all(is_filled(data.get(field)) for field in ["synthese_redigee", "conclusion"]):
        return False
    
    recommandations = data.get("recommandations", [])
    if not recommandations or not any(is_filled(r) for r in recommandations):
        return False
    
    return True

def create_json_download(data: dict) -> BytesIO:
    """Create downloadable JSON"""
    buffer = BytesIO()
    buffer.write(json.dumps(data, indent=2, ensure_ascii=False).encode())
    buffer.seek(0)
    return buffer

def handle_file_upload_with_legend(label: str, file_types: List[str], key: str) -> List[dict]:
    """Handle file upload with legends"""
    uploaded_files = st.file_uploader(label, type=file_types, accept_multiple_files=True, key=key)
    
    figures = []
    for i, file in enumerate(uploaded_files or []):
        path = save_uploaded_file(file)
        legend = st.text_input(f"Légende pour {file.name}", key=f"{key}_legend_{i}")
        st.image(path, caption=legend, width=200)
        figures.append({"chemin": path, "legende": legend})
    
    return figures

def prepare_report_for_export(data: dict) -> dict:
    """Prepare report data with additional metadata for generation"""
    # Add generation metadata
    data["_metadata"] = {
        "generated_at": datetime.now().isoformat(),
        "version": "1.0",
        "format": "manoeuvrability_report"
    }
    
    # Add section order for report generation
    data["_structure"] = {
        "sections": [
            "metadonnees_rapport",
            "introduction", 
            "donnees_entree",
            "donnees_navires",
            "simulations",
            "analyse_synthese",
            "conclusion",
            "annexes"
        ]
    }
    
    # Ensure consistent data structure
    if "simulations" in data and isinstance(data["simulations"], dict):
        # Make sure we have the right structure
        if "simulations" not in data["simulations"]:
            data["simulations"]["simulations"] = []
    
    return data

def get_report_summary(data: dict) -> dict:
    """Extract key metrics from report data"""
    summary = {}
    
    # Basic info - NOUVELLE STRUCTURE
    metadata = data.get("metadonnees", {})  # Changé de "metadonnees_rapport"
    summary["titre"] = metadata.get("titre", "")
    summary["client"] = metadata.get("client", "")  # Pas de code_document imbriqué
    summary["projet"] = metadata.get("projet", "")
    
    # Counts
    navires_data = data.get("donnees_navires", {})
    navires = navires_data.get("navires", {}).get("navires", [])
    summary["nb_navires"] = len(navires)
    
    remorqueurs = navires_data.get("remorqueurs", {}).get("remorqueurs", [])
    summary["nb_remorqueurs"] = len(remorqueurs)
    
    simulations_data = data.get("simulations", {})
    simulations = simulations_data.get("simulations", [])
    summary["nb_simulations"] = len(simulations)
    
    # Success rate
    if simulations:
        reussites = sum(1 for sim in simulations if sim.get("resultat") == "Réussite")
        summary["taux_reussite"] = reussites / len(simulations)
    else:
        summary["taux_reussite"] = 0
    
    return summary
