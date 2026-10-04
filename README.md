cat > README.md << 'EOF'
# 🚧 Restricted Zone Detection Module

> Part of the **Industrial Monitoring System** 
> Detects when a person enters a predefined restricted polygon zone in real time.

---

## 📌 Overview

This module watches a camera/video feed, detects people using **YOLOv8**, and checks whether they enter any of the **user-defined polygon zones** (e.g., machine areas, electrical rooms, hazardous floors). When a person stays inside a zone longer than a configurable **dwell time**, it emits a **violation event** in the Common Event Format consumed by the Safety Platform (Member 5).

---

## ✨ Features

- 🎯 **YOLOv8 person detection** with multi-object tracking
- 🟦 **Multiple polygon zones** defined in a simple JSON file
- 🧠 **3-tier containment logic** — foot point → centroid → bbox overlap
- ⏱️ **Dwell-time based alerts** (avoids false positives from passers-by)
- 🔔 **One-shot alerting per person per zone** (no event spam)
- 🎨 **Live visualization** — zones drawn with severity colors, tracked people highlighted
- 📄 **Common Event Format** output as line-delimited JSON (`.jsonl`)
- 🧩 **Plug-and-play** with Kafka / Redis / MQTT / FastAPI
- 🛠️ **Zone picker utility** to click-draw polygons on a frame

---

## 📁 Project Structure
