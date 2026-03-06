import streamlit as st
import pandas as pd
import networkx as nx

st.title("Graph-based Clinical Decision Support Demo")

# Load dataset (NO HEADER)
file_path = "data/graph/gene_disease_edges_demo.tsv"

df = pd.read_csv(
    file_path,
    sep="\t",
    header=None,
    names=["gene", "disease", "score"]
)

st.write("Dataset preview")
st.dataframe(df.head())

# Build graph
G = nx.from_pandas_edgelist(
    df,
    source="gene",
    target="disease",
    edge_attr="score",
    create_using=nx.DiGraph()
)

# Input
gene = st.text_input("Enter Gene ID")

if gene:

    # convert to int because dataset gene IDs are integers
    try:
        gene = int(gene)
    except:
        st.error("Gene ID must be a number")
        st.stop()

    if gene not in G:
        st.error("Gene not found in graph")
    else:
        diseases = list(G.neighbors(gene))
        st.write("Associated Diseases:", diseases)