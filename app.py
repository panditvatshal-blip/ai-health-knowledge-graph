import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


# =============================================================
# 1. PAGE CONFIG
# =============================================================

st.set_page_config(
    page_title="Enterprise AI Health Knowledge Graph",
    layout="wide",
    page_icon="🩺"
)


# =============================================================
# 2. HEADER
# =============================================================

st.markdown(
    """
    <h1 style="color:#1E3A8A;">
        🩺 Enterprise AI Health Knowledge Graph Engine
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="font-size:1.1rem;color:#4B5563;">
        GraphRAG & Topological Graph Traversal System for Clinical Decision Support
    </p>
    """,
    unsafe_allow_html=True
)

st.write("---")


# =============================================================
# 3. KNOWLEDGE GRAPH
# =============================================================

@st.cache_resource
def build_large_health_graph():

    G = nx.DiGraph()

    medical_data = [

        # -----------------------------------------------------
        # ACIDITY & GASTRITIS
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


        # -----------------------------------------------------
        # FOOD POISONING
        # -----------------------------------------------------

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
        # DENGUE FEVER
        # -----------------------------------------------------

        ("high fever", "Dengue Fever", "IS_SYMPTOM_OF"),
        ("joint pain", "Dengue Fever", "IS_SYMPTOM_OF"),

        (
            "Dengue Fever",
            "Hydration & Doctor-Guided Supportive Care",
            "TREATED_BY"
        ),

        (
            "Dengue Fever",
            "Avoid Aspirin & Ibuprofen Unless Advised by a Doctor",
            "PRECAUTION"
        ),

        (
            "Dengue Fever",
            "Adequate Fluids & Nutritious Foods",
            "RECOMMENDED_DIET"
        ),


        # -----------------------------------------------------
        # MIGRAINE
        # -----------------------------------------------------

        ("severe headache", "Migraine", "IS_SYMPTOM_OF"),
        ("light sensitivity", "Migraine", "IS_SYMPTOM_OF"),

        (
            "Migraine",
            "Rest in a Dark Quiet Room & Maintain Hydration",
            "TREATED_BY"
        ),

        (
            "Migraine",
            "Avoid Loud Noises, Bright Screens & Skipping Meals",
            "PRECAUTION"
        ),

        (
            "Migraine",
            "Balanced Meals & Magnesium-Rich Foods",
            "RECOMMENDED_DIET"
        ),


        # -----------------------------------------------------
        # DIABETES
        # -----------------------------------------------------

        ("high blood sugar", "Diabetes", "IS_SYMPTOM_OF"),
        ("frequent urination", "Diabetes", "IS_SYMPTOM_OF"),

        (
            "Diabetes",
            "Follow Doctor-Prescribed Medication & Blood Sugar Monitoring",
            "TREATED_BY"
        ),

        (
            "Diabetes",
            "Avoid Excess Sugar, Sweet Beverages & Refined Sweets",
            "PRECAUTION"
        ),

        (
            "Diabetes",
            "Low Glycemic Index & High Fiber Diet",
            "RECOMMENDED_DIET"
        ),


        # -----------------------------------------------------
        # COMMON COLD
        # -----------------------------------------------------

        ("runny nose", "Common Cold", "IS_SYMPTOM_OF"),
        ("sneezing", "Common Cold", "IS_SYMPTOM_OF"),

        (
            "Common Cold",
            "Rest, Warm Fluids & Supportive Care",
            "TREATED_BY"
        ),

        (
            "Common Cold",
            "Avoid Smoke, Irritants & Anything That Worsens Symptoms",
            "PRECAUTION"
        ),

        (
            "Common Cold",
            "Warm Soup, Fruits & Adequate Fluids",
            "RECOMMENDED_DIET"
        )
    ]

    for source, target, relationship in medical_data:

        G.add_edge(
            source.lower(),
            target,
            relationship=relationship
        )

    return G


G = build_large_health_graph()


# =============================================================
# 4. ANALYZE SYMPTOMS
# =============================================================

def analyze_symptoms(user_input):

    user_input_clean = user_input.lower().strip()

    matched_symptoms = []
    matched_diseases = set()

    # ---------------------------------------------------------
    # MATCH SYMPTOMS
    # ---------------------------------------------------------

    for node in G.nodes():

        if not isinstance(node, str):
            continue

        if node in user_input_clean:

            for neighbor in G.neighbors(node):

                relationship = G[node][neighbor]["relationship"]

                if relationship == "IS_SYMPTOM_OF":

                    matched_symptoms.append(node)
                    matched_diseases.add(neighbor)

    # Remove duplicate symptoms
    matched_symptoms = list(
        dict.fromkeys(matched_symptoms)
    )


    # ---------------------------------------------------------
    # DIRECT DISEASE NAME MATCH
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
    # GET TREATMENT / PRECAUTION / DIET
    # ---------------------------------------------------------

    treatments = []
    precautions = []
    diets = []

    for disease in matched_diseases:

        if disease not in G:
            continue

        for neighbor in G.neighbors(disease):

            relationship = G[disease][neighbor]["relationship"]

            if relationship == "TREATED_BY":

                treatments.append(neighbor)

            elif relationship == "PRECAUTION":

                precautions.append(neighbor)

            elif relationship == "RECOMMENDED_DIET":

                diets.append(neighbor)


    # Remove duplicates
    treatments = list(dict.fromkeys(treatments))
    precautions = list(dict.fromkeys(precautions))
    diets = list(dict.fromkeys(diets))


    return (
        matched_symptoms,
        list(matched_diseases),
        treatments,
        precautions,
        diets
    )


