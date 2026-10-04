"""Person detection using YOLO."""

from dataclasses import dataclass
from typing import List
import numpy as np
from ultralytics import YOLO

from config import YOLO_MODEL, PERSON_CLASS_ID, CONF_THRESHOLD, IOU_THRESHOLD


@dataclass
class Detection:
    bbox: tuple          # (x1, y1, x2, y2) in pixels
    confidence: float
    class_id: int
    track_id: int = -1   # filled if tracking is enabled

    @property
    def centroid(self) -> tuple:
        x1, y1, x2, y2 = self.bbox
        return (int((x1 + x2) / 2), int((y1 + y2) / 2))

    @property
    def foot_point(self) -> tuple:
        """Bottom-center — best anchor for 'person standing in zone'."""
        x1, y1, x2, y2 = self.bbox
        return (int((x1 + x2) / 2), int(y2))


class PersonDetector:
    def __init__(self, model_path: str = YOLO_MODEL):
        self.model = YOLO(model_path)

    def detect(self, frame: np.ndarray, use_tracking: bool = False) -> List[Detection]:
        if use_tracking:
            results = self.model.track(
                frame,
                persist=True,
                classes=[PERSON_CLASS_ID],
                conf=CONF_THRESHOLD,
                iou=IOU_THRESHOLD,
                verbose=False,
            )
        else:
            results = self.model.predict(
                frame,
                classes=[PERSON_CLASS_ID],
                conf=CONF_THRESHOLD,
                iou=IOU_THRESHOLD,
                verbose=False,
            )

        detections: List[Detection] = []
        for r in results:
            if r.boxes is None:
                continue
            boxes = r.boxes.xyxy.cpu().numpy()
            confs = r.boxes.conf.cpu().numpy()
            ids = (
                r.boxes.id.cpu().numpy().astype(int)
                if r.boxes.id is not None
                else np.full(len(boxes), -1)
            )
            for bbox, conf, tid in zip(boxes, confs, ids):
                detections.append(
                    Detection(
                        bbox=tuple(map(int, bbox)),
                        confidence=float(conf),
                        class_id=PERSON_CLASS_ID,
                        track_id=int(tid),
                    )
                )
        return detections