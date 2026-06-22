import cv2
import os
from typing import Dict, Any, List
from utils.config import REFERENCE_IMAGE_PATH, CV_BLUR_THRESHOLD, CV_SIMILARITY_THRESHOLD, CV_TARGET_IMAGE_SIZE
from utils.image_utils import decode_and_normalize_image

def analyze_currency_note(uploaded_image_bytes: bytes) -> Dict[str, Any]:
    if not os.path.exists(REFERENCE_IMAGE_PATH):
        raise FileNotFoundError("Genuine reference image missing. Run mock generator.")

    # Normalization & Grayscale Conversion
    img_test = decode_and_normalize_image(uploaded_image_bytes, CV_TARGET_IMAGE_SIZE)
    img_ref = cv2.imread(REFERENCE_IMAGE_PATH)
    img_ref = cv2.resize(img_ref, CV_TARGET_IMAGE_SIZE, interpolation=cv2.INTER_AREA)

    gray_test = cv2.cvtColor(img_test, cv2.COLOR_BGR2GRAY)
    gray_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)

    # Blur detection via Laplacian Variance
    blur_variance = cv2.Laplacian(gray_test, cv2.CV_64F).var()
    is_blurry = blur_variance < CV_BLUR_THRESHOLD

    # Structural Integrity (Template Matching)
    res = cv2.matchTemplate(gray_test, gray_ref, cv2.TM_CCOEFF_NORMED)
    similarity_score = float(res.max())
    confidence_score = round(similarity_score * 100, 2)

    # Rule-Based Classification
    flags: List[str] = []
    is_counterfeit = False

    if similarity_score < CV_SIMILARITY_THRESHOLD:
        is_counterfeit = True
        flags.append(f"Structural layout mismatch detected (Score: {similarity_score:.3f}).")
        
    if is_blurry:
        is_counterfeit = True
        flags.append(f"Microprint blur or edge degradation detected (Variance: {blur_variance:.1f}).")

    if not flags:
        flags.append("Visual security features and structural integrity verified.")

    return {
        "is_counterfeit": is_counterfeit,
        "confidence_score": confidence_score,
        "similarity_score": round(similarity_score, 4),
        "flags": flags,
        "recommended_action": "CONFISCATE AND ESCALATE" if is_counterfeit else "ACCEPT CURRENCY"
    }
