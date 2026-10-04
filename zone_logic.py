"""Polygon zone geometry & containment logic."""

from dataclasses import dataclass
from typing import List, Dict
import json
import cv2
import numpy as np
from shapely.geometry import Polygon, Point, box as shapely_box

from detector import Detection
from config import MIN_OVERLAP_RATIO


@dataclass
class Zone:
    id: str
    name: str
    severity: str
    polygon: Polygon
    polygon_points: np.ndarray   # Nx2 int32, for cv2.fillPoly / polylines
    allowed_roles: List[str]

    def contains_point(self, pt: tuple) -> bool:
        """Fast point-in-polygon using OpenCV."""
        return cv2.pointPolygonTest(self.polygon_points, pt, False) >= 0


class ZoneManager:
    def __init__(self, zones_json_path: str):
        with open(zones_json_path, "r") as f:
            data = json.load(f)

        self.camera_id = data["camera_id"]
        self.frame_size = tuple(data.get("frame_size", [0, 0]))
        self.zones: List[Zone] = []

        for z in data["zones"]:
            pts = np.array(z["polygon"], dtype=np.int32)
            self.zones.append(
                Zone(
                    id=z["id"],
                    name=z["name"],
                    severity=z.get("severity", "medium"),
                    polygon=Polygon(z["polygon"]),
                    polygon_points=pts,
                    allowed_roles=z.get("allowed_roles", []),
                )
            )

    def get_zone(self, zone_id: str) -> Zone | None:
        return next((z for z in self.zones if z.id == zone_id), None)

    # ---------- Core containment checks ----------

    def point_in_zone(self, zone: Zone, point: tuple) -> bool:
        """Simple centroid/foot-point check."""
        return zone.contains_point(point)

    def bbox_overlap_ratio(self, zone: Zone, bbox: tuple) -> float:
        """Fraction of the person bbox area covered by the zone polygon."""
        x1, y1, x2, y2 = bbox
        if x2 <= x1 or y2 <= y1:
            return 0.0
        person_poly = shapely_box(x1, y1, x2, y2)
        if not person_poly.intersects(zone.polygon):
            return 0.0
        inter_area = person_poly.intersection(zone.polygon).area
        return inter_area / person_poly.area

    def check_detection(self, detection: Detection) -> List[Dict]:
        """
        Return a list of zone matches for one detection.
        Each match: {zone, method, ratio}
        """
        matches = []
        foot = detection.foot_point
        centroid = detection.centroid

        for zone in self.zones:
            # Method 1: foot point inside zone (most reliable for people)
            if self.point_in_zone(zone, foot):
                matches.append({"zone": zone, "method": "foot_point", "ratio": 1.0})
                continue

            # Method 2: centroid inside zone
            if self.point_in_zone(zone, centroid):
                matches.append({"zone": zone, "method": "centroid", "ratio": 1.0})
                continue

            # Method 3: bbox overlap ratio
            ratio = self.bbox_overlap_ratio(zone, detection.bbox)
            if ratio >= MIN_OVERLAP_RATIO:
                matches.append({"zone": zone, "method": "bbox_overlap", "ratio": ratio})

        return matches

    # ---------- Drawing helpers ----------

    def draw_zones(self, frame: np.ndarray, alpha: float = 0.25) -> np.ndarray:
        overlay = frame.copy()
        for z in self.zones:
            color = self._severity_color(z.severity)
            cv2.fillPoly(overlay, [z.polygon_points], color)
            cv2.polylines(frame, [z.polygon_points], True, color, 2)
            x, y = z.polygon_points[0]
            cv2.putText(
                frame, z.name, (x, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2,
            )
        return cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    @staticmethod
    def _severity_color(severity: str) -> tuple:
        return {
            "low": (0, 200, 255),
            "medium": (0, 165, 255),
            "high": (0, 0, 255),
            "critical": (0, 0, 180),
        }.get(severity, (0, 165, 255))
        