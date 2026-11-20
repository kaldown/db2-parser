# db2-parser Makefile
# Downloads WoW DB2 tables from wago.tools

PYTHON := python3
SCRIPTS := scripts
ARTIFACTS := artifacts
SCHEMA := schema

# Crafting-focused tables. A required table missing from a build fails the fetch.
TABLES := Spell SpellName Item ItemSparse SkillLine SkillLineAbility SpellReagents SpellEffect ItemEffect Faction SpellTotems TotemCategory

# Fetched best-effort: present only in some builds (see BUILDS.md).
# ItemXItemEffect links recipe items to their effects where ItemEffect has no ParentItemID (Forever).
OPTIONAL_TABLES := ItemXItemEffect

# Fetch specific version
# Usage: make fetch VERSION=2.5.5.65463
fetch:
ifndef VERSION
	$(error VERSION is required. Usage: make fetch VERSION=2.5.5.65463)
endif
	@$(PYTHON) $(SCRIPTS)/fetch.py --version $(VERSION) --tables $(TABLES) --optional-tables $(OPTIONAL_TABLES) --output $(ARTIFACTS)

# Fetch latest build for expansion, within one wago.tools product
# Usage: make latest EXPANSION=1 PRODUCT=wow_classic_era
# Without PRODUCT it stops if several products have builds for that major version.
latest:
ifndef EXPANSION
	$(error EXPANSION is required. Usage: make latest EXPANSION=1 PRODUCT=wow_classic_era)
endif
	@$(PYTHON) $(SCRIPTS)/latest.py --expansion $(EXPANSION) $(if $(PRODUCT),--product $(PRODUCT)) --tables $(TABLES) --optional-tables $(OPTIONAL_TABLES) --output $(ARTIFACTS)

# List builds (product, version, date) for a major version
# Usage: make list-builds EXPANSION=1 [PRODUCT=wowf]
list-builds:
ifndef EXPANSION
	$(error EXPANSION is required. Usage: make list-builds EXPANSION=1 [PRODUCT=wowf])
endif
	@$(PYTHON) $(SCRIPTS)/latest.py --expansion $(EXPANSION) $(if $(PRODUCT),--product $(PRODUCT)) --list

# Validate schema matches downloaded CSVs
# Usage: make validate VERSION=2.5.5.65463
validate:
ifndef VERSION
	$(error VERSION is required. Usage: make validate VERSION=2.5.5.65463)
endif
	@$(PYTHON) $(SCRIPTS)/validate.py --version $(VERSION) --schema $(SCHEMA) --artifacts $(ARTIFACTS)

# Remove all artifacts
clean:
	rm -rf $(ARTIFACTS)/*

# List available tables
list-tables:
	@echo "Required tables:"
	@for table in $(TABLES); do echo "  - $$table"; done
	@echo "Optional tables:"
	@for table in $(OPTIONAL_TABLES); do echo "  - $$table"; done

.PHONY: fetch latest list-builds validate clean list-tables
