import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components

# Neo4j connection
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

st.title("Graph-based Clinical Decision Support System")

gene_id = st.text_input("Enter Gene ID")


def query_graph(tx, gene_id):

    query = """
    MATCH (g:Gene {gene_id:$gene_id})-[r:ASSOCIATED_WITH]-(d:Disease)
    RETURN g.symbol AS gene_symbol,
           g.gene_id AS gene_id,
           d.name AS disease,
           r.score AS score
    ORDER BY score DESC
    LIMIT 20
    """

    result = tx.run(query, gene_id=gene_id)

    return [record.data() for record in result]


if st.button("Search"):

    if gene_id.strip() == "":
        st.warning("Please enter a Gene ID")
        st.stop()

    with driver.session() as session:

        data = session.execute_read(query_graph, gene_id)

        if data:

            df = pd.DataFrame(data)

            st.subheader("Ranked Disease Associations")

            st.dataframe(df)

            # graph visualization
            net = Network(height="500px", width="100%", directed=True)

            gene_symbol = df.iloc[0]["gene_symbol"]
            gene_node = f"{gene_symbol} ({gene_id})"

            net.add_node(gene_node, color="blue", size=30)

            for _, row in df.iterrows():

                disease = row["disease"]
                score = row["score"]

                net.add_node(disease, color="red")

                if score:
                    net.add_edge(gene_node, disease, value=float(score), title=str(score))
                else:
                    net.add_edge(gene_node, disease)

            net.save_graph("graph.html")

            HtmlFile = open("graph.html", "r", encoding="utf-8")
            components.html(HtmlFile.read(), height=500)

        else:

            st.warning("No associations found")