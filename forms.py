# =============================================================================
# forms.py - Form components
# =============================================================================

import streamlit as st
from typing import Dict, Any
from utils import *

class MetadataForm:
    @staticmethod
    def render() -> Dict[str, Any]:
        st.subheader("📁 Métadonnées du rapport", divider=True)
        
        titre = st.text_input("Titre du rapport *")
        projet = st.text_input("Nom du projet *")
        code_projet = st.text_input("Code projet *")
        type_etude = st.selectbox(
            "Type d'étude",
            ("initiale", "complémentaire", "provisoire"),
            accept_new_options=True,
            placeholder="Veuillez sélectionner le type d'étude"
        )
        
        # Main image
        main_image = st.file_uploader("Image principale", type=["png", "jpg", "jpeg"])
        image_path = save_uploaded_file(main_image) if main_image else ""
        if image_path:
            st.image(image_path, width=200)
        
        st.subheader("Informations du client", divider=True)
        client = st.text_input("Client *")
        
        # Logo
        logo = st.file_uploader("Logo du client", type=["png", "jpg", "jpeg"])
        logo_path = save_uploaded_file(logo) if logo else ""
        if logo_path:
            st.image(logo_path, width=200)
        
        st.subheader("Informations du document", divider=True)
        type_doc = st.text_input("Type de document *")
        numero_doc = st.text_input("Numéro de document *")
        annee_doc = st.text_input("Année *")
        
        # Revisions
        st.subheader("Révisions", divider=True)
        revisions = MetadataForm._render_revisions()
        
        return {
            "titre": titre,
            "projet": projet,
            "type_etude": type_etude,
            "main_image": image_path,
            "code_projet": code_projet,
            "client": client,
            "client_logo": logo_path,
            "type": type_doc,
            "numero": numero_doc,
            "annee": annee_doc,
            "historique_revisions": revisions
        }
    
    @staticmethod
    def _render_revisions():
        if "revisions" not in st.session_state:
            st.session_state.revisions = []
        
        if st.button("➕ Ajouter une révision"):
            st.session_state.revisions.append({})
        
        revisions = []
        for i in range(len(st.session_state.revisions)):
            with st.expander(f"Révision {i+1}"):
                col1, col2 = st.columns(2)
                with col1:
                    version = st.text_input("Version", key=f"rev_version_{i}")
                    date = st.date_input("Date", format="DD/MM/YYYY", key=f"rev_date_{i}")
                    description = st.text_input("Description", key=f"rev_description_{i}")
                with col2:
                    auteur = st.text_input("Auteur", key=f"rev_auteur_{i}")
                    verificateur = st.text_input("Vérificateur", key=f"rev_verificateur_{i}")
                    approbateur = st.text_input("Approbateur", key=f"rev_approbateur_{i}")
                
                revisions.append({
                    "version": version,
                    "date": str(date),
                    "description": description,
                    "auteur": auteur,
                    "verificateur": verificateur,
                    "approbateur": approbateur
                })
        
        return revisions

class IntroductionForm:
    @staticmethod
    def render() -> Dict[str, str]:
        st.subheader("✍️ Introduction", divider=True)
        
        guidelines = st.text_area("Éléments à inclure dans l'introduction *")
        objectifs = st.text_area("Objectifs de l'étude *")
        
        return {
            "guidelines": guidelines,
            "objectifs": objectifs
        }

