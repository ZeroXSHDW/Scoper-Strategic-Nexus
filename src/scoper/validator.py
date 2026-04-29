"""Data Validation Engine for Scoper."""

import json
from pathlib import Path
from typing import Dict, Any

class Validator:
    """Validates the structure and references in the scoper data catalog."""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def validate(self) -> Dict[str, Any]:
        """Run validation on the data catalog."""
        results = {
            "errors": [],
            "warnings": [],
            "passed": True
        }

        try:
            catalog_path = self.data_dir / "services" / "catalog.json"
            packs_path = self.data_dir / "compliance" / "packs.json"

            if not catalog_path.exists():
                results["errors"].append(f"Catalog file missing at {catalog_path}")
                results["passed"] = False
                return results

            if not packs_path.exists():
                results["errors"].append(f"Packs file missing at {packs_path}")
                results["passed"] = False
                return results

            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            packs = json.loads(packs_path.read_text(encoding="utf-8"))

            catalog_codes = {s.get("code") for s in catalog if isinstance(s, dict)}

            # Validate Packs
            for pack in packs.get("packs", []):
                for code in pack.get("services", []):
                    if code not in catalog_codes:
                        results["errors"].append(f"Pack [{pack.get('id')}] references non-existent service code: {code}")
                        results["passed"] = False

            # Validate Catalog
            for service in catalog:
                if not isinstance(service, dict):
                    continue
                if not service.get("code") or not service.get("label") or "priceRangeMin" not in service:
                    results["errors"].append(f"Service entry missing mandatory fields: {service.get('code', 'UNKNOWN')}")
                    results["passed"] = False

        except Exception as e:
            results["errors"].append(f"Validation crashed: {str(e)}")
            results["passed"] = False

        return results
