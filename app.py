import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components

st.set_page_config(page_title="Clinical Graph CDS", layout="wide")

st.title("Graph-based Clinical Decision Support System")
st.write("Explore gene–disease associations using a graph-based reasoning model.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/graph_demo.csv")
    return df

df = load_data()

gene_id = st.text_input("Enter Gene ID (example: 10157)")

if st.button("Run CDS Reasoning"):

    try:
        gene_id = int(gene_id)
    except:
        st.warning("Please enter a valid Gene ID")
        st.stop()

    results = df[df["gene_id"] == gene_id]

    if results.empty:
        st.warning("No associations found for this gene")
        st.stop()

    # ranking
    results = results.sort_values(by="score", ascending=False)

    col1, col2 = st.columns([1,1])

    # ------------------------
    # Ranked disease results
    # ------------------------
    with col1:

        st.subheader("Ranked Disease Associations")

        ranked = results[["gene_symbol","disease_name","score"]]

        st.dataframe(
            ranked,
            use_container_width=True
        )

    # ------------------------
    # Explainability panel
    # ------------------------
    with col2:

        st.subheader("Explainable Reasoning")

        gene_symbol = results.iloc[0]["gene_symbol"]

        for _, row in results.head(5).iterrows():

            disease = row["disease_name"]
            score = row["score"]

            st.markdown(
                f"""
                **Path Explanation**

                Gene **{gene_symbol}**  
                ⟶ associated_with  
                Disease **{disease}**

                **Association Score:** {score}
                """
            )

    # ------------------------
    # Graph visualization
    # ------------------------
    st.subheader("Graph Visualization")

    net = Network(height="600px", width="100%", directed=True)

    gene_symbol = results.iloc[0]["gene_symbol"]

    net.add_node(
        gene_symbol,
        label=gene_symbol,
        color="blue",
        size=35
    )

    for _, row in results.head(20).iterrows():

        disease = row["disease_name"]
        score = row["score"]

        net.add_node(
            disease,
            label=disease,
            color="red"
        )

        net.add_edge(
            gene_symbol,
            disease,
            value=score if pd.notna(score) else 1
        )

    net.save_graph("graph.html")

    HtmlFile = open("graph.html", "r", encoding="utf-8")
    components.html(HtmlFile.read(), height=600)