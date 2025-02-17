# PFC_HIVEBOX

PFC practical project based on [devopsroadmap.io](https://devopsroadmap.io/projects/hivebox/) Hivebox learning project.

[![Dynamic DevOps Roadmap](https://devopshive.net/badges/dynamic-devops-roadmap.svg)](https://github.com/DevOpsHiveHQ/dynamic-devops-roadmap)

This project is divided into **2 phases**:

## Phase 1 (Dec - Feb 2025)

Phase 1 relies on a **Python Flask app** that returns values from a **single sensor** ([5eba5fbad46fb8001b799786](https://opensensemap.org/explore/5eba5fbad46fb8001b799786)) to retrieve **temperature data**. Phase 1 ended up with a basic test in kind where the app Dockerfile was used inside a kubernetes pod.

### Phase 1 Checklist:
- &#9745; Python Flask Application
- &#9745; Kubernetes Pod (basic test)


## Phase 2 (Apr - June 2025)

Phase 2 includes **three sensors close to each other**:
 > **Hotzelsroda**: ([5b267cac1fef04001b78f88b](https://opensensemap.org/explore/5b267cac1fef04001b78f88b)) 
 
 > **EA Wartenberg**: ([5d13ec6630bde6001a618df5](https://opensensemap.org/explore/5d13ec6630bde6001a618df5)) 

 > **Gerstungen**: ([5d0fc7fd30bde6001a364a79](https://opensensemap.org/explore/5d0fc7fd30bde6001a364a79))

These sensors will retrieve the original **temperature data** (/temperature) and  **version of the app** (/version), along with  **prometheus metrics** (/metrics) and  **stored time of data** (/store) and, if time allows  **readyness of data** (/readyz).

During this Phase, I aim to follow the steps of the original project up to the Phase 5. This means that I'll need:

### Phase 2 Checklist:
- &#9744; Update Python Flask Application (iteration)
- &#9744; Kubernetes Kind config with Ingress-Nginx + Manifests to deploy
- &#9744; Caching and Storage layers (Valkey + MinIO)
- &#9744; SSL Encryptation and FreeDNS, connect to the cluster
- &#9744; Deploy Grafana to collect logs and metrics, move to cluster

### Extras:
- Kyverno for Policy as Code
- Terraform for multi-environment (Dev, Stage, Prod)
- TestKube for testing
- Kubernetes Operator to handle app operations


