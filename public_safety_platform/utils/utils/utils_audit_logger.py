import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any
from utils.config import REPORT_DIR, AUDIT_LOG_PATH

def log_decision(module_name: str, input_reference: str, outcome: Dict[str, Any]) -> str:
    """Securely appends system decisions to a JSON-lines audit trail."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    audit_id = f"AUDIT-{uuid.uuid4().hex[:10].upper()}"
    
    audit_entry = {
        "audit_id": audit_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "module": module_name,
        "input_reference": input_reference,
        "outcome": outcome
    }
    
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as file:
        file.write(json.dumps(audit_entry) + "\n")
        
    return audit_id
