import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. PAGE CONFIG & STYLING
# -------------------------------------------------------------
st.set_page_config(page_title="Enterprise AI Health Knowledge Graph", layout="wide", page_icon="🩺")

# Custom CSS for HTML Cards
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 1.1rem; color: #4B5563; }
    
    .box-treatment {
        background-color: #D1FAE5;
        border-left: 6px solid #10B981;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        color: #065F46;
    }
    .box-avoid {
        background-color: #FEE2E2;
        border-left: 6px solid #EF4444;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        color: #991B1B;
    }
    .box-diet {
        background-color: #DBEAFE;
        border-left: 6px solid #3B82F6;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        color: #1E40AF;
    }
    .box-title {
        font-weight: bold;
        font-size: 1.15rem;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🩺 Enterprise AI Health Knowledge Graph Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">GraphRAG & Topological Graph Traversal System for Clinical Decision Support</div>', unsafe_allow_html=True)
st.write("---")

# -------------------------------------------------------------
# 2. COMPLETE KNOWLEDGE GRAPH DATASET
# -------------------------------------------------------------
@st.cache_resource
def build_large_health_graph():
    G = nx.DiGraph()
    
    # Complete Dataset ensuring every disease has TREATED_BY, PRECAUTION, and RECOMMENDED_DIET
    medical_data = [
        # --- Stomach Pain / Acidity / Food Poisoning ---
        ("stomach pain", "Acidity & Gastritis", "IS_SYMPTOM_OF"),
        ("heartburn", "Acidity & Gastritis", "IS_SYMPTOM_OF"),
        ("acidity", "Acidity & Gastritis", "IS_SYMPTOM_OF"),
        ("Acidity & Gastritis", "Antacids, ENO & Warm Water", "TREATED_BY"),
        ("Acidity & Gastritis", "Avoid Spicy Food, Tea, Coffee & Carbonated Drinks", "PRECAUTION"),
        ("Acidity & Gastritis", "Avoid Sleeping Immediately After Eating", "PRECAUTION"),
        ("Acidity & Gastritis", "Cold Milk & High-Fiber Foods", "RECOMMENDED_DIET"),

        ("stomach pain", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("vomiting", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("Food Poisoning", "ORS Solution & Oral Hydration", "TREATED_BY"),
        ("Food Poisoning", "Avoid Outside / Heavy / Dairy / Oily Food", "PRECAUTION"),
        ("Food Poisoning", "Avoid Antibiotics Without Doctor Prescription", "PRECAUTION"),
        ("Food Poisoning", "BRAT Diet (Bananas, Rice, Applesauce, Toast)", "RECOMMENDED_DIET"),

        # --- Dengue Fever ---
        ("high fever", "Dengue Fever", "IS_SYMPTOM_OF"),
        ("joint pain", "Dengue Fever", "IS_SYMPTOM_OF"),
        ("Dengue Fever", "Hydration & Paracetamol", "TREATED_BY"),
        ("Dengue Fever", "AVOID ASPIRIN & IBUPROFEN (Causes Internal Bleeding)", "PRECAUTION"),
        ("Dengue Fever", "Papaya Leaf Extract & Coconut Water", "RECOMMENDED_DIET"),

        # --- Migraine ---
        ("severe headache", "Migraine", "IS_SYMPTOM_OF"),
        ("light sensitivity", "Migraine", "IS_SYMPTOM_OF"),
        ("Migraine", "Dark Room Rest & Adequate Hydration", "TREATED_BY"),
        ("Migraine", "Avoid Loud Noises, Bright Screens & Skip Meals", "PRECAUTION"),
        ("Migraine", "Magnesium-Rich Foods & Herbal Tea", "RECOMMENDED_DIET"),

        # --- Diabetes ---
        ("high blood sugar", "Diabetes", "IS_SYMPTOM_OF"),
        ("frequent urination", "Diabetes", "IS_SYMPTOM_OF"),
        ("Diabetes", "Insulin & Doctor Prescribed Medication", "TREATED_BY"),
        ("Diabetes", "Avoid Sugar, Sweet Beverages & Refined Sweets", "PRECAUTION"),
        ("Diabetes", "Low Glycemic Index & High Fiber Diet", "RECOMMENDED_DIET"),

        # --- Common Cold ---
        ("runny nose", "Common Cold", "IS_SYMPTOM_OF"),
        ("sneezing", "Common Cold", "IS_SYMPTOM_OF"),
        ("Common Cold", "Steam Inhalation & Warm Salt Water Gargle", "TREATED_BY"),
        ("Common Cold", "Avoid Cold Drinks, Ice Creams & Chilled Items", "PRECAUTION"),
        ("Common Cold", "Hot Soup & Vitamin-C Rich Citrus Fruits", "RECOMMENDED_DIET")
    ]
    
    for u, v, rel in medical_data:
        G.add_edge(u.lower(), v, relationship=rel)
        
    return G

G = build_large_health_graph()

# -------------------------------------------------------------
# 3. GRAPH TRAVERSAL ENGINE
# -------------------------------------------------------------
def analyze_symptoms(user_input):
    user_input_clean = user_input.lower()
    matched_symptoms = []
    matched_diseases = set()
    
    # 1. Match Symptoms
    for node in G.nodes():
        if isinstance(node, str) and node in user_input_clean:
            matched_symptoms.append(node)
            neighbors = list(G.neighbors(node))
            for n in neighbors:
                rel = G[node][n]['relationship']
                if rel == "IS_SYMPTOM_OF":
                    matched_diseases.add(n)
                    
    all_treatments = set()
    all_precautions = set()
    all_diets = set()
    
    # 2. Traverse Graph Edges
    for dis in matched_diseases:
        for n in G.neighbors(dis):
            rel = G[dis][n]['relationship']
            if rel == "TREATED_BY":
                all_treatments.add(f"{n} <i>(for {dis})</i>")
            elif rel == "PRECAUTION":
                all_precautions.add(f"{n} <i>(for {dis})</i>")
            elif rel == "RECOMMENDED_DIET":
                all_diets.add(f"{n} <i>(for {dis})</i>")
            
    return matched_symptoms, list(matched_diseases), list(all_treatments), list(all_precautions), list(all_diets)

# -------------------------------------------------------------
# 4. USER INTERFACE LAYOUT
# -------------------------------------------------------------
col1, col2 = st.columns([1.1, 0.9])

with col1:
    st.subheader("🔍 Enter Symptoms / स्वास्थ्य लक्षण लिखें")
    
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
                    
                    # 1. संभावी बीमारी (1 Bar Only)
                    diseases_str = " | ".join(diseases)
                    st.markdown(f"### 🔴 **संभावित बीमारी:** `{diseases_str}`")
                    st.write(f"**Identified Symptom Node(s):** `{', '.join(symptoms).title()}`")
                    st.write("---")
                    
                    # 2. 🟢 क्या करें / इलाज Box
                    if treatments:
                        t_html = "".join([f"<li style='margin-bottom: 5px;'>{t}</li>" for t in treatments])
                        st.markdown(f"""
                            <div class="box-treatment">
                                <div class="box-title">🟢 क्या करें / इलाज (Treatment):</div>
                                <ul style="margin-bottom: 0px;">{t_html}</ul>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # 3. 🔴 क्या न लें / क्या न करें Box
                    if precautions:
                        p_html = "".join([f"<li style='margin-bottom: 5px;'>{p}</li>" for p in precautions])
                        st.markdown(f"""
                            <div class="box-avoid">
                                <div class="box-title">🚫 क्या न लें / क्या न करें (Avoid / Precautions):</div>
                                <ul style="margin-bottom: 0px;">{p_html}</ul>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # 4. 🔵 खान-पान की सलाह Box
                    if diets:
                        d_html = "".join([f"<li style='margin-bottom: 5px;'>{d}</li>" for d in diets])
                        st.markdown(f"""
                            <div class="box-diet">
                                <div class="box-title">🥗 खान-पान की सलाह (Dietary Advice):</div>
                                <ul style="margin-bottom: 0px;">{d_html}</ul>
                            </div>
                        """, unsafe_allow_html=True)
                        
                else:
                    st.error("❌ कोई बीमारी मैच नहीं हुई। कृपया लक्षण (जैसे: `stomach pain`, `headache`, `fever`, `acidity`) जाँचकर दोबारा टाइप करें।")
                
                st.warning("⚠️ **Medical Disclaimer:** This system provides structured informational outputs from a Knowledge Graph. Consult a qualified medical practitioner for formal clinical evaluation.")

with col2:
    st.subheader("🌐 Visual Knowledge Graph Network")
    fig, ax = plt.subplots(figsize=(10, 9))
    
    pos = nx.spring_layout(G, k=2.0, iterations=50, seed=42)
    
    # Draw Edges
    nx.draw_networkx_edges(G, pos, edge_color="#CBD5E1", arrows=True, arrowsize=12, width=1.0, ax=ax)
    
    # Draw Nodes
    nx.draw_networkx_nodes(G, pos, node_color="#2563EB", node_size=1600, alpha=0.9, ax=ax)
    
    # Labels with Boxes to avoid text overlap
    labels = {node: node.title() for node in G.nodes()}
    for node, (x, y) in pos.items():
        ax.text(x, y, labels[node], fontsize=6.5, fontweight='bold', color='white',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#1E40AF', edgecolor='none', alpha=0.75))
    
    plt.axis("off")
    st.pyplot(fig)
