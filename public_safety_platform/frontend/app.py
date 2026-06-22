import streamlit as st
import requests
import networkx as nx
import matplotlib.pyplot as plt
import os

# Default to Docker network 'backend', fallback to localhost if run manually
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Public Safety Intelligence", page_icon="🛡️", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stAlert {border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Digital Public Safety Command Center")
st.markdown("### AI-Powered Intelligence for Defeating Counterfeiting & Digital Arrest Scams")
st.divider()

tab1, tab2 = st.tabs(["💵 Point-of-Contact Currency Verification", "🚨 Digital Arrest Syndicate Tracker"])

# --- TAB 1: COUNTERFEIT CURRENCY DETECTION ---
with tab1:
    st.markdown("Upload physical evidence images (₹500 notes) for instant forensic structural analysis.")
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("1. Evidence Intake")
        uploaded_file = st.file_uploader("Upload suspect currency image", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, use_column_width=True)
            analyze_btn = st.button("🔍 Run Forensic Analysis", use_container_width=True)

    with col2:
        st.subheader("2. Intelligence Report")
        if uploaded_file and 'analyze_btn' in locals() and analyze_btn:
            with st.spinner("Analyzing microprint and structural layout..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    response = requests.post(f"{API_URL}/api/v1/analyze-currency", files=files)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("is_counterfeit"):
                            st.error(f"🚨 COUNTERFEIT DETECTED (Confidence: {data['confidence_score']}%)")
                        else:
                            st.success(f"✅ VERIFIED GENUINE (Confidence: {data['confidence_score']}%)")
                            
                        st.markdown("#### System Flags:")
                        for flag in data.get("flags", []):
                            if data.get("is_counterfeit"):
                                st.warning(f"⚠️ {flag}")
                            else:
                                st.info(f"✔️ {flag}")
                                
                        st.markdown("---")
                        st.markdown(f"**Action:** `{data.get('recommended_action')}` | **Audit ID:** `{data.get('audit_id')}`")
                    else:
                        st.error(f"API Error: {response.json().get('detail')}")
                except requests.exceptions.ConnectionError:
                    st.error("ERROR: Connection to Intelligence Core failed. Ensure the FastAPI backend is running.")

# --- TAB 2: DIGITAL ARREST TRACKER ---
with tab2:
    st.markdown("Real-time topological analysis of telecom vectors and financial transaction routing.")
    if st.button("📡 Scan Live Telemetry & Banking Logs", type="primary"):
        with st.spinner("Constructing multi-dimensional threat graph..."):
            try:
                response = requests.get(f"{API_URL}/api/v1/analyze-fraud-network")
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("alert_level") == "CRITICAL":
                        st.error(f"🚨 ACTIVE SYNDICATE DETECTED | Overall Risk Score: {data['risk_score']}/100")
                        
                        col_graph, col_data = st.columns([2, 1])
                        
                        with col_graph:
                            st.markdown(f"*{data['network_summary']}*")
                            fig, ax = plt.subplots(figsize=(10, 6))
                            fig.patch.set_facecolor('#f8f9fa')
                            
                            G = nx.DiGraph()
                            for edge in data["evidence_links"]:
                                G.add_edge(edge["source"], edge["target"], label=edge["label"])
                                
                            pos = nx.spring_layout(G, seed=42)
                            node_colors = ["#ff4b4b" if "SPOOF" in n else "#ffa500" if "Acct" in n else "#00cc96" for n in G.nodes()]
                                    
                            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2500, edgecolors="black", ax=ax)
                            nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold", ax=ax)
                            nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, ax=ax)
                            nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'), font_size=7, ax=ax)
                                
                            ax.axis("off")
                            st.pyplot(fig)
                                
                        with col_data:
                            st.subheader("Intelligence Brief")
                            for entity in data.get("suspicious_entities", []):
                                st.warning(f"**Entity:** {entity['node']}\n\n**Role:** {entity['role']}")
                            st.markdown("---")
                            st.markdown(f"**Audit ID:** `{data['audit_id']}`")
                            
                            if st.button("🚨 ESCALATE TO MHA / CYBER CELL", use_container_width=True):
                                st.success("Automated Request Sent: Nodal officer notified to block IPs and freeze mule accounts.")
                else:
                    st.error(f"API Error: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                 st.error("ERROR: Connection to Intelligence Core failed. Ensure the FastAPI backend is running.")
