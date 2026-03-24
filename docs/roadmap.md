# Roadmap: Achieving full RCP (whitepaper alignment)

This document maps **[`whitepaper.md`](whitepaper.md)** (Ramanujan Compression Protocol) to **concrete engineering work**. It complements **[`WHITEPAPER_IMPLEMENTATION_NOTES.md`](WHITEPAPER_IMPLEMENTATION_NOTES.md)**, which explains what the current **backend (FastAPI)** service does *instead* of full RCP.

**Goal:** Implement the paper’s **embedding-space** pipeline: Ramanujan transform → top‑\(k\) coefficients → reconstruction (discrete and **soft prompt**) → evaluation comparable to §Experiments.

**Status:** The phased execution plan below (§Phases 0–8) is a **future roadmap, contingent on funding** for research-grade GPU work, model licenses, and evaluation. The shipped **`ram`** API remains the **string-level** path documented in [`WHITEPAPER_IMPLEMENTATION_NOTES.md`](WHITEPAPER_IMPLEMENTATION_NOTES.md); this document does **not** commit the product to full RCP until that funding and scope are explicit.

---

## Executive summary

| Layer | What you need | Outcome |
|--------|----------------|--------|
| **Math / core** | \(R_q\) over **vectors** \(x_i \in \mathbb{R}^d\), fast \(c_q(i)\) computation, top‑\(k\) by \(\|R_q\|_2\) | Matches Algorithm 1 (compression) in spirit |
| **Models** | Frozen LM \(f\) for embeddings and downstream eval; optional small **adapter** \(\phi\) | Matches §Methodology / §Reconstruction |
| **Infra** | GPU memory for 7B-class models, dataset licenses, pinned seeds | Reproducible §Experiments |
| **Product (optional)** | Separate from paper: string-level API can stay; full RCP is a **research stack** or **future tier** | Clear positioning |
| **Budget** | GPU time + specialized headcount + legal (if commercial) | See **§Budget & indicative pricing** below |

Full RCP is **achievable** as a multi-phase R&D program; it is **not** a small patch on the current tokenizer-only path.

---

## Budget & indicative pricing (USD)

**Disclaimer:** Figures are **order-of-magnitude planning bands**, not quotes. Cloud list prices, salaries, and taxes change by region and date—**re-validate** with vendor calculators and local payroll before committing.

### Compute (GPU cloud)

| Class | Typical use | Indicative on-demand $/hr (US/EU, 2025–2026) |
|--------|-------------|-----------------------------------------------|
| **High-end datacenter** (e.g. A100 40/80GB) | Paper-style 7B runs, long contexts | ~**$1.5–$4.0**/hr (varies widely: budget clouds ~$1.5; hyperscalers often ~$2.7–$3.7 for single A100-class) |
| **Mid** (L40, A10, A6000-class) | Prototyping, smaller \(n\), smaller open models | ~**$0.5–$2.0**/hr |
| **Consumer / spot** (where allowed) | Debugging only; not for published benchmarks | Lower, but **availability and reproducibility** suffer |

**Rule of thumb — GPU-hours:** Development + full eval (multiple datasets, seeds, baselines) often lands in **hundreds to a few thousand GPU-hours** for a serious replication—not a single overnight job.

| Milestone | Rough GPU-hours (indicative) | Compute-only @ ~$2.5/hr |
|-----------|------------------------------|-------------------------|
| Phases 0–4 (pipeline to reconstruction) | 200–600 | **$500–$1,500** |
| Phase 5–6 (adapter + spectral) | 200–800 | **$500–$2,000** |
| Phase 7 (full baselines + sweeps) | 500–3,000+ | **$1,250–$7,500+** |

Use **spot/preemptible** instances where acceptable to cut 30–70%; add **buffer** for restarts.

### Minimum price: how to submit benchmark results

**Goal:** Publish defensible numbers (tables, seeds, configs) while spending **as little GPU money** as possible. Strategy: **cheap hardware for most hours**, **expensive tier only for final runs**, and **cut wasted repeats**.

