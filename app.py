import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- CONFIGURATION (C'est ici qu'on connecte le cerveau) ---

# Vérifie si l'application est en local ou sur Streamlit Cloud
if 'GOOGLE_API_KEY' in st.secrets:
    api_key = st.secrets['GOOGLE_API_KEY']
else:
    # Solution de repli pour tester en local
    api_key = os.environ.get("GEMINI_API_KEY", "CLÉ_NON_TROUVÉE_TEST_LOCAL")

MODEL_NAME = 'gemini-1.5-pro-latest'

# 1. On crée l'objet Client
# Ceci utilise la clé récupérée ci-dessus
genai.configure(api_key=api_key) 

# 2. On crée l'objet Modèle (qui utilise le client)
# Ceci corrige le NameError et utilise la syntaxe stable
model = genai.GenerativeModel(MODEL_NAME)

# --- LE PROMPT SUPRÊME (V10) --- 
SYSTEM_PROMPT = """
# ... le reste du prompt commence ici.
Tu es un assistant logistique expert pour Pause Café Soleil.
Regarde cette photo de ma liste de route.

1. Extrais toutes les adresses.

2. SÉCURITÉ TOTALE (D'ABORD) :
  • Affiche la liste des clients trouvés.
  • Confirme mes contraintes dictées.
  • Affiche l'heure de fin estimée (ex: "🏁 Fin prévue vers 15h30").

3. Optimise le trajet.

4. Règle de temps : 20 min par défaut, 5 min si "Livraison" ou "Drop".

5. STRATÉGIE "ANTI-BUG" (AFFICHAGE DES LIENS) :
  • Planifie une pause dîner de 30 minutes vers midi.
  • Coupe la route en 2 blocs distincts (autour de cette pause).
  • Donne-moi 2 liens GPS séparés : 
    🌞 MATIN (De l'entrepôt jusqu'au dîner) Link: [Lien Google Maps]
    🍔 APRÈS-MIDI (Repart du prochain client après la pause de 30 min) Link: [Lien Google Maps]

Départ : 3098 Chem. Royal, Québec, QC G1E 1T6.
"""

# --- L'INTERFACE (Ce que Claude va voir sur son téléphone) ---
st.set_page_config(page_title="RouteMaster PCS", page_icon="🚚")

st.title("🚚 RouteMaster V1")
st.write("Optimisation de route pour Pause Café Soleil")

# 1. La Photo
uploaded_file = st.file_uploader("📸 Prends une photo de ta liste", type=["jpg", "png", "jpeg"])

# 2. La Dictée (Zone de texte)
# Sur mobile, Claude appuie sur le micro de son clavier pour remplir ça
contraintes = st.text_area("🗣️ Dicte tes contraintes ici (ex: IGA fermé midi)", height=100)

# 3. Le Bouton Magique
if st.button("🚀 GÉNÉRER LA ROUTE"):
    if uploaded_file is not None:
        with st.spinner('Analyse de la route en cours... (Donne-moi 10 secondes)'):
            try:
                # Préparer l'image pour Gemini
                image = Image.open(uploaded_file)
                
                # Construire la demande complète
                full_request = [
                    SYSTEM_PROMPT, 
                    f"⬇️⬇️⬇️ CONTRAINTES DICTÉES : {contraintes}",
                    image
                ]
                
                # Envoyer à l'IA
                response = model.generate_content(full_request)
                
                # Afficher le résultat
                st.markdown("---")
                st.markdown(response.text)
                st.success("Route calculée avec succès !")
                
            except Exception as e:
                st.error(f"Oups, petite erreur : {e}")
    else:
        st.warning("⚠️ N'oublie pas de mettre la photo de ta liste !") 