# Cloud Native DevOps Platform

A FastAPI app deployed through a full DevOps pipeline: containerized with Docker, tested and built via GitHub Actions, deployed to Kubernetes, managed with ArgoCD (GitOps), and provisioned with Terraform.

Built as a hands-on learning project to go from zero DevOps experience to a working, end-to-end pipeline.

## Architecture

```
Push to GitHub
    ↓
GitHub Actions (test → build → push image to GHCR)
    ↓
ArgoCD detects the change in Git
    ↓
Renders the Helm chart and deploys to Kubernetes
    ↓
App runs in the cluster, reachable via NodePort
```

Terraform provisions the underlying infrastructure (VPC, subnet, EC2) separately, using LocalStack to simulate AWS locally.

## Stack

- **App**: FastAPI, two endpoints (`/`, `/health`)
- **Containerization**: Docker, layer ordering set up for build caching
- **CI/CD**: GitHub Actions — pytest on every push, Docker build and push to GitHub Container Registry (GHCR) gated on tests passing
- **Orchestration**: Kubernetes (local `kind` cluster)
- **Deployment**: Helm chart, templated Deployment and Service
- **GitOps**: ArgoCD, auto-syncs the cluster to match the `fastapi-chart/` directory in this repo
- **Infrastructure as Code**: Terraform against LocalStack (VPC, subnet, EC2 instance)

## Repo structure

```
.
├── main.py                   # FastAPI app
├── test_main.py               # pytest suite
├── Dockerfile
├── .github/workflows/ci.yml   # CI/CD pipeline
├── k8s/                        # Plain Kubernetes manifests (reference)
├── fastapi-chart/              # Helm chart (active ArgoCD source)
├── terraform/                  # AWS infra via LocalStack
└── kind-config.yml              # Local cluster config with NodePort mapping
```

## Running it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Test endpoints:
```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
```

## Running the full pipeline

**1. Build and run the container**
```bash
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

**2. Spin up a local cluster**
```bash
kind create cluster --config kind-config.yml
```

**3. Deploy the Helm chart** (or point ArgoCD at `fastapi-chart/`)
```bash
helm install fastapi-release ./fastapi-chart
```

**4. Provision infrastructure with Terraform** (requires LocalStack running)
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## What this project demonstrates

- Writing and testing a REST API with automated checks that actually fail when the code breaks
- A CI/CD pipeline where deployment is gated on tests passing, not just "it builds"
- Kubernetes fundamentals: Pods, Deployments, Services, NodePort networking, and why each exists
- GitOps as a practice, not just a buzzword: the cluster's state comes from Git, and a manual `kubectl delete` gets reverted automatically
- Helm templating as an alternative to static YAML, and a clear-eyed case for when it's actually worth the overhead
- Infrastructure as Code with Terraform, including state management and how `plan`/`apply` map to real dependency graphs

## Notes

This runs on a personal Alpine Linux homelab server. `kind`'s NodePort access requires an explicit port mapping in `kind-config.yml`, since `kind`'s Docker-based nodes don't expose NodePort to the host by default. That's documented in the config file itself.

The `k8s/` folder holds the original plain-YAML manifests from before the Helm migration. They're kept as a reference for the difference between the two approaches. ArgoCD currently syncs from `fastapi-chart/`.
