# LLM Inference Performance Analysis: Batching vs. Parallelism on Single GPU

## Overview

This project analyzes the performance characteristics of Large Language Model (LLM) inference on a single NVIDIA L4 GPU using different deployment strategies. The analysis compares three distinct approaches: single-pod batching, dual-pod parallelism with MPS (Multi-Process Service), and triple-pod parallelism with MPS.

## Architecture Scenarios

| Scenario | GPU Allocation | Pods | MPS Enabled | Strategy | Use Case |
|----------|----------------|------|-------------|----------|----------|
| **Scenario 1** | 100% GPU | 1 | No | Batching | Low-latency, high-throughput |
| **Scenario 2** | ~45% GPU per pod | 2 | Yes | Parallelism | Balanced concurrency |
| **Scenario 3** | ~30% GPU per pod | 3 | Yes | Parallelism | High concurrency |

## Performance Results

### Latency & Throughput Summary

| Metric | Single Pod (Batching) | Dual Pods (MPS) | Triple Pods (MPS) |
|--------|----------------------|-----------------|-------------------|
| **Requests Processed** | 2,696 | 2,308 | 1,863 |
| **Median Latency** | **2,200ms** | 2,500ms | 3,100ms |
| **95th Percentile** | **2,200ms** | 2,600ms | 3,200ms |
| **99th Percentile** | **2,600ms** | 2,800ms | 3,400ms |
| **Average Latency** | **2,176.61ms** | 2,524.07ms | 3,124.51ms |
| **Max Latency** | 4,456ms | 6,482ms | **6,192ms** |
| **Throughput (RPS)** | **23.6** | 20 | 16 |
| **Failures** | 0 | 0 | 0 |

### Key Performance Insights

#### **Winner: Single Pod with Batching**
- **Best overall performance** across all metrics
- **23.6 RPS** throughput (18% better than dual pods)
- **Lowest latency** at all percentiles
- **Zero failures** with optimal resource utilization

#### **Runner-up: Dual Pods with MPS**
- **Reasonable trade-off** for scenarios requiring isolation
- **20 RPS** throughput (15% reduction from single pod)
- **Acceptable latency** increase (~15% higher)
- **Good for** multi-tenant or fault-isolation requirements

#### **Not Recommended: Triple Pods with MPS**
- **Significant performance degradation** (32% lower throughput)
- **High latency** increase (43% higher than single pod)
- **Resource contention** outweighs parallelism benefits

## Infrastructure Setup

This project includes Kubernetes manifests and setup commands for GKE deployment:

- `vllm-single-pod.yaml` - Single pod configuration
- `vllm-mps-dual-pods.yaml` - Dual pods with MPS
- `vllm-mps-triple-pods.yaml` - Triple pods with MPS
- `commands.md` - GKE cluster setup instructions

### Quick Start

1. **Create GKE cluster** with GPU node pool
2. **Deploy HuggingFace token secret**
3. **Apply desired pod configuration**
4. **Run load testing** with 50 concurrent users
5. **Monitor performance metrics**

## Methodology

### Test Configuration
- **Model**: Gemma-3-1B-IT
- **GPU**: NVIDIA L4 (single)
- **Load**: 50 concurrent users
- **Ramp up users/sec**: 10
- **Duration**: Sustained load testing for 2 minutes for each scenario
- **Output Limit**: 100 max_tokens per request
- **Metrics**: Latency percentiles, throughput, failures

### Tools Used
- **vLLM** for inference serving
- **Kubernetes** for orchestration
- **GKE** for managed cluster
- **Locust** for performance measurement

## Conclusion

**Batching in a single pod significantly outperforms parallel pod deployments** for LLM inference on single GPU setups. The 18% throughput improvement and 15% latency reduction make it the clear choice for most production workloads.

This analysis provides a data-driven foundation for making informed architectural decisions in LLM deployment scenarios.
