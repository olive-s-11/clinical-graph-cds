# Clinical Data

This directory contains **raw and processed biomedical datasets** used by the *Clinical Graph CDS* project.

>  **Important**: Large datasets are intentionally **not tracked by Git**. They are recreated locally using scripts to keep the repository lightweight and reproducible.

---

## Data Source

### Comparative Toxicogenomics Database (CTD)

* **Dataset**: Gene–Disease Associations
* **Files used**:

  * `CTD_genes_diseases.tsv`
  * `all_gene_disease_associations.tsv`
* **Identifiers**:

  * Genes: NCBI Gene ID
  * Diseases: MeSH IDs

CTD integrates curated and inferred relationships between chemicals, genes, and diseases, making it suitable for graph-based clinical reasoning.

---

## Directory Structure

```text
clinical-data/
├── raw/            # downloaded datasets (ignored by git)
├── processed/      # derived datasets (ignored by git)
├── scripts/        # download & preprocessing scripts
└── README.md       # this file
```

---

## How to Reproduce the Data

### 1. Download CTD data

Place the downloaded CTD TSV files into:

```text
clinical-data/raw/
```

(Download links are provided on the CTD website under bulk downloads.)

---

### 2. Filter Gene–Disease Associations

Run the preprocessing script from the **repository root**:

```bash
python3 scripts/ctd/filter_ctd_gene_disease.py
```

This generates:

```text
clinical-data/processed/ctd_gene_disease_filtered.tsv
```

---

## Expected Output Statistics

* **Input rows**: ~122,721,284
* **Filtered rows kept**: ~109,560,842
* **Columns**:

  * `GeneSymbol`
  * `GeneID`
  * `DiseaseName`
  * `DiseaseID`
  * `DirectEvidence`
  * `InferenceChemical`
  * `InferenceScore`
  * `PubMedID`

If your numbers are close, the pipeline is working correctly.

---

## Why Data Is Not Committed

* GitHub file size limits
* Faster cloning and CI
* Standard practice in ML / bioinformatics
* Data can always be regenerated from source

---

## Next Steps

* Chunked ingestion into Neo4j / cuGraph
* GPU-accelerated graph construction
* Explainable disease–gene path queries

This setup ensures the project remains **clean, reproducible, and scalable**.