# Rules of Engagement Template

**Document Type**: Rules of Engagement  
**Version**: 1.0  
**Date**: [DATE]  
**Related Scope**: [Reference to Scope Statement]  
**Classification**: Confidential  

---

## 1. Introduction

### 1.1 Purpose
This document establishes the rules, procedures, and constraints for conducting authorized penetration testing activities. All parties must adhere to these rules to ensure:
- Legal compliance
- Business continuity
- Data protection
- Safe testing practices

### 1.2 Scope of This Document
These rules govern:
- Permitted testing techniques
- Prohibited activities
- Communication procedures
- Emergency protocols
- Data handling requirements
- Evidence preservation

---

## 2. Authorization

### 2.1 Legal Authorization
```
AUTHORIZED BY: [Client Organization Name]
AUTHORIZATION DATE: [Date]
SCOPE REFERENCE: [Linked Scope Statement ID]

This penetration testing engagement is conducted with explicit written 
authorization from the system owners. All testing activities are performed 
against systems for which the client has legal authority to permit security testing.
```

### 2.2 Authorization Boundaries
- Testing is **limited to assets** listed in the Scope Statement
- Testing is **valid only during** the agreed testing window
- Testing must **adhere to** all constraints listed in Section 4

---

## 3. Communication Procedures

### 3.1 Primary Contacts

| Role | Name | Email | Phone | Slack/Teams |
|------|------|-------|-------|-------------|
| **Client Project Lead** | [Name] | [Email] | [Phone] | [Handle] |
| **Client Security Lead** | [Name] | [Email] | [Phone] | [Handle] |
| **Test Team Lead** | [Name] | [Email] | [Phone] | [Handle] |
| **Test Engineer** | [Name] | [Email] | [Phone] | [Handle] |

### 3.2 Escalation Contacts (24/7)

| Role | Name | Email | Phone |
|------|------|-------|-------|
| **Emergency - Client** | [Name] | [Email] | [Phone] |
| **Emergency - Test Team** | [Name] | [Email] | [Phone] |

### 3.3 Communication Schedule

| Meeting/Frequency | Purpose | Attendees | Format |
|-------------------|---------|-----------|--------|
| Kickoff Call | Scope review, procedures | All contacts | Video call |
| Daily Standup (optional) | Status update | Leads | Slack/Teams |
| Weekly Report | Findings summary | Project leads | Email + Call |
| Critical Finding Alert | Immediate notification | Security lead | Phone + Email |
| Exit Interview | Preliminary findings | All contacts | Video call |
| Final Debrief | Report walkthrough | Stakeholders | In-person/Video |

### 3.4 Communication Channels

| Channel | Use Case | Response Time |
|---------|----------|---------------|
| Email | Formal communications, reports | Within 4 business hours |
| Slack/Teams | Quick questions, status | Within 2 hours during testing |
| Phone | Critical issues, emergencies | Immediate |
| Encrypted Email | Sensitive findings | Within 4 business hours |

---

## 4. Testing Constraints

### 4.1 Absolute Prohibitions

The following activities are **NEVER permitted** without explicit written approval:

| Prohibited Activity | Rationale | Exception Available? |
|---------------------|-----------|---------------------|
| Denial of Service (DoS) attacks | Business continuity | ☐ Yes ☐ No |
| Data exfiltration | Data protection | ☐ Yes ☐ No |
| Physical intrusion | Legal/safety | ☐ Yes ☐ No |
| Social engineering (non-physical) | Human safety | ☐ Yes ☐ No |
| Modifying system configurations | Availability | ☐ Yes ☐ No |
| Deleting data or logs | Evidence integrity | ☐ Yes ☐ No |
| Deploying malware/backdoors | Legal | ☐ Yes ☐ No |
| Brute force attacks on auth systems | Account lockout | ☐ Yes ☐ No |
| Testing production payment systems | Revenue impact | ☐ Yes ☐ No |

### 4.2 Testing Time Restrictions

| Day | Allowed Hours | Notes |
|-----|---------------|-------|
| Monday | TBD | |
| Tuesday | TBD | |
| Wednesday | TBD | |
| Thursday | TBD | |
| Friday | TBD | |
| Saturday | TBD | |
| Sunday | TBD | |

**Testing Window**: [Start Date/Time] to [End Date/Time]

### 4.3 Rate Limiting

| Test Type | Limitation | Notes |
|-----------|------------|-------|
| Port scans | Max [X] packets/second | Nmap rate limit |
| HTTP requests | Max [X] requests/second | Burp throttle |
| Authentication attempts | Max [X] per account | To prevent lockout |
| Credential stuffing | **NOT ALLOWED** | Prohibited activity |

### 4.4 Source IP Whitelisting

All testing must originate from the following IP addresses:

```
PRIMARY TESTER IPs:
- TBD

FAILOVER IPs:
- TBD

If testing must originate from other IPs, pre-approval required.
```

---

## 5. Safety Protocols

### 5.1 Kill Switch Criteria
Testing must be **immediately paused** if any of the following occur:

- [ ] System becomes unresponsive or crashes
- [ ] Business-critical service disruption detected
- [ ] Alert from security operations center
- [ ] Unexpected data access (beyond test scope)
- [ ] Any legal concern raised
- [ ] Client requests immediate halt
- [ ] Evidence of active compromise by third party

### 5.2 Kill Switch Procedure

```
STEP 1: Testing engineer identifies kill switch trigger
STEP 2: Immediately cease ALL active testing
STEP 3: Document:
        - What triggered the stop
        - Last command/action performed
        - Systems affected
        - Evidence collected
STEP 4: Contact Client Emergency Contact within 15 minutes
STEP 5: Await written authorization before resuming
STEP 6: Resume only after root cause addressed
```

