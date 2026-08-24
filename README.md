# Scoper Strategic Nexus — Financial Regulatory Requirements CLI

This repository is a minimal Python CLI for generating the two approved vendor regulatory scoping deliverables:

- `Penetration Testing - Scoping/Generated/Regulatory/regulatory_requirements_reference_latest.xlsx`
- `Penetration Testing - Scoping/Generated/Regulatory/regulatory_vendor_questionnaire_template_latest.docx`

The CLI downloads or uses cached official source material, builds a local SQLite requirements index, and exports the XLSX reference workbook and concise DOCX vendor questionnaire from the same indexed data.

## Scope

The source manifest is intentionally narrow:

| Regulatory family | Covered material |
|---|---|
| EU DORA | DORA Regulation (EU) 2022/2554 plus ICT risk and TLPT RTS material |
| US FRB and FFIEC | Federal Reserve SR 23-4 and FFIEC Information Security material |
| HKMA CFI / iCAST | HKMA CFI 2.0 and iCAST source material |
| PRA / Bank of England CBEST | CBEST implementation guide material |
| Supplied scope templates | Three local ZeroDev scope PDFs used as questionnaire design inputs |

Broad security frameworks such as OWASP, NIST, ISO, PCI, HIPAA, SOC 2, GDPR, FedRAMP, and cloud vendor guidance are not part of this generator unless the manifest is deliberately changed.

## Prerequisites

Use Python 3.12, the exact interpreter declared in [`.python-version`](.python-version).

A refresh requires network access to the HTTPS sources listed in `regulatory_requirements/sources.json`; offline builds use the reviewed source archives already present in the repository. No credentials are required for the public-source workflow.

## Installation and setup

Use Python 3.12, the exact verification runtime in
[`.python-version`](.python-version).

```bash
python3 -m pip install -r requirements.txt
```

Editable package install is optional:

```bash
python3 -m pip install -e .
```

## Data and provenance

The source manifest is the single source of truth for authorities, URLs, local cache paths, parser profiles, and provenance notes. `build-all --offline` is deterministic against the reviewed local cache; `build-all --refresh` may update cached source material only after HTTPS validation and records the resulting source status and hashes.

The SQLite index, provenance logs, dated exports, and intermediate build files are local derived state. `clean` removes those temporary outputs while preserving the two approved `latest` deliverables. Do not commit credentials, private scope material, generated caches, or machine-specific paths.

## Build

Use the cached source files already in the repository:

```bash
python3 -m regulatory_requirements build-all --offline
```

Refresh official sources before building:

```bash
python3 -m regulatory_requirements build-all --refresh
```

If installed with `pip install -e .`, the console command is also available:

```bash
regulatory-requirements build-all --refresh
```

The build writes a local `index.db`, provenance log, dated outputs, and latest output copies under `Penetration Testing - Scoping/Generated/Regulatory/`. Source archives, provenance logs, and the SQLite index use same-directory atomic replacement; a failed parse does not destroy the previous index. Git tracks only the two latest approved deliverables.

Remove local-only build files while keeping the two approved latest deliverables:

```bash
python3 -m regulatory_requirements clean
```

## Test

```bash
PYTHONPATH=. python3 -m pytest -q
# Alternative standard-library test command:
python3 -m unittest tests/test_regulatory_requirements.py
python3 -m regulatory_requirements clean
./scripts/audit-git-tracking.sh --strict-local
```

## Repository Layout

| Path | Purpose |
|---|---|
| `regulatory_requirements/` | Python downloader, indexer, XLSX exporter, and DOCX exporter |
| `regulatory_requirements/sources.json` | Approved source manifest |
| `tests/` | Unit and artifact structure tests |
| `requirements.txt` | Runtime dependency ranges for local use |
| `requirements-ci.in` / `requirements-ci.txt` | Hash-locked Python 3.12 verification graph |
| `SOURCE_DOCUMENTS.md` | Human-readable source register |
| `Penetration Testing - Scoping/Compliance Frameworks/` | Cached official source archives required for offline rebuilds |
| `Penetration Testing - Scoping/Generated/Regulatory/` | Approved latest XLSX and DOCX deliverables |
| `scripts/audit-git-tracking.sh` | Publication hygiene check |

## Publishing Checklist

1. Run `python3 -m regulatory_requirements build-all --refresh`.
2. Run `PYTHONPATH=. python3 -m pytest -q` (or `python3 -m unittest tests/test_regulatory_requirements.py`).
3. Run `python3 -m regulatory_requirements clean`.
4. Run `./scripts/audit-git-tracking.sh --strict-local`.
5. Confirm the two `latest` deliverables are the intended files to publish.
6. Keep local databases, dated generated files, logs, caches, dependencies, and OS metadata untracked.

## Verification

The pull-request gate reads the exact Python version from `.python-version`,
installs the hash-locked verification graph, checks dependency consistency,
audits installed dependencies, builds a wheel without a second unpinned build
environment, and runs the fixture-backed test suite:

```bash
git diff --check
python3 -m pip install --require-hashes -r requirements-ci.txt
python3 -m pip install --no-deps --no-build-isolation -e .
python3 -m pip check
python3 -m pip_audit --progress-spinner off
python3 -m build --wheel --no-isolation
PYTHONPATH=. python3 -m pytest -q
```

Refresh the reviewed graph only after checking dependency changes:

```bash
uv pip compile requirements-ci.in --python-version 3.12 --universal \
  --generate-hashes --output-file requirements-ci.txt
```

## License

MIT — see [LICENSE](LICENSE)

## Contributing

Keep the package deterministic and fixture-backed. Run the verification commands above and see [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Security

Report vulnerabilities privately using [SECURITY.md](SECURITY.md). Do not publish sensitive scope definitions, credentials, or local paths.

## Features

- Deterministic strategic-scope models with fixture-backed output.
- Package, wheel, dependency, and test gates suitable for reviewable releases.

## Configuration

Keep environment-specific settings outside the repository unless they are
non-secret fixtures. Review the package's documented configuration and
publishing checklist before changing output paths or release artifacts.

## Troubleshooting

Run `python3 -m pip check` first, then rerun the narrowest failing fixture or
build command. Do not replace a failing fixture with a live service call just
to obtain a green result.
