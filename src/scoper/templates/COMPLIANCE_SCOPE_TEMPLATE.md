# Compliance Coverage Scope Template

**Document Type**: Compliance Scope Definition  
**Version**: 1.0  
**Date**: [DATE]  
**Classification**: Confidential  

---

## 1. Organization Overview

| Field | Details |
|-------|---------|
| **Organization Name** | |
| **Industry** | Financial Services / Banking |
| **Annual Revenue** | |
| **Number of Employees** | |
| **Primary Locations** | |
| **Data Centers/Cloud Regions** | |

---

## 2. Applicable Compliance Frameworks

### 2.1 Regulatory Compliance Requirements

| Framework | Applicable | Version | Assessment Date | Next Due Date |
| ---------- | ----------- | -------- | --------------- | --------------- |
| ☐ DORA | ☐ Yes ☐ No | | | |
| ☐ FRB Supervision | ☐ Yes ☐ No | | | |
| ☐ HKMA iCAST | ☐ Yes ☐ No | | | |
| ☐ PRA CBEST | ☐ Yes ☐ No | | | |

### 2.2 Supervisory/Regulatory Authorities

| Authority | Jurisdiction | Reporting Frequency | Last Engagement | Next Due |
|-----------|-------------|--------------------|-----------------|----------|
| | | | | |
| | | | | |

---

## 3. Data Classification Summary

| Classification | Description | Systems | Volume (Est.) | Compliance Impact |
|----------------|-------------|---------|---------------|------------------|
| **Trading Data** | Market execution, order books | | | FRB, PRA, HKMA |
| **Customer Financial** | Account balances, transactions | | | DORA, FRB |
| **SWIFT Messages** | Cross-border transaction records | | | Systemic Risk |
| **Confidential** | Business sensitive strategy | | | Internal policy |
| **Public** | Publicly available data | | | Minimal |

---

## 4. System Inventory by Compliance Domain

### 4.1 DORA Scope (EU Financial)

| Function Category | Classification | ICT Systems | Outsourced? |
|-----------------|---------------|-------------|-------------|
| **Critical Functions** | ☐ Critical ☐ Important | | ☐ Yes ☐ No |
| **Financial Services** | | | ☐ Yes ☐ No |
| **Payment Services** | | | ☐ Yes ☐ No |

**Supervisory Authority**:  
**Last TLPT**: ☐ Yes ☐ No ☐ Scheduled:  

---

### 4.2 FRB Supervision Scope (US)

| Component Type | System Name | Criticality | Service Model |
|---------------|-------------|-------------|---------------|
| **Core Banking** | | | ☐ On-Prem ☐ Cloud |
| **Payment Gateways**| | | |
| **Third-Party Risk**| | | |

**Current Assessment Status**: ☐ Satisfactory ☐ Needs Improvement ☐ Planning

---

### 4.3 HKMA iCAST Scope (Hong Kong)

| Domain | In Scope | Primary Systems | Dependency |
|--------|----------|-----------------|------------|
| **CFI Requirements** | ☐ Yes ☐ No | | |
| **Critical Internet Facing**| ☐ Yes ☐ No | | |
| **Core Financial Systems** | ☐ Yes ☐ No | | |

**Intelligence-Led Phase Complete**: ☐ Yes ☐ No

---

### 4.4 PRA CBEST Scope (UK)

| Threat Scenario | Primary Target | Critical Business Service | White Cell Contact |
|-----------------|----------------|---------------------------|--------------------|
| | | | |
| | | | |

**Phase**: ☐ Intelligence ☐ Execution ☐ Remediation

---

## 5. Network Architecture Overview

### 5.1 Network Zones and Segmentation

| Zone | Purpose | IP Range | Controls | Compliance Boundary |
|------|---------|----------|----------|---------------------|
| **Core Banking** | Ledger and balances | | Firewall, MFA, VLAN | FRB / PRA |
| **Trading DMZ** | Low latency execution | | WAF, IDS/IPS | HKMA / FRB |
| **Payment Gateways**| SWIFT/SEPA integration| | Network isolation | DORA / Systemic |
| **Internal Corp** | General business | | Standard controls | All |
| **Cloud VPC** | Cloud workloads | | Security groups | Framework-specific |

