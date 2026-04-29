import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from jinja2 import Environment, FileSystemLoader

from .export import export_raw_html_to_pdf
from .nexus import NexusEngine
from .omni import OmniController

class ScopingPackGenerator:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or (Path(__file__).parent / "data")
        self.nexus = NexusEngine(self.data_dir)
        self.omni = OmniController(self.data_dir)
        
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader([str(template_dir)]))

    def generate(self, client_name: str, region: str, selected_codes: List[str], output_path: Path, pack_id: Optional[str] = None):
        catalog = json.loads((self.data_dir / 'services' / 'catalog.json').read_text(encoding='utf-8'))
        packs_data = json.loads((self.data_dir / 'compliance' / 'packs.json').read_text(encoding='utf-8')).get('packs', [])
        guidance_data = json.loads((self.data_dir / 'regulatory' / 'detailed-guidance.json').read_text(encoding='utf-8')).get('guidance', [])
        
        pack = None
        if pack_id:
            pack = next((p for p in packs_data if p.get('id') == pack_id), None)
            if pack:
                for svc in pack.get('services', []):
                    if svc not in selected_codes:
                        selected_codes.append(svc)
        
        # Build selected services list from catalog
        selected_services = []
        for service in catalog:
            if service.get("code") in selected_codes:
                # Add calculated price/days for rendering
                # Using defaults or basic calc to match JS behavior
                price = service.get("priceRangeMin", 0)
                days = price / 1500 if price else 1 # basic estimate
                selected_services.append({
                    "code": service.get("code"),
                    "label": service.get("label"),
                    "description": service.get("description", ""),
                    "calculatedPrice": price,
                    "calculatedDays": round(days)
                })

        nexus_data = self.nexus.calculate_nexus_score(selected_codes)
        score = nexus_data['score']
        coverage = nexus_data['coverage']
        
        fingerprint = self.omni.get_fingerprint({
            "clientName": client_name, 
            "selectedServices": selected_services
        })

        content = ""

        # --- CHAPTER 0: NEXUS COVER ---
        content += f"""<div class="cover-v33">
          <div class="v33-lines"></div>
          <div class="v33-top">
            <span class="v33-id">FINGERPRINT // {fingerprint[:16]}</span>
            <span class="v33-cl">// CONFIDENTIAL STRATEGY //</span>
          </div>
          <div class="v33-center">
            <div class="v33-box"></div>
            <div class="v33-kicker">Regulatory Vendor Scoping Request</div>
            <h1>Scope<br/><span>Definition</span></h1>
            <p>DORA TLPT, PRA CBEST, & HKMA iCAST Vendor Requirements</p>
          </div>
          <div class="v33-footer">
            <div class="v33-m"><span>ENTITY</span><strong>{client_name}</strong></div>
            <div class="v33-m"><span>NEXUS SCORE</span><strong>{score}%</strong></div>
          </div>
        </div>"""

        from .visuals import generate_nexus_radar_chart
        radar_svg = generate_nexus_radar_chart(coverage)
        
        # --- CHAPTER 1: NEXUS RADAR ---
        ch1 = f"""<div style="display: flex; gap: 40px; align-items: flex-start; page-break-inside: avoid;">
            <div style="flex: 1;">
                <div class="v33-score-card" style="margin-top: 0;">
                    <div class="v33-score-main">
                        <div class="v33-score-val">{score}</div>
                        <div class="v33-score-lbl">NEXUS INDEX</div>
                    </div>
                    <div class="v33-score-text">
                        <h3>1.1 Engagement Coverage Index</h3>
                        <p>This score reflects the breadth of technical validation across core governance pillars.</p>
                    </div>
                </div>
                <table class="v33-table">
                    <thead><tr><th>Pillar</th><th>Status</th><th>Priority</th></tr></thead>
                    <tbody>"""
        
        for k, v in coverage.items():
            status = '<span class="v33-v">VALIDATED</span>' if v else '<span class="v33-x">GAP</span>'
            ch1 += f"<tr><td>{k.replace('P_', '')}</td><td>{status}</td><td>Strategic</td></tr>"
            
        ch1 += f"""</tbody>
                </table>
            </div>
            <div style="flex: 1; display: flex; justify-content: center; align-items: center; background: var(--glass_bg); border: 1px solid var(--card_border); border-radius: 16px; padding: 20px; box-shadow: var(--shadow); backdrop-filter: blur(20px);">
                {radar_svg}
            </div>
        </div>"""
        
        content += self._page("Nexus Strategic Analysis", ch1, "PART I: STRATEGY")

        # --- CHAPTER 1.5: REGULATORY ALIGNMENT ---
        if pack:
            ch_reg = f"""<h3>1.5 Regulatory Alignment: {pack.get('label')}</h3>
            <p><strong>Narrative:</strong> {pack.get('narrative')}</p>"""
            
            has_guidance = False
            for f_id in pack.get('frameworks', []):
                g = next((x for x in guidance_data if x.get('frameworkId') == f_id), None)
                if g:
                    has_guidance = True
                    ch_reg += f"""<div class="v33-ws" style="margin-top: 20px;">
                        <div class="v33-ws-h"><span>FRAMEWORK</span> {f_id}</div>
                        <div class="v33-ws-b">"""
                    for sec in g.get('sections', []):
                        ch_reg += f"<h4>{sec.get('title')}</h4><p>{sec.get('content')}</p>"
                    ch_reg += """</div></div>"""
            if has_guidance:
                content += self._page("Regulatory Framework Analysis", ch_reg, "PART I.b: COMPLIANCE")

        # --- CHAPTER 1.6: THREAT INTELLIGENCE PROFILES ---
        ch_threat = f"""<h3>1.6 Threat Intelligence Scenarios</h3>
        <p>In accordance with the stringent intelligence-led requirements of <strong>DORA TLPT</strong>, <strong>PRA CBEST</strong>, and <strong>HKMA iCAST</strong>, the following Advanced Persistent Threat (APT) profiles are designated as in-scope for simulation.</p>
        <table class="v33-table">
            <thead><tr><th>Threat Actor</th><th>Target Sector</th><th>Primary Objective</th><th>Kill-Chain Focus</th></tr></thead>
            <tbody>
                <tr><td><strong>FIN7 / Carbanak</strong></td><td>Financial Services</td><td>Financial Theft, Ransomware</td><td>Initial Access, Lateral Movement, Exfiltration</td></tr>
                <tr><td><strong>Lazarus Group</strong></td><td>Global Banking</td><td>SWIFT compromise, Cryptocurrency</td><td>Defense Evasion, Persistence, C2</td></tr>
                <tr><td><strong>Cozy Bear (APT29)</strong></td><td>Government & Finance</td><td>Espionage, Supply Chain</td><td>Supply Chain Compromise, Discovery</td></tr>
            </tbody>
        </table>"""
        content += self._page("Threat Intelligence Modeling", ch_threat, "PART I.c: INTELLIGENCE")

        # --- CHAPTER 2: DATA GOVERNANCE ---
        ch2 = f"""<h3>2.1 Digital Chain of Evidence</h3>
          <p>Artifacts produced during this engagement follow a cryptographically-verifiable lifecycle.</p>"""
        
        c_rows = ""
        for step in self.nexus.custody_steps:
            c_rows += f"<tr><td>{step.get('name')}</td><td>{step.get('method')}</td></tr>"
            
        ch2 += f"""<table class="v33-table">
            <thead><tr><th>Lifecycle Phase</th><th>Validation Method</th></tr></thead>
            <tbody>{c_rows}</tbody>
        </table>
        
        <br/>
        
        <h3>2.2 Data Sovereignty & Handling</h3>
        <p>Strict data localization and handling protocols are enforced during testing.</p>
        <table class="v33-table">
        <thead><tr><th>Data Classification</th><th>Processing Region</th><th>Retention SLA</th></tr></thead>
        <tbody>
            <tr><td>Engagement Metadata</td><td>{region} (Primary)</td><td>7 Years (Regulatory)</td></tr>
            <tr><td>Vulnerability Findings</td><td>{region} (Encrypted)</td><td>90 Days post-remediation</td></tr>
            <tr><td>PII / Sensitive Artifacts</td><td>Volatile Memory Only</td><td>Wiped immediately post-validation</td></tr>
        </tbody>
        </table>"""
        content += self._page("Data Governance & Sovereignty", ch2, "PART II: GOVERNANCE")

        currency = "€"
        r_lower = region.lower()
        if any(x in r_lower for x in ["us", "united states", "apac", "singapore", "hong kong", "australia"]):
            currency = "$"
        elif any(x in r_lower for x in ["uk", "united kingdom", "london"]):
            currency = "£"

        # --- CHAPTER 3: TECHNICAL WORKSTREAMS ---
        ch3 = '<div class="v33-ws-grid">'
        for s in selected_services:
            ch3 += f"""<div class="v33-ws">
                <div class="v33-ws-h"><span>{s['code']}</span> {s['label']}</div>
                <div class="v33-ws-b">
                    <p>{s['description']}</p>
                    <div class="v33-ws-f">Expected Duration: {s['calculatedDays']} Days</div>
                </div>
            </div>"""
        ch3 += '</div>'
        content += self._page("Technical Scope of Work", ch3, "PART III: EXECUTION")

        # --- CHAPTER 3.1: TARGET ENVIRONMENT PROFILE ---
        ch_target = f"""<h3>3.1 Target Asset Profile (Scale of Effort)</h3>
        <p>To accurately scope this engagement, the vendor must account for the following documented attack surface scale.</p>
        <table class="v33-table">
            <thead><tr><th>Asset Category</th><th>Target Scope Quantity</th><th>Notes</th></tr></thead>
            <tbody>
                <tr><td><strong>External Infrastructure</strong></td><td>~1,500 Active IPs (2x /16 Subnets)</td><td>Includes legacy branch office subnets.</td></tr>
                <tr><td><strong>Web Applications</strong></td><td>3 Mission-Critical Portals</td><td>Authenticated testing required (3 role levels each).</td></tr>
                <tr><td><strong>Cloud Environments</strong></td><td>2 AWS Organizations, 1 Azure Tenant</td><td>Includes Entra ID integration testing.</td></tr>
                <tr><td><strong>Human Factor (Phishing)</strong></td><td>5,000 High-Privilege Employees</td><td>Spear-phishing against IT/DevOps/Finance.</td></tr>
            </tbody>
        </table>"""
        content += self._page("Target Environment Profile", ch_target, "PART III.b: TARGET SCOPE")

        # --- CHAPTER 3.2, 3.3 & 3.4: EXECUTION CONSTRAINTS ---
        ch_constraints = f"""<h3>3.2 Prohibited Testing Methods (Rules of Engagement)</h3>
        <p>The following activities are strictly prohibited to ensure production stability during testing.</p>
        <table class="v33-table">
            <thead><tr><th>Prohibited Activity</th><th>Constraint Reason</th></tr></thead>
            <tbody>
                <tr><td><strong>Denial of Service (DoS/DDoS)</strong></td><td>Production disruption is strictly forbidden under banking regulations.</td></tr>
                <tr><td><strong>Physical Destruction / Lock-Picking</strong></td><td>Physical access is limited to tailgating and badge cloning; no property damage.</td></tr>
                <tr><td><strong>Database Record Modification</strong></td><td>Read-only proof of access is permitted. No destructive payloads or data alteration.</td></tr>
            </tbody>
        </table>
        
        <br/>
        
        <h3>3.3 Third-Party ICT Dependencies</h3>
        <p>Per regulatory mandate, all Critical Third-Party Providers (CTPPs) in scope must be explicitly authorized.</p>
        <table class="v33-table">
            <thead><tr><th>Vendor / CTPP</th><th>Service Provided</th><th>Testing Authorization</th><th>Status</th></tr></thead>
            <tbody>
                <tr><td>Amazon Web Services (AWS)</td><td>Cloud Infrastructure</td><td>Verified (AWS Pentest Rules)</td><td><span class="v33-v">AUTHORIZED</span></td></tr>
                <tr><td>Microsoft Azure</td><td>Entra ID & Cloud Hosting</td><td>Verified (Azure Rules of Engagement)</td><td><span class="v33-v">AUTHORIZED</span></td></tr>
                <tr><td>External SaaS Platform</td><td>Core Banking Integration</td><td>Pending Written Approval</td><td><span class="v33-x">PENDING</span></td></tr>
            </tbody>
        </table>
        
        <br/>
        
        <h3>3.4 Regulatory Exclusions & Justification</h3>
        <p>Any significant asset excluded from this testing must have management-approved justification.</p>
        <table class="v33-table">
            <thead><tr><th>Asset / System</th><th>Category</th><th>Exclusion Justification</th></tr></thead>
            <tbody>
                <tr><td>Legacy Mainframe (Z-OS)</td><td>Core Processing</td><td>In-flight migration to Cloud; frozen state until Q4. Risk accepted by Board.</td></tr>
                <tr><td>Third-Party Payment Gateway</td><td>Payment Processing</td><td>Vendor explicitly prohibits intrusive dynamic testing. Covered under SOC2 Type II.</td></tr>
            </tbody>
        </table>"""
        content += self._page("Execution Constraints & RoE", ch_constraints, "PART III.c: CONSTRAINTS")

        # --- CHAPTER 3.5 & 3.6: GOVERNANCE & ESCALATION ---
        raci_rows = self.omni.get_raci_rows()
        ch_gov = ""
        if raci_rows:
            ch_gov += f"""<h3>3.5 RACI Governance Matrix</h3>
            <p>Responsibility Assignment Matrix for engagement activities.</p>
            <table class="v33-table">
            <thead><tr><th>Activity</th><th>External Vendor</th><th>Internal Sec Lead</th><th>Internal IT</th><th>Internal Exec</th></tr></thead>
            <tbody>"""
            for r in raci_rows:
                if len(r) >= 5:
                    ch_gov += f"<tr><td>{r[0]}</td><td><strong>{r[1]}</strong></td><td><strong>{r[2]}</strong></td><td><strong>{r[3]}</strong></td><td><strong>{r[4]}</strong></td></tr>"
            ch_gov += "</tbody></table><br/>"

        ch_gov += f"""<h3>3.6 Incident Escalation Matrix</h3>
        <p>Pre-defined SLAs for communicating critical findings during active execution.</p>
        <table class="v33-table">
        <thead><tr><th>Severity Level</th><th>Escalation SLA</th><th>Primary Contact</th><th>Communication Channel</th></tr></thead>
        <tbody>
            <tr><td><strong style="color:#ef4444;">CRITICAL (Zero-Day / Active Breach)</strong></td><td>&lt; 4 Hours</td><td>Client CISO</td><td>Out-of-band encrypted comms</td></tr>
            <tr><td><strong style="color:#f97316;">HIGH (Exploitable Path)</strong></td><td>&lt; 24 Hours</td><td>SOC Lead</td><td>Encrypted Portal Ticket</td></tr>
            <tr><td><strong style="color:#eab308;">MEDIUM / LOW</strong></td><td>End of Phase</td><td>Project Manager</td><td>Weekly Status Report</td></tr>
        </tbody></table>"""
        content += self._page("Governance & Escalation", ch_gov, "PART III.d: GOVERNANCE")

        # --- CHAPTER 3.7: REGULATORY DELIVERABLES ---
        ch_del = f"""<h3>3.7 Mandatory Regulatory Deliverables</h3>
        <p>The selected vendor is contractually obligated to produce the following artifacts in strict accordance with DORA TLPT / PRA CBEST guidelines.</p>
        <table class="v33-table">
        <thead><tr><th>Deliverable Name</th><th>Description</th><th>Submission Phase</th></tr></thead>
        <tbody>
            <tr><td><strong>Targeted Threat Intelligence Report (TTIR)</strong></td><td>Deep-dive intelligence report identifying active threat actors and attack scenarios mapped to the target.</td><td>Phase 1 (Pre-Execution)</td></tr>
            <tr><td><strong>Red Team Test Plan (RTTP)</strong></td><td>Step-by-step attack playbooks derived from the TTIR, to be submitted to regulators for approval.</td><td>Phase 1 (Pre-Execution)</td></tr>
            <tr><td><strong>Comprehensive Attack Log</strong></td><td>Minute-by-minute cryptographic logging of all executed commands, payloads, and indicators of compromise.</td><td>Phase 2 (Active Execution)</td></tr>
            <tr><td><strong>Final Regulatory Report</strong></td><td>Executive and technical breakdown mapped to MITRE ATT&CK, including a joint remediation matrix.</td><td>Phase 3 (Closure)</td></tr>
        </tbody></table>"""
        content += self._page("Regulatory Deliverables", ch_del, "PART III.e: REPORTING")

        # --- CHAPTER 4: VENDOR COMPLIANCE REQUIREMENTS ---
        ch4 = f"""<h3>4.1 Mandatory Vendor Qualifications</h3>
        <p>To be considered eligible for this engagement, the external vendor must attest to the following minimum regulatory and operational requirements.</p>
        <table class="v33-table">
            <thead><tr><th>Qualification Domain</th><th>Minimum Requirement</th><th>Vendor Attestation (Yes/No)</th></tr></thead>
            <tbody>
                <tr><td><strong>Regulatory Status</strong></td><td>Approved provider under PRA CBEST, HKMA iCAST, or equivalent regulatory frameworks.</td><td></td></tr>
                <tr><td><strong>Technical Certification</strong></td><td>CREST Defensible Penetration Testing (or equivalent organizational accreditation).</td><td></td></tr>
                <tr><td><strong>Lead Operator Status</strong></td><td>Lead Threat Intelligence / Execution operators must hold active CREST CCSAS / OSCE3 equivalent.</td><td></td></tr>
                <tr><td><strong>Liability Insurance</strong></td><td>Active Professional Indemnity and Cyber Liability Insurance ($5M Minimum).</td><td></td></tr>
            </tbody>
        </table>"""
        content += self._page("Vendor Qualifications", ch4, "PART IV: COMPLIANCE")

        # --- CHAPTER 5: VERIFICATION ---
        ch5 = f"""<div class="v33-auth">
          <div class="v33-seal-wrap">
            <div class="v33-seal-box"></div>
            <span>VENDOR SEAL</span>
          </div>
          <div class="v33-sigs">
            <div class="v33-sig">Internal Executive Sponsor<div class="l"></div></div>
            <div class="v33-sig">External Vendor Authorized Signatory<div class="l"></div></div>
          </div>
        </div>
        <div class="v33-fp">FINGERPRINT // {fingerprint}</div>"""
        content += self._page("Vendor Acknowledgment & Scope Sign-off", ch5, "PART V: AUTHORIZATION")

        import yaml
        theme_path = self.data_dir.parent / "config" / "theme.yaml"
        theme = {
            "accent": "#f8fafc",
            "neon": "#00f0ff",
            "slate": "#94a3b8",
            "bg": "#020617",
            "glass_bg": "rgba(15, 23, 42, 0.75)",
            "card_border": "rgba(255, 255, 255, 0.08)",
            "shadow": "0 10px 40px -10px rgba(0,240,255,0.15)",
            "table_bg": "rgba(255, 255, 255, 0.02)",
            "table_bg_alt": "rgba(255, 255, 255, 0.04)",
            "text_muted": "#64748b"
        }
        if theme_path.exists():
            with open(theme_path, 'r') as f:
                config = yaml.safe_load(f)
                if config and 'theme' in config:
                    theme.update(config['theme'])
                    
        style_path = self.data_dir.parent / "assets" / "style.css"
        base_style = style_path.read_text() if style_path.exists() else ""
        
        css_vars = "\n".join([f"            --{k}: {v};" for k, v in theme.items()])
        
        custom_style = f"""
          :root {{
{css_vars}
          }}
          {base_style}
        """

        # Removed Master Forms loading to strictly limit the PDF size and ensure zero fluff
        compliance_forms = ""

        template = self.env.get_template('GLOBAL_COMPLIANCE_SCOPE.html')
        full_html = template.render(
            title=f"Regulatory Vendor Scoping Request - {client_name}",
            content=content,
            customStyle=custom_style,
            compliance_forms=compliance_forms
        )
        
        try:
            pdf_path = export_raw_html_to_pdf(full_html, str(output_path))
            return pdf_path
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"PDF generation failed: {e}")
            return output_path

    def _page(self, title: str, content: str, kicker: str = "") -> str:
        k_html = f'<div class="kicker">{kicker}</div>' if kicker else ''
        return f"""<div class="md-section">
            <div class="section-head">
                <h2>{title}</h2>
                {k_html}
            </div>
            {content}
        </div>"""
