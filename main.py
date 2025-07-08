# =============================================================================
# main_app.py - Main application
# =============================================================================

import streamlit as st
from forms import *
from utils import *
from config import Config
from word_export import export_word_ui


def main():
    st.set_page_config(page_title="Générateur de Rapport de Manœuvrabilité", layout="wide")
    Config.setup_directories()
    
    st.title("📄 Générateur de Rapport de Manœuvrabilité")
    
    # Create tabs
    tabs = st.tabs([
        "📁 Métadonnées",
        "✍️ Introduction", 
        "📊 Données d'entrée",
        "🚢 Navires",
        "🌀 Simulations",
        "📈 Analyse",
        "📝 Conclusion",
        "📎 Annexes",
        "🧾 Export"
    ])
    
    # Initialize report data
    rapport = {}
    
    # Render forms
    with tabs[0]:
        rapport["metadonnees"] = MetadataForm.render()
    
    with tabs[1]:
        rapport["introduction"] = IntroductionForm.render()
    
    with tabs[2]:
        rapport["donnees_entree"] = DataInputForm.render()
    
    with tabs[3]:
        rapport["donnees_navires"] = ShipsForm.render()
    
    with tabs[4]:
        rapport["simulations"] = SimulationsForm.render()
    
    with tabs[5]:
        simulations_data = rapport["simulations"]["simulations"] if "simulations" in rapport else []
        rapport["analyse_synthese"] = AnalysisForm.render(simulations_data)
    
    with tabs[6]:
        conclusion_data = ConclusionForm.render()
        rapport.update(conclusion_data)
    with tabs[7]:
        annexes = AnnexesForm.render()
        rapport.update(annexes)
    # Export tab
    with tabs[8]:
        st.subheader("🧾 Export", divider=True)
        
        # Validation
        is_valid = validate_report(rapport)
        
        if is_valid:
            st.success("✅ Rapport prêt pour l'export")
            
            # Download JSON
            json_buffer = create_json_download(rapport)
            st.download_button(
                "📥 Télécharger JSON",
                json_buffer,
                file_name="rapport.json",
                mime="application/json"
            )
            
            # Show summary
            st.subheader("Résumé")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Titre:** {rapport['metadonnees']['titre']}")
                st.write(f"**Client:** {rapport['metadonnees']['client']}")
                
            with col2:
                st.write(f"**Navires:** {len(rapport['donnees_navires']['navires']['navires'])}")
                st.write(f"**Simulations:** {len(rapport['simulations']['simulations'])}")
                taux = rapport['analyse_synthese']['taux_reussite']
                st.write(f"**Taux de réussite:** {taux:.1%}")
        else:
            st.warning("⚠️ Veuillez remplir tous les champs obligatoires")
            
        # Preview JSON
        if "show_json" not in st.session_state:
            st.session_state.show_json = False

        if st.button("👁️ Aperçu JSON"):
            st.session_state.show_json = not st.session_state.show_json

        if st.session_state.show_json:
            st.json(rapport)
        
        # Export DOCX
        export_word_ui(rapport)
    

if __name__ == "__main__":
    main()
