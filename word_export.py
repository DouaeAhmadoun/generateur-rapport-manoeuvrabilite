import streamlit as st
from datetime import datetime
import os
import json
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches, Mm
from io import BytesIO
import base64

def prepare_context_for_template(rapport_data, doc_template=None):
    """
    Prépare le contexte sans créer les InlineImage tout de suite - on garde les chemins
    """
    context = rapport_data.copy()
    
    # On ne fait que vérifier l'existence des images, pas de création d'InlineImage
    if "metadonnees" in context:
        metadonnees = context["metadonnees"]
        
        # Juste vérifier l'existence
        if metadonnees.get("main_image") and os.path.exists(metadonnees["main_image"]):
            metadonnees["main_image_exists"] = True
        else:
            metadonnees["main_image_exists"] = False
            
        if metadonnees.get("client_logo") and os.path.exists(metadonnees["client_logo"]):
            metadonnees["client_logo_exists"] = True
        else:
            metadonnees["client_logo_exists"] = False
        
        # Formatage des dates
        if "historique_revisions" in metadonnees:
            for revision in metadonnees["historique_revisions"]:
                if revision.get("date"):
                    revision["date"] = format_date(revision["date"])
    
    # Calcul du taux de réussite
    if "simulations" in context and "simulations" in context["simulations"]:
        simulations = context["simulations"]["simulations"]
        if simulations and "analyse_synthese" in context:
            nb_essais = len(simulations)
            nb_reussis = sum(1 for sim in simulations if sim.get("resultat") == "Réussite")
            context["analyse_synthese"]["taux_reussite_pct"] = round((nb_reussis / nb_essais) * 100, 1) if nb_essais > 0 else 0
    
    return context

def process_nested_images(context, doc_template=None):
    """
    Traite les images dans toutes les sections imbriquées avec InlineImage
    """
    # Traitement des images dans les données d'entrée
    if "donnees_entree" in context:
        # Images bathymétrie
        if "bathymetrie" in context["donnees_entree"] and "figures" in context["donnees_entree"]["bathymetrie"]:
            for fig in context["donnees_entree"]["bathymetrie"]["figures"]:
                if fig.get("chemin") and os.path.exists(fig["chemin"]):
                    fig["exists"] = True
                    if doc_template:
                        fig["inline_image"] = InlineImage(doc_template, fig["chemin"], width=Mm(120))
                else:
                    fig["exists"] = False
        
        # Images plan de masse
        if "plan_de_masse" in context["donnees_entree"] and "phases" in context["donnees_entree"]["plan_de_masse"]:
            if "phases" in context["donnees_entree"]["plan_de_masse"]["phases"]:
                for phase in context["donnees_entree"]["plan_de_masse"]["phases"]["phases"]:
                    if "figures" in phase:
                        for fig in phase["figures"]:
                            if fig.get("chemin") and os.path.exists(fig["chemin"]):
                                fig["exists"] = True
                                if doc_template:
                                    fig["inline_image"] = InlineImage(doc_template, fig["chemin"], width=Mm(120))
                            else:
                                fig["exists"] = False
        
        # Images étude d'agitation
        if "etude_agitation" in context["donnees_entree"] and "figures" in context["donnees_entree"]["etude_agitation"]:
            for fig in context["donnees_entree"]["etude_agitation"]["figures"]:
                if fig.get("chemin") and os.path.exists(fig["chemin"]):
                    fig["exists"] = True
                    if doc_template:
                        fig["inline_image"] = InlineImage(doc_template, fig["chemin"], width=Mm(120))
                else:
                    fig["exists"] = False
    
    # Traitement des images de navires
    if "donnees_navires" in context:
        # Images navires
        if "navires" in context["donnees_navires"] and "navires" in context["donnees_navires"]["navires"]:
            for navire in context["donnees_navires"]["navires"]["navires"]:
                if navire.get("figure") and os.path.exists(navire["figure"]):
                    navire["figure_exists"] = True
                    if doc_template:
                        navire["figure_inline"] = InlineImage(doc_template, navire["figure"], width=Mm(80))
                else:
                    navire["figure_exists"] = False
        
        # Images remorqueurs
        if "remorqueurs" in context["donnees_navires"] and "remorqueurs" in context["donnees_navires"]["remorqueurs"]:
            for remorqueur in context["donnees_navires"]["remorqueurs"]["remorqueurs"]:
                if remorqueur.get("figure") and os.path.exists(remorqueur["figure"]):
                    remorqueur["figure_exists"] = True
                    if doc_template:
                        remorqueur["figure_inline"] = InlineImage(doc_template, remorqueur["figure"], width=Mm(80))
                else:
                    remorqueur["figure_exists"] = False
    
    # Traitement des images de simulations
    if "simulations" in context and "simulations" in context["simulations"]:
        for sim in context["simulations"]["simulations"]:
            if "images" in sim and "planche" in sim["images"]:
                if sim["images"]["planche"] and os.path.exists(sim["images"]["planche"]):
                    sim["images"]["planche_exists"] = True
                    if doc_template:
                        sim["images"]["planche_inline"] = InlineImage(doc_template, sim["images"]["planche"], width=Mm(140))
                else:
                    sim["images"]["planche_exists"] = False
        
        # Images scénarios d'urgence
        if "scenarios_urgence" in context["simulations"] and "scenarios" in context["simulations"]["scenarios_urgence"]:
            for scenario in context["simulations"]["scenarios_urgence"]["scenarios"]:
                if scenario.get("figure") and os.path.exists(scenario["figure"]):
                    scenario["figure_exists"] = True
                    if doc_template:
                        scenario["figure_inline"] = InlineImage(doc_template, scenario["figure"], width=Mm(120))
                else:
                    scenario["figure_exists"] = False
    
    # Traitement des images des annexes
    if "figures" in context:
        for fig in context["figures"]:
            if fig.get("chemin") and os.path.exists(fig["chemin"]):
                fig["exists"] = True
                if doc_template:
                    fig["inline_image"] = InlineImage(doc_template, fig["chemin"], width=Mm(120))
            else:
                fig["exists"] = False
    
    return context

