CREATE CONSTRAINT gene_id_unique IF NOT EXISTS
FOR (g:Gene)
REQUIRE g.gene_id IS UNIQUE;

CREATE CONSTRAINT disease_id_unique IF NOT EXISTS
FOR (d:Disease)
REQUIRE d.disease_id IS UNIQUE;