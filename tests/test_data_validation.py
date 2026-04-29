import json
from pathlib import Path

def test_packs_json_structure():
    data_dir = Path(__file__).parent.parent / "src" / "scoper" / "data"
    packs_file = data_dir / "compliance" / "packs.json"
    assert packs_file.exists(), "packs.json does not exist"
    
    with open(packs_file, 'r') as f:
        data = json.load(f)
        
    assert "packs" in data
    for pack in data["packs"]:
        assert "id" in pack
        assert "label" in pack
        assert "frameworks" in pack
        assert isinstance(pack["frameworks"], list)
        assert "services" in pack
        assert isinstance(pack["services"], list)

def test_frameworks_json_structure():
    data_dir = Path(__file__).parent.parent / "src" / "scoper" / "data"
    frameworks_file = data_dir / "compliance" / "frameworks.json"
    assert frameworks_file.exists(), "frameworks.json does not exist"
    
    with open(frameworks_file, 'r') as f:
        data = json.load(f)
        
    assert "frameworks" in data
    for framework in data["frameworks"]:
        assert "id" in framework
        assert "name" in framework
        assert "region" in framework

def test_relational_integrity():
    data_dir = Path(__file__).parent.parent / "src" / "scoper" / "data"
    packs_file = data_dir / "compliance" / "packs.json"
    frameworks_file = data_dir / "compliance" / "frameworks.json"
    
    with open(packs_file, 'r') as f:
        packs_data = json.load(f)
        
    with open(frameworks_file, 'r') as f:
        frameworks_data = json.load(f)
        
    valid_framework_ids = {fw["id"] for fw in frameworks_data.get("frameworks", [])}
    
    for pack in packs_data["packs"]:
        # Ensure at least one primary regulatory framework from the pack exists in frameworks.json
        mapped = [fid for fid in pack["frameworks"] if fid in valid_framework_ids]
        assert len(mapped) > 0, f"Pack {pack['id']} has no valid core regulatory frameworks defined in frameworks.json"
