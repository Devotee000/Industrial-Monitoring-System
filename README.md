# Industrial-Monitoring-System
All OF YOUB INSTALL PYTHON 3.11

                         CAMERA / VIDEO
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
 ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
 │ MEMBER 1        │ │ MEMBER 2        │ │ MEMBER 3        │
 │ PPE             │ │ RESTRICTED ZONE │ │ FALL            │
 │                 │ │                 │ │                 │
 │ YOLO            │ │ Person YOLO     │ │ Pose            │
 │ Helmet          │ │ Zone Polygon    │ │ Posture         │
 │ Vest            │ │ Zone Logic      │ │ Temporal        │
 └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
          │                   │                   │
          │    PPE Event      │ Zone Event        │ Fall Event
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              │
                       ┌──────▼──────┐
                       │  MEMBER 4   │
                       │ PROXIMITY   │
                       │             │
                       │ Worker      │
                       │ Machine     │
                       │ Distance    │
                       └──────┬──────┘
                              │
                              ▼
                   ┌────────────────────┐
                   │ COMMON EVENT FORMAT│
                   └─────────┬──────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    MEMBER 5      │
                    │ SAFETY PLATFORM  │
                    │                  │
                    │ Rule Engine      │
                    │ Event Manager    │
                    │ FastAPI          │
                    │ Database         │
                    │ Dashboard        │
                    └────────┬─────────┘
                             │
                 ┌───────────┼───────────┐
                 ▼           ▼           ▼
              ALERTS      DATABASE    DASHBOARD


Kedar - Fall Module
Yukta - Proximity Module
Shreeyash - PPE Module
Shaunak - Restricted Zone module
Varad - Safety Platform
