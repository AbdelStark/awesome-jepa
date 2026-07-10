# Awesome JEPA [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of papers, models, code, datasets, and learning resources for Joint Embedding Predictive Architectures (JEPA), the self-supervised approach to world models proposed by Yann LeCun.

JEPA learns by predicting representations rather than reconstructing pixels or tokens. This page collects the canonical work from Meta FAIR alongside the wider research that has grown around it. Every link was checked and every attribution verified against primary sources in June 2026.

## Contents

- [What is JEPA?](#what-is-jepa)
- [Foundations](#foundations)
- [Core Architectures](#core-architectures)
- [Theory, Analysis, and Recipes](#theory-analysis-and-recipes)
- [Variants by Domain](#variants-by-domain)
  - [Audio and Speech](#audio-and-speech)
  - [3D and Point Clouds](#3d-and-point-clouds)
  - [Graphs and Molecules](#graphs-and-molecules)
  - [Time Series and Tabular Data](#time-series-and-tabular-data)
  - [Medical Imaging and Biosignals](#medical-imaging-and-biosignals)
  - [Earth Observation and Remote Sensing](#earth-observation-and-remote-sensing)
  - [Language and Recommendation](#language-and-recommendation)
  - [Generative Modeling](#generative-modeling)
- [World Models, Robotics, and Planning](#world-models-robotics-and-planning)
- [Models and Weights](#models-and-weights)
- [Code and Frameworks](#code-and-frameworks)
- [Datasets](#datasets)
- [Benchmarks](#benchmarks)
- [Talks and Lectures](#talks-and-lectures)
- [Courses](#courses)
- [Articles and Explainers](#articles-and-explainers)
- [Contributing](#contributing)
- [License](#license)

## What is JEPA?

A Joint Embedding Predictive Architecture predicts the representation of a target signal from the representation of a context signal, entirely in an abstract latent space. Where generative models reconstruct every pixel or token, a JEPA predicts features, so it can discard unpredictable detail and keep the structure that matters for understanding, reasoning, and planning.

A JEPA has three parts: a context encoder, a target encoder, and a predictor that maps context embeddings to predicted target embeddings. Predicting in embedding space admits a trivial solution where everything collapses to a constant, so JEPAs use an asymmetry to prevent this, such as a stop-gradient target encoder updated as an exponential moving average, or an explicit variance and covariance penalty.

This design is the centerpiece of LeCun's proposal for autonomous machine intelligence, where an agent learns a predictive world model in representation space and plans by searching for actions that lead to desired predicted states. The family began with images (I-JEPA) and video (V-JEPA, V-JEPA 2) and now reaches audio, point clouds, graphs, time series, and many scientific domains.

## Foundations

- **[A Path Towards Autonomous Machine Intelligence](https://openreview.net/forum?id=BZ5a1r-kVsf)** (Yann LeCun, 2022). The position paper that introduced the JEPA concept and a blueprint for world-model-driven autonomous agents. [pdf](https://openreview.net/pdf?id=BZ5a1r-kVsf)
- **[Introduction to Latent Variable Energy-Based Models](https://arxiv.org/abs/2306.02572)** (Anna Dawid and Yann LeCun, 2023). A tutorial connecting energy-based models to the autonomous-intelligence proposal that motivates JEPA.

## Core Architectures

The canonical JEPA line from Meta FAIR.

- **[I-JEPA: Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2301.08243)** (Mahmoud Assran et al., CVPR 2023). The first image JEPA, predicting representations of target image blocks from a single context block without hand-crafted augmentations. [code](https://github.com/facebookresearch/ijepa) · [models](https://huggingface.co/models?search=facebook/ijepa) · [blog](https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/)
- **[V-JEPA: Revisiting Feature Prediction for Learning Visual Representations from Video](https://arxiv.org/abs/2404.08471)** (Adrien Bardes et al., ICLR 2025). Learns video representations purely by predicting masked spatiotemporal features in latent space. [code](https://github.com/facebookresearch/jepa) · [blog](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)
- **[V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning](https://arxiv.org/abs/2506.09985)** (Mido Assran et al., 2025). A video world model trained on over one million hours of video, with an action-conditioned variant (V-JEPA 2-AC) that enables zero-shot robot planning. [code](https://github.com/facebookresearch/vjepa2) · [models](https://huggingface.co/collections/facebook/v-jepa-2-6841bad8413014e185b497a6) · [blog](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)
- **[V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning](https://arxiv.org/abs/2603.14482)** (Lorenzo Mur-Labadia et al., 2026). Extends V-JEPA 2 with dense predictive loss, deep self-supervision, multimodal tokenizers, and released pretrained checkpoints for dense video and image features. [code and models](https://github.com/facebookresearch/vjepa2#v-jepa-21-pretrained-checkpoints)
- **[MC-JEPA: A Joint-Embedding Predictive Architecture for Self-Supervised Learning of Motion and Content Features](https://arxiv.org/abs/2307.12698)** (Adrien Bardes, Jean Ponce, Yann LeCun, 2023). Jointly learns optical flow and content features in a shared encoder.

## Theory, Analysis, and Recipes

- **[LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics](https://arxiv.org/abs/2511.08544)** (Randall Balestriero and Yann LeCun, 2025). A theory of JEPAs that identifies the isotropic Gaussian as the optimal embedding distribution, plus SIGReg, a single heuristics-free objective that needs no stop-gradient or teacher-student network. [code](https://github.com/galilai-group/lejepa)
- **[A Lightweight Library for Energy-Based Joint-Embedding Predictive Architectures](https://arxiv.org/abs/2602.03604)** (Basile Terver et al., 2026). Introduces EB-JEPA, a single-GPU library and tutorial spanning image representation learning, video prediction, and action-conditioned JEPA planning. [code](https://github.com/facebookresearch/eb_jepa)
- **[Joint Embedding Predictive Architectures Focus on Slow Features](https://arxiv.org/abs/2211.10831)** (Vlad Sobal et al., 2022). Shows that JEPAs preferentially capture slowly varying factors of the input.
- **[How JEPA Avoids Noisy Features](https://arxiv.org/abs/2407.03475)** (Etai Littwin et al., 2024). Analyzes the implicit bias of deep linear self-distillation networks underlying JEPA.
- **[Connecting Joint-Embedding Predictive Architecture with Contrastive Self-supervised Learning](https://arxiv.org/abs/2410.19560)** (Shentong Mo et al., 2024). Relates the JEPA objective to contrastive learning.
- **[Why and How Auxiliary Tasks Improve JEPA Representations](https://arxiv.org/abs/2509.12249)** (Jiacan Yu et al., 2025). Studies when auxiliary objectives help JEPA pretraining.
- **[Learning and Leveraging World Models in Visual Representation Learning](https://arxiv.org/abs/2403.00504)** (Quentin Garrido et al., 2024). Introduces Image World Models (IWM), generalizing I-JEPA to broader latent-prediction tasks.
- **[LiDAR: Sensing Linear Probing Performance in Joint Embedding SSL Architectures](https://arxiv.org/abs/2312.04000)** (Vimal Thilak et al., 2023). A metric that predicts downstream linear-probing quality of joint-embedding models.
- **[VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning](https://arxiv.org/abs/2105.04906)** (Adrien Bardes et al., 2021). The anti-collapse regularizer reused by several JEPA variants.
- **[Understanding Self-Supervised Learning Dynamics without Contrastive Pairs](https://arxiv.org/abs/2102.06810)** (Yuandong Tian et al., 2021). Foundational analysis of why non-contrastive methods avoid collapse.
- **[Var-JEPA: A Variational Formulation of the Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2603.20111)** (Moritz Gögl et al., 2026). Recasts the JEPA objective in a variational framework.
- **[Gaussian Joint Embeddings for Self-Supervised Representation Learning](https://arxiv.org/abs/2603.26799)** (Yongchao Huang et al., 2026). Studies Gaussian embedding distributions for joint-embedding SSL.

## Variants by Domain

### Audio and Speech

- **[A-JEPA: Joint-Embedding Predictive Architecture Can Listen](https://arxiv.org/abs/2311.15830)** (Zhengcong Fei et al., 2023). Applies masked latent prediction to audio spectrograms.
- **[Investigating Design Choices in Joint-Embedding Predictive Architectures for General Audio](https://arxiv.org/abs/2405.08679)** (Alain Riou et al., 2024). An empirical study of masking and architecture choices for audio JEPA.
- **[Stem-JEPA: A Joint-Embedding Predictive Architecture for Musical Stem Compatibility Estimation](https://arxiv.org/abs/2408.02514)** (Alain Riou et al., 2024). Predicts compatibility between musical stems in embedding space.
- **[Audio-JEPA: Joint-Embedding Predictive Architecture for Audio Representation Learning](https://arxiv.org/abs/2507.02915)** (Ludovic Tuncay et al., 2025). General audio representation learning with the JEPA recipe.
- **[WavJEPA: Semantic learning unlocks robust audio foundation models for raw waveforms](https://arxiv.org/abs/2509.23238)** (Goksenin Yuksel et al., 2025). A JEPA that operates directly on raw waveforms.
- **[JEP-KD: Joint-Embedding Predictive Architecture Based Knowledge Distillation for Visual Speech Recognition](https://arxiv.org/abs/2403.18843)** (Chang Sun et al., 2024). Uses a JEPA for knowledge distillation in lip reading.

### 3D and Point Clouds

- **[Point-JEPA: A Joint Embedding Predictive Architecture for Self-Supervised Learning on Point Cloud](https://arxiv.org/abs/2404.16432)** (Ayumu Saito et al., 2024). Brings JEPA to point cloud pretraining with a token sequencer.
- **[3D-JEPA: A Joint Embedding Predictive Architecture for 3D Self-Supervised Representation Learning](https://arxiv.org/abs/2409.15803)** (Naiwen Hu et al., 2024). JEPA pretraining for 3D scene and object representations.
- **[CrossJEPA: Cross-Modal Joint-Embedding Predictive Architecture for Efficient 3D Representation Learning from 2D Images](https://arxiv.org/abs/2511.18424)** (Avishka Perera et al., 2025). Learns 3D representations by predicting from 2D images.

### Graphs and Molecules

- **[Graph-level Representation Learning with Joint-Embedding Predictive Architectures](https://arxiv.org/abs/2309.16014)** (Geri Skenderi et al., 2023). Adapts JEPA to graph-level self-supervised learning.
- **[Joint Embedding Predictive Architecture for self-supervised pretraining on polymer molecular graphs](https://arxiv.org/abs/2506.18194)** (Francesco Piccoli et al., 2025). JEPA pretraining over polymer molecular graphs. [code](https://github.com/Intelligent-molecular-systems/Polymer-JEPA)

### Time Series and Tabular Data

- **[LaT-PFN: A Joint Embedding Predictive Architecture for In-context Time-series Forecasting](https://arxiv.org/abs/2405.10093)** (Stijn Verdenius et al., 2024). Combines a JEPA with prior-fitted networks for in-context forecasting.
- **[T-JEPA: A Joint-Embedding Predictive Architecture for Trajectory Similarity Computation](https://arxiv.org/abs/2406.12913)** (Lihuan Li et al., 2024). Learns trajectory representations for similarity search.
- **[T-JEPA: Augmentation-Free Self-Supervised Learning for Tabular Data](https://arxiv.org/abs/2410.05016)** (Hugo Thimonier et al., 2024). A JEPA for tabular data that needs no augmentations.
- **[Joint Embeddings Go Temporal](https://arxiv.org/abs/2509.25449)** (Sofiane Ennadir et al., 2025). Extends joint-embedding self-supervision to time series.
- **[Koopman Invariants as Drivers of Emergent Time-Series Clustering in JEPAs](https://arxiv.org/abs/2511.09783)** (Pablo Ruiz-Morales et al., 2025). Analyzes time-series clustering that emerges in JEPA embeddings through Koopman invariants.
- **[MTS-JEPA: Multi-Resolution Joint-Embedding Predictive Architecture for Time-Series Anomaly Prediction](https://arxiv.org/abs/2602.04643)** (Yanan He et al., 2026). A multi-resolution JEPA for anomaly prediction.
- **[Giving Sensors a Voice: Multimodal JEPA for Semantic Time-Series Embeddings](https://arxiv.org/abs/2605.31580)** (Utsav Dutta et al., 2026). Learns semantic embeddings for multimodal sensor time series.

### Medical Imaging and Biosignals

- **[S-JEPA: towards seamless cross-dataset transfer through dynamic spatial attention](https://arxiv.org/abs/2403.11772)** (Pierre Guetschel et al., 2024). Signal-JEPA for EEG and brain-computer interfaces.
- **[Brain-JEPA: Brain Dynamics Foundation Model with Gradient Positioning and Spatiotemporal Masking](https://arxiv.org/abs/2409.19407)** (Zijian Dong et al., NeurIPS 2024). A JEPA foundation model for brain dynamics.
- **[Self-Supervised Pre-Training with JEPA Boosts ECG Classification Performance](https://arxiv.org/abs/2410.13867)** (Kuba Weimann et al., 2024). JEPA pretraining improves downstream ECG classification.
- **[From Video to EEG: Adapting JEPA to Brain Signal Analysis](https://arxiv.org/abs/2507.03633)** (Amirabbas Hojjati et al., 2025). Transfers the JEPA recipe from video to EEG.
- **[Self-supervised learning of imaging and clinical signatures using a multimodal JEPA](https://arxiv.org/abs/2509.15470)** (Thomas Z. Li et al., 2025). Joint-embedding prediction across imaging and clinical data.
- **[RadJEPA: Radiology Encoder for Chest X-Rays via Joint Embedding Predictive Architecture](https://arxiv.org/abs/2601.15891)** (Anas Anwarul Haq Khan et al., 2026). A JEPA encoder for chest radiographs.
- **[EchoJEPA: A Latent Predictive Foundation Model for Echocardiography](https://arxiv.org/abs/2602.02603)** (Alif Munim et al., 2026). A JEPA foundation model for echocardiogram video.
- **[JEPA-DNA: Grounding Genomic Foundation Models through Joint-Embedding Predictive Architectures](https://arxiv.org/abs/2602.17162)** (Ariel Larey et al., 2026). Applies JEPA to genomic sequence modeling.
- **[US-JEPA: A Joint Embedding Predictive Architecture for Medical Ultrasound](https://arxiv.org/abs/2602.19322)** (Ashwath Radhachandran et al., 2026). A JEPA for ultrasound representation learning.

### Earth Observation and Remote Sensing

- **[Predicting Gradient is Better: Exploring Self-Supervised Learning for SAR ATR with a JEPA](https://arxiv.org/abs/2311.15153)** (Weijie Li et al., 2023). A JEPA for synthetic aperture radar automatic target recognition.
- **[AnySat: One Earth Observation Model for Many Resolutions, Scales, and Modalities](https://arxiv.org/abs/2412.14123)** (Guillaume Astruc et al., 2024). A joint-embedding model spanning Earth-observation resolutions and modalities.
- **[REJEPA: A Novel Joint-Embedding Predictive Architecture for Efficient Remote Sensing Image Retrieval](https://arxiv.org/abs/2504.03169)** (Shabnam Choudhury et al., 2025). A JEPA for remote-sensing image retrieval.
- **[X-JEPA: A Novel Joint Learning Cross-Modal Predictive Alignment Framework for Remote Sensing Image Retrieval](https://openaccess.thecvf.com/content/WACV2026/html/Choudhury_X-JEPA_A_Novel_Joint_Learning_Cross-Modal_Predictive_Alignment_Framework_for_WACV_2026_paper.html)** (Shabnam Choudhury et al., WACV 2026). Cross-modal predictive alignment for remote-sensing retrieval.

### Language and Recommendation

- **[TI-JEPA: An Innovative Energy-based Joint Embedding Strategy for Text-Image Multimodal Systems](https://arxiv.org/abs/2503.06380)** (Khang H. N. Vo et al., 2025). An energy-based joint embedding for text and image.
- **[LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures](https://arxiv.org/abs/2509.14252)** (Hai Huang et al., 2025). Brings the JEPA objective to large language model training.
- **[JEPA4Rec: Learning Effective Language Representations for Sequential Recommendation via JEPA](https://arxiv.org/abs/2504.10512)** (Minh-Anh Nguyen et al., 2025). Applies JEPA to sequential recommendation.

### Generative Modeling

- **[Denoising with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2410.03755)** (Dengsheng Chen et al., 2024). D-JEPA, which casts generative modeling as denoising in embedding space.
- **[Improving Joint Embedding Predictive Architecture with Diffusion Noise](https://arxiv.org/abs/2507.15216)** (Yuping Qiu et al., 2025). Combines diffusion-style noise with the JEPA objective.
- **[JEPA-T: Joint-Embedding Predictive Architecture with Text Fusion for Image Generation](https://arxiv.org/abs/2510.00974)** (Siheng Wan et al., 2025). Adds text conditioning to a JEPA for image generation.

## World Models, Robotics, and Planning

- **[What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?](https://arxiv.org/abs/2512.24497)** (Basile Terver et al., 2025). A study of the design factors behind JEPA world models for planning. [weights](https://huggingface.co/facebook/jepa-wms)
- **[ACT-JEPA: Novel Joint-Embedding Predictive Architecture for Efficient Policy Representation Learning](https://arxiv.org/abs/2501.14622)** (Aleksandar Vujinovic et al., 2025). A JEPA for learning policy representations.
- **[Value-guided action planning with JEPA world models](https://arxiv.org/abs/2601.00844)** (Matthieu Destrade et al., 2025). Plans actions by guiding search with learned values over JEPA predictions.
- **[VLA-JEPA: Enhancing Vision-Language-Action Model with Latent World Model](https://arxiv.org/abs/2602.10098)** (Jingwen Sun et al., 2026). Couples a vision-language-action model with a JEPA latent world model.
- **[Causal-JEPA: Learning World Models through Object-Level Latent Masking](https://arxiv.org/abs/2602.11389)** (Heejeong Nam et al., 2026). Learns object-centric world models with latent masking.
- **[Learning Invariant Visual Representations for Planning with Joint-Embedding Predictive World Models](https://arxiv.org/abs/2602.18639)** (Leonardo F. Toso et al., 2026). Studies invariant representations for planning with JEPA world models.
- **[LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels](https://arxiv.org/abs/2603.19312)** (Lucas Maes et al., 2026). Learns action-conditioned latent world models directly from pixels with a two-term JEPA objective using SIGReg for anti-collapse. [code](https://github.com/lucas-maes/le-wm) · [website](https://le-wm.github.io/) · [checkpoints and data](https://huggingface.co/collections/quentinll/lewm)
- **[Hierarchical Planning with Latent World Models](https://arxiv.org/abs/2604.03208)** (Wancong Zhang et al., 2026). Plans across multiple temporal scales in latent world models, improving long-horizon zero-shot control while reducing planning-time compute. [website](https://kevinghst.github.io/HWM/) · [code](https://github.com/kevinghst/HWM_PLDM)
- **[stable-worldmodel: A Platform for Reproducible World Modeling Research and Evaluation](https://arxiv.org/abs/2605.21800)** (Lucas Maes et al., 2026). Provides a standardized world-model research stack with data conversion, baselines, planning solvers, and controllable evaluation environments. [code](https://github.com/galilai-group/stable-worldmodel) · [docs](https://galilai-group.github.io/stable-worldmodel/)

## Models and Weights

- **I-JEPA checkpoints** on Hugging Face: [ijepa_vith14_1k](https://huggingface.co/facebook/ijepa_vith14_1k), [ijepa_vith14_22k](https://huggingface.co/facebook/ijepa_vith14_22k), [ijepa_vith16_1k](https://huggingface.co/facebook/ijepa_vith16_1k), [ijepa_vitg16_22k](https://huggingface.co/facebook/ijepa_vitg16_22k). ViT-Huge and ViT-Giant encoders pretrained on ImageNet-1K and ImageNet-22K.
- **[V-JEPA 2 collection](https://huggingface.co/collections/facebook/v-jepa-2-6841bad8413014e185b497a6)** on Hugging Face: ViT-L, ViT-H, and ViT-g encoders including [vjepa2-vitl-fpc64-256](https://huggingface.co/facebook/vjepa2-vitl-fpc64-256), [vjepa2-vith-fpc64-256](https://huggingface.co/facebook/vjepa2-vith-fpc64-256), [vjepa2-vitg-fpc64-256](https://huggingface.co/facebook/vjepa2-vitg-fpc64-256), and [vjepa2-vitg-fpc64-384](https://huggingface.co/facebook/vjepa2-vitg-fpc64-384), plus Something-Something v2 and Diving48 fine-tunes.
- **[V-JEPA 2.1 checkpoints](https://github.com/facebookresearch/vjepa2#v-jepa-21-pretrained-checkpoints)** in `facebookresearch/vjepa2`: ViT-B, ViT-L, ViT-g, and ViT-G 384-resolution pretrained checkpoints, with PyTorch Hub loaders.
- **[JEPA-WMs](https://huggingface.co/facebook/jepa-wms)**. Joint-embedding predictive world-model checkpoints for physical planning, trained on robotics environments such as DROID, Metaworld, and Push-T.

## Code and Frameworks

- **[facebookresearch/ijepa](https://github.com/facebookresearch/ijepa)**. Official PyTorch codebase for I-JEPA (archived read-only).
- **[facebookresearch/jepa](https://github.com/facebookresearch/jepa)**. Official PyTorch codebase for V-JEPA.
- **[facebookresearch/vjepa2](https://github.com/facebookresearch/vjepa2)**. Official PyTorch codebase and models for V-JEPA 2.
- **[facebookresearch/eb_jepa](https://github.com/facebookresearch/eb_jepa)**. Meta FAIR's lightweight EB-JEPA library with self-contained examples for image JEPA, video JEPA, and action-conditioned video JEPA planning. [paper](https://arxiv.org/abs/2602.03604)
- **[galilai-group/lejepa](https://github.com/galilai-group/lejepa)**. Official implementation of LeJEPA and the SIGReg objective.
- **[lucas-maes/le-wm](https://github.com/lucas-maes/le-wm)**. Official codebase for LeWorldModel, with training and evaluation configs for the SIGReg-stabilized JEPA world model.
- **[galilai-group/stable-worldmodel](https://github.com/galilai-group/stable-worldmodel)**. Open-source platform used by LeWorldModel for environment management, data loading, planning, and evaluation.
- **[kevinghst/HWM_PLDM](https://github.com/kevinghst/HWM_PLDM)**. Minimal implementation of Hierarchical Planning with Latent World Models on PLDM and Diverse Maze. [paper](https://arxiv.org/abs/2604.03208) · [website](https://kevinghst.github.io/HWM/)
- **[Transformers: I-JEPA](https://huggingface.co/docs/transformers/en/model_doc/ijepa)** and **[Transformers: V-JEPA 2](https://huggingface.co/docs/transformers/en/model_doc/vjepa2)**. Hugging Face integrations with `AutoModel` support.
- **[keon/jepa](https://github.com/keon/jepa)**. A community PyTorch reimplementation useful for learning the I-JEPA objective.
- **[AbdelStark/ProvableWorldModel](https://github.com/AbdelStark/ProvableWorldModel)**. A commit-and-audit proof system for deterministic, quantized inference of a JEPA-style world model (LeWorldModel), enabling verifiable AI inference with zero-knowledge proofs. [website](https://abdelstark.github.io/ProvableWorldModel/)
- **[Hanno-Labs/langset](https://github.com/Hanno-Labs/langset)**. A library that fine-tunes a pretrained LLM into a JEPA world model by emitting discrete FSQ latents in its own token stream, trained against an EMA-twin (or SIGReg) target and co-trained with next-token cross-entropy, with autoregressive latent rollout and a learned STOP.

## Datasets

- **[ImageNet](https://www.image-net.org/)**. The image pretraining corpus for I-JEPA. See the [ILSVRC paper](https://arxiv.org/abs/1409.0575) (Olga Russakovsky et al., 2014).
- **[Kinetics](https://arxiv.org/abs/1705.06950)** (Will Kay et al., 2017). Human action video dataset used to pretrain V-JEPA. Downloader: [cvdfoundation/kinetics-dataset](https://github.com/cvdfoundation/kinetics-dataset).
- **[Something-Something v2](https://arxiv.org/abs/1706.04261)** (Raghav Goyal et al., 2017). Fine-grained motion video dataset used to evaluate V-JEPA models.
- **[EPIC-KITCHENS-100](https://epic-kitchens.github.io/)** (Dima Damen et al., [2020](https://arxiv.org/abs/2006.13256)). Egocentric video used for action anticipation.
- **[DROID](https://droid-dataset.github.io/)**. A large in-the-wild robot manipulation dataset used in JEPA world-model planning.

## Benchmarks

Physical-reasoning benchmarks released with V-JEPA 2.

- **[IntPhys 2](https://arxiv.org/abs/2506.09849)** (Florian Bordes et al., 2025). Measures whether a model can tell physically plausible scenes from implausible ones.
- **[Minimal Video Pairs (MVPBench)](https://arxiv.org/abs/2506.09987)** (Benno Krojer et al., 2025). A shortcut-aware video question-answering benchmark for physical understanding.
- **[CausalVQA](https://arxiv.org/abs/2506.09943)** (Aaron Foss et al., 2025). Tests physical cause-and-effect reasoning in video models.

## Talks and Lectures

- **[Objective-Driven AI: Towards AI systems that can learn, remember, reason, and plan](https://www.youtube.com/watch?v=MiqLoAZFRSE)** (Yann LeCun, 2024).
- **[Self-Supervised Learning, JEPA, World Models, and the future of AI](https://www.youtube.com/watch?v=yUmDRxV0krg)** (Yann LeCun, 2025).
- **[Yann LeCun on Meta AI, Open Source, Limits of LLMs, AGI, and the Future of AI](https://www.youtube.com/watch?v=5t1vTLU7s40)** (Lex Fridman Podcast 416, 2024).
- **[A Path Towards Autonomous Machine Intelligence](https://www.youtube.com/watch?v=OKkEdTchsiE)** (Yann LeCun, 2023).
- **[V-JEPA: Revisiting Feature Prediction (Explained)](https://www.youtube.com/watch?v=7UkJPwz_N_0)** (Yannic Kilcher, 2024).
- **[JEPA, A Path Towards Autonomous Machine Intelligence (Paper Explained)](https://www.youtube.com/watch?v=jSdHmImyUjk)** (Yannic Kilcher, 2022).
- **[Yann LeCun's $1B Bet Against LLMs [Part 1]](https://www.youtube.com/watch?v=kYkIdXwW2AE)** (Welch Labs, 2026). Welch Labs interviewing Yann, with high-level explanations mixed in.
- **[Yann LeCun's $1B Bet Against LLMs [Part 2]](https://www.youtube.com/watch?v=v_jDvpEGTIg)** (Welch Labs, 2026). Welch Labs interviewing Yann, with high-level explanations mixed in.

## Courses

- **[NYU Deep Learning (DS-GA 1008)](https://atcold.github.io/NYU-DLSP21/)** (Yann LeCun and Alfredo Canziani). Includes a lecture on [energy-based models and self-supervised learning](https://www.youtube.com/watch?v=tVwV14YkbYs).
- **[Hugging Face Computer Vision Course: I-JEPA unit](https://huggingface.co/learn/computer-vision-course/unit13/i-jepa)**. A hands-on walkthrough of the I-JEPA architecture.

## Articles and Explainers

- **[I-JEPA: The first AI model based on Yann LeCun's vision](https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/)** (Meta AI, 2023).
- **[V-JEPA: The next step toward advanced machine intelligence](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)** (Meta AI, 2024).
- **[Introducing the V-JEPA 2 world model and new benchmarks for physical reasoning](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)** (Meta AI, 2025).
- **[Yann LeCun on a vision to make AI learn and reason like animals and humans](https://ai.meta.com/blog/yann-lecun-advances-in-ai-research/)** (Meta AI, 2022).
- **[What Is JEPA? Joint Embedding Predictive Architecture](https://www.turingpost.com/p/jepa)** (Turing Post, 2024).
- **[Meta AI's I-JEPA, Explained](https://encord.com/blog/i-jepa-explained/)** (Encord, 2023).
- **[A Guided Tour of the Joint-Embedding Predictive Architecture](https://patricknicolas.substack.com/p/a-guided-tour-of-the-joint-embedding)** (Patrick Nicolas, 2026).
- **[Yann LeCun's new venture is a contrarian bet against large language models](https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/)** (MIT Technology Review, 2026).


## Contributing

Contributions are welcome. Please open a pull request that follows the existing format: link to the primary source, attribute the first author and year accurately, and write one factual sentence describing the resource. Verify that every link resolves and that arXiv identifiers match the cited title before submitting.

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

To the extent possible under law, the contributors have waived all copyright and related or neighboring rights to this work.
