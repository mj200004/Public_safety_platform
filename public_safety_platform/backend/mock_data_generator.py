import os
import sys
import pandas as pd
import numpy as np
import cv2

# Adjust path for direct script execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import DATA_DIR, MOCK_LOGS_PATH, REFERENCE_IMAGE_PATH, CV_TARGET_IMAGE_SIZE

def generate_telecom_logs():
    data = {
        "event_id": [f"EVT_{str(i).zfill(4)}" for i in range(1, 9)],
        "source_entity": ["+91_SPOOF_881", "+91_SPOOF_881", "Victim_A", "+91_SPOOF_881", "Victim_B", "+91_SPOOF_992", "Victim_C", "Victim_A"],
        "target_entity": ["Victim_A", "Victim_B", "Mule_Acct_XYZ_998", "Victim_C", "Mule_Acct_XYZ_998", "Victim_C", "Mule_Acct_ABC_112", "Mule_Acct_ABC_112"],
        "interaction_type": ["Video Call (Threat)", "Voice Call", "IMPS Transfer", "Video Call", "NEFT Transfer", "Voice Call", "UPI Transfer", "RTGS Transfer"],
        "duration_or_amount": ["145 mins", "80 mins", "Rs 5,00,000", "200 mins", "Rs 2,50,000", "15 mins", "Rs 1,00,000", "Rs 8,00,000"]
    }
    pd.DataFrame(data).to_csv(MOCK_LOGS_PATH, index=False)

def generate_reference_note():
    width, height = CV_TARGET_IMAGE_SIZE
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (190, 210, 190)
    cv2.putText(img, "500", (40, 80), cv2.FONT_HERSHEY_DUPLEX, 2.5, (0, 80, 0), 4)
    cv2.putText(img, "RESERVE BANK OF INDIA", (40, 160), cv2.FONT_HERSHEY_COMPLEX, 0.8, (20, 20, 20), 2)
    cv2.line(img, (int(width * 0.7), 0), (int(width * 0.7), height), (120, 150, 120), 12)
    cv2.imwrite(REFERENCE_IMAGE_PATH, img)

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    generate_telecom_logs()
    generate_reference_note()
    print("Mock data provisioned successfully. You can now start the server.")
