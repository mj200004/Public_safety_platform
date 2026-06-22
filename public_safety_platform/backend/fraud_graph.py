import pandas as pd
import networkx as nx
import os
from typing import Dict, Any, List
from utils.config import MOCK_LOGS_PATH, GRAPH_SCAMMER_OUT_DEGREE, GRAPH_MULE_IN_DEGREE, GRAPH_CRITICAL_RISK_SCORE, GRAPH_BASE_RISK_SCORE

def build_and_analyze_threat_network() -> Dict[str, Any]:
    if not os.path.exists(MOCK_LOGS_PATH):
        return {"error": "Telemetry data unavailable. Please initialize mock data generator."}

    try:
        df = pd.read_csv(MOCK_LOGS_PATH)
    except Exception as e:
        return {"error": f"Failed to parse CSV logs. Details: {str(e)}"}

    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row['source_entity'], row['target_entity'], label=row['interaction_type'])

    # Centrality & Pattern Mapping
    out_degree = dict(G.out_degree())
    in_degree = dict(G.in_degree())
    suspicious_entities: List[Dict[str, str]] = []
    
    for node in G.nodes():
        if out_degree.get(node, 0) >= GRAPH_SCAMMER_OUT_DEGREE and "SPOOF" in node:
            suspicious_entities.append({"node": node, "role": "Suspected Scammer Hub (Aggressor)"})
        if in_degree.get(node, 0) >= GRAPH_MULE_IN_DEGREE and "Acct" in node:
            suspicious_entities.append({"node": node, "role": "Suspected Mule Account (Financial Sink)"})

    evidence_links = [{"source": u, "target": v, "label": d.get('label', 'Unknown')} for u, v, d in G.edges(data=True)]
    is_critical = len(suspicious_entities) > 0

    return {
        "risk_score": GRAPH_CRITICAL_RISK_SCORE if is_critical else GRAPH_BASE_RISK_SCORE,
        "alert_level": "CRITICAL" if is_critical else "LOW",
        "suspicious_entities": suspicious_entities,
        "network_summary": f"Analyzed graph topology containing {len(G.nodes())} distinct entities and {len(G.edges())} interactions.",
        "evidence_links": evidence_links
    }
