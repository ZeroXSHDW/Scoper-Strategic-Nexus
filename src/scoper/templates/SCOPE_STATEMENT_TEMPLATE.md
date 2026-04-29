# Penetration Testing Scope Statement Template

**Document Type**: Scope Definition  
**Version**: 2.0  
**Date**: [DATE]  
**Classification**: Confidential  
**Industry**: [Investment Management / Financial Services / Government Contracting]

---

## 1. Executive Information

| Field | Details |
|-------|---------|
| **Project Name** | [Project/Engagement Name] |
| **Client Organization** | [Company Name] |
| **Client Contact** | [Name, Title, Email, Phone] |
| **Testing Provider** | [Company Name] |
| **Tester Lead** | [Name, Email, Phone] |
| **Engagement Manager** | [Name, Email, Phone] |
| **Scope Effective Date** | [Start Date] |
| **Scope Expiration Date** | [End Date] |
| **Assessment Tier** | [Tier 1 (Critical) / Tier 2 (High) / Tier 3 (Medium) / Tier 4 (Low)] |

---

## 2. Business Context

### 2.1 Purpose of Assessment

```
[Describe why this penetration test is being conducted]

Example:
Annual security assessment required for DORA TLPT compliance and SOC 2 Type II 
certification. The assessment will evaluate the security posture of customer-facing 
applications, core banking systems, and internal network infrastructure to 
identify vulnerabilities before they can be exploited by threat actors.
```

### 2.2 Applicable Regulations

| Regulation | Jurisdiction | Testing Requirement |
|------------|-------------|-------------------|
| [DORA] | [EU] | [Threat-Led PT / Annual PT] |
| [PCI DSS] | [Global] | [Annual / After Changes] |
| [SWIFT CSP] | [Global] | [Annual] |
| [MAS TRM] | [Singapore] | [Annual] |
| [SEC/FINRA] | [US] | [Annual (Recommended)] |
| [SAMA] | [Saudi Arabia] | [Annual] |
| [Other] | [Other] | [Other] |

### 2.3 Business Objectives
- [ ] Identify critical vulnerabilities before exploitation
- [ ] Meet compliance requirements ([DORA / PCI DSS / SWIFT CSP / MAS / Other])
- [ ] Validate effectiveness of existing security controls
- [ ] Assess readiness for new system deployment
- [ ] Support security awareness program
- [ ] Other: _______________

### 2.4 Success Criteria
```
[Define what constitutes a successful assessment]

Example:
- All critical and high-severity vulnerabilities identified and documented
- Testing completed within agreed timeline
- Comprehensive report delivered within 2 weeks of testing completion
- Client able to use findings to remediate vulnerabilities within SLA
- Regulatory compliance evidence documented
```

---

## 3. Technical Scope

### 3.1 In-Scope Assets - Core Banking & Financial Systems

#### Core Banking Systems
| Asset ID | Name/Description | Type | Owner | Data Sensitivity |
|----------|------------------|------|-------|------------------|
| CORE-001 | [Core Banking Platform] | [Temenos/FLEXCUBE/Other] | [Owner] | [Critical - Financial Data] |
| CORE-002 | [Payment Processing] | [Type] | [Owner] | [Critical - Transaction Data] |

#### Trading & Treasury Systems
| Asset ID | Name/Description | Type | Owner | Data Sensitivity |
|----------|------------------|------|-------|------------------|
| TRAD-001 | [Trading Platform] | [Type] | [Owner] | [Critical - Market Data] |
| TRAD-002 | [Treasury System] | [Type] | [Owner] | [Critical - Financial Data] |

### 3.2 In-Scope Assets - Digital Channels

#### Internet & Mobile Banking
| Asset ID | Name/Description | Platform | URL/Endpoint | Owner |
|----------|------------------|----------|---------------|-------|
| DIG-001 | [Internet Banking] | Web | [URL] | [Owner] |
| DIG-002 | [Mobile Banking - iOS] | iOS | [Bundle ID] | [Owner] |
| DIG-003 | [Mobile Banking - Android] | Android | [Package] | [Owner] |

#### ATM/POS Network
| Asset ID | Name/Description | Type | Owner |
|----------|------------------|------|-------|
| ATM-001 | [ATM Network] | ATM | [Owner] |
| POS-001 | [POS Network] | POS | [Owner] |

### 3.3 In-Scope Assets - Network Infrastructure

#### External Assets (Internet-Facing)
| Asset ID | Name/Description | IP Address/URL | Owner | Data Sensitivity |
|----------|------------------|-----------------|-------|------------------|
| EXT-001 | [Name] | [IP/URL] | [Owner] | [Public/Internal/Confidential] |
| EXT-002 | [Name] | [IP/URL] | [Owner] | [Public/Internal/Confidential] |
| EXT-003 | [Name] | [IP/URL] | [Owner] | [Public/Internal/Confidential] |

**Total External IPs/URLs**: ___

#### Internal Assets
| Asset ID | Name/Description | Network Segment | Owner | Data Sensitivity |
|----------|------------------|-----------------|-------|------------------|
| INT-001 | [Name] | [VLAN/Subnet] | [Owner] | [Public/Internal/Confidential] |
| INT-002 | [Name] | [VLAN/Subnet] | [Owner] | [Public/Internal/Confidential] |

**Total Internal Hosts**: ___

### 3.4 In-Scope Assets - Applications

| App ID | Application Name | Type | URL/Endpoint | Authentication | Owner |
|--------|------------------|------|--------------|----------------|-------|
| APP-001 | [Name] | Web/Mobile/API | [URL] | [Method] | [Owner] |
| APP-002 | [Name] | Web/Mobile/API | [URL] | [Method] | [Owner] |

**Total Applications**: ___

