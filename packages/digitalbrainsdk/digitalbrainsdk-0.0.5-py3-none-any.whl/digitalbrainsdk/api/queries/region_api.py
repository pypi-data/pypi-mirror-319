import requests
from digitalbrainsdk.api.api.core import Core
from digitalbrainsdk.config import ConfigManager
import os
from treelib import Tree

class RegionApi:
    def __init__(self, environment="PRODUCTION", species="mouse"):
        self.core = Core(environment)
        self.region_data = None
        self.region_type = None
        self.species = species
        cache_dir_name = ConfigManager().get("CACHE", "CacheDir")
        self.cache_dir = None
        if not self.cache_dir:
            self.cache_dir = os.path.join(os.getcwd(), cache_dir_name)
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_region(self, id=None, file=None):
        if not self.region_data:
            self._download_region_data()
        target_region = None
        if self.region_data:
            if id:
                target_region = self._get_region_by_id(id)
            elif file:
                target_region = self._get_region_by_file(file)
        if target_region:
            content =  self._download_region(target_region)
            file_path = f"{self.cache_dir}/{target_region['file']}"
            with open(file_path, 'wb') as f:
                f.write(content)
            return file_path
        return None

    def _download_region_data(self):
        url = f"{self.core.base_url}/info/{self.species}/{self.species}.region.info.json"
        response = requests.get(url)
        self.region_data = response.json()["region_data"]
        self.region_type = response.json()["region_type"]
            

    def _get_region_by_id(self, id):
        if self.region_data and id in self.region_data:
            return self.region_data[id]
        return None

    def _get_region_by_file(self, file):
        if self.region_data:
            for _, region in self.region_data.items():
                if region["file"] == file:
                    return region
    
    def _download_region(self, region):
        # TODO
        return f"test {region['file']}".encode()
    
    def _recover_tree(self,json_file, tree=Tree()):
        for node in json_file:
            if isinstance(node, dict):
                if node['parent_uid']==None:
                    tree.create_node(identifier=node['id'], data={'acronym':node['acronym'], 'name':node['name']})
                else:
                    tree.create_node(identifier=node['id'], data={'acronym':node['acronym'], 'name':node['name']}, 
                                        parent=node['parent_uid'])
                for item in node.keys():
                    if isinstance(node[item], list) and len(node[item])>0:
                        self._recover_tree(node[item], tree=tree)
        return tree

    def region_tree(self):
        if not self.region_data:
            self._download_region_data()
        return self._recover_tree(self.region_data)
