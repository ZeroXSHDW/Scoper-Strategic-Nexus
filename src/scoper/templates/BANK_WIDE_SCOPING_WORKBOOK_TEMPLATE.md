# Bank-Wide Regulatory Scoping Workbook Template

**Template purpose:** Simple blank intake for bank departments. Complete the document by regulatory body first, then list only the affected services, systems, vendors, evidence owners, and approvals.

**Important:** This workbook captures scope only. It does not approve testing, authorize access, permit scanning, permit exploitation, or replace a signed SOW, Rules of Engagement, legal approval, or operational change approval.

## 1. Bank Entity

| Field | Blank response |
|---|---|
| Legal entity |  |
| Business unit / department |  |
| Department owner |  |
| Critical or important business service |  |
| Country / region |  |
| Primary contact |  |
| Notes |  |

## 2. Regulatory Body Scope Register

Complete one row for each applicable regulatory body or standard. Mark non-applicable rows as N/A. Do not add technical testing detail here unless it is needed to identify the regulated service or evidence owner.

| Regulatory body / standard | Applies when | In scope? | Business service / process | Systems, applications, vendors, or data | Evidence owner / source | Approval status |
|---|---|---|---|---|---|---|
| DORA (EU) | ICT risk, resilience testing, incident reporting, ICT third-party risk for critical functions | Yes / No / N/A |  |  |  | Not started / Draft / Pending / Approved / N/A |
| FRB Supervision (US) | US-facing entities, US customer data, core banking controls, SR 13-1 oversight | Yes / No / N/A |  |  |  | Not started / Draft / Pending / Approved / N/A |
| HKMA iCAST (Hong Kong) | Cyber resilience, intelligence-led simulation for CFI designated systems | Yes / No / N/A |  |  |  | Not started / Draft / Pending / Approved / N/A |
| PRA CBEST (UK) | UK-regulated operations, UK important business services (CBS), threat-led testing | Yes / No / N/A |  |  |  | Not started / Draft / Pending / Approved / N/A |

## 3. One-Line System Register

Use this only to identify what each regulatory row covers. Keep one row per service, system, vendor, or process.

| Business service / process | System, application, data set, or vendor | Regulatory bodies / standards | Owner | Evidence source | Approval status |
|---|---|---|---|---|---|
|  |  |  |  |  | Not started / Draft / Pending / Approved / N/A |
|  |  |  |  |  | Not started / Draft / Pending / Approved / N/A |
|  |  |  |  |  | Not started / Draft / Pending / Approved / N/A |

## 4. Approval Gate

This table records scoping approval only. Authority to test must still come from the approved SOW, Rules of Engagement, change process, and legal authorization path.

| Role | Name | Decision | Date | Conditions / comments |
|---|---|---|---|---|
| Business owner |  | Approved / Rejected / Pending / N/A |  |  |
| Department owner |  | Approved / Rejected / Pending / N/A |  |  |
| Technical owner |  | Approved / Rejected / Pending / N/A |  |  |
| Security owner |  | Approved / Rejected / Pending / N/A |  |  |
| IT Operations / Change owner |  | Approved / Rejected / Pending / N/A |  |  |
| Compliance / GRC |  | Approved / Rejected / Pending / N/A |  |  |
| Privacy / Legal |  | Approved / Rejected / Pending / N/A |  |  |

## 5. High-Risk Confirmation

Complete this only when the regulatory scope involves payment systems, production banking apps, TLPT/red team, social engineering, core banking, SWIFT, or physical testing.

| High-risk area | Applies? | Extra approval owner | Stop / safety condition |
|---|---|---|---|
| Payment systems / SWIFT / Core Banking | Yes / No / N/A | Payments, Core Banking owner, SWIFT owner, Security, Legal | Payment or financial-message risk pauses testing |
| Production digital banking apps / APIs | Yes / No / N/A | App owner, IT Ops, Security, Privacy, business sponsor | Customer impact or instability pauses testing |
| Red team / TLPT / CBEST / iCAST | Yes / No / N/A | CISO, Legal, Risk, SOC, white cell, regulator path where applicable | White cell can pause or stop activity immediately |
| Social engineering | Yes / No / N/A | Legal, HR, Privacy, Security Awareness, business sponsor | Wellbeing and HR controls override campaign execution |
| Physical security | Yes / No / N/A | Facilities, Legal, Security, site manager | Emergency phrase or staff safety concern stops testing |

## 6. Evidence And Retention

| Evidence area | Owner | Evidence source | Retention period | Redaction rule |
|---|---|---|---|---|
| Regulatory mapping |  |  |  |  |
| Asset / system reference |  |  |  |  |
| Approval evidence |  |  |  |  |
| Test evidence, if later authorized |  |  |  |  |

## 7. Scoper Appendix: Service Code Routing

Departments do not need to complete this appendix. The scoper can use it after the regulatory register is complete.

| Scope family | Service codes |
|---|---|
| External perimeter | `PT-NET-EXT`, `VA-NET-EXT` |
| Internal network | `PT-NET-INT`, `VA-NET-INT` |
| Identity / AD / Entra | `PT-NET-AD` |
| Web applications | `PT-APP-WEB`, `VA-APP-WEB` |
| APIs / integrations | `PT-APP-API` |
| Mobile apps | `PT-APP-MOB` |
| Secure code / SDLC | `PT-APP-SCR` |
| Cloud infrastructure | `PT-CLD-INF` |
| Containers / Kubernetes | `PT-CLD-K8S` |
| Red team / TLPT | `PT-ADV-RT`, `RT-FULL` |
| Purple team / SOC validation | `PT-ADV-PT` |
| Social engineering | `PT-ADV-SE` |
| Physical security | `PT-SPEC-PHY` |
