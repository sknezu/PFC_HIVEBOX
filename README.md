# PFC_HIVEBOX

PFC practical project based on [devopsroadmap.io](https://devopsroadmap.io/projects/hivebox/) Hivebox learning project.

[![Dynamic DevOps Roadmap](https://devopshive.net/badges/dynamic-devops-roadmap.svg)](https://github.com/DevOpsHiveHQ/dynamic-devops-roadmap)

This project is divided into **2 phases**:

## Phase 1

Phase 1 relies on a **Python Flask app** that returns values from a **single sensor** ([5eba5fbad46fb8001b799786](https://opensensemap.org/explore/5eba5fbad46fb8001b799786)) to retrieve **temperature data**. Deploying it inside a **Kubernetes cluster**, this data will be gathered by **Prometheus** and shown in **Grafana** with a **Dashboard**, alongside the **Kubernetes cluster status**.

### Phase 1 Checklist:
- [x] Python Flask Application
- [x] Kubernetes Cluster
- [x] Prometheus & Grafana basic configuration inside K8s
- [x] Nginx as frontend (website) and/or data source (ingress)
- [x] Python to Prometheus data gathering

## Phase 2

Phase 2 will be further developed as Phase 1 evolves. This will include additional features and improvements as the project grows.

---

## Installation and Setup

### Prerequisites
- Python 3.x
- Flask
- Kubernetes Cluster
- Prometheus and Grafana
- Nginx


