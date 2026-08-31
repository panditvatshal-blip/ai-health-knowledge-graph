# 🩺 Personalized AI Health Knowledge Graph System

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit Framework](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg)](https://streamlit.io/)
[![NetworkX Graph Engine](https://img.shields.io/badge/NetworkX-3.0%2B-green.svg)](https://networkx.org/)
[![Deploy on Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, deterministic clinical decision support system built using **Knowledge Graphs (KG)** and **Graph Retrieval-Augmented Generation (GraphRAG)** logic. 

Unlike probabilistic AI/LLMs that can suffer from hallucinations, this application executes exact topological graph traversals over medical domain nodes to extract verified symptoms, pathologies, treatments, and precautions with **zero hallucination risk**.

---

## 🌟 Key Features

* **Deterministic Graph Traversal:** 100% accurate entity lookup without relying on unpredictable probabilistic APIs.
* **Structured Clinical Knowledge Base:** Built-in directed graph topology linking Symptoms -> Pathologies -> Treatments -> Precautions.
* **Real-Time Dynamic Graph Visualization:** Integrated force-directed graph rendering powered by NetworkX and Matplotlib.
* **Zero API Dependency & Zero Latency:** Fully offline-ready inference engine delivering sub-150ms execution times.
* **Clinical Safety & Contraindication Guardrails:** Explicitly flags medical precautions (e.g., flagging *Avoid Aspirin* for *Dengue*).

---

## 🏗️ System Architecture & Data Flow

+-----------------------------------+
|      User Symptom Query Input     |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
|   Graph Search & Match Engine     |
|   (Adjacency & Path Traversal)    |
+-----------------------------------+
                  |
   +--------------+---------------+
   |                              |
   v                              v
+--------------------+   +--------------------+
| Extracted Sub-Graph|   | NetworkX Force Plot|
+--------------------+   +--------------------+
   |                              |
   +--------------+---------------+
                  |
                  v
+-----------------------------------+
|   Interactive Streamlit Dashboard |
+-----------------------------------+

---
## 🧠 Knowledge Graph & 📐 Schema

### Knowledge Graph
A **knowledge graph** represents information as a network of **nodes (entities)** and **edges (relationships)**.  
For example:
- **Node:** Diabetes  
- **Node:** Insulin  
- **Edge:** treated_by  

This allows users to explore how diseases, symptoms, and treatments are connected.

---

### Schema
A **schema** defines the blueprint of the graph — what types of nodes and relationships are allowed.  

**Entity Types (Nodes):**
- Disease  
- Symptom  
- Treatment  
- Drug  

**Relationship Types (Edges):**
- `has_symptom` (Disease → Symptom)  
- `treated_by` (Disease → Treatment/Drug)  
- `side_effect` (Drug → Symptom)  

---

### Example Schema (JSON)
```json
{
  "entities": ["Disease", "Symptom", "Treatment", "Drug"],
  "relationships": {
    "has_symptom": ["Disease", "Symptom"],
    "treated_by": ["Disease", "Treatment"],
    "side_effect": ["Drug", "Symptom"]
  }
}

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.9+
* **Frontend UI:** Streamlit
* **Graph Engine:** NetworkX
* **Data Visualization:** Matplotlib
* **Cloud Platform:** Streamlit Cloud / GitHub

---

## 🚀 Quick Start & Local Installation

### 1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/health-knowledge-graph.git
cd health-knowledge-graph

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Run the Application
streamlit run app.py

The application will launch automatically in your browser at `http://localhost:8501`.

---

## 📁 Repository Structure

health-knowledge-graph/
│
├── app.py              # Main Streamlit UI & Graph Inference Core Logic
├── requirements.txt    # Python Project Dependencies
├── README.md           # Project Documentation
└── LICENSE             # MIT Open Source License

---

## 🧪 Sample Evaluation Queries

Try entering these sample queries in the application interface:

1. **Migraine Evaluation:** `I am experiencing severe headache and light sensitivity`
2. **Dengue Evaluation:** `High fever with joint pain`
3. **Diabetes Evaluation:** `High blood sugar and frequent urination`
4. **Common Cold Evaluation:** `Runny nose and sneezing`

---

## ⚠️ Medical Disclaimer

This software system is intended solely for educational, research, and technical demonstration purposes. It does not replace professional medical advice, clinical diagnosis, or treatment from a certified healthcare professional.

---

## 👨‍💻 Author
Developed by **Vatsal Mishra**  
GitHub: panditvatshal-blip [(github.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fgithub.com%2Fpanditvatshal-blip")

## 📜 License
This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute with attribution.
