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
# 2. KNOWLEDGE GRAPH BUILDER (Complete Dataset)
# -------------------------------------------------------------
@st.cache_resource
def build_large_health_graph():
    G = nx.DiGraph()
    
    # मेडिकल नॉलेज ग्राफ का डेटासेट
    medical_data = [
        # 1. Stomach Pain / Acidity / Food Poisoning
        ("stomach pain", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("vomiting", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("Food Poisoning", "ORS & Oral Rehydration Solution", "TREATED_BY"),
        ("Food Poisoning", "Avoid Outside / Heavy / Dairy Food", "PRECAUTION"),
        ("Food Poisoning", "Avoid Self-Medication with Antibiotics", "PRECAUTION"),

        ("stomach pain", "Acidity / Gastritis", "IS_SYMPTOM_OF"),
        ("heartburn", "Acidity / Gastritis", "IS_SYMPTOM_OF"),
        ("acidity", "Acidity / Gastritis", "IS_SYMPTOM_OF"),
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
# 3. GRAPH RETRIEVAL ENGINE (Single Output Aggregator)
# -------------------------------------------------------------
def analyze_symptoms(user_input):
    user_input_clean = user_input.lower()
    matched_symptoms = []
    matched_diseases = set()
    
    # 1. Matches nodes from user query
    for node in G.nodes():
        if isinstance(node, str) and node in user_input_clean:
            matched_symptoms.append(node)
            neighbors = list(G.neighbors(node))
            for n in neighbors:
                rel = G[node][n]['relationship']
                if rel == "IS_SYMPTOM_OF":
                    matched_diseases.add(n)
                    
    # 2. Consolidate Treatments, Precautions & Diets across all matched diseases
    all_treatments = set()
    all_precautions = set()
    all_diets = set()
    
    for dis in matched_diseases:
        for n in G.neighbors(dis):
            rel = G[dis][n]['relationship']
            if rel == "TREATED_BY":
                all_treatments.add(f"{n} (for {dis})")
            elif rel == "PRECAUTION":
                all_precautions.add(f"{n} (for {dis})")
            elif rel == "RECOMMENDED_DIET":
                all_diets.add(f"{n} (for {dis})")
            
    return matched_symptoms, list(matched_diseases), list(all_treatments), list(all_precautions), list(all_diets)

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
                symptoms, diseases, treatments, precautions, diets = analyze_symptoms(user_query)
                
                if diseases:
                    st.success("🎯 Knowledge Graph Traversal Completed!")
                    
                    # 1. संभावी बीमारी (केवल एक बार दिखेगी)
                    diseases_str = " | ".join(diseases)
                    st.markdown(f"### 🔴 **संभावित बीमारी (Detected Condition):** `{diseases_str}`")
                    st.write(f"**Identified Symptom Node(s):** `{', '.join(symptoms).title()}`")
                    st.write("---")
                    
                    # 2. 🟢 क्या करें / इलाज (Treatment Box)
                    if treatments:
                        st.success("🟢 **क्या करें / इलाज (Treatment):**\n\n" + "\n".join([f"• {t}" for t in treatments]))
                    
                    # 3. 🔴 क्या न लें / सावधानियां (Avoid Box)
                    if precautions:
                        st.error("🚫 **क्या न लें / क्या न करें (Avoid / Precautions):**\n\n" + "\n".join([f"• {p}" for p in precautions]))
                    
                    # 4. 🔵 खान-पान की सलाह (Diet Box)
                    if diets:
                        st.info("🥗 **खान-पान की सलाह (Dietary Advice):**\n\n" + "\n".join([f"• {d}" for d in diets]))
                        
                else:
                    st.error("❌ कोई बीमारी मैच नहीं हुई। कृपया लक्षण (जैसे: `stomach pain`, `headache`, `fever`, `acidity`) जाँचकर दोबारा टाइप करें।")
                
                st.warning("⚠️ **Medical Disclaimer:** This system provides structured informational outputs from a Knowledge Graph. Consult a qualified medical practitioner for formal clinical evaluation.")

with col2:
    st.subheader("🌐 Visual Knowledge Graph Network")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # k=1.2 नोड्स को आपस में चिपकने से रोकेगा
    pos = nx.spring_layout(G, k=1.2, seed=42)
    
    # नोड्स और टेक्स्ट का स्टाइल
    nx.draw_networkx_nodes(G, pos, node_color="#2563EB", node_size=1800, alpha=0.85, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=7, font_color="white", font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="#9CA3AF", arrows=True, arrowsize=12, width=1.2, ax=ax)
    
    plt.axis("off")
    st.pyplot(fig)
