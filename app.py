import ast
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Startup Semantic Map",
    layout="wide",
)

st.title("Startup Semantic Map")
st.caption("Semantic visualization of startup descriptions using precomputed embeddings, 2D projection, and clustering.")


DEFAULT_EMBEDDED_CSV = "startups_2026_embedded.csv"
FALLBACK_RAW_CSV = "startups_2026.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    embedded_path = Path(DEFAULT_EMBEDDED_CSV)

    if embedded_path.exists():
        df = pd.read_csv(embedded_path, encoding="utf-8-sig")
    else:
        st.warning(
            f"`{DEFAULT_EMBEDDED_CSV}` was not found. "
            f"Please run `preprocess_embeddings.py` first."
        )
        fallback_path = Path(FALLBACK_RAW_CSV)

        if not fallback_path.exists():
            st.error("No startup CSV file found.")
            st.stop()

        df = pd.read_csv(fallback_path, encoding="utf-8-sig")

    df.columns = [col.strip().lower() for col in df.columns]

    required_columns = {"name", "description", "location", "type"}
    missing = required_columns - set(df.columns)

    if missing:
        st.error(f"Missing required columns: {sorted(missing)}")
        st.stop()

    if "x" not in df.columns or "y" not in df.columns:
        st.error(
            "The CSV does not contain `x` and `y` coordinates. "
            "Run `preprocess_embeddings.py` to generate the embedded CSV."
        )
        st.stop()

    if "cluster" not in df.columns:
        df["cluster"] = "Unknown"

    if "cluster_label" not in df.columns:
        df["cluster_label"] = "Cluster " + df["cluster"].astype(str)

    for col in ["name", "description", "location", "type", "cluster_label"]:
        df[col] = df[col].fillna("").astype(str)

    return df


df = load_data()

total_startups = len(df)
total_clusters = df["cluster"].nunique()
top_location = df["location"].value_counts().idxmax() if total_startups else "N/A"
top_type = df["type"].value_counts().idxmax() if total_startups else "N/A"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Startups", total_startups)

with col2:
    st.metric("Clusters", total_clusters)

with col3:
    st.metric("Top location", top_location)

with col4:
    st.metric("Top type", top_type)


fig = px.scatter(
    df,
    x="x",
    y="y",
    color="cluster_label",
    hover_name="name",
    hover_data={
        "description": True,
        "location": True,
        "type": True,
        "cluster_label": True,
        "x": False,
        "y": False,
    },
    title="Startup Map by Semantic Similarity",
    height=750,
)

fig.update_traces(
    marker=dict(
        size=12,
        opacity=0.85,
        line=dict(width=0.5),
    )
)

fig.update_layout(
    xaxis_title="Dimension 1",
    yaxis_title="Dimension 2",
    legend_title="Cluster",
    margin=dict(l=20, r=20, t=60, b=20),
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Cluster overview")

cluster_summary = (
    df.groupby("cluster_label")
    .agg(
        startups=("name", "count"),
        examples=("name", lambda x: ", ".join(list(x.head(5)))),
        common_types=("type", lambda x: ", ".join(x.value_counts().head(3).index)),
    )
    .reset_index()
    .sort_values("startups", ascending=False)
)

st.dataframe(cluster_summary, use_container_width=True, hide_index=True)


st.subheader("Startup data")

search = st.text_input("Search startups", placeholder="Search by name, description, location, or type")

filtered_df = df.copy()

if search:
    search_lower = search.lower()
    filtered_df = filtered_df[
        filtered_df["name"].str.lower().str.contains(search_lower, na=False)
        | filtered_df["description"].str.lower().str.contains(search_lower, na=False)
        | filtered_df["location"].str.lower().str.contains(search_lower, na=False)
        | filtered_df["type"].str.lower().str.contains(search_lower, na=False)
        | filtered_df["cluster_label"].str.lower().str.contains(search_lower, na=False)
    ]

display_columns = [
    "name",
    "description",
    "location",
    "type",
    "cluster_label",
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
)