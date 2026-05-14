# Diligence Grid Workers

- `doc-reader`
  - scopes the folder, samples documents, and prepares extraction batches
- `extractor`
  - extracts per-document values, states, quotes, and locations
- `normalizer`
  - reconciles option sets, format drift, and implausible values
- `grid-writer`
  - owns final write scope for the CSV outputs and summary memo
