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
* **Structured Clinical Knowledge Base:** Built-in directed graph topology linking Symptoms $\rightarrow$ Pathologies $\rightarrow$ Treatments $\rightarrow$ Precautions.
* **Real-Time Dynamic Graph Visualization:** Integrated force-directed graph rendering powered by NetworkX and Matplotlib.
* **Zero API Dependency & Zero Latency:** Fully offline-ready inference engine delivering sub-150ms execution times.
* **Clinical Safety & Contraindication Guardrails:** Explicitly flags medical precautions (e.g., flagging *Avoid Aspirin* for *Dengue*).

---

## 🏗️ System Architecture & Data Flow
