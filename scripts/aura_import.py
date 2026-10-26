from neo4j import GraphDatabase
import pandas as pd

URI = "neo4j+s://832fd729.databases.neo4j.io"
USERNAME = "neo4j"
PASSWORD = input("Enter Aura password: ")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD),
    encrypted=True
)

genes = pd.read_csv("data/graph/genes.tsv", sep="\t")
diseases = pd.read_csv("data/graph/diseases.tsv", sep="\t")
edges = pd.read_csv("data/graph/gene_disease_edges.tsv", sep="\t")

with driver.session() as session:

    print("Creating gene nodes...")
    for gid in genes['gene_id']:
        session.run(
            "MERGE (:Gene {gene_id:$gid})",
            gid=int(gid)
        )

    print("Creating disease nodes...")
    for did in diseases['disease_id']:
        session.run(
            "MERGE (:Disease {disease_id:$did})",
            did=str(did)
        )

    print("Creating relationships...")
    for _, row in edges.iterrows():
        session.run("""
            MATCH (g:Gene {gene_id:$gid})
            MATCH (d:Disease {disease_id:$did})
            MERGE (g)-[:ASSOCIATED_WITH {inference_score:$score}]->(d)
        """,
        gid=int(row['gene_id']),
        did=str(row['disease_id']),
        score=float(row['inference_score'])
        )

driver.close()

print("Import completed successfully.")
