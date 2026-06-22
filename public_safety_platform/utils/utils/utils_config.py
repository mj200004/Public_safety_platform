import os

# Base Directory Resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "sample_data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# File Paths
REFERENCE_IMAGE_PATH = os.path.join(DATA_DIR, "genuine_reference.jpg")
MOCK_LOGS_PATH = os.path.join(DATA_DIR, "mock_telecom_logs.csv")
AUDIT_LOG_PATH = os.path.join(REPORT_DIR, "audit_log.json")

# Computer Vision Thresholds
CV_BLUR_THRESHOLD = 50.0
CV_SIMILARITY_THRESHOLD = 0.85
CV_TARGET_IMAGE_SIZE = (600, 300) # Width, Height

# Graph Intelligence Thresholds
GRAPH_SCAMMER_OUT_DEGREE = 2
GRAPH_MULE_IN_DEGREE = 2
GRAPH_CRITICAL_RISK_SCORE = 92.5
GRAPH_BASE_RISK_SCORE = 15.0
