"""Builds the Common Event Format event object."""

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from config import CAMERA_ID, MODULE_NAME


def build_zone_event(
    zone_id: str,
    zone_name: str,
    severity: str,
    detection_bbox: tuple,
    confidence: float,
    track_id: int,
    method: str,
    overlap_ratio: float,
    dwell_time: float,
) -> dict:
    """Returns a dict conforming to the common event schema."""
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "camera_id": CAMERA_ID,
        "module": MODULE_NAME,
        "event_type": "restricted_zone_intrusion",
        "severity": severity,
        "type": "violation",
        "bbox": list(detection_bbox),
        "confidence": round(confidence, 3),
        "track_id": track_id,
        "zone": {
            "id": zone_id,
            "name": zone_name,
        },
        "meta": {
            "detection_method": method,
            "overlap_ratio": round(overlap_ratio, 3),
            "dwell_time_sec": round(dwell_time, 2),
        },
    }