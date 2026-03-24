# Whitepaper ↔ Repository alignment

This file accompanies **`whitepaper.md`** (LaTeX source for the Ramanujan Compression Protocol paper). Use it to **disambiguate** research claims from the **`backend`** (FastAPI) service and **`frontend`** app, and to **patch** the LaTeX where needed.

---

## 1. Scope: what the paper describes vs what ships

| Topic | Paper (`docs/whitepaper.md`) | Current repo (`backend/`) |
|--------|-------------------------|----------------------------------------|
| Core object | Token **embeddings** \(x_i \in \mathbb{R}^d\), Ramanujan sums \(c_q(n)\), coefficients \(R_q\), top‑\(k\) sparsification | **Plain-text** prompts, `ramanujan_compression.RamanujanCompressor` + `CompressionConfig` (strategies, ratios), HF **`AutoTokenizer`** for counts |
| Transform complexity | \(O(n \log n)\) via FFT-style fast Ramanujan sums | **Not** exposed as the paper’s full embedding-level FFT pipeline in the API layer |
| Reconstruction | **Soft prompt** + adapter on frozen LLM (e.g. LLaMA-2-7B); discrete NN optional | **`/generate`** sends **compressed text** to an **OpenAI-compatible** chat API; no continuous soft-prompt tensors in the product path |
| Empirical results | GSM8K table, BERTScore, multi-dataset | **Not** reproduced by the FastAPI app; tables are **paper experiments**, not live SLA guarantees |

**Conclusion:** The paper is a **research specification** for RCP. The repository is a **practical API/UI** that uses the **same family** of ideas (Ramanujan-flavored compression via the SDK) but **does not implement** the full embedding-level RCP + soft-prompt stack described in the main sections.

---

## 2. Suggested new section for `whitepaper.md` (paste into LaTeX)

Add **after the Introduction** or **before Conclusion** (recommended: **§ near Implementation Details** or new **§ Deployment and reference implementation**):

```latex
\subsection{Reference implementation and deployment scope}
\label{sec:deployment}

The experiments in this work use a full embedding-space pipeline (Section~\ref{sec:methodology}) with frozen encoder features and optional soft-prompt adapters. Separately, we maintain a \textbf{lightweight deployment stack} intended for integration testing and product APIs: it applies a tokenizer-based length model and the \texttt{ramanujan\_compression} library with configurable strategies (\emph{e.g.}, hybrid and sparse-modular modes) to \textbf{natural-language prompts}, without materializing the Ramanujan coefficient tensors $R_q$ over embedding matrices in the serving path described here.

Accordingly, \textbf{numerical results in Section~\ref{sec:experiments}} should be understood as obtained from the \textbf{research codebase} matching the methodology above, not as guaranteed metrics of any particular HTTP service. We document this split to avoid overstating equivalence between the theoretical RCP object and a string-level compressor.
```

Adjust `\ref{...}` labels to match your final section labels (`\label{sec:experiments}` etc.).

---

## 3. Reproducibility statement (replace or extend)

**Current risk:** The statement promises “complete source code” and evaluation pipelines for the **paper** setup.

**Suggested replacement paragraph:**

```latex
We release code sufficient to reproduce the \textbf{embedding-based} experiments described in the main text (transform, top-$k$ selection, evaluation harness), subject to hardware and license constraints for third-party models and datasets. A separate \textbf{reference API} implementation compresses text prompts using the same mathematical family of tools in a reduced form; it is documented alongside the repository and is not claimed to reproduce Table~\ref{tab:gsm8k} without the full experimental stack.
```

Add `\label{tab:gsm8k}` to the GSM8K results table if you use this sentence.

---

## 4. Soft prompts (clarify in §Reconstruction)

After the soft-prompt enumeration, add one sentence:

```latex
\textbf{Product deployments} may omit the soft-prompt path and instead feed \textbf{discretized text} from a string-level compressor into a chat API; this trades the theoretical guarantees of continuous reconstruction for integration simplicity and is outside the main empirical claims unless otherwise noted.
```

---

## 5. LaTeX structural fixes (apply inside `whitepaper.md`)

### 5.1 Duplicate `\caption` in `algorithm` environments

The compression block uses **two** `\caption{...}` commands (lines ~136–149). **`algorithm` allows one caption** (or use `\caption` + `\floatname` once).

**Fix:** Keep a single caption, e.g.:

```latex
\begin{algorithm}[t]
\caption{RCP Compression}
\label{alg:rcp-compress}
\begin{algorithmic}[1]
...
\end{algorithmic}
\end{algorithm}
```

Remove the second `\caption{Ramanujan Compression Protocol (Compression)}` at the end of that block. Repeat the same pattern for the **Reconstruction** algorithm (lines ~167–181).

### 5.2 Acknowledgments

`\begin{acknowledgments}` is **not** standard in `article`. Replace with:

```latex
\section*{Acknowledgments}
We thank the anonymous reviewers for their insightful comments. This work was supported by [funding information].
```

### 5.3 Bibliography spot-checks

- **`li2025prompt`** — confirm venue/year or mark as arXiv/preprint.
- **`li2023selective`** — arXiv id `2305.12345` may be a **placeholder**; replace with the official citation or correct id.

---

## 6. Optional: `PROJECT_SUMMARY.md` / README cross-links

Add one line in **`backend/PROJECT_SUMMARY.md`** (or root README):

> Research claims and benchmark numbers: see **`docs/whitepaper.md`** and **`docs/WHITEPAPER_IMPLEMENTATION_NOTES.md`** for the distinction between the **paper RCP** and the **deployed API**.

(Only if you want repo navigation; skip if you prefer minimal docs.)

---

## 7. If you later align **code** with the paper (roadmap)

Not required for documentation honesty, but for **scientific** alignment:

1. **Embedding extraction** from a frozen LM (same \(f\) as in §Problem Formulation).
2. **Explicit** \(R_q\) accumulation and top‑\(k\) selection as in Algorithm 1.
3. **Soft-prompt** path: tensor input to model + adapter training script.
4. **Eval**: GSM8K / BERTScore scripts pinned to paper hyperparameters.

Until then, the **deployment note** (Section 2 above) is the correct way to avoid over-claiming.

---

## File index

| File | Role |
|------|------|
| `docs/whitepaper.md` | LaTeX paper source (RCP theory + experiments) |
| `docs/WHITEPAPER_IMPLEMENTATION_NOTES.md` | This file — scope, paste-in snippets, LaTeX fixes |
| `backend/app/services/compression_service.py` | String-level + SDK compression used by the API |