# =============================================================
# 5. MAIN LAYOUT
# =============================================================

col1, col2 = st.columns([1.1, 0.9])


# =============================================================
# LEFT COLUMN
# =============================================================

with col1:

    st.subheader(
        "🔍 Enter Symptoms / स्वास्थ्य लक्षण लिखें"
    )


    # ---------------------------------------------------------
    # QUICK TEST
    # ---------------------------------------------------------

    preset = st.selectbox(
        "⚡ क्विक टेस्ट हेतु लक्षण सेलेक्ट करें (या खुद टाइप करें):",

        [
            "-- खुद टाइप करें --",
            "stomach pain and acidity",
            "severe headache with light sensitivity",
            "high fever and joint pain",
            "high blood sugar and frequent urination",
            "vomiting and stomach pain",
            "runny nose and sneezing"
        ]
    )


    if preset == "-- खुद टाइप करें --":

        default_text = ""

    else:

        default_text = preset


    # ---------------------------------------------------------
    # INPUT
    # ---------------------------------------------------------

    user_query = st.text_area(
        "यहाँ अपने लक्षण लिखें:",
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


            # =================================================
            # DISEASE FOUND
            # =================================================

            if diseases:

                st.success(
                    "🎯 Knowledge Graph Traversal Completed!"
                )


                # -------------------------------------------------
                # POSSIBLE DISEASE
                # -------------------------------------------------

                diseases_str = " | ".join(diseases)

                st.markdown(
                    f"### 🔴 संभावित बीमारी: `{diseases_str}`"
                )


                if symptoms:

                    st.write(
                        "**Identified Symptom Node(s):** "
                        f"`{', '.join(symptoms).title()}`"
                    )


                st.write("---")


                # =================================================
                # 🟢 WHAT TO DO
                # =================================================

                st.subheader(
                    "🟢 क्या करें / What To Do"
                )

                if treatments:

                    for treatment in treatments:

                        st.success(
                            f"✅ {treatment}"
                        )

                else:

                    st.info(
                        "इस बीमारी के लिए treatment information "
                        "Knowledge Graph में उपलब्ध नहीं है।"
                    )


                # =================================================
                # 🚫 WHAT NOT TO DO
                # =================================================

                st.subheader(
                    "🚫 क्या न करें / What To Avoid"
                )

                if precautions:

                    for precaution in precautions:

                        st.error(
                            f"❌ {precaution}"
                        )

                else:

                    st.info(
                        "इस बीमारी के लिए precaution information "
                        "Knowledge Graph में उपलब्ध नहीं है।"
                    )


                # =================================================
                # 🥗 DIET
                # =================================================

                st.subheader(
                    "🥗 खान-पान की सलाह / Dietary Advice"
                )

                if diets:

                    for diet in diets:

                        st.info(
                            f"🥗 {diet}"
                        )

                else:

                    st.info(
                        "इस बीमारी के लिए dietary information "
                        "Knowledge Graph में उपलब्ध नहीं है।"
                    )


                # =================================================
                # ⚠️ DOCTOR NOTE
                # =================================================

                st.warning(
                    """
                    ⚠️ **कब डॉक्टर से संपर्क करें?**

                    अगर लक्षण बहुत गंभीर हों, तेजी से बिगड़ रहे हों,
                    लगातार बने रहें, या आपको अपनी स्थिति को लेकर चिंता हो,
                    तो qualified doctor/health professional से medical evaluation लें।
                    """
                )


            # =================================================
            # NO DISEASE FOUND
            # =================================================

            else:

                st.error(
                    """
                    ❌ कोई बीमारी मैच नहीं हुई।

                    कृपया इनमें से कोई symptom try करें:

                    `stomach pain`  
                    `acidity`  
                    `heartburn`  
                    `vomiting`  
                    `high fever`  
                    `joint pain`  
                    `severe headache`  
                    `light sensitivity`  
                    `high blood sugar`  
                    `frequent urination`  
                    `runny nose`  
                    `sneezing`
                    """
                )


            # =================================================
            # DISCLAIMER
            # =================================================

            st.caption(
                "⚠️ Medical Disclaimer: This system provides "
                "structured informational outputs from a Knowledge Graph "
                "and is not a substitute for professional medical diagnosis."
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


    # ---------------------------------------------------------
    # GRAPH POSITION
    # ---------------------------------------------------------

    pos = nx.spring_layout(
        G,
        k=2.0,
        iterations=50,
        seed=42
    )


    # ---------------------------------------------------------
    # EDGES
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
    # NODES
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
    # LABELS
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
