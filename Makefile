# db2-parser Makefile
# Downloads WoW DB2 tables from wago.tools

PYTHON := python3
SCRIPTS := scripts
ARTIFACTS := artifacts
SCHEMA := schema

# Crafting-focused tables
TABLES := Spell SpellName Item ItemSparse SkillLine SkillLineAbility SpellReagents SpellEffect

# Fetch specific version
# Usage: make fetch VERSION=2.5.5.65463
fetch:
ifndef VERSION
	$(error VERSION is required. Usage: make fetch VERSION=2.5.5.65463)
endif
	@$(PYTHON) $(SCRIPTS)/fetch.py --version $(VERSION) --tables $(TABLES) --output $(ARTIFACTS)

# Fetch latest for expansion
# Usage: make latest EXPANSION=2
latest:
ifndef EXPANSION
	$(error EXPANSION is required. Usage: make latest EXPANSION=2)
endif
	@$(PYTHON) $(SCRIPTS)/latest.py --expansion $(EXPANSION) --tables $(TABLES) --output $(ARTIFACTS)

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
	@echo "Available tables:"
	@for table in $(TABLES); do echo "  - $$table"; done

.PHONY: fetch latest validate clean list-tables
