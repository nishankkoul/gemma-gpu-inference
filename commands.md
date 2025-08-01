# GKE Cluster Setup Commands for Gemma-3-1B-IT GPU Inference

## Common Cluster Creation
```bash
gcloud container clusters create gemma-inference-cluster \
  --project=<project-id> \
  --zone=us-west1-a \
  --workload-pool=<project-id>.svc.id.goog \
  --release-channel=rapid \
  --num-nodes=1 \
  --disk-size=100
```

## Common Authentication and Secret Setup
```bash
gcloud container clusters get-credentials gemma-inference-cluster \
  --zone us-west1-a \
  --project <project-id>

kubectl create secret generic hf-secret \
  --from-literal=hf_api_token=<your-hf-token>
```

## Scenario 1: Single GPU
```bash
gcloud container node-pools create gpupool \
  --accelerator type=nvidia-l4,count=1,gpu-driver-version=latest \
  --project=<project-id> \
  --zone=us-west1-a \
  --cluster=gemma-inference-cluster \
  --machine-type=g2-standard-16 \
  --num-nodes=1

kubectl apply -f vllm-single-pod.yaml
```

## Scenario 2: Dual Pods with MPS (2 clients per GPU)
```bash
gcloud container node-pools create gpupool \
  --accelerator type=nvidia-l4,count=1,gpu-sharing-strategy=mps,max-shared-clients-per-gpu=2,gpu-driver-version=latest \
  --project=<project-id> \
  --zone=us-west1-a \
  --cluster=gemma-inference-cluster \
  --machine-type=g2-standard-16 \
  --num-nodes=1

kubectl apply -f vllm-mps-dual-pods.yaml
```

## Scenario 3: Triple Pods with MPS (3 clients per GPU)
```bash
gcloud container node-pools create gpupool \
  --accelerator type=nvidia-l4,count=1,gpu-sharing-strategy=mps,max-shared-clients-per-gpu=3,gpu-driver-version=latest \
  --project=<project-id> \
  --zone=us-west1-a \
  --cluster=gemma-inference-cluster \
  --machine-type=g2-standard-16 \
  --num-nodes=1

kubectl apply -f vllm-mps-triple-pods.yaml
```

## Cleanup
```bash
kubectl delete -f vllm-single-pod.yaml
# or
kubectl delete -f vllm-mps-dual-pods.yaml
# or
kubectl delete -f vllm-mps-triple-pods.yaml

gcloud container clusters delete gemma-inference-cluster \
  --zone=us-west1-a \
  --<project-id>
```