| Principle | What to do |
|-------------|------------|
| **Tiered GPUs** | Do **Phases 0–4** (pipeline, correctness, unit tests) mostly on **mid-tier** (~$0.5–$2/hr). Reserve **A100-class** for long context, large batch, or when VRAM is the limit—not for every debug loop. |
| **Spot / preemptible** | Use for **batch eval** and **hyperparameter sweeps** when jobs checkpoint frequently. Expect interruptions: **save checkpoints** and **resume**. Effective cost often **30–70%** below on-demand; effective $/hr can approach **~$0.5–$1.5** on budget clouds if you tolerate ops overhead. |
| **One “gold” run** | After the pipeline is stable, run **one** fully pinned configuration (git SHA, `requirements` hash, model revision, dataset snapshot) on **on-demand** A100 (or equivalent) for **submission-grade** rows only—avoid paying top tier while still iterating on bugs. |
| **Shrink before widen** | **Subset** datasets (e.g. 100–500 examples) and **1 seed** during development; scale to full test split and **5 seeds** (or paper protocol) only for the **final** table. |
| **Cache artifacts** | **Precompute and store** token embeddings (or intermediate tensors) so ablations and baselines **reuse** them—large savings versus re-forwarding the LM every time. |
| **Baseline order** | Implement **cheap baselines first** (random \(k\), Fourier) before heavy ones (ToMe, LLMLingua) so you fail fast on integration issues. |
| **Phase 7 last** | Treat Phase 7 (full harness) as **burn** phase: only start when Phases 0–6 don’t change daily—otherwise you pay the **500–3000+ GPU-hour** band **twice**. |

**What to submit** (keeps reviews happy without extra compute): `environment.yml` or lockfile, random seeds, dataset splits/versions, model checkpoint IDs, **hardware note** (GPU model + VRAM), wall-clock and **GPU-hours** per experiment, and raw logs or Weights & Biases (or MLflow) run links. Honest limitation: “subset used for development; full eval in appendix row X” if you split that way.

**Rough spend mindset:** If **~$2.5/hr** is your planning rate for A100-class on-demand, use **mid-tier + spot** for ~**70–90%** of hours so your **blended** effective rate is often closer to **~$1/hr or less** for the project—then pay **full rate** only for the short **final** verification window.

### People

| Role | Indicative US fully-loaded annual cost | Notes |
|------|----------------------------------------|--------|
| Senior ML / research engineer | **$180k–$280k**/yr | One FTE often spans Phases 1–7 over **9–18 months** |
| ML engineer (mid) | **$130k–$190k**/yr | Implementation-heavy |
| Contractor (hourly) | **$80–$180**/hr | Common for short spikes; no benefits in rate |

**Rule of thumb:** A **credible** path to paper-aligned stack + eval harness is rarely **less than ~0.5–1.0 FTE-year** of specialized time even with strong tooling.

### Models, data, and software

| Item | Typical cost |
|------|----------------|
| **Open-weight LMs** (Llama, Mistral-class) | **$0** download; **license** may restrict commercial use—legal review for SaaS |
| **Datasets** (GSM8K, HotpotQA, etc.) | Often **$0** for research; **redistribution** or **product** use may need agreements |
| **PyTorch, HF, baselines** | **$0** OSS; pin versions for reproducibility |
| **Experiment tracking** (Weights & Biases, MLflow hosting) | **$0–$50+/mo** depending on seats and retention |
| **Artifact storage** (checkpoints, logs) | **$10–$100+/mo** at modest scale |

### Legal & compliance (if product touches this stack)

- **License review** (model + data + outbound API): often **$5k–$30k** one-time via outside counsel, highly variable.
- **Commercial terms** for third-party models/datasets: **case-by-case** (sometimes revenue share or per-seat).

### Scenario totals (all-in bands, not quotes)

| Scenario | What’s included | Indicative **total** (USD) |
|----------|------------------|------------------------------|
| **Lean prototype** | Smaller GPU, shorter \(n\), 1 part-time engineer, Phases 0–4 only | **$25k–$80k** |
| **Paper-aligned R&D** | A100-class (or equivalent), 1 FTE ~12 months, Phases 0–7, honest baselines | **$200k–$500k** |
| **Full replication + Phase 8 product integration** | Team of 2+, compliance, sustained GPU, staging API | **$500k–$1.5M+** |

These totals **include** rough people + compute + overhead; they **exclude** equity, office, and profit margin if using an agency.

---

## Current state (baseline)

