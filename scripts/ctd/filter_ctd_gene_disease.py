#!/usr/bin/env python3

import sys
from pathlib import Path

RAW_FILE = Path("clinical-data/raw/CTD_genes_diseases.tsv")
OUT_FILE = Path("clinical-data/processed/ctd_gene_disease_filtered.tsv")

MIN_SCORE = 4.0

def main():
    if not RAW_FILE.exists():
        print(f"ERROR: {RAW_FILE} not found", file=sys.stderr)
        sys.exit(1)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    kept = 0

    with RAW_FILE.open("r", encoding="utf-8") as fin, \
         OUT_FILE.open("w", encoding="utf-8") as fout:

        # header
        fout.write(
            "GeneSymbol\tGeneID\tDiseaseName\tDiseaseID\tDirectEvidence\t"
            "InferenceChemical\tInferenceScore\tPubMedID\n"
        )


        for line in fin:
            if line.startswith("#"):
                continue

            total += 1
            parts = line.rstrip("\n").split("\t")

            # Defensive check
            if len(parts) < 7:
                continue

            gene_symbol = parts[0]
            gene_id = parts[1]
            disease_name = parts[2]
            disease_id = parts[3]
            direct_evidence = parts[4]
            chemical = parts[5]
            score_str = parts[6]
            pubmed = parts[8] if len(parts) > 8 else ""


            try:
                score = float(score_str)
            except ValueError:
                continue

            if score < MIN_SCORE:
                continue

            fout.write(
                f"{gene_symbol}\t{gene_id}\t{disease_name}\t{disease_id}\t"
                f"{direct_evidence}\t{chemical}\t{score}\t{pubmed}\n"
            )

            kept += 1

            if kept % 1_000_000 == 0:
                print(f"Kept {kept:,} rows...", file=sys.stderr)

    print("Done.")
    print(f"Total rows read : {total:,}")
    print(f"Rows kept       : {kept:,}")
    print(f"Output written  : {OUT_FILE}")

if __name__ == "__main__":
    main()