class DataInputForm:
    @staticmethod
    def render() -> Dict[str, Any]:
        st.subheader("📊 Données d'entrée", divider=True)
        
        tabs = st.tabs([
            "📍 Plan de masse",
            "🚩 Plan de balisage",
            "🗺️ Bathymétrie",
            "🌬️ Conditions environnementales",
            "🌊 Étude d’agitation"
        ])

        with tabs[0]:
            phases = DataInputForm._render_phases()
        
        with tabs[1]:
            agitation = DataInputForm._render_balisage()
        
        with tabs[2]:
            bathymetrie = DataInputForm._render_bathymetry()
        
        with tabs[3]:
            conditions = DataInputForm._render_conditions()
        
        with tabs[4]:
            agitation = DataInputForm._render_agitation()
        
        return {
            "plan_de_masse": {"phases": phases},
            "bathymetrie": bathymetrie,
            "conditions_environnementales": conditions,
            "etude_agitation": agitation
        }
    
    @staticmethod
    def _render_phases():
        if "phases" not in st.session_state:
            st.session_state.phases = []
        
        if st.button("➕ Ajouter une phase"):
            st.session_state.phases.append({})
        
        phases = []
        for i in range(len(st.session_state.phases)):
            with st.expander(f"Phase {i+1}"):
                nom = st.text_input(f"Nom phase {i+1} *", key=f"phase_nom_{i}")
                description = st.text_area(f"Description", key=f"phase_desc_{i}")
                figures = handle_file_upload_with_legend("Figures", ["png", "jpg"], f"phase_fig_{i}")
                
                phases.append({
                    "nom": nom,
                    "description": description,
                    "figures": figures
                })

        commentaire = ""
        if st.checkbox("➕ Ajouter un commentaire sur le plan de masse"):
            commentaire = st.text_area("Commentaire plan de masse")
        
        return {
            "phases": phases,
            "commentaire": commentaire
        }
    
    @staticmethod
    def _render_balisage():
        figures = handle_file_upload_with_legend("Planches de balisage", ["png", "jpg"], "balisage_fig")
        
        commentaire = ""
        if st.checkbox("➕ Ajouter un commentaire sur les plans de balisage"):
            commentaire = st.text_area("Commentaire sur les planches de balisage")

        return {
            "actif": True,
            "figures": figures,
            "commentaire": commentaire
        }
    
    @staticmethod
    def _render_bathymetry():
        source = st.text_input("Source bathymétrie *")
        date = st.text_input("Date *")
        notes = st.text_area("Notes profondeur *")
        figures = handle_file_upload_with_legend("Figures bathymétrie", ["png", "jpg"], "bathy_fig")
        
        commentaire = ""
        if st.checkbox("➕ Ajouter un commentaire sur la bathymétrie"):
            commentaire = st.text_area("Commentaire bathymétrie")
        
        return {
            "source": source,
            "date": date,
            "notes_profondeur": notes,
            "figures": figures,
            "commentaire": commentaire
        }
    
    @staticmethod
    def _render_conditions():
        # Simplified conditions
        vent = st.text_input("Conditions de vent")
        houle = st.text_input("Conditions de houle")
        maree = st.text_input("Marée")

        commentaire = ""
        if st.checkbox("➕ Ajouter un commentaire sur les conditions environnementales"):
            commentaire = st.text_area("Commentaire sur les conditions environnementales")
        
        return {
            "vent": [vent] if vent else [],
            "houle": [houle] if houle else [],
            "maree": maree,
            "commentaire": commentaire
        }
    
    @staticmethod
    def _render_agitation():
        if not st.checkbox("Inclure étude d'agitation"):
            return {"actif": False}
        
        figures = handle_file_upload_with_legend("Planches d'agitation", ["png", "jpg"], "agitation_fig")
        
        tableaux = []
        table_files = st.file_uploader(
            "Importer les tableaux d’agitation (.xlsx, .csv)",
            type=["xlsx", "csv"],
            accept_multiple_files=True,
            key="agitation_tables"
        )
        for file in table_files:
            path = os.path.join("uploads", file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            tableaux.append(path)
                
        commentaire = ""
        if st.checkbox("➕ Ajouter un commentaire sur l'étude d'agitation"):
            commentaire = st.text_area("Commentaire sur les planches d’agitation")

        return {
            "actif": True,
            "figures": figures,
            "tableaux": tableaux,
            "commentaire": commentaire
        }

class ShipsForm:
    @staticmethod
    def render() -> Dict[str, Any]:        
        navires = ShipsForm._render_ships()
        commentaire_navires = ""
        if st.checkbox("➕ Ajouter un commentaire sur les navires"):
            commentaire_navires = st.text_area("Commentaire navires")
        
        remorqueurs = ShipsForm._render_tugboats()
        commentaire_remorqueurs = ""
        if st.checkbox("➕ Ajouter un commentaire sur les remorqueurs"):
            commentaire_remorqueurs = st.text_area("Commentaire remorqueurs")
        
        return {
            "navires": {
                "navires": navires,
                "commentaire": commentaire_navires
            },
            "remorqueurs": {
                "remorqueurs": remorqueurs,
                "commentaire": commentaire_remorqueurs
            }
        }
    
    @staticmethod
    def _render_ships():
        st.subheader("🚢 Navires projetés", divider=True)
        if "navires" not in st.session_state:
            st.session_state.navires = []
        
        if st.button("➕ Ajouter un navire"):
            st.session_state.navires.append({})
        
        navires = []
        for i in range(len(st.session_state.navires)):
            with st.expander(f"Navire {i+1}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nom = st.text_input("Nom du navire", key=f"nav_nom_{i}")
                    type_nav = st.text_input("Type", key=f"nav_type_{i}")
                    etat_charge = st.selectbox("État de charge", ["chargé", "sur lest"], key=f"nav_etat_{i}")
                    longueur = st.number_input("Longueur (m)", key=f"nav_longueur_{i}", step=0.5)
                    largeur = st.number_input("Largeur (m)", key=f"nav_largeur_{i}", step=0.5)
                    tirant_av = st.number_input("Tirant d’eau avant (m)", key=f"nav_tir_av_{i}", step=0.5)
                    tirant_ar = st.number_input("Tirant d’eau arrière (m)", key=f"nav_tir_ar_{i}", step=0.5)
                    deplacement = st.number_input("Déplacement (tonnes)", key=f"nav_deplacement_{i}", step=0.5)

                with col2:
                    propulsion = st.text_input("Type de propulsion", key=f"nav_propulsion_{i}")
                    puissance = st.text_input("Puissance machine", key=f"nav_puissance_{i}")
                    est_actif = st.selectbox("Ce navire est-il :", ["actif", "passif"], key=f"nav_role_{i}")
                    remarque = st.text_area("Remarques", key=f"nav_remarque_{i}")

                    image = st.file_uploader("Image (facultative)", type=["png", "jpg"], key=f"nav_img_{i}")
                    img_path = ""
                    if image:
                        img_path = os.path.join("uploads", image.name)
                        with open(img_path, "wb") as f:
                            f.write(image.getbuffer())
                        st.image(img_path, caption="Profil navire", width=200)

                navires.append({
                    "nom": nom,
                    "type": type_nav,
                    "etat_de_charge": etat_charge,
                    "longueur": longueur,
                    "largeur": largeur,
                    "tirant_eau_av": tirant_av,
                    "tirant_eau_ar": tirant_ar,
                    "deplacement": deplacement,
                    "propulsion": propulsion,
                    "puissance_machine": puissance,
                    "remarques": remarque,
                    "figure": img_path,
                    "est_actif": est_actif == "actif"
                })
        
        return navires
    
    @staticmethod
    def _render_tugboats():
        st.subheader("🚤 Remorqueurs", divider=True)
        if "remorqueurs" not in st.session_state:
            st.session_state.remorqueurs = []
        
        if st.button("➕ Ajouter un remorqueur"):
            st.session_state.remorqueurs.append({})
        
        remorqueurs = []
        for i in range(len(st.session_state.remorqueurs)):
            with st.expander(f"Remorqueur {i+1}"):
                col1, col2 = st.columns(2)

            with col1:
                nom = st.text_input("Nom", key=f"rem_nom_{i}")
                type_rem = st.text_input("Type (ASD, conventionnel…)", key=f"rem_type_{i}")
                longueur = st.number_input("Longueur (m)", key=f"rem_longueur_{i}", step=0.5)
                lbp = st.number_input("LBP (m)", key=f"rem_lbp_{i}", step=0.5)
                largeur = st.number_input("Largeur (m)", key=f"rem_largeur_{i}", step=0.5)
                tirant_eau = st.number_input("Tirant d’eau (m)", key=f"rem_tirant_{i}", step=0.5)

            with col2:
                vitesse = st.number_input("Vitesse max (nœuds)", key=f"rem_vitesse_{i}", step=0.5)
                traction = st.number_input("Capacité de traction (tonnes)", key=f"rem_traction_{i}", step=0.5)
                remarque = st.text_area("Remarques", key=f"rem_remarque_{i}")
                image = st.file_uploader("Image (facultative)", type=["png", "jpg"], key=f"rem_img_{i}")
                img_path = ""
                if image:
                    img_path = os.path.join("uploads", image.name)
                    with open(img_path, "wb") as f:
                        f.write(image.getbuffer())
                    st.image(img_path, caption="Profil remorqueur", width=200)

            remorqueurs.append({
                "nom": nom,
                "type": type_rem,
                "longueur": longueur,
                "lbp": lbp,
                "largeur": largeur,
                "tirant_eau": tirant_eau,
                "vitesse": vitesse,
                "traction": traction,
                "remarques": remarque,
                "figure": img_path
            })
        
        return remorqueurs

class SimulationsForm_:
    @staticmethod
    def render() -> list:
        st.header("🌀 Simulations", divider=True)
        
        if "simulations" not in st.session_state:
            st.session_state.simulations = []
        
        if st.button("➕ Ajouter une simulation"):
            st.session_state.simulations.append({})
        
        simulations = []
        for i in range(len(st.session_state.simulations)):
            with st.expander(f"Simulation {i+1}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    navire = st.text_input("Navire", key=f"sim_navire_{i}")
                    manoeuvre = st.text_input("Manœuvre", key=f"sim_manoeuvre_{i}")
                    vent = st.text_input(f"Vent", key=f"sim_vent_{i}")
                    reussite = st.checkbox("✔️ Manœuvre réussie ?", key=f"sim_success_{i}")
                
                with col2:
                    image = st.file_uploader("Image", type=["png", "jpg"], key=f"sim_img_{i}")
                    img_path = save_uploaded_file(image) if image else ""
                    commentaire = st.text_area("Commentaire", key=f"sim_comment_{i}")
                
                simulations.append({
                    "id": i + 1,
                    "navire": navire,
                    "manoeuvre": manoeuvre,
                    "conditions_env": {"vent": vent},
                    "resultat": "Réussite" if reussite else "Échec",
                    "commentaire_pilote": commentaire,
                    "images": {"planche": img_path}
                })
        
        return simulations
    @staticmethod
    def _render_ships():
        return

class SimulationsForm:
    @staticmethod
    def render() -> list:
        simulations = SimulationsForm._render_simulations()
        scenarios, commentaire_scenarios = SimulationsForm._render_scenarios()

        return {
            "simulations": simulations,
            "scenarios_urgence":{
                "scenarios": scenarios,
                "commentaire": commentaire_scenarios
            }
        }
        
    @staticmethod
    def _render_simulations():
        st.subheader("🌀 Simulations", divider=True)
        
        if "simulations" not in st.session_state:
            st.session_state.simulations = []
        
        if st.button("➕ Ajouter une simulation"):
            st.session_state.simulations.append({})
        
        simulations = []
        for i in range(len(st.session_state.simulations)):
            with st.expander(f"Simulation {i+1}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    navire = st.text_input("Navire", key=f"sim_navire_{i}")
                    manoeuvre = st.text_input("Manœuvre", key=f"sim_manoeuvre_{i}")
                    vent = st.text_input(f"Vent", key=f"sim_vent_{i}")
                    reussite = st.checkbox("✔️ Manœuvre réussie ?", key=f"sim_success_{i}")
                
                with col2:
                    image = st.file_uploader("Image", type=["png", "jpg"], key=f"sim_img_{i}")
                    img_path = save_uploaded_file(image) if image else ""
                    commentaire = st.text_area("Commentaire du pilote", key=f"sim_comment_{i}")
                
                simulations.append({
                    "id": i + 1,
                    "navire": navire,
                    "manoeuvre": manoeuvre,
                    "conditions_env": {"vent": vent},
                    "resultat": "Réussite" if reussite else "Échec",
                    "commentaire_pilote": commentaire,
                    "images": {"planche": img_path}
                })
        
        return simulations

    @staticmethod
    def _render_scenarios():
        st.subheader("⚠️ Scénarios d'urgence simulés", divider=True)
        
        if "scenarios" not in st.session_state:
            st.session_state.scenarios = []

        if st.button("➕ Ajouter un scénario d'urgence"):
            st.session_state.scenarios.append({})
        
        scenarios = []
        evenements_possibles = [
            "Panne moteur", "Perte gouvernail", "Défaillance remorqueur",
            "Conditions extrêmes", "Manœuvre d'urgence", "Arrêt d'urgence"
        ]

        for i in range(len(st.session_state.scenarios)):
             with st.expander(f"Scénario d'urgence {i+1}"):
                col1, col2 = st.columns(2)

                with col1:
                    evenement = st.selectbox(
                        f"Événement simulé",
                        evenements_possibles,
                        key=f"evenement_{i}"
                    )
                with col2:
                    image = st.file_uploader("Image", type=["png", "jpg"], key=f"sim_img_{i}")
                    img_path = save_uploaded_file(image) if image else ""
                
                analyse = st.text_area("Analyse du scénario", key=f"analyse_scenario_{i}")
                scenarios.append({
                    "evenement": evenement,
                    "analyse": analyse,
                    "figure": img_path
                })
        commentaire = ""
        if st.checkbox("➕ Ajouter un commentaire sur les scénarios d'urgence"):
            commentaire = st.text_area("Commentaire sur les scénarios d'urgence")

        return scenarios, commentaire

class AnalysisForm:
    @staticmethod
    def render(simulations: list) -> Dict[str, Any]:
        st.subheader("📈 Analyse", divider=True)
        
        nb_essais = len(simulations)
        nb_reussis = sum(1 for sim in simulations if sim["resultat"] == "Réussite")
        taux_reussite = round(nb_reussis / nb_essais, 2) if nb_essais > 0 else 0.0
        
        st.metric("Nombre d'essais", nb_essais)
        st.metric("Taux de réussite", f"{taux_reussite:.1%}")
        
        conditions_critiques = st.text_area("Conditions critiques").split("\n")

        distances = st.text_input("Distances trajectoires")
        
        commentaire = ""
        if st.checkbox("➕ Ajouter un commentaire d'analyse"):
            commentaire = st.text_area("Commentaire analyse")

        return {
            "nombre_essais": nb_essais,
            "taux_reussite": taux_reussite,
            "conditions_critiques": [c.strip() for c in conditions_critiques if c.strip()],
            "distances_trajectoires": distances,
            "commentaire": commentaire
        }

class ConclusionForm:
    @staticmethod
    def render() -> Dict[str, Any]:
        st.subheader("📝 Conclusion", divider=True)
        
        synthese = st.text_area("Synthèse rédigée *")
        conclusion = st.text_area("Conclusion *")
        recommandations_text = st.text_area("Recommandations (une par ligne) *")
        recommandations = [r.strip() for r in recommandations_text.split("\n") if r.strip()]
        
        return {
            "synthese_redigee": synthese,
            "conclusion": conclusion,
            "recommandations": recommandations
        }

class AnnexesForm:
    @staticmethod
    def render() -> Dict[str, Any]:
        st.subheader("📎 Annexes", divider=True)
        
        if "figures" not in st.session_state:
            st.session_state.figures = []
        
        figures = handle_file_upload_with_legend("Figures", ["png", "jpg"], f"annexes_fig")
        
        # === Tableaux dynamiques ===
        if "tableaux" not in st.session_state:
            st.session_state.tableaux = []

        if st.button("➕ Ajouter un tableau"):
            st.session_state.tableaux.append("")

        tableaux = []
        for i in range(len(st.session_state.tableaux)):
            table_file = st.file_uploader(f"Fichier tableau {i+1}", type=["xlsx", "csv"], key=f"table_file_{i}")
            table_path = ""
            if table_file:
                table_path = os.path.join("uploads", table_file.name)
                with open(table_path, "wb") as f:
                    f.write(table_file.getbuffer())
                tableaux.append(table_path)
        
        return {
            "figures": figures,
            "tableaux": tableaux
            }