- **`backend/`**: HF tokenizer → integer token IDs → `ramanujan_compression` heuristics (hybrid / sparse-modular); `/generate` uses **compressed text**, not soft-prompt tensors.
- **Diagnostics**: Optional Ramanujan spectral metrics on **scalar** token IDs (interpretability only).

**Gap to close for “whitepaper parity”:** embedding tensors, \(O(n \log n)\) fast path, top‑\(k\) vector coefficients, inverse reconstruction, soft-prompt + adapter, and the **evaluation harness** (datasets, baselines, metrics).

---

## Funding-contingent roadmap: full embedding-level RCP + soft-prompt stack

This section states **what must be built** if funding is provided to pursue **whitepaper parity**. It is the conceptual companion to §Phases 0–8 (same work, organized as two halves plus surrounding requirements).

### Embedding-level RCP (the “compression” half)

This operates on **token embeddings** \(x_i \in \mathbb{R}^d\), not token IDs alone.

| Piece | Requirement |
|--------|-------------|
| **Frozen LM** | Produce \(X = [x_1,\ldots,x_n]\) from token IDs (paper: e.g. **input embedding layer**; ablations may use deeper layers). |
| **Vector transform** | \(R_q = \sum_i x_i\, c_q(i)\) with **\(R_q \in \mathbb{C}^d\)** (or an explicit real/imag convention)—not scalar projections on IDs. |
| **Fast path at scale** | Target **\(O(n \log n)\)** via FFT / fast Ramanujan-sum methods; naive \(O(n^2)\) is for debugging only. |
| **Sparse encoding** | Top‑\(k\) by \(\|R_q\|_2\); defined **storage/API format** for \(\{(R_q,q)\}_{q\in Q_k}\) and metadata (\(n,k,d\), tokenizer). |
| **Inverse** | \(\hat{x}_i = \sum_{q\in Q_k} R_q\, c_q(i)\) (paper convention for real part) → sequence of **continuous** vectors. |

Without this block, there is no “embedding-level RCP” in the paper’s sense.

### Soft-prompt half (how the LM consumes RCP)

The paper’s **primary** result path is **not** “map \(\hat{x}_i\) to discrete tokens and call the chat API.”

| Piece | Requirement |
|--------|-------------|
| **Injection** | Feed continuous \(\hat{x}_i\) (or adapter output) **where the transformer expects token embeddings**—**model-specific** hooks (shape, dtype, masks, sequence length). |
| **Adapter \(\phi\)** | Small **trainable** module (paper: e.g. linear layer on a small train split) to align compressed/reconstructed distributions to the frozen LM. |
| **Training** | Loop with forward, loss, checkpoints—loss aligned with the eval protocol (task accuracy, LM loss, etc.). |

**Full stack (one line):** *frozen LM embeddings → Ramanujan transform on vectors → top‑\(k\) → inverse to \(\hat{x}_i\) → adapter-trained soft injection into the same LM*, plus **fast transforms**, **eval harness**, and **model integration**—not merely a better string compressor.

### Surrounding requirements (funding scope)

- **GPU / memory:** 7B-class models and long \(n\) need serious VRAM; mitigation: shorter contexts first, smaller open models with documented caveats, checkpointing.
- **Evaluation:** Datasets, baselines (LLMLingua, Fourier, ToMe, …), BERTScore and task metrics, multiple seeds—**fair comparison is its own workstream**.
- **Legal / ops:** Model and dataset licenses; reproducible environments; artifact storage for checkpoints and logs.

### Relationship to the shipped product

The **tokenizer → integer compressor → decode to string → OpenAI-compatible chat** path does **not** implement vector \(R_q\), inverse \(\hat{x}_i\), or soft-prompt tensors. It can stay as the **commercial** tier; **full RCP + soft prompt** is a **separate research/inference stack** (§Phase 8 sketches optional product bridges).

---

## Execution plan (Phases 0–8, when funded)

> **Scope:** Execute the following phases when **research funding** (and agreed scope) is available. Until then, treat this as planning only.

### Phase 0 — Reproducibility and scope

**Deliverables**