### 5.2 Third-Party ICT Provider Connections

| Provider | Service Type | Data Shared | Compliance Coverage | Contract Review |
|----------|-------------|-------------|---------------------|----------------|
| | | | | ☐ Yes ☐ No |
| | | | | ☐ Yes ☐ No |

---

## 6. Testing Requirements by Framework

### 6.1 Summary Matrix

| Framework | External Test | Internal Test | App Test | Cloud Test | Segmentation Test | Social Eng | Threat-Led / RT |
|-----------|--------------|--------------|----------|------------|-------------------|------------|-----------------|
| **DORA** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | TLPT |
| **FRB** | ✓ | ✓ | ✓ | ✓ | ✓ | Optional | Expected |
| **HKMA** | ✓ | ✓ | ✓ | ✓ | - | Optional | iCAST |
| **PRA** | ✓ | ✓ | ✓ | ✓ | ✓ | Optional | CBEST |

### 6.2 Frequency Requirements

| Framework | Minimum Frequency | Additional Triggers |
|-----------|------------------|-------------------|
| **DORA Basic** | Annual | - |
| **DORA TLPT** | Every 3 years | Competent authority may adjust |
| **FRB Supervision**| Annual | Significant changes |
| **HKMA iCAST** | Defined by CFI tier | Significant changes |
| **PRA CBEST** | Every 2-3 years | Competent authority guidance |

---

## 7. Tester Qualification Requirements

| Framework | Independence Required | Certification Required | Specific Certification |
|-----------|---------------------|----------------------|----------------------|
| **DORA TLPT** | Required (external) | Required | Qualified tester standards |
| **FRB** | Required | Recommended | Threat-Intel/Red Team verified |
| **HKMA iCAST**| Required | Required | CREST / Relevant provider |
| **PRA CBEST** | Required | Required | CREST / CSCS |

---

## 8. Deliverables Mapping

### 8.1 Required Deliverables by Framework

| Deliverable | DORA | FRB | HKMA | PRA |
|-------------|------|-----|------|-----|
| Executive Summary | ✓ | ✓ | ✓ | ✓ |
| Technical Report | ✓ | ✓ | ✓ | ✓ |
| Finding Details with CVSS | ✓ | ✓ | ✓ | ✓ |
| Threat Intelligence Report| TLPT | Optional | iCAST | CBEST |
| Finding-to-Control Mapping | ✓ | ✓ | ✓ | ✓ |
| Retest Evidence | ✓ | ✓ | ✓ | ✓ |

---

## 9. Risk Prioritization

### 9.1 Severity Classification

| Rating | CVSS Range | Definition | Generic SLA |
|--------|------------|-----------|------------|
| **Critical** | 9.0-10.0 | Exploitable, wide impact | Immediate |
| **High** | 7.0-8.9 | Exploitable, significant impact | 7 days |
| **Medium** | 4.0-6.9 | Potentially exploitable | 30 days |
| **Low** | 0.1-3.9 | Difficult to exploit | 90 days |
| **Informational** | N/A | Observation | None |

### 9.2 Framework-Specific Adjustments

| Framework | Critical Definition | High Definition |
|-----------|-------------------|----------------|
| **DORA** | Threat to critical functions | Significant security weakness |
| **FRB** | Systemic risk to core banking | Major risk to availability/integrity |
| **HKMA** | Compromise of critical systems | Substantial access breach |
| **PRA** | Successful CBEST scenario | High impact on CBS |

---

## 10. Sign-Off

### Client Certification

I certify that the compliance scope described in this document is accurate and complete.

**Name**: _________________________

**Title**: _________________________

**Signature**: _________________________

**Date**: _________________________

### Testing Provider Acceptance

**Name**: _________________________

**Title**: _________________________

**Signature**: _________________________

**Date**: _________________________

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial version |
