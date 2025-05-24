# PFC_HIVEBOX

PFC practical project based on [devopsroadmap.io](https://devopsroadmap.io/projects/hivebox/) Hivebox learning project.

[![Dynamic DevOps Roadmap](https://devopshive.net/badges/dynamic-devops-roadmap.svg)](https://github.com/DevOpsHiveHQ/dynamic-devops-roadmap)

This project is divided into **2 phases**:

## Phase 1 (Dec - Feb 2025)

Phase 1 relies on a **Python Flask app** that returns values from a **single sensor** (**Groß Glienicke**: [5eba5fbad46fb8001b799786](https://opensensemap.org/explore/5eba5fbad46fb8001b799786)) to retrieve **temperature data**. Phase 1 ended up with a basic test in kind where the app Dockerfile was used inside a kubernetes pod. It is kept in the repository for potential scalability and deployment in K8s.

### Phase 1 Checklist:
- &#9745; Python Flask Application
- &#9745; Kubernetes Pod (basic test)


## Phase 2 (Apr - June 2025)

Phase 2 includes **three sensors close to each other**:
 > **Hotzelsroda**: ([5b267cac1fef04001b78f88b](https://opensensemap.org/explore/5b267cac1fef04001b78f88b)) 
 
 > **EA Wartenberg**: ([5d13ec6630bde6001a618df5](https://opensensemap.org/explore/5d13ec6630bde6001a618df5)) 

 > **Gerstungen**: ([5d0fc7fd30bde6001a364a79](https://opensensemap.org/explore/5d0fc7fd30bde6001a364a79))

These sensors will retrieve the original **temperature data** (/temperature) and  **version of the app** (/version), along with **prometheus metrics** (/metrics).

During this Phase, the objective is to retrieve the metrics from the **Python Flask app** using **Prometheus** to then feed them into a **Grafana Dashboard**. Then, create a front-end website embeded into the app with **bootsrap** to enable user friendly UI and access to both the Prometheus raw metrics and the Dashboard. I decided to leave the Grafana access and credentials to showcase better this project during my presentation, but it could be simplified to simply redirect to the Dashboard.

### Phase 2 Checklist:
- &#9745; Update Python Flask Application with a Bootstrap Website
- &#9745; Connect Prometheus to the Flask app & Grafana
- &#9745; Add Nginx as reverse proxy
- &#9744; Iterate

### Extras:
- Create a Kubernetes cluster for the App
- Kyverno for Policy as Code
- Terraform for multi-environment (Dev, Stage, Prod)
- TestKube for testing
- Kubernetes Operator to handle app operations


