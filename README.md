# Startup Semantic Map — precomputed embeddings version

This version avoids loading `sentence-transformers` inside the Streamlit app.

## Files

- `startups_2026.csv` — raw startup data.
- `preprocess_embeddings.py` — run once to create embeddings, 2D coordinates, clusters, and cluster labels.
- `startups_2026_embedded.csv` — generated output file. Commit this file with the app.
- `app.py` — Streamlit app that only loads the precomputed CSV and plots it.
- `requirements-app.txt` — lightweight dependencies for the hosted app.
- `requirements-preprocess.txt` — heavier dependencies for one-time preprocessing.

## 1. Precompute embeddings locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-preprocess.txt
python preprocess_embeddings.py --input startups_2026.csv --output startups_2026_embedded.csv --reducer umap
```

This creates `startups_2026_embedded.csv` with these columns:

- `name`
- `description`
- `location`
- `type`
- `text_for_embedding`
- `embedding_model`
- `embedding`
- `x`
- `y`
- `cluster`
- `cluster_label`
- `reducer`

## 2. Run the app

```bash
pip install -r requirements-app.txt
streamlit run app.py
```

## Why this is better

The hosted app does not download or load a sentence-transformer model at page load.
It only reads `startups_2026_embedded.csv`, so startup is much faster and hosting is lighter.

## Hosting note

For Streamlit specifically, Streamlit Community Cloud is usually the easiest free host.
Vercel is better for static or serverless apps. For Vercel, you can precompute embeddings and export a static Plotly HTML page, or build a Next.js frontend that loads the CSV.