- [ ] Pin **Python**, **PyTorch**, **CUDA**, **transformers** versions in a `requirements-research.txt` or conda lockfile.
- [ ] Document **hardware** floor (paper: single A100; adjust if using smaller models with caveat in write-up).
- [ ] Obtain **model weights** access (e.g. LLaMA-2-7B or an openly licensed substitute) and **dataset** access per §Experiments.
- [ ] Create `experiments/README.md`: how to run one end-to-end smoke test (one dataset, one seed).

**Exit criteria:** One command runs “embed → transform → top‑k → reconstruct” on a toy sequence without crashing.

---

### Phase 1 — Embedding extraction (\(X = \{x_i\}\))

**Paper reference:** §Problem Formulation, §Implementation Details.

**Deliverables**

- [ ] Load frozen LLM; extract **input token embeddings** \(x_i \in \mathbb{R}^d\) for sequences of length \(n\) (paper uses embedding layer; ablations can use deeper layers).
- [ ] Batch API with **max length** and padding/mask handling.
- [ ] Optional: cache embeddings for benchmark splits to save compute.

**Exit criteria:** For a batch of prompts, output `FloatTensor` of shape `(batch, n, d)` aligned with token indices.

---

### Phase 2 — Ramanujan transform (vector \(R_q\))

**Paper reference:** §Ramanujan Transform; Algorithm 1 (lines computing \(R_q\)).

**Deliverables**

- [ ] Implement \(c_q(i)\) (complex) and projection  
  \(R_q = \sum_i x_i \, c_q(i)\) with **vector** \(R_q \in \mathbb{C}^d\) (or split real/imag if you fix a convention).
- [ ] **Fast path:** integrate or implement **FFT-based / fast convolution** for Ramanujan sums (paper cites \(O(n \log n)\); see §Complexity Analysis). Naive \(O(n^2)\) is fine for prototyping only.
- [ ] Unit tests: small \(n\), compare naive vs fast (within tolerance).

**Exit criteria:** For fixed embeddings, full set of \(\{R_q\}_{q=1}^{n}\) computed and \(\|R_q\|_2\) available for sorting.

---

### Phase 3 — Sparse encoding (top‑\(k\) coefficients)

**Paper reference:** §Sparse Encoding.

**Deliverables**

- [ ] Select \(Q_k\): indices of **\(k\)** largest \(\|R_q\|_2\) (paper formulation).
- [ ] **On-disk / API representation:** store \(\{(R_q, q)\}_{q \in Q_k}\) (and metadata: \(n, k, d\), tokenizer id).
- [ ] Report **compression ratio** consistent with paper (clarify token vs coefficient count in docs).

**Exit criteria:** Compress arbitrary length‑\(n\) embedding sequence to \(k\) coefficient vectors + indices; ratio matches defined formula.

---

### Phase 4 — Reconstruction

**Paper reference:** §Reconstruction (inverse formula); discrete vs soft.

**Deliverables**

- [ ] **Continuous reconstruction:**  
  \(\hat{x}_i = \sum_{q \in Q_k} R_q \cdot c_q(i)\) (use **real part** as in paper if that is your convention).
- [ ] **Discrete path:** nearest neighbor in vocabulary embedding table to \(\hat{x}_i\) → token IDs → detokenize (for BERTScore / baselines).
- [ ] Validate MSE in embedding space vs full \(n\) coefficients (sanity check).

**Exit criteria:** From compressed \(\{(R_q,q)\}\), recover \(\hat{x}_i\) and optionally discrete tokens; measure distortion vs original \(x_i\).

---

### Phase 5 — Soft prompt + adapter (\(\phi\))

**Paper reference:** §Reconstruction, §Implementation Details (5% train split, linear adapter).

**Deliverables**

- [ ] Feed \(\phi(\hat{x}_i)\) (or \(\hat{x}_i\) after adapter) as **soft prompt** into the frozen LM forward (exact hook depends on model API).
- [ ] Implement **small trainable adapter** (e.g. single linear layer as in paper); train on small fraction of each dataset.
- [ ] Training loop: loss aligned with paper (e.g. next-token or task loss on downstream objective — match your experimental protocol).

**Exit criteria:** Downstream task runs with soft prompts; numbers are comparable in *kind* to paper (not necessarily equal without full hyperparameter search).

---

### Phase 6 — Spectral validation (paper §Spectral Analysis)

**Paper reference:** §Spectral Analysis of Language Embeddings; cumulative energy \(E(k)\).

