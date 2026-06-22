import pytest
import os
from backend.fraud_graph import build_and_analyze_threat_network
from backend.counterfeit_detector import analyze_currency_note
from utils.config import REFERENCE_IMAGE_PATH

@pytest.fixture(autouse=True)
def setup_mock_data():
    """Ensure mock data is generated before tests run."""
    from backend.mock_data_generator import generate_telecom_logs, generate_reference_note
    if not os.path.exists(REFERENCE_IMAGE_PATH):
        generate_telecom_logs()
        generate_reference_note()

def test_fraud_graph_engine():
    """Validate Graph Centrality identifies the scammer and mule accounts."""
    result = build_and_analyze_threat_network()
    assert "error" not in result
    assert result["alert_level"] == "CRITICAL"
    assert len(result["suspicious_entities"]) > 0

def test_counterfeit_engine_genuine_pass():
    """Validate OpenCV structural similarity correctly passes the genuine reference."""
    with open(REFERENCE_IMAGE_PATH, "rb") as img_file:
        result = analyze_currency_note(img_file.read())
    assert result["is_counterfeit"] is False
    assert result["recommended_action"] == "ACCEPT CURRENCY"
