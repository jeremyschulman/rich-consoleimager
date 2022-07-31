PACKAGE_and_VERSION = $(shell poetry version)
PACKAGE_NAME = $(word 1, $(PACKAGE_and_VERSION))
PACKAGE_VERSION = $(word 2, $(PACKAGE_and_VERSION))

# -----------------------------------------------------------------------------
# Devel targets
# -----------------------------------------------------------------------------

.PHONY: precheck
precheck:
	black .
	pre-commit run -a
	interrogate -c pyproject.toml

.PHONY: test
test:
	cd tests && pytest

.PHONY: run
run:
	poetry run ${PACKAGE_NAME}

kill:
	pgrep -f ${PACKAGE_NAME} | xargs kill -9

clean:
	rm -rf .pytest_cache
	find . -name '__pycache__' | xargs rm -rf

