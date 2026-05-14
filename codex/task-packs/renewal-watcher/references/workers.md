# Renewal Watcher Workers

- `repo-reader`
  - reads repository metadata and supporting contract context
- `deadline-calculator`
  - computes candidate cancel-by, renewal, and notice dates
- `alert-writer`
  - owns final write scope for the alert memo
