# Asset Inventory Template

**Project**: [Project Name]  
**Date**: [Date]  
**Owner**: [Name]  
**Classification**: Confidential  

---

## 1. Asset Registry

### 1.1 External Assets (Internet-Facing)

| Asset ID | Name | Type | IP Address | URL/Domain | Owner | Data Sensitivity | Tier | Last Security Review |
|----------|------|------|------------|------------|-------|------------------|------|----------------------|
| EXT-001 | | | | | | | | |
| EXT-002 | | | | | | | | |
| EXT-003 | | | | | | | | |
| EXT-004 | | | | | | | | |
| EXT-005 | | | | | | | | |

**Asset Type Legend**: Web Server | DNS | Email | VPN | CDN | Cloud LB | API | Trade Gateway | Open Banking API
**Data Sensitivity Legend**: Public | Internal | Confidential | Restricted | Critical Financial
**Tier Legend**: 1 = Critical (CBS) | 2 = Important | 3 = Standard

### 1.2 Internal Network Assets

| Asset ID | Name | Type | IP Address | MAC Address | VLAN/Subnet | Owner | Data Sensitivity | Tier |
|----------|------|------|------------|-------------|-------------|-------|------------------|------|
| INT-001 | | | | | | | | |
| INT-002 | | | | | | | | |
| INT-003 | | | | | | | | |
| INT-004 | | | | | | | | |
| INT-005 | | | | | | | | |

**Asset Type Legend**: Server | Workstation | Network Device | Database | Mainframe | Payment Gateway | Core Banking

### 1.3 Application Assets

| App ID | Name | Type | URL/Endpoint | Platform | Auth Method | Users | Data Sensitivity | Owner | Tier |
|--------|------|------|--------------|----------|-------------|-------|------------------|-------|------|
| APP-001 | | | | | | | | | |
| APP-002 | | | | | | | | | |
| APP-003 | | | | | | | | | |
| APP-004 | | | | | | | | | |
| APP-005 | | | | | | | | | |

**Application Type**: Web | Mobile | API | Desktop | Embedded | SaaS (Third-Party ICT)
**Authentication Method**: None | Basic Auth | Form-based | OAuth 2.0 | SAML | LDAP | API Key | JWT | Multi-factor

### 1.4 Cloud Infrastructure

| Cloud ID | Provider | Account/Project | Region | Services | Owner | Tier |
|----------|----------|-----------------|--------|----------|-------|------|
| CLD-001 | AWS/Azure/GCP | | | | | |
| CLD-002 | AWS/Azure/GCP | | | | | |
| CLD-003 | AWS/Azure/GCP | | | | | |

**Services**: Compute | Storage | Database | Networking | Security | Analytics | Mainframe as a Service

### 1.5 Mobile Applications

| Mobile ID | App Name | Platform | Version | Backend URL | Owner | App Store | Tier |
|-----------|----------|----------|---------|-------------|-------|-----------|------|
| MOB-001 | | iOS/Android | | | | Yes/No | |
| MOB-002 | | iOS/Android | | | | Yes/No | |

---

## 2. Network Architecture

### 2.1 Network Zones

| Zone | Description | IP Range | Security Level | Connected Zones |
|------|-------------|----------|----------------|-----------------|
| DMZ | External facing web and API | | High | Internal, Internet |
| Core Banking | Ledger, balances, core apps | | Critical | Internal |
| Trading DMZ | Low latency execution / fix | | Critical | External exchanges |
| Payment Network | SWIFT, SEPA | | Critical | Core Banking |
| Internal | Corporate workstations | | Medium | DMZ, Data Center |

### 2.2 Network Diagram Reference
**Attached**: ☐ Yes ☐ No  
**Location**: [Reference link or file path]

---

## 3. Third-Party Connections (ICT Providers)

| Third Party | System | Connection Type | Data Shared | Risk Level | Contract Review |
|-------------|--------|-----------------|-------------|-------------|------------------|
| | | VPN/Direct/API | | Low/Med/High | ☐ Yes ☐ No |
| | | VPN/Direct/API | | Low/Med/High | ☐ Yes ☐ No |
| | | VPN/Direct/API | | Low/Med/High | ☐ Yes ☐ No |

---

## 4. Data Classification Summary

| Classification | Examples | Systems | Risk Level |
|----------------|----------|---------|------------|
| **Restricted** | SWIFT messaging, PANs, Trade Secrets, Auth Tokens | | Highest |
| **Confidential** | Customer Financial Data, Market Orders, PII | | High |
| **Internal** | Corporate policies, internal ops | | Medium |
| **Public** | Marketing materials, public disclosures | | Low |

---

## 5. Compliance Scope Mapping

| Compliance Framework | Data Types / Focus | Systems in Scope | Testing Frequency Required |
|---------------------|--------------------|------------------|---------------------------|
| DORA | Critical financial & payment services | | Annual (TLPT 3 yrs) |
| FRB Supervision | Core banking and systemic risk | | Annual |
| HKMA iCAST | CFI designated critical systems | | Simulation based |
| PRA CBEST | Critical business services (CBS) | | 2-3 years |

---

## 6. Asset Criticality Assessment

### 6.1 Business Impact Factors

| Factor | Weight | Assessment |
|--------|--------|------------|
| Systemic Financial Impact| 25% | $___ per hour transaction loss |
| Customer Financial Impact| 20% | ___ retail/commercial customers |
| Reputational Impact | 20% | High/Medium/Low |
| Regulatory Impact | 15% | Potential license revocation |
| Operational Impact | 10% | Recovery time |
| Data Sensitivity | 10% | Classification |

### 6.2 Asset Criticality Matrix

```
                    Low Impact          Medium Impact          High Impact
                ┌─────────────────┬─────────────────┬─────────────────┐
  High Likelihood │     HIGH         │    CRITICAL      │    CRITICAL     │
                ├─────────────────┼─────────────────┼─────────────────┤
 Medium Likelihood │     MEDIUM       │     HIGH         │    CRITICAL     │
                ├─────────────────┼─────────────────┼─────────────────┤
   Low Likelihood  │      LOW         │     MEDIUM       │      HIGH       │
                └─────────────────┴─────────────────┴─────────────────┘
```

---

**Document Maintenance**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial asset inventory |
| | | | |

**Next Review Date**: [Date]
