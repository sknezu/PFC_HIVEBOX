# PFC_HIVEBOX
PFC practical project based on [devopsroadmap.io](https://devopsroadmap.io/projects/hivebox/) Hivebox learning project.

[![Dynamic DevOps Roadmap](https://devopshive.net/badges/dynamic-devops-roadmap.svg)](https://github.com/DevOpsHiveHQ/dynamic-devops-roadmap)

This project is divided in 2 phases:
    > Phase 1 relies on a python flask app that returns values of 1 sensor [5eba5fbad46fb8001b799786](https://opensensemap.org/explore/5eba5fbad46fb8001b799786) to retrieve temperature data. Deploying inside a kubernetes cluster, this data will be gathered by Prometheus and shown into Grafana in a Dashboard, along with the kubernetes cluster status.
        CHECKLIST:
        - Python App
        - Kubernetes Cluster
        - Prometheus & Grafana basic configuration inside K8s
        - Nginx as frontend (website) and/or data source (ingress)
        - Python to Prometheus data gathering

    > Phase 2 will be further developed as Phase 1 evolves.

