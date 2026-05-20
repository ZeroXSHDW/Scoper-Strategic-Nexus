# Regulatory Source Register

Project: Financial Regulatory Requirements Scoping Toolkit
Last updated: 2026-05-21

This register is intentionally limited to the official financial regulatory sources used by the Python pipeline in `regulatory_requirements/`. The pipeline should remain focused on DORA, FRB/FFIEC supervision, HKMA CFI/iCAST, PRA/Bank of England CBEST, and the three supplied ZeroDev scope PDFs.

Do not add broad security or compliance frameworks such as OWASP, NIST, ISO, PCI DSS, HIPAA, SOC 2, GDPR, FedRAMP, CIS, MITRE, or cloud-vendor guidance to this regulatory downloader unless the project scope is deliberately changed.

## Source Manifest

The machine-readable source manifest is:

`regulatory_requirements/sources.json`

The downloader writes source provenance and freshness results to:

`Penetration Testing - Scoping/Generated/Regulatory/download-log.json`

The database stores the same source metadata in:

`Penetration Testing - Scoping/Generated/Regulatory/index.db`

## Approved Official Sources

| Source ID | Framework | Authority | Official source | Local archive path | Access and refresh behavior |
|---|---|---|---|---|---|
| `dora-regulation-eu-2022-2554` | DORA | European Parliament and Council of the European Union | https://op.europa.eu/en/publication-detail/-/publication/0caf473a-85bd-11ed-9887-01aa75ed71a1/language-en | `Compliance Frameworks/International/DORA_RTS/DORA_Regulation_EU_2022_2554.pdf` | Public official Publications Office page and PDF. Refreshed by landing-page and archive SHA-256 comparison. |
| `dora-rts-ict-risk-management` | DORA | European Supervisory Authorities (EBA, EIOPA, ESMA) | https://www.esma.europa.eu/document/final-report-draft-rts-ict-risk-management-framework-and-simplified-ict-risk-management | `Compliance Frameworks/International/DORA_RTS/DORA_RTS_ICT_Risk_Management_Framework.pdf` | Public official ESA PDF via ESMA document library. Refreshed by landing-page and archive SHA-256 comparison. |
| `dora-rts-threat-led-penetration-testing` | DORA_TLPT | European Supervisory Authorities (EBA, EIOPA, ESMA) | https://www.esma.europa.eu/document/final-report-draft-rts-specifying-elements-related-threat-led-penetration-tests | `Compliance Frameworks/International/DORA_RTS/DORA_RTS_TLPT.pdf` | Public official ESA PDF via ESMA document library. Refreshed by landing-page and archive SHA-256 comparison. |
| `federal-reserve-sr-23-4-third-party-risk` | FRB_SUPERVISION | Board of Governors of the Federal Reserve System | https://www.federalreserve.gov/supervisionreg/srletters/SR2304.htm | `Compliance Frameworks/FRB/FRB_SR_23_4_Third_Party_Risk_Management.pdf` | Public direct PDF. Landing page is checked during refresh and archive is compared by SHA-256. |
| `ffiec-it-handbook-information-security` | FFIEC | Federal Financial Institutions Examination Council | https://www.ffiec.gov/sites/default/files/media/press-releases/2016/2016-%20it-handbook-information-security-booklet.pdf | `Compliance Frameworks/FFIEC/FFIEC_IT_Handbook_Information_Security.pdf` | Public direct PDF. HTML fallback may be used if automated PDF access fails. |
| `hkma-cfi-icast-overview` | HKMA_ICAST | Hong Kong Monetary Authority | https://www.hkma.gov.hk/eng/key-functions/international-financial-centre/fintech/research-and-applications/cybersecurity-fortification-initiative-cfi | `Compliance Frameworks/International/HKMA/HKMA_CFI_iCAST_Overview.html` | Public official landing page. Archived as HTML and refreshed by page hash. |
| `hkma-cfi-2-0-circular` | HKMA_ICAST | Hong Kong Monetary Authority | https://www.hkma.gov.hk/media/eng/doc/key-information/guidelines-and-circular/2020/20201103e1.pdf | `Compliance Frameworks/International/HKMA/HKMA_CFI_2_0_Circular.pdf` | Public direct PDF. Landing page is checked during refresh and archive is compared by SHA-256. |
| `hkma-cfi-2-0-annex` | HKMA_ICAST | Hong Kong Monetary Authority | https://www.hkma.gov.hk/media/eng/doc/key-information/guidelines-and-circular/2020/20201103e1a1.pdf | `Compliance Frameworks/International/HKMA/HKMA_CFI_2_0_Annex.pdf` | Public direct PDF. Landing page is checked during refresh and archive is compared by SHA-256. |
| `bank-of-england-cbest-implementation-guide` | PRA_CBEST | Bank of England / PRA | https://www.bankofengland.co.uk/financial-stability/operational-resilience-of-the-financial-sector/cbest-threat-intelligence-led-assessments-implementation-guide | `Compliance Frameworks/CBEST/CBEST_Implementation_Guide.pdf` | Public direct PDF. Landing page is checked during refresh and archive is compared by SHA-256. |

## Supplied Scope PDFs

These files are not downloaded from a regulator. They are workspace-supplied design and workflow inputs for the vendor pack.

| Source ID | Framework | Local file | Purpose |
|---|---|---|---|
| `supplied-global-enterprise-compliance-scope` | SCOPE_TEMPLATE | `../Global_Enterprise_Compliance_Scope.pdf` | Global enterprise scoping workflow target. |
| `supplied-regulated-bank-compliance-mapping` | SCOPE_TEMPLATE | `../Document_Regulated_Bank_Scope_compliance_mapping_v1_2026-04-23.pdf` | Regulated bank compliance mapping workflow target. |
| `supplied-premium-enterprise-compliance-scope` | SCOPE_TEMPLATE | `../Premium_Enterprise_Compliance_Scope.pdf` | Premium enterprise compliance scope template target. |

## Freshness Commands

Recommended publishing build:

```bash
python3 -m regulatory_requirements build-all --refresh
```

Refresh official sources without rebuilding artifacts:

```bash
python3 -m regulatory_requirements refresh-sources
```

Offline rebuild from cached/local sources:

```bash
python3 -m regulatory_requirements build-all --offline
```

Strict mode for CI or release gates:

```bash
python3 -m regulatory_requirements build-all --refresh --fail-on-download-error
```

## Status Notes

- `current`: online refresh succeeded and the archived source hash has not changed.
- `updated`: online refresh found a changed source and replaced the local archive.
- `downloaded`: source did not exist locally and was downloaded.
- `cached`: existing local source was used without an online refresh.
- `cached_refresh_failed`: a local archive exists, but the online refresh attempt failed.
- `fallback_available`: a configured fallback local source was used.
- `missing`: no usable local source exists.
- `workspace_supplied`: source is a user-supplied local PDF, not a regulator download.

Review source issues in the generated workbook `Source Issues` sheet before vendor release.
