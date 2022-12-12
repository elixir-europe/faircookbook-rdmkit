import requests
from ruamel.yaml import YAML
from github import Github
import sys
import yaml
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re


def client(url):
    """API object fetcher"""
    yaml = YAML()
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=15)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    r = session.get(url)
    if r.status_code == requests.codes.ok:
        return yaml.load(r.text)


def parse_fcb_id(yaml_segment, fcb_new_content):
    """
    Loop over a  segment from the FAIRCookbook TOC dict to populate the new content dictionary with FCBID:Title pairs.
    """
    for recipe in yaml_segment:
        if 'title' in recipe and recipe['title'] and 'file' in recipe and recipe['file'] and recipe.ca.items:
            if 'file' in recipe.ca.items:
                for attr in recipe.ca.items['file']:
                    if attr and attr.value and attr.value.strip():
                        fcb_new_content[attr.value.strip(
                        )] = recipe['title'].strip()

            elif 'title' in recipe.ca.items:
                for attr in recipe.ca.items['title']:
                    if attr and attr.value and attr.value.strip():
                        fcb_new_content[attr.value.strip(
                        )] = recipe['title'].strip()

        if 'sections' in recipe and recipe['sections']:
            parse_fcb_id(recipe['sections'], fcb_new_content)


def parse_rdmkit_id(yaml_segment, rdmkit_new_content):
    """
    Populate the new content dictionary with RDMkitURL:Title pairs.
    """
    if 'subitems' in yaml_segment and yaml_segment['subitems']:
        for page in yaml_segment['subitems']:
            if 'title' in page and page['title'] and 'url' in page and page['url']:
                rdmkit_new_content[page['url'].strip("/")] = page['title']
            if 'subitems' in page and page['subitems']:
                parse_rdmkit_id(page, rdmkit_new_content)

            
# Params
fcb_content_url = "https://raw.githubusercontent.com/FAIRplus/the-fair-cookbook/main/_toc.yml"
fcb_cache_path = 'cached-branch/cache/fcb_content.yaml'

rdmkit_content_url = "https://raw.githubusercontent.com/elixir-europe/rdmkit/master/_data/sidebars/data_management.yml"
rdmkit_cache_path = 'cached-branch/cache/rdmkit_content.yaml'


# ---- Parsing content from resources ----

print('Parsing content from resources')
# Parse FCB remote TOC yml file
fcb_new_content = {}
fcb_content = client(fcb_content_url)
for part in fcb_content:
    if 'chapters' in part and part['chapters']:
        parse_fcb_id(part['chapters'], fcb_new_content)
print('... FCB Parsed')

# Parse RDMkit sidebar yml file
rdmkit_new_content = {}
rdmkit_content = client(rdmkit_content_url)
parse_rdmkit_id(rdmkit_content, rdmkit_new_content)
print('... RDMkit Parsed')

# ---- Parsing cached content ----

# FAIRCookbook
with open(fcb_cache_path, 'r') as fcb_cache:
    fcb_cached_content = yaml.load(fcb_cache, Loader=yaml.FullLoader)

# RDMkit
with open(rdmkit_cache_path, 'r') as rdmkit_cache:
    rdmkit_cached_content = yaml.load(rdmkit_cache, Loader=yaml.FullLoader)


# ---- Create GitHub connection ----

github_token = sys.argv[1]
g = Github(github_token)
repo = g.get_repo("elixir-europe/faircookbook-rdmkit")


# ---- Create New Issue if a change is made in the pulled content compared to the cached content ----

# FAIRCookbook
for fcb_new_content_id, fcb_new_content_title in fcb_new_content.items():
    if fcb_new_content_id not in fcb_cached_content:
        repo.create_issue(title=f"A new recipe was added to FCB: {fcb_new_content_id}", body=f"The recipe with FCB identifier {fcb_new_content_id} and title '{fcb_new_content_title}' was created.", labels=["new content","bot"])
        print(f"A new recipe was added to FCB: {fcb_new_content_id}")
# RDMkit
for rdmkit_new_content_id, rdmkit_new_content_title in rdmkit_new_content.items():
    if rdmkit_new_content_id not in rdmkit_cached_content:
        repo.create_issue(title=f"A new page was added to RDMkit: {rdmkit_new_content_id}", body=f"The page with RDMkit path {rdmkit_new_content_id} and title '{rdmkit_new_content_title}' was created.", labels=["new content","bot"])
        print(f"A new page was added to RDMkit: {rdmkit_new_content_id}")

# ---- Update cached content files ----

# FAIRCookbook
contents = repo.get_contents(fcb_cache_path, ref="cache")
repo.update_file(contents.path, "Update cache file", yaml.safe_dump(fcb_new_content, sort_keys=True), contents.sha, branch="cache")

# RDMkit
contents = repo.get_contents(rdmkit_cache_path, ref="cache")
repo.update_file(contents.path, "Update cache file", yaml.safe_dump(rdmkit_new_content, sort_keys=True), contents.sha, branch="cache")