def format_success_rate(rate):
    """
    Formate le taux de réussite en pourcentage
    """
    return f"{rate:.1%}" if isinstance(rate, (int, float)) else "0%"

def format_date(date_str):
    """
    Formate une date pour l'affichage
    """
    if not date_str:
        return ""
    try:
        # Si c'est déjà une string de date formatée
        if isinstance(date_str, str) and len(date_str) == 10:
            return date_str
        # Sinon essayer de parser et reformater
        dt = datetime.fromisoformat(str(date_str))
        return dt.strftime("%d/%m/%Y")
    except:
        return str(date_str)

# Fonctions inspirées de votre notebook qui marchait
def is_image_path(value):
    """Vérifie si une valeur est un chemin d'image"""
    if not isinstance(value, str):
        return False
    
    # Vérifier l'extension
    ext = os.path.splitext(value)[1].lower()
    is_img = ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]
    
    return is_img

def context_aware_image(doc, path, key_context=None):
    """Crée une InlineImage avec taille adaptée selon le contexte"""
    from PIL import Image
    from docx.shared import Mm

    # Règles de taille par mot-clé (comme dans votre notebook)
    image_rules = {
        "logo": (30, 30),
        "client_logo": (25, 25),
        "main": (140, 100),
        "main_image": (140, 100),
        "gallery": (100, 80),
        "simulation": (120, 90),
        "figure": (120, 90),
        "planche": (140, 100),
        "default": (120, 90)
    }

    # Trouver la règle appropriée
    key_lower = key_context.lower() if key_context else ""
    for keyword, (max_w, max_h) in image_rules.items():
        if keyword in key_lower:
            max_width, max_height = max_w, max_h
            break
    else:
        max_width, max_height = image_rules["default"]

    try:
        img = Image.open(path)
        dpi = 96  # DPI par défaut
        width_px, height_px = img.size
        width_mm = width_px * 25.4 / dpi
        height_mm = height_px * 25.4 / dpi

        # Redimensionner si nécessaire
        if width_mm > max_width or height_mm > max_height:
            scale = min(max_width / width_mm, max_height / height_mm)
            width_mm *= scale
            height_mm *= scale

        return InlineImage(doc, path, width=Mm(width_mm), height=Mm(height_mm))

    except Exception as e:
        st.error(f"⚠️ Erreur image {path} (contexte: {key_context}): {e}")
        return f"[Image non disponible: {os.path.basename(path)}]"

