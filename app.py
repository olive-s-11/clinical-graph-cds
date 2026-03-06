import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import streamlit.components.v1 as components

# ---------------------------
# Neo4j Connection
# ---------------------------

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


# ---------------------------
# Query Neo4j
# ---------------------------

def find_diseases_from_gene(gene_id):

    query = """
    MATCH (g:Gene {gene_id:$gene_id})-[r:INVOLVED_IN]->(d:Disease)
    RETURN g.gene_id AS gene,
           d.name AS disease,
           r.score AS score
    ORDER BY score DESC
    LIMIT 20
    """

    with driver.session() as session:
        result = session.run(query, gene_id=gene_id)
        return [record.data() for record in result]


# ---------------------------
# Graph Visualization
# ---------------------------

def visualize_paths(results):

    net = Network(height="600px", width="100%", notebook=False)

    for r in results:

        gene = r["gene"]
        disease = r["disease"]
        score = r["score"]

        net.add_node(gene, label=gene, color="blue")
        net.add_node(disease, label=disease, color="red")

        net.add_edge(gene, disease, value=score)

    net.save_graph("graph.html")

    HtmlFile = open("graph.html", "r", encoding="utf-8")
    components.html(HtmlFile.read(), height=600)


# ---------------------------
# Streamlit UI
# ---------------------------

st.title("Clinical Graph-based CDS")

st.write("Explore gene–disease relationships using a graph database.")

gene_input = st.text_input("Enter Gene ID")

if st.button("Find Diseases"):

    results = find_diseases_from_gene(gene_input)

    if not results:

        st.warning("No diseases found for this gene.")

    else:

        st.subheader("Ranked Diseases")

        for r in results:
            st.write(
                f"Disease: {r['disease']} | Score: {r['score']}"
            )

        st.subheader("Graph Visualization")

        visualize_paths(results)