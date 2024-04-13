# Variables
BLACK = black
AUTOFLAKE = autoflake

# Directories
SRC_DIR = *.py 

# Targets
.PHONY: format
format:
	$(BLACK) $(SRC_DIR)

.PHONY: lint
lint:
	$(BLACK) --check $(SRC_DIR)

.PHONY: remove_unused_imports
remove_unused_imports:
	$(AUTOFLAKE) --remove-all-unused-imports --in-place $(SRC_DIR)
	@echo "Unused imports removed successfully."

.PHONY: run
run:
	uvicorn main:app --reload --log-level debug 