import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any

class OmniController:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.omni = json.loads((data_dir / 'matrix' / 'omni-matrix.json').read_text(encoding='utf-8'))
        self.raci = json.loads((data_dir / 'matrix' / 'raci.json').read_text(encoding='utf-8'))

    def get_control_mappings(self, service_codes: List[str]) -> List[Dict[str, Any]]:
        covered_ids = set()
        service_control_map = self.omni.get('service_control_map', {})
        for code in service_codes:
            ids = service_control_map.get(code, [])
            for id_ in ids:
                covered_ids.add(id_)
        
        controls = self.omni.get('controls', [])
        return [c for c in controls if c.get('id') in covered_ids]

    def get_fingerprint(self, data: Any) -> str:
        data_str = json.dumps(data, separators=(',', ':'))
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest().upper()

    def get_raci_rows(self) -> List[Any]:
        return self.raci.get('matrix', [])

    def get_raci_roles(self) -> List[Any]:
        return self.raci.get('roles', [])
