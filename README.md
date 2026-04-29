# Scoper: Regulatory Vendor Scoping Request Generator

Scoper is an enterprise-grade, intelligence-led scoping engine strictly built for top-tier financial regulatory frameworks: **DORA TLPT, PRA CBEST, and HKMA iCAST**.

This project features a highly advanced generator engine that produces beautiful, purely technical **Regulatory Vendor Scoping Requests (RFPs)**. It completely removes internal budgetary fluff to give your external penetration testing vendors exactly what they need to scope and bid on a highly regulated engagement.

🚀 **[View the Sample Output PDF](output/Vendor_RFP_DORA_PRA_HKMA_Scope.pdf)**

## Core Features
*   **Target Environment Profiling**: Quantifies the exact scale of assets (Web Apps, External IPs, Phishing Targets) for accurate vendor quoting.
*   **Targeted Threat Profiles**: Emulates real-world Advanced Persistent Threats (APTs) required by DORA and PRA.
*   **Execution Constraints & RoE**: Explicitly prohibits dangerous testing methods (like DoS/DDoS) to ensure production safety.
*   **Mandatory Regulatory Deliverables**: Contractually obligates vendors to produce TTIRs, RTTPs, and Cryptographic Attack Logs.
*   **Vendor Qualifications**: Enforces strict CREST/CBEST attestation and liability insurance minimums.

## Installation

Ensure you have Python 3.9+ installed. The project is bundled for native global installation:

```bash
pip install -e .
playwright install chromium
```

## Usage

### 1. Generate the V33 Strategic SOW (PDF)
Use the CLI to construct an engagement mapping specific services against a global compliance pack. The following command generates the massive, premium-styled ultimate scoping document:
```bash
python -m scoper.cli generate-pack --client "Global Financial Bank" --pack global-unified-pack --output output/tlpt_strategy_premium.pdf
```

### 2. View Intelligence Catalogs
Inspect the loaded Red Team services, frameworks, and targeted threat actors:
```bash
scoper dashboard
```

### 3. Classic Markdown SOW Generator
For standard project initialization:
```bash
scoper init MyProject
scoper add MyProject "PT-APP-API"
scoper build MyProject
```

## Architecture
-   `src/scoper/data/intelligence/actors.json`: Target APT profiling.
-   `src/scoper/data/matrix/omni-matrix.json`: Financial resilience control mappings.
-   `src/scoper/assets/style.css`: Premium V33 stylesheet with glassmorphism and print-media adjustments.
-   `src/scoper/generator.py`: The V33 HTML/PDF compiler engine.
