import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. PAGE CONFIG & TITLE
# -------------------------------------------------------------
st.set_page_config(page_title="AI Health Knowledge Graph", layout="wide")
st.title("🩺 Personalized AI Health Knowledge Graph System")
st.write("ज्ञान का ग्राफ (Knowledge Graph) + AI का उपयोग करके सटीक स्वास्थ्य सलाह।")

# -------------------------------------------------------------
# 2. KNOWLEDGE GRAPH BUILDER (NetworkX)
# -------------------------------------------------------------
@st.cache_resource
def build_health_graph():
    G = nx.DiGraph()
    
    # Adding nodes and relationships (Symptom -> Disease -> Treatment/Precaution)
    edges = [
        # Dengue
        ("High Fever", "Dengue", "IS_SYMPTOM_OF"),
        ("Joint Pain", "Dengue", "IS_SYMPTOM_OF"),
        ("Dengue", "Hydration & Paracetamol", "TREATED_BY"),
        ("Dengue", "Avoid Aspirin", "PRECAUTION"),
        
        # Diabetes
        ("High Blood Sugar", "Diabetes", "IS_SYMPTOM_OF"),
        ("Frequent Urination", "Diabetes", "IS_SYMPTOM_OF"),
        ("Diabetes", "Low Carb Diet", "RECOMMENDED_DIET"),
        ("Diabetes", "Insulin/Metformin", "TREATED_BY"),

        # Common Cold
        ("Runny Nose", "Common Cold", "IS_SYMPTOM_OF"),
        ("Sneezing", "Common Cold", "IS_SYMPTOM_OF"),
        ("Common Cold", "Steam Inhalation & Rest", "TREATED_BY"),
        
        # Migraine
        ("Severe Headache", "Migraine", "IS_SYMPTOM_OF"),
        ("Light Sensitivity", "Migraine", "IS_SYMPTOM_OF"),
        ("Migraine", "Dark Room Rest & Painkillers", "TREATED_BY")
    ]
    
    for u, v, rel in edges:
        G.add_edge(u, v, relationship=rel)
        
    return G

G = build_health_graph()

# -------------------------------------------------------------
# 3. GRAPH ENGINE (NO API KEY REQUIRED)
# -------------------------------------------------------------
def analyze_health_query(user_input):
    matched_diseases = set()
    retrieved_facts = []
    
    user_input_lower = user_input.lower()
    
    for node in G.nodes():
        if node.lower() in user_input_lower:
            neighbors = list(G.neighbors(node))
            for n in neighbors:
                rel = G[node][n]['relationship']
                retrieved_facts.append(f"• **{node}** {rel} **{n}**")
                if rel == "IS_SYMPTOM_OF":
                    matched_diseases.add(n)
                    
    # Generate Treatments for matched diseases
    treatments = []
    for dis in matched_diseases:
        for n in G.neighbors(dis):
            rel = G[dis][n]['relationship']
            treatments.append(f"• For **{dis}** ({rel}): {n}")
            
    return retrieved_facts, matched_diseases, treatments

# -------------------------------------------------------------
# 4. MAIN UI LAYOUT
# -------------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔍 लक्षण/समस्या बताएं")
    user_query = st.text_area("अपने लक्षण यहाँ लिखें (e.g., I have severe headache and light sensitivity):", height=120)
    
    if st.button("AI से सलाह लें"):
        if not user_query:
            st.warning("कृपया कुछ लक्षण लिखें!")
        else:
            with st.spinner("Knowledge Graph विश्लेषण जारी है..."):
                facts, diseases, treatments = analyze_health_query(user_query)
                
                st.success("विश्लेषण सफलतापूर्वक पूरा हुआ!")
                st.markdown("### 📋 AI परामर्श एवं निदान (AI Diagnosis):")
                
                if diseases:
                    st.write(f"**संभावित स्थिति (Detected Condition):** {', '.join(diseases)}")
                    st.write("**अनुशंसित उपचार व परहेज (Recommended Actions):**")
                    for t in treatments:
                        st.write(t)
                else:
                    st.write("ज्ञान के नक्शे (Knowledge Graph) में लिखे लक्षणों के आधार पर कोई सीधी बीमारी मैच नहीं हुई। कृपया लक्षण दोबारा जांचें।")
                
                st.warning("⚠️ **Disclaimer:** यह एक AI आधारित नॉलेज ग्राफ सिस्टम है। किसी भी गंभीर स्थिति में डॉक्टर की सलाह अवश्य लें।")
                
                if facts:
                    st.info("**Knowledge Graph से एक्सट्रैक्ट किए गए रिलेशंस:**\n\n" + "\n".join(facts))

with col2:
    st.subheader("🌐 मेडिकल नॉलेज ग्राफ (Visual Graph)")
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=1500, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, ax=ax)
    st.pyplot(fig)