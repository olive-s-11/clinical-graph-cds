"""
Graph schema definitions for the Clinical Graph CDS project.

This file defines:
- Node types (Gene, Disease)
- Edge types (ASSOCIATED_WITH)
- Canonical property names

This schema is intentionally backend-agnostic:
- Can be used with Neo4j
- Can be used with RAPIDS / cuGraph
"""

# ---------- Node labels ----------

GENE_NODE = "Gene"
DISEASE_NODE = "Disease"

# ---------- Node properties ----------

GENE_ID = "gene_id"          # NCBI GeneID (int)
DISEASE_ID = "disease_id"    # MeSH ID (string)

# ---------- Edge types ----------

GENE_DISEASE_EDGE = "ASSOCIATED_WITH"

# ---------- Edge properties ----------

EDGE_SCORE = "score"         # CTD inference score (float)
EDGE_SOURCE = "source"       # Dataset name (e.g., "CTD")

# ---------- Dataset metadata ----------

CTD_SOURCE_NAME = "CTD"
