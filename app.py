import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

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
# 2. LARGE-SCALE KNOWLEDGE GRAPH BUILDER
# -------------------------------------------------------------
@st.cache_resource
def build_large_health_graph():
    G = nx.DiGraph()
    
    # 🌟 लाखों डेटा जोड़ने के लिए (Large Dataset Structure)
    # आप चाहें तो pd.read_csv("medical_knowledge_base.csv") से भी लोड कर सकते हैं
    medical_data = [
        # Stomach & Digestion Problems
        ("stomach pain", "Acidity", "IS_SYMPTOM_OF"),
        ("stomach pain", "Gastritis", "IS_SYMPTOM_OF"),
        ("stomach pain", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("abdominal cramps", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("vomiting", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("heartburn", "Acidity", "IS_SYMPTOM_OF"),
        ("Acidity", "Antacids & Warm Water", "TREATED_BY"),
        ("Acidity", "Avoid Spicy Food", "PRECAUTION"),
        ("Food Poisoning", "ORS & Hydration", "TREATED_BY"),
        ("Food Poisoning", "Avoid Outside Food", "PRECAUTION"),
        ("Gastritis", "Bland Diet & Probiotics", "RECOMMENDED_DIET"),

        # Migraine & Headaches
        ("severe headache", "Migraine", "IS_SYMPTOM_OF"),
        ("headache", "Migraine", "IS_SYMPTOM_OF"),
        ("light sensitivity", "Migraine", "IS_SYMPTOM_OF"),
        ("nausea", "Migraine", "IS_SYMPTOM_OF"),
        ("Migraine", "Dark Room Rest & Painkillers", "TREATED_BY"),
        ("Migraine", "Avoid Loud Noise & Bright Lights", "PRECAUTION"),

        # Dengue & Viral Infections
        ("high fever", "Dengue", "IS_SYMPTOM_OF"),
        ("fever", "Dengue", "IS_SYMPTOM_OF"),
        ("joint pain", "Dengue", "IS_SYMPTOM_OF"),
        ("body pain", "Dengue", "IS_SYMPTOM_OF"),
        ("Dengue", "Hydration & Paracetamol", "TREATED_BY"),
        ("Dengue", "Avoid Aspirin & Ibuprofen", "PRECAUTION"),

        # Diabetes & Metabolism
        ("high blood sugar", "Diabetes", "IS_SYMPTOM_OF"),
        ("frequent urination", "Diabetes", "IS_SYMPTOM_OF"),
        ("excessive thirst", "Diabetes", "IS_SYMPTOM_OF"),
        ("Diabetes", "Low Carb Diet & Exercise", "RECOMMENDED_DIET"),
        ("Diabetes", "Insulin / Metformin", "TREATED_BY"),

        # Common Cold & Respiratory
        ("runny nose", "Common Cold", "IS_SYMPTOM_OF"),
        ("sneezing", "Common Cold", "IS_SYMPTOM_OF"),
        ("cough", "Common Cold", "IS_SYMPTOM_OF"),
        ("sore throat", "Common Cold", "IS_SYMPTOM_OF"),
        ("Common Cold", "Steam Inhalation & Salt Gargle", "TREATED_BY")
    ]
    
    for u, v, rel in medical_data:
        G.add_edge(u.lower(), v, relationship=rel)
        
    return G

G = build_large_health_graph()

# -------------------------------------------------------------
# 3. GRAPH RETRIEVAL ENGINE (GraphRAG Logic)
# -------------------------------------------------------------
def analyze_symptoms(user_input):
    user_input_clean = user_input.lower()
    matched_symptoms = []
    matched_diseases = set()
    retrieved_relations = []
    
    # Matching symptoms from input string
    for node in G.nodes():
        if isinstance(node, str) and node in user_input_clean:
            matched_symptoms.append(node)
            neighbors = list(G.neighbors(node))
            for n in neighbors:
                rel = G[node][n]['relationship']
                retrieved_relations.append((node.title(), rel, n))
                if rel == "IS_SYMPTOM_OF":
                    matched_diseases.add(n)
                    
    # Fetch Treatments & Precautions for detected diseases
    disease_details = {}
    for dis in matched_diseases:
        disease_details[dis] = []
        for n in G.neighbors(dis):
            rel = G[dis][n]['relationship']
            disease_details[dis].append((rel, n))
            
    return matched_symptoms, matched_diseases, disease_details, retrieved_relations

# -------------------------------------------------------------
# 4. USER INTERFACE LAYOUT
# -------------------------------------------------------------
col1, col2 = st.columns([1.1, 0.9])

with col1:
    st.subheader("🔍 Enter Symptoms / स्वास्थ्य लक्षण लिखें")
    
    # Preset Options for Easy Testing
    preset = st.selectbox("⚡ क्विक टेस्ट हेतु कोई लक्षण चुनें (या नीचे खुद टाइप करें):", 
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
                symptoms, diseases, details, relations = analyze_symptoms(user_query)
                
                if diseases:
                    st.success("🎯 Knowledge Graph Traversal Completed!")
                    
                    st.markdown("### 📋 Clinical Findings:")
                    st.write(f"**Identified Symptom Node(s):** `{', '.join(symptoms).title()}`")
                    st.write(f"**Possible Pathology / Disease:** `{', '.join(diseases)}`")
                    
                    st.markdown("---")
                    st.markdown("### 💊 Recommended Actions & Safety Warnings:")
                    for dis, info in details.items():
                        st.markdown(f"#### 🔴 **{dis}**")
                        for rel, target in info:
                            if rel == "TREATED_BY":
                                st.success(f"✅ **Treatment (`{rel}`):** {target}")
                            elif rel == "PRECAUTION":
                                st.error(f"⚠️ **Precaution (`{rel}`):** {target}")
                            elif rel == "RECOMMENDED_DIET":
                                st.info(f"🥗 **Dietary Advice (`{rel}`):** {target}")
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