### 3.5 In-Scope Assets - Cloud Infrastructure

| Cloud ID | Provider | Services | Account/Project | Owner |
|----------|----------|----------|----------------|-------|
| CLD-001 | AWS/Azure/GCP | [Services] | [Account] | [Owner] |
| CLD-002 | AWS/Azure/GCP | [Services] | [Account] | [Owner] |

### 3.6 In-Scope Assets - Payment Systems

| Payment ID | System Name | Type | Owner | Regulatory Requirement |
|------------|-------------|------|-------|-----------------------|
| PMT-001 | [SWIFT Alliance] | SWIFT | [Owner] | [SWIFT CSP] |
| PMT-003 | [ACH/Payment] | ACH | [Owner] | [NACHA/Regulatory] |

---

### 3.7 Out-of-Scope Assets

The following are explicitly **excluded** from this assessment:

- [ ] Production database servers (write access limited)
- [ ] Mobile applications (separate engagement)
- [ ] Third-party vendor systems not owned by client
- [ ] Physical security systems (unless specifically requested)
- [ ] Social engineering (unless specifically requested)
- [ ] Third-party SaaS applications (except: _____________)
- [ ] Legacy systems (end-of-life, documented risk)
- [ ] Physical security assessments
- [ ] Social engineering assessments
- [ ] Denial of Service testing
- [ ] Supply chain assessments
- [ ] [Other exclusions]

**Reason for Exclusions**: 
```
[Explain why certain assets are out of scope and any compensating controls]
```

---

### 3.3 Network Diagrams

**Attached**: ☐ Yes ☐ No  
**Location**: [Reference to attached diagrams or Confluence URL]

---

## 4. Testing Types

### 4.1 Required Testing Types

| Test Type | Included | Notes |
|-----------|----------|-------|
| External Network Assessment | ☐ | [Any limitations] |
| Internal Network Assessment | ☐ | [VLANs excluded] |
| Web Application Testing | ☐ | [OWASP Top 10 + business logic] |
| API Security Testing | ☐ | [REST/GraphQL/SOAP] |
| Mobile Application Testing | ☐ | [iOS/Android/Backend] |
| Cloud Security Assessment | ☐ | [AWS/Azure/GCP] |
| Wireless Network Assessment | ☐ | [Specific SSIDs] |
| Social Engineering | ☐ | [Phishing/Physical] |
| Red Team / Full Attack Simulation | ☐ | [Objectives] |

### 4.2 Testing Methodology

The following methodologies will be followed:

- [ ] NIST SP 800-115 (Technical Guide to Security Testing)
- [ ] OWASP Testing Guide v4.2
- [ ] OWASP ASVS
- [ ] PTES (Penetration Testing Execution Standard)
- [ ] CIS Controls Benchmark
- [ ] Cloud-specific ([CIS Benchmark / Vendor Best Practices])
- [ ] Custom methodology (describe below)

```
[If custom methodology, describe approach]
```

---

## 5. Compliance Requirements

### 5.1 Applicable Frameworks

| Framework | Requirement | Testing Scope |
|-----------|-------------|---------------|
| ☐ ISO 27001 | A.12.6.1 | [Vulnerability management] |
| ☐ GDPR | Article 32 | [Technical measures] |
| ☐ SOX | IT General Controls | [Segregation of duties] |
| ☐ NIST CSF | PR.AC | [Access controls] |
| ☐ Industry-Specific | [Name] | [Requirements] |

### 5.2 Compliance Deliverables

- [ ] Compliance-specific findings mapping
- [ ] Remediation guidance for compliance gaps
- [ ] Attestation letter for auditors
- [ ] Executive summary for board
- [ ] Raw scan data for auditor review

---

## 6. Constraints and Restrictions

### 6.1 Time Constraints

| Day | Time Window | Notes |
|-----|-------------|-------|
| Monday | [Allowed/Hours] | [Notes] |
| Tuesday-Thursday | [Allowed/Hours] | [Notes] |
| Friday | [Allowed/Hours] | [Notes] |
| Weekend | [Allowed/Hours] | [Notes] |

**Testing Window**: [Start Date] to [End Date]

### 6.2 Technical Restrictions

| Restriction | Affected Systems | Mitigation |
|-------------|------------------|------------|
| No DoS testing | [Systems] | Excluded from scope |
| No credential brute force | [Systems] | Limited to 5 attempts |
| No database deletion | [Systems] | Read-only access only |
| No malware deployment | [Systems] | [Alternative approach] |
| Source IP restriction | [All/Specific] | [Whitelisted IPs below] |

**Whitelisted Tester IPs**:
```
[IP 1]
[IP 2]
```

### 6.3 Data Handling

- [ ] No data exfiltration allowed
- [ ] Evidence limited to screenshots/evidence files
- [ ] PII handling required (PII Processing Agreement attached)
- [ ] Data retention: 90 days post engagement

---

## 7. Authorization and Approval

### 7.1 Authorization Matrix

| Role | Name | Title | Signature | Date |
|------|------|-------|-----------|------|
| System Owner | | | | |
| Network Owner | | | | |
| Security Lead | | | | |
| Legal Counsel | | | | |
| Executive Sponsor | | | | |

### 7.2 Supporting Documents Attached

- [ ] Network diagrams
- [ ] Asset inventory
- [ ] Authorization letters
- [ ] PII Processing Agreement
- [ ] Data Classification Guide
- [ ] Previous penetration test reports
- [ ] Security policies

---

## 8. Sign-Off

By signing below, the parties confirm that:

1. The assets and scope listed above are accurate and authorized for testing
2. All necessary approvals have been obtained
3. Rules of Engagement have been reviewed and accepted
4. Emergency contacts have been established

### Client Authorization

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

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial version |
