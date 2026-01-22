# PERLA Notebooks

This collection of Jupyter notebooks provides comprehensive analysis tools for perovskite solar cell data from **PERLA** (Perovskite Living Archive) in NOMAD.

## Overview

PERLA is a continuously updated database of perovskite solar cell performance data, combining both legacy human-curated entries and modern LLM-extracted entries from scientific literature.

## Getting Started

### Prerequisites

1. **Query the database first**: Start with the query notebook to generate the required data file
2. **Install dependencies**: Ensure you have the necessary Python packages installed from the souce repositroy. uv is recommended to be used.

### Workflow

1. **Generate the dataset** (required first step):
   - Run [query-perovskite-database.ipynb](query-perovskite-database.ipynb) to download data from NOMAD and create `perovskite_solar_cell_database.parquet`
   - ⚠️ **Note**: This query may take up to 1 hour due to API rate limits

2. **Analyze the data**: Once you have the parquet file, you can run any of the analysis notebooks

## Notebooks

### Data Retrieval
- **[query-perovskite-database.ipynb](query-perovskite-database.ipynb)** - Download perovskite solar cell data from NOMAD and save as parquet file *(run this first)*

### Performance and Evolution Analysis
- **[performance-evolution.ipynb](performance-evolution.ipynb)** - Temporal evolution of power conversion efficiency and device performance metrics
- **[architecture-evolution.ipynb](architecture-evolution.ipynb)** - Device architecture trends (n-i-p vs. p-i-n) and material layer evolution
- **[bandgap-evolution.ipynb](bandgap-evolution.ipynb)** - Temporal changes in bandgap values and absorber compositions

### Diversity and Discovery
- **[diversity-analysis.ipynb](diversity-analysis.ipynb)** - Material diversity evolution using entropy metrics and Heap's law analysis

### Machine Learning Applications
- **[crabnet-perovskite-bandgap-prediction.ipynb](crabnet-perovskite-bandgap-prediction.ipynb)** - Composition-based bandgap prediction using CrabNet neural network
- **[ml-distribution-shift-case-study.ipynb](ml-distribution-shift-case-study.ipynb)** - Analysis of distribution shift challenges in ML models for perovskite property prediction

### Data Quality and Validation
- **[physics_filter.ipynb](physics_filter.ipynb)** - Physics consistency validation comparing legacy database vs. PERLA pipeline
- **[perla-evals-analysis.ipynb](perla-evals-analysis.ipynb)** - Evaluation metrics for PERLA LLM extraction pipeline performance

### Automation and Tools
- **[perovskite-paperbot-plot.ipynb](perovskite-paperbot-plot.ipynb)** - Visualization of automated literature extraction pipeline filtering steps

## Data Structure

The `perovskite_solar_cell_database.parquet` file contains structured data including:
- Device performance metrics (PCE, Voc, Jsc, FF)
- Material compositions (absorber, ETL, HTL)
- Device architecture information
- Publication metadata
- Extraction source (Manual Entry vs. LLM Extracted)