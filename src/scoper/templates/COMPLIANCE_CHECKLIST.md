# Penetration Testing Compliance Checklist

**Organization**: [Name]  
**Assessment Period**: [Date Range]  
**Completed By**: [Name/Role]  
**Date Completed**: [Date]  

---

## Pre-Assessment Planning

### 1.1 Compliance Identification

- [ ] Identified all applicable banking compliance frameworks (DORA, FRB, HKMA, PRA)
- [ ] Documented specific supervisory authority requirements
- [ ] Identified critical business services (CBS) and underlying ICT systems
- [ ] Mapped core financial data types to compliance requirements
- [ ] Confirmed whether Threat-Led Penetration Testing (TLPT/CBEST/iCAST) is mandated

### 1.2 Stakeholder Identification

- [ ] Legal counsel and regulatory liaison informed
- [ ] Chief Risk Officer / Compliance officer involved
- [ ] IT security team engaged
- [ ] Business unit owners for Critical Functions identified
- [ ] White Cell / Control Group established (if TLPT/CBEST)

### 1.3 Budget and Timeline

- [ ] Budget approved for penetration testing and threat intelligence
- [ ] Timeline aligned with regulatory submission deadlines
- [ ] Resource allocation confirmed (including internal blue team if applicable)
- [ ] Executive sponsor secured

---

## Scope Definition

### 2.1 Asset Inventory

- [ ] Complete asset inventory for critical financial systems documented
- [ ] Asset owners identified
- [ ] Financial data classification completed (Market, Customer, SWIFT)
- [ ] System boundaries defined for each regulatory framework

### 2.2 Data Flow Mapping

- [ ] Data flows documented for sensitive transaction paths
- [ ] Processing, storage, and transmission identified
- [ ] Third-party ICT provider dependencies mapped
- [ ] Cross-border data transfers and data residency constraints identified

### 2.3 Network Architecture

- [ ] Network diagrams updated
- [ ] Segmentation boundaries for core banking identified
- [ ] Cloud architecture and multi-tenant isolation documented
- [ ] On-premise and trading DMZ infrastructure mapped

---

## Framework-Specific Requirements

### 3.1 DORA Checklist (EU)

| Requirement | Description | Applicable | Status |
|------------|-------------|-----------|--------|
| Art. 24 | General digital resilience testing program | ☐ | ☐ Complete ☐ N/A |
| Art. 25 | Vulnerability assessments and scanning | ☐ | ☐ Complete ☐ N/A |
| Art. 26 | TLPT performed (every 3 years) | ☐ | ☐ Complete ☐ N/A |
| Art. 26 | Critical functions (CBS) covered | ☐ | ☐ Complete ☐ N/A |
| Art. 26 | External tester qualifications met | ☐ | ☐ Complete ☐ N/A |
| Art. 26 | TIBER-EU methodology aligned | ☐ | ☐ Complete ☐ N/A |
| Art. 28 | Third-party ICT provider inclusion | ☐ | ☐ Complete ☐ N/A |
| Remediation | Remediation plans implemented | ☐ | ☐ Complete ☐ N/A |

### 3.2 PRA CBEST Checklist (UK)

| Requirement | Description | Applicable | Status |
|------------|-------------|-----------|--------|
| Planning | Scoping and engagement planning complete | ☐ | ☐ Complete ☐ N/A |
| Intel | Targeted threat intelligence gathered | ☐ | ☐ Complete ☐ N/A |
| Scenario | Threat scenarios approved by White Cell | ☐ | ☐ Complete ☐ N/A |
| Execution | Red Team execution completed | ☐ | ☐ Complete ☐ N/A |
| Detection | Blue Team detection logging retained | ☐ | ☐ Complete ☐ N/A |
| Replay | Purple Team / replay phase conducted | ☐ | ☐ Complete ☐ N/A |
| Reporting | CBEST report finalized for PRA | ☐ | ☐ Complete ☐ N/A |
| Remediation | Remediation plan agreed with regulator | ☐ | ☐ Complete ☐ N/A |

### 3.3 HKMA iCAST Checklist (Hong Kong)

| Requirement | Description | Applicable | Status |
|------------|-------------|-----------|--------|
| CFI Mapping | Applicable CFI tier determined | ☐ | ☐ Complete ☐ N/A |
| Intelligence | Threat intelligence phase complete | ☐ | ☐ Complete ☐ N/A |
| Simulation | Attack simulation executed | ☐ | ☐ Complete ☐ N/A |
| Red Team | CREST-certified testers utilized | ☐ | ☐ Complete ☐ N/A |
| Report | iCAST report submitted to HKMA | ☐ | ☐ Complete ☐ N/A |
| Defenses | Cybersecurity resilience posture verified | ☐ | ☐ Complete ☐ N/A |

