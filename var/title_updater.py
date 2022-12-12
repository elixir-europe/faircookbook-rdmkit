
from ruamel.yaml import YAML
import yaml
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re

yaml = YAML()

# Params
fcb_cache_path = 'cached-branch/cache/fcb_content.yaml'
rdmkit_cache_path = 'cached-branch/cache/rdmkit_content.yaml'
mapping_path = 'faircookbook_rdmkit_mapping.yml'

# ---- Parsing cached content ----

# FAIRCookbook
with open(fcb_cache_path, 'r') as fcb_cache:
    fcb_cached_content = yaml.load(fcb_cache)

# RDMkit
with open(rdmkit_cache_path, 'r') as rdmkit_cache:
    rdmkit_cached_content = yaml.load(rdmkit_cache)

# ---- Parsing mapping file ----
# RDMkit
with open(mapping_path, 'r') as mapping_file:
    mapping_dict = yaml.load(mapping_file)

# ---- Updating mapping dict with titles from respective cache files ----

for i,rdmkit_page in enumerate(mapping_dict):
    if rdmkit_page['rdmkit_filename'] in rdmkit_cached_content:
        mapping_dict[i]['rdmkit_title'] = rdmkit_cached_content[rdmkit_page['rdmkit_filename']]
    if 'links' in rdmkit_page and rdmkit_page['links']:
        for j,fcb_recipe in enumerate(rdmkit_page['links']):
            if fcb_recipe['fcb_id'] in fcb_cached_content:
                mapping_dict[i]['links'][j]['fcb_title'] = fcb_cached_content[fcb_recipe['fcb_id']]

# ---- Dump changes to file ----

with open(mapping_path, 'w') as mapping_file:
    yaml.dump(mapping_dict, mapping_file)