def replace_all_images(data, doc, key_context=None):
    """
    Remplace récursivement tous les chemins d'images par des InlineImage
    Basé sur votre code qui marchait dans le notebook
    """
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            new_value = replace_all_images(v, doc, key_context=k)
            result[k] = new_value
        return result
    elif isinstance(data, list):
        return [replace_all_images(item, doc, key_context=key_context) for item in data]
    elif is_image_path(data) and os.path.exists(data):
        inline_img = context_aware_image(doc, data, key_context)
        return inline_img
    else:
        return data
    """
    Convertit l'image en format compatible avec Word si nécessaire
    """
    from PIL import Image
    import tempfile
    
    # Formats supportés par Word
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    # Vérifier l'extension
    file_ext = os.path.splitext(image_path.lower())[1]
    
    if file_ext in supported_formats:
        return image_path
    
    # Convertir si nécessaire
    try:
        with Image.open(image_path) as img:
            # Convertir en RGB si nécessaire
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Créer un nouveau fichier temporaire
            temp_dir = os.path.dirname(image_path)
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            new_path = os.path.join(temp_dir, f"{base_name}_converted.jpg")
            
            img.save(new_path, 'JPEG', quality=95)
            return new_path
    except Exception as e:
        st.warning(f"Impossible de convertir l'image {image_path}: {e}")
        return image_path
    """
    Nettoie le contexte pour l'aperçu JSON (supprime les objets InlineImage)
    """
    import copy
    clean_context = copy.deepcopy(context)
    
    def remove_inline_images(obj):
        if isinstance(obj, dict):
            # Supprimer les clés qui contiennent des objets InlineImage
            keys_to_remove = [k for k in obj.keys() if k.endswith('_inline')]
            for key in keys_to_remove:
                del obj[key]
            # Récursivement nettoyer les valeurs
            for value in obj.values():
                remove_inline_images(value)
        elif isinstance(obj, list):
            for item in obj:
                remove_inline_images(item)
    
    remove_inline_images(clean_context)
    return clean_context

def generate_word_report_with_template(rapport_data, template_path="templates/report_template.docx"):
   """
   Génère un fichier Word en utilisant l'approche qui marchait dans votre notebook
   """
   try:
       # Vérifier que le template existe
       if not os.path.exists(template_path):
           raise FileNotFoundError(f"Template non trouvé : {template_path}")
       
       # Charger le template
       doc = DocxTemplate(template_path)
       
       # Préparer le contexte (SANS créer les InlineImage)
       context = prepare_context_for_template(rapport_data)
       
       st.write("🔍 **Debug:** Préparation du contexte terminée")
       
       # MAINTENANT on remplace toutes les images par des InlineImage
       # (comme dans votre notebook qui marchait)
       st.write("🖼️ **Traitement des images...**")
       context = replace_all_images(context, doc)
       
       st.write("✅ **Images traitées avec succès**")
       
       # Ajouter des fonctions utilitaires au contexte
       context["format_success_rate"] = format_success_rate
       context["format_date"] = format_date
       
       # Rendre le document
       st.write("📝 **Génération du document...**")
       doc.render(context)
       
       # Sauvegarder
       timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
       filename = f"rapport_manoeuvrabilite_{timestamp}.docx"
       output_path = os.path.join("exports", filename)
       
       # Créer le dossier si nécessaire
       os.makedirs("exports", exist_ok=True)
       
       doc.save(output_path)
       
       return output_path, filename
       
   except Exception as e:
       st.error(f"Erreur lors de la génération : {str(e)}")
       import traceback
       st.error(f"Détails de l'erreur : {traceback.format_exc()}")
       return None, None

def export_word_ui(rapport_data):
    """
    Interface Streamlit pour l'export Word
    """
    st.subheader("📄 Export Word avec Template")
    
    # Options de génération
    col1, col2 = st.columns([2, 2])
    
    with col1:
        # Informations sur le template
        template_path = "templates/report_template.docx"
        if os.path.exists(template_path):
            st.success(f"✅ Template trouvé : {template_path}")
        else:
            st.error(f"❌ Template non trouvé : {template_path}")
            st.info("Assurez-vous que le fichier 'report_template.docx' est dans le répertoire templates.")
            return
    
    with col2:
        st.info("Le rapport sera généré en utilisant le template de l'entreprise")
    
    if st.button("🔄 Générer le rapport", type="primary"):
            with st.spinner("Génération du rapport en cours..."):
                output_path, filename = generate_word_report_with_template(rapport_data, template_path)
                
                if output_path and os.path.exists(output_path):
                    # Bouton de téléchargement
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="📥 Télécharger le rapport Word",
                            data=file.read(),
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            type="primary"
                        )
                    
                    st.success(f"✅ Rapport généré avec succès : {filename}")
                    
                    # Afficher un aperçu des données utilisées
                    with st.expander("👁️ Aperçu des données du contexte en JSON"):
                        # Créer un aperçu simplifié pour l'affichage
                        context_preview = prepare_context_for_template(rapport_data)
                        st.json(context_preview)
                        
                else:
                    st.error("❌ Erreur lors de la génération du rapport")
    