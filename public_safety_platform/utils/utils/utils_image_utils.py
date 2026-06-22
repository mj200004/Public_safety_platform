import cv2
import numpy as np
from typing import Tuple

def decode_and_normalize_image(image_bytes: bytes, target_shape: Tuple[int, int]) -> np.ndarray:
    """Decodes raw bytes into an OpenCV matrix and normalizes dimensions."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Image decoding failed. The file is corrupted or unsupported.")
    
    # Defensive resizing to guarantee matrix dimension alignment
    normalized_img = cv2.resize(img, target_shape, interpolation=cv2.INTER_AREA)
    return normalized_img
