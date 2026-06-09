# Awesome JEPA

> A curated collection of resources, papers, models, and code for **JEPA** — Joint Embedding Predictive Architectures, world models, and self-supervised predictive learning.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

---

## Contents

- [What is JEPA?](#what-is-jepa)
- [Papers](#papers)
- [Models & Weights](#models--weights)
- [Code & Frameworks](#code--frameworks)
- [Related Work & World Models](#related-work--world-models)
- [Benchmarks & Datasets](#benchmarks--datasets)
- [Blog Posts & Articles](#blog-posts--articles)

---

## What is JEPA?

**JEPA** (Joint Embedding Predictive Architecture) is a family of self-supervised learning architectures introduced by Yann LeCun and FAIR. Unlike generative models that reconstruct inputs in pixel or token space, JEPA learns predictive world models in a **latent representation space**. The core idea: predict the representation of an input from the representation of a context — without ever decoding back to the observation space.

This makes JEPA particularly well-suited for:
- **World models** in autonomous agents and robotics
- **Self-supervised pretraining** on video and sensory streams
- **Scalable representation learning** without generative decoding bottlenecks

---

## Papers

### Foundational

| Paper | Year | Authors | Links |
|-------|------|---------|-------|
| **Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture** | 2023 | Assran et al. (FAIR) | [arXiv](https://arxiv.org/abs/2301.08243) · [GitHub](https://github.com/facebookresearch/ijepa) |
| **Revisiting Feature Prediction for Learning Visual Representations from Video** (V-JEPA 2) | 2024 | Bardes et al. (FAIR) | [arXiv](https://arxiv.org/abs/2301.08243) · [GitHub](https://github.com/facebookresearch/vjepa2) |

### Extensions & Variants

| Paper | Year | Authors | Links |
|-------|------|---------|-------|
| **LeJEPA: A Leap in World Models via Joint Embedding Predictive Architectures** | 2025 | GalilAI Group | [arXiv](https://arxiv.org/abs/2511.08544) · [GitHub](https://github.com/galilai-group/lejepa) |
| **EchoJEPA: Joint Embedding Predictive Architecture for Echocardiogram Video Understanding** | 2026 | Wang Lab (UHN) | [arXiv](https://arxiv.org/abs/2602.02603) · [GitHub](https://github.com/bowang-lab/EchoJEPA) |
| **BioFoundation: A Foundation Model for Biosignals** | 2026 | PULP-Bio | [arXiv](https://arxiv.org/abs/2603.19100) · [GitHub](https://github.com/pulp-bio/biofoundation) |

---

## Models & Weights

| Model | Description | Weights |
|-------|-------------|---------|
| **I-JEPA** | Image-based JEPA pretrained on ImageNet | [Hugging Face](https://huggingface.co/facebook/ijepa_vith14_1k) |
| **V-JEPA 2** | Video JEPA for self-supervised video representation learning | [Hugging Face](https://huggingface.co/facebook/vjepa_vitl14_k400) |
| **LeJEPA** | Leap in world models via JEPA | [Hugging Face](https://huggingface.co/galilai/lejepa) |
| **EchoJEPA** | JEPA for echocardiogram video understanding | [Hugging Face](https://huggingface.co/bowang-lab/EchoJEPA) |
| **BioFoundation** | Foundation model for biosignals (EEG, ECG, etc.) | [Hugging Face](https://huggingface.co/pulp-bio/biofoundation) |

---

## Code & Frameworks

| Repository | Description | Language |
|------------|-------------|----------|
| [facebookresearch/ijepa](https://github.com/facebookresearch/ijepa) | Official I-JEPA implementation (images) | Python / PyTorch |
| [facebookresearch/vjepa2](https://github.com/facebookresearch/vjepa2) | Official V-JEPA 2 implementation (video) | Python / PyTorch |
| [galilai-group/lejepa](https://github.com/galilai-group/lejepa) | LeJEPA: Leap in world models | Python / PyTorch |
| [bowang-lab/EchoJEPA](https://github.com/bowang-lab/EchoJEPA) | JEPA for echocardiogram video understanding | Python / PyTorch |
| [pulp-bio/biofoundation](https://github.com/pulp-bio/biofoundation) | Foundation model for biosignals | Python / PyTorch |

---

## Related Work & World Models

| Repository | Description | Paper / Link |
|------------|-------------|--------------|
| [lucas-maes/le-wm](https://github.com/lucas-maes/le-wm) | Latent Exploration World Models — exploration-driven world model learning | [GitHub](https://github.com/lucas-maes/le-wm) |
| [galilai-group/stable-worldmodel](https://github.com/galilai-group/stable-worldmodel) | Stable World Models by GalilAI Group | [GitHub](https://github.com/galilai-group/stable-worldmodel) |
| [BADA'S](https://badas.nexar.app/) | Benchmark for Autonomous Driving Agents — evaluation platform for world models in autonomous driving | [Website](https://badas.nexar.app/) |

---

## Benchmarks & Datasets

| Benchmark | Description | Link |
|-----------|-------------|------|
| **BADA'S** | Benchmark for Autonomous Driving Agents — world model evaluation in driving scenarios | [badas.nexar.app](https://badas.nexar.app/) |
| **ImageNet-1K** | Standard pretraining dataset for I-JEPA | [image-net.org](https://www.image-net.org/) |
| **Kinetics-400** | Video pretraining dataset for V-JEPA | [deepmind.com/kinetics](https://deepmind.google/discover/open-source/kinetics/) |
| **EchoNet-Dynamic** | Echocardiogram video dataset for EchoJEPA | [echonet.github.io/dynamic](https://echonet.github.io/dynamic/) |

---

## Blog Posts & Articles

- [Yann LeCun's Vision for Autonomous Machine Intelligence](https://openreview.net/forum?id=BZ5a1r-kVsf) — The original JEPA manifesto (2022)
- [Meta AI: Teaching AI to see, hear, and learn from video with V-JEPA](https://ai.meta.com/blog/v-jepa-video-joint-embedding-predictive-architecture/) — Meta AI blog on V-JEPA (2024)

---

## Contributing

Contributions welcome! Please open a PR to add papers, models, code, or resources. Follow the existing format and ensure all entries include links to papers and code when available.

---

## License

This list is released under [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
