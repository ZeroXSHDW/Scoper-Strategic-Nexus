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
            <div class="v33-kicker">Omnipotence Engagement Architecture</div>
            <h1>Strategic<br/><span>Nexus</span></h1>
            <p>Strategic Security Scoping v33.0 Omni-Review</p>
          </div>
          <div class="v33-footer">
            <div class="v33-m"><span>ENTITY</span><strong>{client_name}</strong></div>
            <div class="v33-m"><span>NEXUS SCORE</span><strong>{score}%</strong></div>
          </div>
        </div>"""

        # --- CHAPTER 1: NEXUS RADAR ---
        ch1 = f"""<div class="v33-score-card">
            <div class="v33-score-main">
                <div class="v33-score-val">{score}</div>
                <div class="v33-score-lbl">NEXUS INDEX</div>
            </div>
            <div class="v33-score-text">
                <h3>1.1 Engagement Coverage Index</h3>
                <p>This score reflects the breadth of technical validation across core governance pillars.</p>
            </div>
        </div>"""
        
        # radarRows = Object.entries(nexus.coverage).map(([k,v]) => [k.replace('P_', ''), v ? '<span class="v33-v">VALIDATED</span>' : '<span class="v33-x">GAP</span>', "Strategic"]);
        rows = ""
        for k, v in coverage.items():
            status = '<span class="v33-v">VALIDATED</span>' if v else '<span class="v33-x">GAP</span>'
            rows += f"<tr><td>{k.replace('P_', '')}</td><td>{status}</td><td>Strategic</td></tr>"
            
        ch1 += f"""<table class="v33-table">
            <thead><tr><th>Pillar</th><th>Status</th><th>Priority</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>"""
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

        # --- CHAPTER 2: DATA CUSTODY ---
        ch2 = f"""<h3>2.1 Digital Chain of Evidence</h3>
          <p>Artifacts produced during this engagement follow a cryptographically-verifiable lifecycle.</p>"""
        
        c_rows = ""
        for step in self.nexus.custody_steps:
            c_rows += f"<tr><td>{step.get('name')}</td><td>{step.get('method')}</td></tr>"
            
        ch2 += f"""<table class="v33-table">
            <thead><tr><th>Lifecycle Phase</th><th>Validation Method</th></tr></thead>
            <tbody>{c_rows}</tbody>
        </table>"""
        content += self._page("Technical Data Governance", ch2, "PART II: GOVERNANCE")

        # --- CHAPTER 3: TECHNICAL WORKSTREAMS ---
        ch3 = '<div class="v33-ws-grid">'
        for s in selected_services:
            ch3 += f"""<div class="v33-ws">
                <div class="v33-ws-h"><span>{s['code']}</span> {s['label']}</div>
                <div class="v33-ws-b">
                    <p>{s['description']}</p>
                    <div class="v33-ws-f">{s['calculatedDays']} Days | €{s['calculatedPrice']:,} Budgetary ALLOC</div>
                </div>
            </div>"""
        ch3 += '</div>'
        content += self._page("Technical Scope of Work", ch3, "PART III: EXECUTION")

        # --- CHAPTER 3.5: OMNI MATRIX ---
        omni_controls = self.omni.get_control_mappings(selected_codes)
        if omni_controls:
            ch3b = f"""<h3>3.1 Omni Control Mapping</h3>
            <p>The following granular controls are in scope for the selected execution modules.</p>
            <table class="v33-table">
            <thead><tr><th>Control ID</th><th>Domain</th><th>Description</th></tr></thead>
            <tbody>"""
            for c in omni_controls:
                ch3b += f"<tr><td><strong>{c.get('id')}</strong></td><td>{c.get('domain')}</td><td>{c.get('description')}</td></tr>"
            ch3b += "</tbody></table>"
            content += self._page("Omni Control Matrix", ch3b, "PART III.b: OMNI MATRIX")
            
        # --- CHAPTER 3.6: RACI GOVERNANCE ---
        raci_rows = self.omni.get_raci_rows()
        if raci_rows:
            ch3c = f"""<h3>3.2 RACI Governance Matrix</h3>
            <p>Responsibility Assignment Matrix for engagement activities.</p>
            <table class="v33-table">
            <thead><tr><th>Activity</th><th>Provider</th><th>Client Sec Lead</th><th>Client IT</th><th>Client Exec</th></tr></thead>
            <tbody>"""
            for r in raci_rows:
                if len(r) >= 5:
                    ch3c += f"<tr><td>{r[0]}</td><td><strong>{r[1]}</strong></td><td><strong>{r[2]}</strong></td><td><strong>{r[3]}</strong></td><td><strong>{r[4]}</strong></td></tr>"
            ch3c += "</tbody></table>"
            content += self._page("RACI Governance", ch3c, "PART III.c: RACI MATRIX")

        # --- CHAPTER 4: VERIFICATION ---
        ch4 = f"""<div class="v33-auth">
          <div class="v33-seal-wrap">
            <div class="v33-seal-box"></div>
            <span>NEXUS SEAL</span>
          </div>
          <div class="v33-sigs">
            <div class="v33-sig">Executive Sponsor Approval<div class="l"></div></div>
            <div class="v33-sig">Lead Strategic Provider<div class="l"></div></div>
          </div>
        </div>
        <div class="v33-fp">FINGERPRINT // {fingerprint}</div>"""
        content += self._page("Verification & Sign-off", ch4, "PART IV: AUTHORIZATION")

        import yaml
        theme_path = self.data_dir.parent / "config" / "theme.yaml"
        theme = {
            "accent": "#020617",
            "neon": "#00f0ff",
            "slate": "#475569",
            "bg": "#f8fafc",
            "glass_bg": "rgba(255, 255, 255, 0.65)",
            "card_border": "rgba(0, 0, 0, 0.05)",
            "shadow": "0 10px 40px -10px rgba(0,0,0,0.08)"
        }
        if theme_path.exists():
            with open(theme_path, 'r') as f:
                config = yaml.safe_load(f)
                if config and 'theme' in config:
                    theme.update(config['theme'])
                    
        style_path = self.data_dir.parent / "assets" / "style.css"
        base_style = style_path.read_text() if style_path.exists() else ""
        
        custom_style = f"""
          :root {{
            --accent: {theme['accent']};
            --neon: {theme['neon']};
            --slate: {theme['slate']};
            --bg: {theme['bg']};
            --glass_bg: {theme['glass_bg']};
            --card_border: {theme['card_border']};
            --shadow: {theme['shadow']};
          }}
          {base_style}
        """

        # Parse Master Forms if using Global Template
        compliance_forms = ""
        import markdown
        from pathlib import Path
        
        def parse_md(filename, kicker):
            try:
                md_path = self.data_dir.parent / "templates" / filename
                if not md_path.exists(): return ""
                html = markdown.markdown(md_path.read_text(encoding='utf-8'), extensions=['tables'])
                html = html.replace('<table>', '<table class="v33-table">')
                html = html.replace('☐', '<span style="color:#94a3b8; font-size:14pt; margin-right:4px;">☐</span>')
                html = html.replace('✓', '<span style="color:#22c55e; font-weight:bold;">✓</span>')
                
                sections = html.split('<h2>')
                out = sections[0]
                for sec in sections[1:]:
                    title = sec.split('</h2>')[0]
                    cont = sec[len(title)+5:]
                    out += f'<div class="md-section"><div class="section-head"><h2>{title}</h2><div class="kicker">{kicker}</div></div><div class="md-content">{cont}</div></div>'
                return out
            except Exception:
                return ""

        from scoper.config import get_config_value
        forms = get_config_value("compliance_forms", [])
        for form in forms:
            compliance_forms += parse_md(form["file"], form["kicker"])

        template = self.env.get_template('GLOBAL_COMPLIANCE_SCOPE.html')
        full_html = template.render(
            title=f"Omni-Strategic Nexus v33.0 - {client_name}",
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
