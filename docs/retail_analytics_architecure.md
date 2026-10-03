                    AWS S3
                      │
                      ▼
              Raw CSV Source Data
                      │
                      ▼
              ┌─────────────────┐
              │ Bronze Layer    │
              │ Raw Delta Data  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Incremental     │
              │ Loading         │
              │ Delta MERGE     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Silver Layer    │
              │ Clean           │
              │ Transform       │
              │ Validate        │
              │ Deduplicate     │
              └───────┬─────────┘
                      │
              ┌───────┴────────┐
              ▼                ▼
        ┌───────────┐    ┌───────────┐
        │ SCD Type 1│    │ SCD Type 2│
        │ Current   │    │ History   │
        └─────┬─────┘    └─────┬─────┘
              └────────┬───────┘
                       ▼
              ┌─────────────────┐
              │ Data Quality    │
              │ Validation      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Gold Reporting  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Databricks SQL  │
              │ / BI Dashboard  │
              └─────────────────┘