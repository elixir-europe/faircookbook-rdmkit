
from ruamel.yaml import YAML
import yaml
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re

yaml = YAML()

# Params
fcb_cache_path = 'cache/fcb_content.yaml'
rdmkit_cache_path = 'cache/rdmkit_content.yaml'
mapping_path = 'faircookbook_rdmkit_mapping.yml'

# ---- Parsing cached content ----

# FAIRCookbook
with open(fcb_cache_path, 'r') as fcb_cache:
    fcb_cached_content = yaml.load(fcb_cache, Loader=yaml.FullLoader)

# RDMkit
with open(rdmkit_cache_path, 'r') as rdmkit_cache:
    rdmkit_cached_content = yaml.load(rdmkit_cache, Loader=yaml.FullLoader)

# ---- Parsing mapping file ----
# RDMkit
with open(mapping_path, 'r') as mapping_file:
    mapping_dict = yaml.load(mapping_file, Loader=yaml.FullLoader)

# ---- Updating mapping dict with titles from respective cache files ----

for rdmkit_page in mapping_dict:
    if rdmkit_page['rdmkit_filename'] in rdmkit_cached_content:
        rdmkit_page['rdmkit_title'] = rdmkit_cached_content[rdmkit_page['rdmkit_filename']]
    if 'links' in rdmkit_page and rdmkit_page['links']:
        for fcb_recipe in rdmkit_page['links']:
            if fcb_recipe['fcb_id'] in fcb_cached_content:
                fcb_recipe['fcb_title'] = fcb_cached_content[fcb_recipe['fcb_id']]