from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.counterfeit_detector import analyze_currency_note
from backend.fraud_graph import build_and_analyze_threat_network
from utils.audit_logger import log_decision

app = FastAPI(
    title="Digital Public Safety API",
    description="Proactive intelligence layer for counterfeit detection and fraud mapping."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "operational"}

@app.post("/api/v1/analyze-currency")
async def process_currency(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file payload provided.")
    try:
        contents = await file.read()
        intelligence_payload = analyze_currency_note(contents)
        # Log to immutable trail
        intelligence_payload["audit_id"] = log_decision("Counterfeit_CV_Engine", file.filename, intelligence_payload)
        return intelligence_payload
    except FileNotFoundError as fnf_err:
        raise HTTPException(status_code=500, detail=str(fnf_err))
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during forensic analysis.")

@app.get("/api/v1/analyze-fraud-network")
async def process_fraud_network():
    try:
        intelligence_payload = build_and_analyze_threat_network()
        if "error" in intelligence_payload:
            raise HTTPException(status_code=404, detail=intelligence_payload["error"])
        # Log to immutable trail
        intelligence_payload["audit_id"] = log_decision("Graph_Intelligence_Engine", "system_telecom_logs", intelligence_payload)
        return intelligence_payload
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during graph formulation.")
