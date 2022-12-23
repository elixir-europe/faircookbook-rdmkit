# FAIR Cookbook - RDMkit

This repository will in the first place be used to link pages between [FAIR Cookbook](https://faircookbook.elixir-europe.org/) and [RDMkit](https://rdmkit.elixir-europe.org/). These links are made and curated by the joint editorial board that exists between both teams. 

Both websites have their content managed and deployed using GitHub:

- RDMkit: https://github.com/elixir-europe/rdmkit
- FAIR Cookbook: https://github.com/FAIRplus/the-fair-cookbook

## Who are we?

To align visions and to keep track of content changes in both repositories we created a joint editorial board between FAIR Cookbook and RDMkit. This board meets every two months.

## The core of our collaboration

Links between the two services are stored in the [`faircookbook_rdmkit_mapping.yml`](https://github.com/elixir-europe/faircookbook-rdmkit/blob/main/faircookbook_rdmkit_mapping.yml) file. Changes made to this file will not immediately impact the websites. On a weekly basis FAIR Cookbook and RDMkit will pull changes from this central YAML file to update there repository. This is done using GitHub actions and is fully automatic. Any links towards FAIR Cookbook/RDMkit that were made manually will be overwritten by this process. In short: this repository holds the truth!

### Code of conduct

Changes made to the [`faircookbook_rdmkit_mapping.yml`](https://github.com/elixir-europe/faircookbook-rdmkit/blob/main/faircookbook_rdmkit_mapping.yml) file will be merged in the `main` branch using pull requests and only when at least one member of each editorial team has approved the changes. The `main` branch is for this reason protected against direct changes to prevent unexpected behaviour on one of the resources.

### Mapping rules
- Data life cycle, your role, and national resources pages are not linked to recipes.
- Domain pages should only link to domain specific recipes.
- Task pages should only link to recipes for generic tasks.

## GitHub Actions to increase sustainability

Because new content gets created over time in both resources, we created two automations to increase the sustainability.

### Automatic updating of the titles in the mapping file

Titles can change, and since the resources list links towards each other including the title, we've put a system in place to prevent they get out of sync with the actual titles. A GitHub action will weekly check for title changes using information from the sidebars of each resource and create a pull request updating the titles in the main YAML file accordingly.

### Automatic issue creation when new content is added to one of the resources

Due to the changing nature of both resources, we will have to repeat the mapping exercise in the future. To make this job easier, we keep track of changes in both resources using GitHub issues which are opened automatically on this repository. Cache files in the `cache` branch are build using the sidebar files of both resources and store the content in the shape of title:url key-value pairs. If a new page or recipe gets added, an issue will be created describing this addition. This GitHub Action is run weekly. The `cache` branch should never be deleted!


---

<img src="https://faircookbook.elixir-europe.org/_static/cookbook-logo-small.png" alt="FAIR Cookbook logo" width="200"/>     

<img src="https://raw.githubusercontent.com/elixir-europe/rdmkit/master/assets/img/RDMkit_logo.svg" alt="RDMkit logo" width="150"/>

