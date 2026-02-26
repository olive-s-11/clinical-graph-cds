CALL {
  LOAD CSV WITH HEADERS FROM 'file:///ctd_gene_disease_filtered.tsv'
  AS row
  FIELDTERMINATOR '\t'
  WITH row
  WHERE row.GeneID IS NOT NULL 
    AND row.DiseaseID IS NOT NULL 
    AND row.GeneID <> "" 
    AND row.DiseaseID <> ""

  MERGE (g:Gene {id: row.GeneID})
    SET g.symbol = row.GeneSymbol

  MERGE (d:Disease {id: row.DiseaseID})
    SET d.name = row.DiseaseName

  MERGE (g)-[r:ASSOCIATED_WITH]->(d)
  SET 
    r.inference_score = toFloat(row.InferenceScore),
    r.direct_evidence = row.DirectEvidence,
    r.pubmed_id = row.PubMedID

} IN TRANSACTIONS OF 1000 ROWS;