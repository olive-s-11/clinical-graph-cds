LOAD CSV FROM 'file:///gene_disease_edges_demo.tsv' AS row
FIELDTERMINATOR '\t'

MERGE (g:Gene {id: row[0]})
MERGE (d:Disease {id: row[1]})
MERGE (g)-[:ASSOCIATED_WITH {score: toFloat(row[2])}]->(d);