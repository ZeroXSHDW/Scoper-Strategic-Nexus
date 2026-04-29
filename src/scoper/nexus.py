import json
from pathlib import Path
from typing import List, Dict, Any

class NexusEngine:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.radar = json.loads((data_dir / 'matrix' / 'nexus-radar.json').read_text(encoding='utf-8'))
        self.custody = json.loads((data_dir / 'matrix' / 'custody.json').read_text(encoding='utf-8'))

    def calculate_nexus_score(self, codes: List[str]) -> Dict[str, Any]:
        score = 0
        has_va = any('VA' in c for c in codes)
        
        coverage = {
            'P_GOV': True,
            'P_RES': any('RT' in c for c in codes),
            'P_INT': any('WEB' in c for c in codes),
            'P_PRI': any('GDPR' in c for c in codes) or has_va,
            'P_SOV': True,
            'P_ID': any('SOC' in c for c in codes)
        }

        for p in self.radar.get('pillars', []):
            if coverage.get(p.get('id')):
                score += p.get('weight', 0)

        return {'score': score, 'coverage': coverage}

    @property
    def custody_steps(self):
        return self.custody.get('steps', [])
