"""Restricted Zone — main pipeline."""

import json
import time
from collections import defaultdict

import cv2

from config import VIDEO_SOURCE, EVENT_LOG_FILE, DWELL_TIME_SEC
from detector import PersonDetector
from zone_logic import ZoneManager
from event_builder import build_zone_event


class RestrictedZonePipeline:
    def __init__(self, zones_path: str = "zones.json"):
        self.detector = PersonDetector()
        self.zone_mgr = ZoneManager(zones_path)

        # track_id -> zone_id -> first_seen_ts
        self.entry_time = defaultdict(dict)
        # track_id -> zone_id -> already alerted
        self.alerted = defaultdict(set)

        self.event_log = open(EVENT_LOG_FILE, "a", buffering=1)  # line-buffered

    # ---------- event emission ----------
    def _emit(self, event: dict):
        self.event_log.write(json.dumps(event) + "\n")
        # ── In production: also push to Redis / MQTT / FastAPI here ──
        print(f"[EVENT] {event['severity'].upper()} | "
              f"zone={event['zone']['name']} | "
              f"track={event['track_id']} | "
              f"dwell={event['meta']['dwell_time_sec']}s")

    # ---------- main loop ----------
    def run(self):
        cap = cv2.VideoCapture(VIDEO_SOURCE)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open video source: {VIDEO_SOURCE}")

        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                frame = self.zone_mgr.draw_zones(frame)
                detections = self.detector.detect(frame, use_tracking=True)

                now = time.time()
                active_tracks = set()

                for det in detections:
                    tid = det.track_id if det.track_id != -1 else -1
                    active_tracks.add(tid)

                    matches = self.zone_mgr.check_detection(det)

                    for m in matches:
                        zone = m["zone"]
                        key = (tid, zone.id)

                        # first time we see this person in this zone
                        if tid not in self.entry_time or zone.id not in self.entry_time[tid]:
                            self.entry_time[tid][zone.id] = now

                        dwell = now - self.entry_time[tid][zone.id]

                        # draw bbox
                        x1, y1, x2, y2 = det.bbox
                        color = (0, 0, 255) if dwell >= DWELL_TIME_SEC else (0, 255, 255)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(
                            frame, f"ID {tid} | {dwell:.1f}s",
                            (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,
                        )

                        # raise violation once dwell threshold is passed
                        if dwell >= DWELL_TIME_SEC and zone.id not in self.alerted[tid]:
                            self.alerted[tid].add(zone.id)
                            event = build_zone_event(
                                zone_id=zone.id,
                                zone_name=zone.name,
                                severity=zone.severity,
                                detection_bbox=det.bbox,
                                confidence=det.confidence,
                                track_id=tid,
                                method=m["method"],
                                overlap_ratio=m["ratio"],
                                dwell_time=dwell,
                            )
                            self._emit(event)

                # clear tracks that disappeared (so we can re-alert next time)
                gone = set(self.entry_time.keys()) - active_tracks
                for tid in gone:
                    self.entry_time.pop(tid, None)
                    self.alerted.pop(tid, None)

                cv2.imshow("Restricted Zone Monitor", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.event_log.close()


if __name__ == "__main__":
    RestrictedZonePipeline("zones.json").run()