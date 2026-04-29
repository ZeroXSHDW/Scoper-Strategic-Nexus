# Scoper: V33 Omni-Strategic Nexus

Scoper is an enterprise-grade, intelligence-led scoping engine built for financial regulatory frameworks (DORA, CBEST, MAS, FRB).

This project features the highly advanced **V33 Omni-Strategic Nexus** architecture, generating beautiful, board-ready Threat-Led Penetration Testing (TLPT) documentation.

🚀 **[View the Sample Output PDF](examples/Sample_Nexus_Pack.pdf)**

## Core Features
*   **Omni-Strategic Radar Charts**: Dynamically generates compliance coverage mapping (P_RESILIENCE, P_INTELLIGENCE, P_GOVERNANCE).
*   **Targeted Threat Profiles**: Emulates real-world Advanced Persistent Threats (APTs) like Cozy Bear (APT29), FIN7, and Lazarus Group.
*   **Execution Timeline (CSS Gantt)**: Beautiful, pure-CSS auto-generated Gantt charts for tracking engagement phases.
*   **Digital Chain of Custody**: Cryptographically-verifiable evidence chains across the Red Team lifecycle.
*   **RACI Matrices & Omni-Controls**: Granular mappings to financial resilience controls with explicit client-provider responsibility assignments.

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