### 5.3 System Impact Thresholds

| Impact Level | Definition | Required Action |
|--------------|------------|-----------------|
| **None** | No observable impact | Continue testing |
| **Minor** | Brief slowdown, normal logs | Document, continue |
| **Moderate** | Service degradation | Pause, notify client |
| **Severe** | Service unavailable | STOP, emergency protocol |
| **Critical** | Data breach/financial impact | STOP, full incident response |

---

## 6. Data Handling

### 6.1 Data Access Boundaries

| Data Type | Access Permitted | Notes |
|-----------|------------------|-------|
| PII (Personally Identifiable Info) | ☐ Yes ☐ No | [Restrictions] |
| Financial data | ☐ Yes ☐ No | [Restrictions] |
| Healthcare data (PHI) | ☐ Yes ☐ No | [Restrictions] |
| Authentication credentials | ☐ Yes ☐ No | [Restrictions] |
| Business confidential | ☐ Yes ☐ No | [Restrictions] |

### 6.2 Evidence Handling

```
EVIDENCE COLLECTION RULES:

1. Only capture evidence necessary to demonstrate vulnerability
2. Screenshots preferred over raw data
3. No actual customer PII in screenshots
4. Hash and preserve original evidence
5. Encrypt all evidence at rest
6. Delete evidence within 90 days of engagement close
7. Evidence accessible only to named team members
```

### 6.3 Data Exfiltration Prevention

- [ ] Proof-of-concept only (no actual data theft)
- [ ] If sensitive data encountered, immediately document and stop
- [ ] Any exfiltrated data will be securely destroyed
- [ ] Client notified immediately if sensitive data accessed

---

## 7. Reporting Procedures

### 7.1 Finding Classification

| Severity | CVSS Range | Definition | SLA |
|----------|------------|------------|-----|
| **Critical** | 9.0-10.0 | Immediate threat, active exploitation risk | 24 hours |
| **High** | 7.0-8.9 | Significant vulnerability, likely exploitation | 7 days |
| **Medium** | 4.0-6.9 | Moderate risk, some exploitation potential | 30 days |
| **Low** | 0.1-3.9 | Limited risk, difficult exploitation | 90 days |
| **Informational** | N/A | Best practice observation | None |

### 7.2 Critical Finding Notification

```
CRITICAL FINDING PROCESS:

1. Tester identifies potential critical finding
2. Verify severity classification
3. Document preliminary evidence
4. Notify client security lead immediately
   - Phone call (required)
   - Follow-up email with details
5. Client confirms receipt and understanding
6. Provide detailed writeup within 24 hours
7. Coordinate remediation timing
8. Retest after remediation (if requested)
```

### 7.3 Report Delivery

| Deliverable | Audience | Format | Timeline |
|-------------|----------|--------|----------|
| Executive Summary | C-Suite, Board | PDF, 2-3 pages | Final report |
| Technical Report | IT/Security Teams | PDF, full detail | Final report |
| Risk Matrix | Management | Excel/CSV | Weekly updates |
| Raw Findings | Security Team | JSON/XML/CSV | Final report |
| Remediation Tracker | IT Teams | Spreadsheet | With report |

---

## 8. Confidentiality

### 8.1 Non-Disclosure

All information gathered during this engagement is confidential:
- Test results and findings
- System architecture and configurations
- Vulnerability details
- Security weaknesses

### 8.2 Data Retention

| Data Type | Retention Period | Destruction Method |
|-----------|-----------------|-------------------|
| Evidence files | 90 days | Secure erase |
| Reports | 1 year | Secure archive |
| Working documents | 30 days | Secure delete |
| Communication records | 1 year | Secure archive |

### 8.3 Third-Party Disclosure

Findings may only be disclosed to:
- Client organization and authorized personnel
- Client's designated auditors (with written approval)
- Legal authorities (if legally required)

---

## 9. Agreement and Signatures

### 9.1 Acceptance

By signing below, all parties agree to the rules and procedures outlined in this document.

### Client Acceptance

**Name**: _________________________

**Title**: _________________________

**Signature**: _________________________

**Date**: _________________________

### Testing Provider Acceptance

**Name**: _________________________

**Title**: _________________________

**Signature**: _________________________

**Date**: _________________________

### Testing Engineer(s)

**Name**: _________________________

**Signature**: _________________________

**Date**: _________________________

---

## Appendix A: Quick Reference Card

```
╔════════════════════════════════════════════════════════════════╗
║              PENETRATION TEST QUICK REFERENCE                  ║
╠════════════════════════════════════════════════════════════════╣
║ TESTING WINDOW: [Date Range]                                   ║
║ WHITELISTED IPs: [IP List]                                    ║
║                                                                ║
║ EMERGENCY CONTACT: [Name] - [Phone]                           ║
║                                                                ║
║ STOP IMMEDIATELY IF:                                          ║
║   - System crashes or becomes unresponsive                    ║
║   - Service disruption detected                               ║
║   - SOC alerts on testing activity                           ║
║   - Unexpected sensitive data access                          ║
║   - Client requests halt                                     ║
║                                                                ║
║ NEVER DO:                                                     ║
║   - DoS testing (unless explicitly authorized)                ║
║   - Data exfiltration                                         ║
║   - Modify configurations                                      ║
║   - Delete data or logs                                       ║
║   - Deploy malware or backdoors                               ║
║   - Physical intrusion                                        ║
║                                                                ║
║ REPORT CRITICAL FINDINGS: Phone call + Email                 ║
║ SLA: 24 hours for critical finding notification               ║
╚════════════════════════════════════════════════════════════════╝
```

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial version |
