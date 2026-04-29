import json
import os

class DataProvider:
    def __init__(self, data_dir=None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        else:
            self.data_dir = data_dir
        
        self.catalogs = {}
        self._load_all()

    def _load_json(self, relative_path):
        filepath = os.path.join(self.data_dir, relative_path)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _load_all(self):
        self.catalogs['services'] = self._load_json(os.path.join('services', 'catalog.json')).get('services', [])
        self.catalogs['frameworks'] = self._load_json(os.path.join('compliance', 'frameworks.json')).get('frameworks', [])
        self.catalogs['packs'] = self._load_json(os.path.join('compliance', 'packs.json')).get('packs', [])
        self.catalogs['omni_controls'] = self._load_json(os.path.join('matrix', 'omni-matrix.json')).get('omni_controls', [])
        self.catalogs['raci'] = self._load_json(os.path.join('matrix', 'raci.json')).get('raci', [])
        self.catalogs['actors'] = self._load_json(os.path.join('intelligence', 'actors.json')).get('actors', [])

    def get_pack(self, pack_id):
        for pack in self.catalogs['packs']:
            if pack['id'] == pack_id:
                return pack
        return None

    def get_framework(self, framework_id):
        for fw in self.catalogs['frameworks']:
            if fw['id'] == framework_id:
                return fw
        return None

    def get_service(self, service_id):
        for svc in self.catalogs['services']:
            if svc['id'] == service_id:
                return svc
        return None

    def get_omni_controls(self):
        return self.catalogs['omni_controls']

    def get_raci(self):
        return self.catalogs['raci']

    def get_actor(self, actor_id):
        for act in self.catalogs['actors']:
            if act['id'] == actor_id:
                return act
        return None
