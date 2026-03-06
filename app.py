import streamlit as st
import pandas as pd
import networkx as nx

st.title("Graph-based Clinical Decision Support Demo")

# Load dataset
file_path = "data/graph/gene_disease_edges_demo.tsv"
df = pd.read_csv(file_path, sep="\t")

# Show dataset columns (helps debugging)
st.write("Dataset columns:", df.columns)

# Assume first column = gene, second column = disease
gene_col = df.columns[0]
disease_col = df.columns[1]

# Build graph
G = nx.from_pandas_edgelist(
    df,
    source=gene_col,
    target=disease_col,
    create_using=nx.DiGraph()
)

# User input
gene = st.text_input("Enter Gene Symbol")

if gene:

    if gene not in G:
        st.error("Gene not found in graph")
    else:
        diseases = list(G.neighbors(gene))
        st.write("Associated Diseases:", diseases)