### 3.4 FRB Supervision Checklist (US)

| Requirement | Description | Applicable | Status |
|------------|-------------|-----------|--------|
| SR 13-1 | Independent audit/testing aligned | ☐ | ☐ Complete ☐ N/A |
| Perimeter | External network penetration testing | ☐ | ☐ Complete ☐ N/A |
| Internal | Internal network and segmentation testing | ☐ | ☐ Complete ☐ N/A |
| App Sec | Application security testing (Core Banking) | ☐ | ☐ Complete ☐ N/A |
| Findings | Risk-based prioritization of findings | ☐ | ☐ Complete ☐ N/A |
| Board | Results reported to risk committee/board | ☐ | ☐ Complete ☐ N/A |

---

## Testing Execution

### 4.1 Pre-Testing Activities

- [ ] Authorization letters and NDAs signed
- [ ] Rules of engagement defined and approved by White Cell
- [ ] Emergency contacts established
- [ ] Kill switch procedures documented for production environments
- [ ] Testing window scheduled (aligned with trading hours/batch processing)
- [ ] IP whitelisting completed (if applicable)
- [ ] Testing credentials provisioned safely

### 4.2 Testing Coverage

- [ ] External reconnaissance performed
- [ ] External vulnerability identification completed
- [ ] External exploitation attempted (authorized)
- [ ] Internal reconnaissance and AD pathing performed
- [ ] Lateral movement assessment completed
- [ ] Web application testing performed (Core Banking)
- [ ] API security testing performed (Payment Gateways)
- [ ] Cloud configuration review completed
- [ ] SWIFT / Payment system segmentation testing completed (if applicable)

### 4.3 Documentation

- [ ] All findings documented with evidence
- [ ] Screenshots captured and preserved (redacting live customer data)
- [ ] CVSS scores assigned
- [ ] Systemic banking impact assessed
- [ ] Remediation steps documented
- [ ] Finding-to-control mapping completed

---

## Remediation

### 5.1 Remediation Tracking

| Finding ID | Title | Severity | Owner | Due Date | Status |
|-----------|-------|---------|-------|----------|--------|
| | | | | | |
| | | | | | |

### 5.2 Remediation Verification

- [ ] Critical findings remediated
- [ ] Retesting performed for critical/high findings
- [ ] Remediation evidence documented for regulators
- [ ] Risk register updated
- [ ] Board / Committee attestation updated

---

## Compliance Evidence Package

### 6.1 Required Documentation

| Document | DORA | FRB | HKMA | PRA |
|---------|------|-----|------|-----|
| Scope Statement | ☐ | ☐ | ☐ | ☐ |
| Rules of Engagement | ☐ | ☐ | ☐ | ☐ |
| Threat Intelligence Report | ☐ | - | ☐ | ☐ |
| Executive Summary | ☐ | ☐ | ☐ | ☐ |
| Technical Report | ☐ | ☐ | ☐ | ☐ |
| Finding Details | ☐ | ☐ | ☐ | ☐ |
| Remediation Plan | ☐ | ☐ | ☐ | ☐ |
| Retest Report | ☐ | ☐ | ☐ | ☐ |

### 6.2 Regulatory Attestation

| Framework | Submission Required | Target Submission Date | Next Cycle Due |
|----------|--------------------|------------------------|----------------|
| DORA TLPT | ☐ | | |
| FRB | ☐ | | |
| HKMA iCAST| ☐ | | |
| PRA CBEST | ☐ | | |

---

## Sign-Off

**Completed By**: _________________________

**Title**: _________________________

**Signature**: _________________________

**Date**: _________________________

**Reviewed By**: _________________________

**Title**: _________________________

**Signature**: _________________________

**Date**: _________________________

---

## Appendix: Finding Summary

### Critical Findings

| Finding ID | Title | Affected CBS | CVSS | Remediation Status |
|-----------|-------|-------------|------|------------------|
| | | | | |

### Statistics

| Metric | Count |
|--------|-------|
| Total Findings | |
| Critical | |
| High | |
| Medium | |
| Low | |
| Informational | |
| Remediated | |
| In Progress | |
| Open | |
