"""Global configuration for the Restricted Zone module."""

YOLO_MODEL = "yolov8n.pt"         
PERSON_CLASS_ID = 0               
CONF_THRESHOLD = 0.4
IOU_THRESHOLD = 0.5


VIDEO_SOURCE = 0

# Zone rules
# How long (seconds) a person must be inside before raising a violation
DWELL_TIME_SEC = 1.0

# Minimum fraction of the person's bbox that must overlap the zone
# 0.0 = any touch, 1.0 = fully inside
MIN_OVERLAP_RATIO = 0.15

# Event output
EVENT_LOG_FILE = "zone_events.jsonl"
CAMERA_ID = "cam_01"
MODULE_NAME = "restricted_zone"