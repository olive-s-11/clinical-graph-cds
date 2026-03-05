LOAD CSV WITH HEADERS FROM 'file:///ctd_gene_disease_filtered.tsv'
AS row
FIELDTERMINATOR '\t'

CALL {
    WITH row

    MERGE (g:Gene {gene_id: row.GeneID})
        ON CREATE SET g.symbol = row.GeneSymbol

    MERGE (d:Disease {disease_id: row.DiseaseID})
        ON CREATE SET d.name = row.DiseaseName

    MERGE (g)-[r:ASSOCIATED_WITH]->(d)
        ON CREATE SET
            r.inference_score = toFloat(row.InferenceScore),
            r.direct_evidence = row.DirectEvidence,
            r.inference_chemical = row.InferenceChemical,
            r.pubmed_id = row.PubMedID

} IN TRANSACTIONS OF 5000 ROWS;