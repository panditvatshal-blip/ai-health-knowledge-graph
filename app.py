import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. PAGE CONFIG & STYLING
# -------------------------------------------------------------
st.set_page_config(page_title="Enterprise AI Health Knowledge Graph", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 1.1rem; color: #4B5563; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🩺 Enterprise AI Health Knowledge Graph Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">GraphRAG & Topological Graph Traversal System for Clinical Decision Support</div>', unsafe_allow_html=True)
st.write("---")

# -------------------------------------------------------------
# 2. KNOWLEDGE GRAPH BUILDER (All Symptoms, Diseases & Precautions)
# -------------------------------------------------------------
@st.cache_resource
def build_large_health_graph():
    G = nx.DiGraph()
    
    # बीमारियों, लक्षणों, इलाजों और सावधानियों का पूरा नेटवर्क
    medical_data = [
        # 1. Stomach Pain / Acidity / Food Poisoning
        ("stomach pain", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("vomiting", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("Food Poisoning", "ORS & Oral Rehydration Solution", "TREATED_BY"),
        ("Food Poisoning", "Avoid Outside / Heavy / Dairy Food", "PRECAUTION"),
        ("Food Poisoning", "Avoid Self-Medication with Antibiotics", "PRECAUTION"),

        ("stomach pain", "Acidity / Gastritis", "IS_SYMPTOM_OF"),
        ("heartburn", "Acidity / Gastritis", "IS_SYMPTOM_OF"),
        ("Acidity / Gastritis", "Antacids & Warm Water", "TREATED_BY"),
        ("Acidity / Gastritis", "Avoid Spicy Food, Tea & Coffee", "PRECAUTION"),
        ("Acidity / Gastritis", "Avoid Sleeping Immediately After Meals", "PRECAUTION"),

        # 2. Dengue
        ("high fever", "Dengue", "IS_SYMPTOM_OF"),
        ("joint pain", "Dengue", "IS_SYMPTOM_OF"),
        ("Dengue", "Hydration & Paracetamol", "TREATED_BY"),
        ("Dengue", "AVOID ASPIRIN & IBUPROFEN (Increases Bleeding Risk)", "PRECAUTION"),

        # 3. Migraine
        ("severe headache", "Migraine", "IS_SYMPTOM_OF"),
        ("light sensitivity", "Migraine", "IS_SYMPTOM_OF"),
        ("Migraine", "Dark Room Rest & Hydration", "TREATED_BY"),
        ("Migraine", "Avoid Bright Lights, Loud Noise & Screen Time", "PRECAUTION"),

        # 4. Diabetes
        ("high blood sugar", "Diabetes", "IS_SYMPTOM_OF"),
        ("frequent urination", "Diabetes", "IS_SYMPTOM_OF"),
        ("Diabetes", "Insulin / Doctor Prescribed Medicine", "TREATED_BY"),
        ("Diabetes", "Avoid Sugar, Sweet Drinks & Refined Carbs", "PRECAUTION"),
        ("Diabetes", "Low Carb High Fiber Diet", "RECOMMENDED_DIET"),

        # 5. Common Cold
        ("runny nose", "Common Cold", "IS_SYMPTOM_OF"),
        ("sneezing", "Common Cold", "IS_SYMPTOM_OF"),
        ("Common Cold", "Steam Inhalation & Salt Water Gargle", "TREATED_BY"),
        ("Common Cold", "Avoid Cold Drinks & Chilled Items", "PRECAUTION")
    ]
    
    for u, v, rel in medical_data:
        G.add_edge(u.lower(), v, relationship=rel)
        
    return G

G = build_large_health_graph()

# -------------------------------------------------------------
# 3. GRAPH RETRIEVAL ENGINE (Traverse Logic)
# -------------------------------------------------------------
def analyze_symptoms(user_input):
    user_input_clean = user_input.lower()
    matched_symptoms = []
    matched_diseases = set()
    
    # Matching symptoms from input string
    for node in G.nodes():
        if isinstance(node, str) and node in user_input_clean:
            matched_symptoms.append(node)
            neighbors = list(G.neighbors(node))
            for n in neighbors:
                rel = G[node][n]['relationship']
                if rel == "IS_SYMPTOM_OF":
                    matched_diseases.add(n)
                    
    # Fetch Treatments & Precautions for detected diseases
    disease_details = {}
    for dis in matched_diseases:
        disease_details[dis] = []
        for n in G.neighbors(dis):
            rel = G[dis][n]['relationship']
            disease_details[dis].append((rel, n))
            
    return matched_symptoms, matched_diseases, disease_details

# -------------------------------------------------------------
# 4. USER INTERFACE LAYOUT
# -------------------------------------------------------------
col1, col2 = st.columns([1.1, 0.9])

with col1:
    st.subheader("🔍 Enter Symptoms / स्वास्थ्य लक्षण लिखें")
    
    # Quick Test Dropdown Menu
    preset = st.selectbox("⚡ क्विक टेस्ट हेतु लक्षण सेलेक्ट करें (या खुद टाइप करें):", 
                         ["-- खुद टाइप करें --", 
                          "stomach pain and acidity", 
                          "severe headache with light sensitivity", 
                          "high fever and joint pain", 
                          "high blood sugar and frequent urination"])
    
    default_text = "" if preset == "-- खुद टाइप करें --" else preset
    
    user_query = st.text_area("यहाँ अपने लक्षण लिखें (e.g., I have stomach pain and heartburn):", 
                              value=default_text, height=100)
    
    if st.button("🚀 Analyze via Knowledge Graph", type="primary"):
        if not user_query.strip():
            st.warning("कृपया पहले कोई लक्षण टाइप करें!")
        else:
            with st.spinner("Traversing Knowledge Graph Nodes..."):
                symptoms, diseases, details = analyze_symptoms(user_query)
                
                if diseases:
                    st.success("🎯 Knowledge Graph Traversal Completed!")
                    st.write(f"**Identified Symptom Node(s):** `{', '.join(symptoms).title()}`")
                    st.write("---")
                    
                    # Output Section with 3 Explicit Color Boxes
                    for dis, info in details.items():
                        st.subheader(f"🔴 संभावित बीमारी: {dis}")
                        
                        # 1. 🟢 क्या करें / इलाज (Treatment)
                        treatments = [target for rel, target in info if rel == "TREATED_BY"]
                        if treatments:
                            st.success("🟢 **क्या करें / इलाज (Treatment):**\n\n" + "\n".join([f"• {t}" for t in treatments]))
                        
                        # 2. 🔴 क्या न लें / क्या न करें (Precautions & Avoided Drugs)
                        precautions = [target for rel, target in info if rel == "PRECAUTION"]
                        if precautions:
                            st.error("🚫 **क्या न लें / क्या न करें (Avoid / Precautions):**\n\n" + "\n".join([f"• {p}" for p in precautions]))
                        
                        # 3. 🔵 खान-पान की सलाह (Dietary Advice)
                        diets = [target for rel, target in info if rel == "RECOMMENDED_DIET"]
                        if diets:
                            st.info("🥗 **खान-पान की सलाह (Dietary Advice):**\n\n" + "\n".join([f"• {d}" for d in diets]))
                        
                        st.write("---")
                else:
                    st.error("❌ कोई बीमारी मैच नहीं हुई। कृपया लक्षण (जैसे: `stomach pain`, `headache`, `fever`, `acidity`) जाँचकर दोबारा टाइप करें।")
                
                st.warning("⚠️ **Medical Disclaimer:** This system provides structured informational outputs from a Knowledge Graph. Consult a qualified medical practitioner for formal clinical evaluation.")

with col2:
    st.subheader("🌐 Visual Knowledge Graph Network")
    fig, ax = plt.subplots(figsize=(8, 7))
    pos = nx.spring_layout(G, seed=42)
    
    # Custom styling for nodes
    nx.draw_networkx_nodes(G, pos, node_color="#3B82F6", node_size=1200, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="white", font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="#9CA3AF", arrows=True, arrowsize=15, ax=ax)
    
    plt.axis("off")
    st.pyplot(fig)