**Deliverables**

- [ ] Implement \(E(k)\) for **Ramanujan**, **Fourier** (DFT on same embedding sequence), **random** basis (paper baselines).
- [ ] Plots/tables: e.g. % of coefficients to reach 90% energy (paper reports illustrative numbers on ShareGPT / GSM8K).
- [ ] Script: `spectral_compare.py --dataset ...`

**Exit criteria:** Reproducible curves/tables that match the *structure* of paper claims (exact numbers may vary by model/data).

---

### Phase 7 — Full experiments harness

**Paper reference:** §Experiments (datasets, baselines, metrics, results table).

**Deliverables**

- [ ] **Data:** GSM8K, ShareGPT sample, ArXiv abstracts, HumanEval, HotpotQA (or substitutes with documented rationale).
- [ ] **Baselines:** no compression, LLMLingua-style or equivalent, Fourier top‑\(k\), autoencoder, random \(k\), ToMe, attention pooling, **RCP**.
- [ ] **Metrics:** compression ratio, BERTScore, task metrics (exact match, pass@1, F1, etc.), timing on defined GPU.
- [ ] **Statistics:** multiple seeds, mean/std, paired tests as in paper.
- [ ] **Tables:** regenerate main results table; link to logs/checkpoints.

**Exit criteria:** Paper’s empirical *claims* are either **replicated** or **explained** (different model, data sample, etc.) with honest limitations.

---

### Phase 8 — Optional: SaaS / `backend` integration

**Not required** for scientific “whitepaper achieved,” but useful for product.

**Ideas (pick any)**

- [ ] **Research API** (internal): endpoint accepts prompts → returns compressed coefficient payload + metrics (heavy GPU job).
- [ ] **Feature flag:** “paper mode” uses embedding RCP when `OPENAI_*` is replaced by local LM + adapter.
- [ ] **Docs:** marketing and API docs state clearly which path is **string-level** vs **full RCP**.

---

## Dependencies and risks

| Risk | Mitigation |
|------|------------|
| **Compute** (7B model, long \(n\)) | Start with smaller \(n\), smaller \(d\) via projection, or smaller open LM with documented tradeoff |
| **Fast Ramanujan** | Use cited literature (e.g. fast Ramanujan-sum algorithms); profile before scaling \(n\) |
| **Soft-prompt API** varies by model | Abstract behind a `SoftPromptInjector` per model family |
| **Baseline fairness** | Pin versions of LLMLingua, ToMe, etc.; same tokenizer where required |
| **Legal / license** | Dataset and model licenses for redistribution and commercial SaaS |

---

## Milestone checklist (single page)

Use this as a **go/no-go** list for “we implemented the whitepaper core.”

1. [ ] Embeddings \(x_i \in \mathbb{R}^d\) from frozen LM  
2. [ ] Full Ramanujan \(R_q\) as **vectors**, top‑\(k\) selection  
3. [ ] Reconstruction \(\hat{x}_i\) and discrete detokenization  
4. [ ] Soft prompt + trained adapter \(\phi\)  
5. [ ] Spectral \(E(k)\) vs Fourier / random  
6. [ ] Full eval harness + main table reproduced or honestly bounded  

---

## Related files

| File | Role |
|------|------|
| [`README.md`](../README.md) | Repository overview |
| [`docs/README.md`](README.md) | Documentation index (this folder) |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Monorepo layout (backend / frontend / docs) |
| [`whitepaper.md`](whitepaper.md) | LaTeX source — definitions, algorithms, experiments |
| [`WHITEPAPER_IMPLEMENTATION_NOTES.md`](WHITEPAPER_IMPLEMENTATION_NOTES.md) | Paper vs deployed API; suggested LaTeX clarifications |
| [`backend/PROJECT_SUMMARY.md`](../backend/PROJECT_SUMMARY.md) | Current SDK / product scope |
| [`backend/app/services/compression_service.py`](../backend/app/services/compression_service.py) | Production string-level compression path |

---

*Last updated: aligned with `whitepaper.md` structure (Introduction through Experiments). Phases 0–8 are **funding-contingent**. **Budget figures are indicative**—verify vendor and payroll pricing before use. Adjust phase ordering if you prioritize spectral validation before soft prompts.*
