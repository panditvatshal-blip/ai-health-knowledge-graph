import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. PAGE CONFIG & STYLING
# -------------------------------------------------------------

st.set_page_config(
    page_title="Enterprise AI Health Knowledge Graph",
    layout="wide",
    page_icon="🩺"
)

# Custom CSS for HTML Cards
st.markdown("""
<style>

.main-header {
    font-size: 2.2rem;
    font-weight: bold;
    color: #1E3A8A;
}

.sub-header {
    font-size: 1.1rem;
    color: #4B5563;
}

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

.box-doctor {
    background-color: #FEF3C7;
    border-left: 6px solid #F59E0B;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    color: #92400E;
}

.box-title {
    font-weight: bold;
    font-size: 1.15rem;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# 2. HEADER
# -------------------------------------------------------------

st.markdown(
    '<div class="main-header">🩺 Enterprise AI Health Knowledge Graph Engine</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">GraphRAG & Topological Graph Traversal System for Clinical Decision Support</div>',
    unsafe_allow_html=True
)

st.write("---")


# -------------------------------------------------------------
# 3. COMPLETE KNOWLEDGE GRAPH DATASET
# -------------------------------------------------------------

@st.cache_resource
def build_large_health_graph():

    G = nx.DiGraph()

    medical_data = [

        # -----------------------------------------------------
        # Stomach Pain / Acidity / Food Poisoning
        # -----------------------------------------------------

        ("stomach pain", "Acidity & Gastritis", "IS_SYMPTOM_OF"),
        ("heartburn", "Acidity & Gastritis", "IS_SYMPTOM_OF"),
        ("acidity", "Acidity & Gastritis", "IS_SYMPTOM_OF"),

        (
            "Acidity & Gastritis",
            "Antacids, ENO & Warm Water",
            "TREATED_BY"
        ),

        (
            "Acidity & Gastritis",
            "Avoid Spicy Food, Tea, Coffee & Carbonated Drinks",
            "PRECAUTION"
        ),

        (
            "Acidity & Gastritis",
            "Avoid Sleeping Immediately After Eating",
            "PRECAUTION"
        ),

        (
            "Acidity & Gastritis",
            "Cold Milk & High-Fiber Foods",
            "RECOMMENDED_DIET"
        ),

        ("stomach pain", "Food Poisoning", "IS_SYMPTOM_OF"),
        ("vomiting", "Food Poisoning", "IS_SYMPTOM_OF"),

        (
            "Food Poisoning",
            "ORS Solution & Oral Hydration",
            "TREATED_BY"
        ),

        (
            "Food Poisoning",
            "Avoid Outside / Heavy / Dairy / Oily Food",
            "PRECAUTION"
        ),

        (
            "Food Poisoning",
            "Avoid Antibiotics Without Doctor Prescription",
            "PRECAUTION"
        ),

        (
            "Food Poisoning",
            "BRAT Diet (Bananas, Rice, Applesauce, Toast)",
            "RECOMMENDED_DIET"
        ),


        # -----------------------------------------------------
        # Dengue Fever
        # -----------------------------------------------------

        ("high fever", "Dengue Fever", "IS_SYMPTOM_OF"),
        ("joint pain", "Dengue Fever", "IS_SYMPTOM_OF"),

        (
            "Dengue Fever",
            "Hydration & Paracetamol",
            "TREATED_BY"
        ),

        (
            "Dengue Fever",
            "AVOID ASPIRIN & IBUPROFEN (Causes Internal Bleeding)",
            "PRECAUTION"
        ),

        (
            "Dengue Fever",
            "Papaya Leaf Extract & Coconut Water",
            "RECOMMENDED_DIET"
        ),


        # -----------------------------------------------------
        # Migraine
        # -----------------------------------------------------

        ("severe headache", "Migraine", "IS_SYMPTOM_OF"),
        ("light sensitivity", "Migraine", "IS_SYMPTOM_OF"),

        (
            "Migraine",
            "Dark Room Rest & Adequate Hydration",
            "TREATED_BY"
        ),

        (
            "Migraine",
            "Avoid Loud Noises, Bright Screens & Skip Meals",
            "PRECAUTION"
        ),

        (
            "Migraine",
            "Magnesium-Rich Foods & Herbal Tea",
            "RECOMMENDED_DIET"
        ),


        # -----------------------------------------------------
        # Diabetes
        # -----------------------------------------------------

        ("high blood sugar", "Diabetes", "IS_SYMPTOM_OF"),
        ("frequent urination", "Diabetes", "IS_SYMPTOM_OF"),

        (
            "Diabetes",
            "Insulin & Doctor Prescribed Medication",
            "TREATED_BY"
        ),

        (
            "Diabetes",
            "Avoid Sugar, Sweet Beverages & Refined Sweets",
            "PRECAUTION"
        ),

        (
            "Diabetes",
            "Low Glycemic Index & High Fiber Diet",
            "RECOMMENDED_DIET"
        ),


        # -----------------------------------------------------
        # Common Cold
        # -----------------------------------------------------

        ("runny nose", "Common Cold", "IS_SYMPTOM_OF"),
        ("sneezing", "Common Cold", "IS_SYMPTOM_OF"),

        (
            "Common Cold",
            "Steam Inhalation & Warm Salt Water Gargle",
            "TREATED_BY"
        ),

        (
            "Common Cold",
            "Avoid Cold Drinks, Ice Creams & Chilled Items",
            "PRECAUTION"
        ),

        (
            "Common Cold",
            "Hot Soup & Vitamin-C Rich Citrus Fruits",
            "RECOMMENDED_DIET"
        )
    ]

    # Add all graph edges
    for u, v, rel in medical_data:
        G.add_edge(
            u.lower(),
            v,
            relationship=rel
        )

    return G


G = build_large_health_graph()


# -------------------------------------------------------------
# 4. GRAPH TRAVERSAL ENGINE
# -------------------------------------------------------------

def analyze_symptoms(user_input):

    user_input_clean = user_input.lower().strip()

    matched_symptoms = []
    matched_diseases = set()

    # ---------------------------------------------------------
    # 1. Match Symptoms
    # ---------------------------------------------------------

    for node in G.nodes():

        if isinstance(node, str) and node in user_input_clean:

            # Check whether node is a symptom node
            neighbors = list(G.neighbors(node))

            for n in neighbors:

                rel = G[node][n]["relationship"]

                if rel == "IS_SYMPTOM_OF":

                    matched_symptoms.append(node)
                    matched_diseases.add(n)

    # Remove duplicate symptoms
    matched_symptoms = list(dict.fromkeys(matched_symptoms))

    # ---------------------------------------------------------
    # 2. Direct Disease Name Match
    # ---------------------------------------------------------

    disease_names = [
        "Acidity & Gastritis",
        "Food Poisoning",
        "Dengue Fever",
        "Migraine",
        "Diabetes",
        "Common Cold"
    ]

    for disease in disease_names:

        if disease.lower() in user_input_clean:
            matched_diseases.add(disease)

    # ---------------------------------------------------------
    # 3. Traverse Graph Edges
    # ---------------------------------------------------------

    all_treatments = set()
    all_precautions = set()
    all_diets = set()

    for dis in matched_diseases:

        for n in G.neighbors(dis):

            rel = G[dis][n]["relationship"]

            if rel == "TREATED_BY":

                all_treatments.add(
                    f"{n} <i>(for {dis})</i>"
                )

            elif rel == "PRECAUTION":

                all_precautions.add(
                    f"{n} <i>(for {dis})</i>"
                )

            elif rel == "RECOMMENDED_DIET":

                all_diets.add(
                    f"{n} <i>(for {dis})</i>"
                )

    return (
        matched_symptoms,
        list(matched_diseases),
        list(all_treatments),
        list(all_precautions),
        list(all_diets)
    )


# -------------------------------------------------------------
# 5. USER INTERFACE LAYOUT
# -------------------------------------------------------------

col1, col2 = st.columns([1.1, 0.9])


# =============================================================
# LEFT COLUMN
# =============================================================

with col1:

    st.subheader(
        "🔍 Enter Symptoms / स्वास्थ्य लक्षण लिखें"
    )

    preset = st.selectbox(
        "⚡ क्विक टेस्ट हेतु लक्षण सेलेक्ट करें (या खुद टाइप करें):",

        [
            "-- खुद टाइप करें --",
            "stomach pain and acidity",
            "severe headache with light sensitivity",
            "high fever and joint pain",
            "high blood sugar and frequent urination"
        ]
    )

    default_text = (
        ""
        if preset == "-- खुद टाइप करें --"
        else preset
    )

    user_query = st.text_area(
        "यहाँ अपने लक्षण लिखें (e.g., I have stomach pain and heartburn):",
        value=default_text,
        height=100
    )


    # ---------------------------------------------------------
    # ANALYZE BUTTON
    # ---------------------------------------------------------

    if st.button(
        "🚀 Analyze via Knowledge Graph",
        type="primary"
    ):

        if not user_query.strip():

            st.warning(
                "कृपया पहले कोई लक्षण टाइप करें!"
            )

        else:

            with st.spinner(
                "Traversing Knowledge Graph Nodes..."
            ):

                (
                    symptoms,
                    diseases,
                    treatments,
                    precautions,
                    diets
                ) = analyze_symptoms(user_query)


            # -------------------------------------------------
            # DISEASE FOUND
            # -------------------------------------------------

            if diseases:

                st.success(
                    "🎯 Knowledge Graph Traversal Completed!"
                )


                # ---------------------------------------------
                # POSSIBLE DISEASE
                # ---------------------------------------------

                diseases_str = " | ".join(diseases)

                st.markdown(
                    f"### 🔴 **संभावित बीमारी:** `{diseases_str}`"
                )

                if symptoms:

                    st.write(
                        f"**Identified Symptom Node(s):** "
                        f"`{', '.join(symptoms).title()}`"
                    )

                st.write("---")


                # =================================================
                # 🟢 WHAT TO DO
                # =================================================

                if treatments:

                    t_html = "".join(
                        [
                            f"<li style='margin-bottom: 7px;'>{t}</li>"
                            for t in treatments
                        ]
                    )

                    st.markdown(
                        f"""
                        <div class="box-treatment">

                            <div class="box-title">
                                🟢 क्या करें / क्या मदद मिल सकती है
                            </div>

                            <ul style="margin-bottom: 0;">
                                {t_html}
                            </ul>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # =================================================
                # 🔴 WHAT NOT TO DO
                # =================================================

                if precautions:

                    p_html = "".join(
                        [
                            f"<li style='margin-bottom: 7px;'>{p}</li>"
                            for p in precautions
                        ]
                    )

                    st.markdown(
                        f"""
                        <div class="box-avoid">

                            <div class="box-title">
                                🚫 क्या न करें / What To Avoid
                            </div>

                            <ul style="margin-bottom: 0;">
                                {p_html}
                            </ul>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # =================================================
                # 🔵 DIETARY ADVICE
                # =================================================

                if diets:

                    d_html = "".join(
                        [
                            f"<li style='margin-bottom: 7px;'>{d}</li>"
                            for d in diets
                        ]
                    )

                    st.markdown(
                        f"""
                        <div class="box-diet">

                            <div class="box-title">
                                🥗 खान-पान की सलाह / Dietary Advice
                            </div>

                            <ul style="margin-bottom: 0;">
                                {d_html}
                            </ul>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # =================================================
                # ⚠️ WHEN TO SEEK MEDICAL HELP
                # =================================================

                st.markdown(
                    """
                    <div class="box-doctor">

                        <div class="box-title">
                            ⚠️ कब डॉक्टर से संपर्क करें?
                        </div>

                        <div>
                            अगर लक्षण बहुत गंभीर हों, तेजी से बिगड़ रहे हों,
                            लगातार बने रहें, या आपको अपनी स्थिति को लेकर चिंता हो,
                            तो qualified doctor/health professional से medical evaluation लें।
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # -------------------------------------------------
            # NO DISEASE FOUND
            # -------------------------------------------------

            else:

                st.error(
                    "❌ कोई बीमारी मैच नहीं हुई। "
                    "कृपया लक्षण (जैसे: "
                    "`stomach pain`, `headache`, `fever`, "
                    "`acidity`, `vomiting`) जाँचकर दोबारा टाइप करें।"
                )


            # -------------------------------------------------
            # MEDICAL DISCLAIMER
            # -------------------------------------------------

            st.warning(
                "⚠️ **Medical Disclaimer:** "
                "This system provides structured informational outputs "
                "from a Knowledge Graph. Consult a qualified medical "
                "practitioner for formal clinical evaluation."
            )


# =============================================================
# RIGHT COLUMN - VISUAL GRAPH
# =============================================================

with col2:

    st.subheader(
        "🌐 Visual Knowledge Graph Network"
    )

    fig, ax = plt.subplots(
        figsize=(10, 9)
    )

    pos = nx.spring_layout(
        G,
        k=2.0,
        iterations=50,
        seed=42
    )


    # ---------------------------------------------------------
    # Draw Edges
    # ---------------------------------------------------------

    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="#CBD5E1",
        arrows=True,
        arrowsize=12,
        width=1.0,
        ax=ax
    )


    # ---------------------------------------------------------
    # Draw Nodes
    # ---------------------------------------------------------

    nx.draw_networkx_nodes(
        G,
        pos,
        node_color="#2563EB",
        node_size=1600,
        alpha=0.9,
        ax=ax
    )


    # ---------------------------------------------------------
    # Labels
    # ---------------------------------------------------------

    labels = {
        node: node.title()
        for node in G.nodes()
    }

    for node, (x, y) in pos.items():

        ax.text(
            x,
            y,
            labels[node],
            fontsize=6.5,
            fontweight="bold",
            color="white",
            ha="center",
            va="center",
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="#1E40AF",
                edgecolor="none",
                alpha=0.75
            )
        )


    plt.axis("off")

    st.pyplot(fig)
