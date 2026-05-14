# Security

## Scope

This repository contains prompt assets, workflow documentation, migration scripts, and generated Codex plugin output for legal workflows.

It does not ship production credentials, hosted services, or managed infrastructure. Do not commit live secrets, private matter data, exported client files, or machine-specific connector configuration.

## Reporting

If you discover a security issue in this repository or its generated plugin surface:

1. Do not open a public issue with exploit details.
2. Contact the repository owner privately through the maintainer contact listed on the public GitHub profile.
3. Include the affected file paths, impact, and reproduction steps.

## Sensitive Data Rules

- keep real connector URLs, keys, and tenant configuration in an untracked local `.env`
- treat legal documents, filings, contracts, and matter records as sensitive source material
- redact client names and identifiers from examples, fixtures, and screenshots unless they are already public and intentionally included
- never present generated outputs as verified legal conclusions without human review
