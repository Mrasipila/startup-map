# Startup Semantic Map — precomputed embeddings version

## Files

- `startups_2026_embedded.csv` — generated output file. Commit this file with the app.
- `app.py` — Streamlit app that only loads the precomputed CSV and plots it.
- `requirements-app.txt` — dependencies

## 1. Run the app

```bash
python -m venv venvs
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
