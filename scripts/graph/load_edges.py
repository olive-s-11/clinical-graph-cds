"""
Edge loader for Gene–Disease associations.

Reads a TSV edge list and yields chunks that can be:
- Inserted into Neo4j
- Converted to cuGraph DataFrames
"""

from pathlib import Path
import csv

from scripts.graph.schema import (
    GENE_ID,
    DISEASE_ID,
    EDGE_SCORE,
    EDGE_SOURCE,
    CTD_SOURCE_NAME,
)


def load_gene_disease_edges(
    edge_file: Path,
    chunk_size: int = 1_000_000,
):
    """
    Generator that yields gene–disease edges in chunks.

    Each yielded item is a list of dicts:
    {
        gene_id: int,
        disease_id: str,
        score: float,
        source: "CTD"
    }
    """

    buffer = []

    with edge_file.open("r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")

        for row in reader:
            gene_id, disease_id, score = row

            buffer.append({
                GENE_ID: int(gene_id),
                DISEASE_ID: disease_id,
                EDGE_SCORE: float(score),
                EDGE_SOURCE: CTD_SOURCE_NAME,
            })

            if len(buffer) >= chunk_size:
                yield buffer
                buffer = []

        if buffer:
            yield buffer
