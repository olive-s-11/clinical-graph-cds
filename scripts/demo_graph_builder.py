import pandas as pd
import networkx as nx

df = pd.read_csv("data/demo_graph_dataset.csv")

G = nx.DiGraph()

for _, row in df.iterrows():
    symptom = row["symptom"]
    disease = row["disease"]
    drug = row["drug"]

    G.add_edge(symptom, disease, relation="causes")
    G.add_edge(disease, drug, relation="treated_by")

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

symptom_query = "Fever"

if symptom_query in G:
    diseases = list(G.successors(symptom_query))
    for d in diseases:
        drugs = list(G.successors(d))
        print("\nSymptom:", symptom_query)
        print("Disease:", d)
        print("Drug:", drugs)
