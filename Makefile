.PHONY: help install lint test test-cov migrate makemigrations shell docs-serve clean

NETBOX_DIR ?= /opt/netbox
NETBOX_MANAGE := $(NETBOX_DIR)/netbox/manage.py
PY := python

help:
	@echo "Common targets:"
	@echo "  make install         Install plugin in editable mode with test extras"
	@echo "  make lint            Run ruff + yamllint"
	@echo "  make test            Run the test suite"
	@echo "  make test-cov        Run tests and emit an HTML coverage report"
	@echo "  make migrate         Apply migrations against the dev NetBox"
	@echo "  make makemigrations  Generate new migrations for netbox_aci"
	@echo "  make shell           Open the NetBox shell with the plugin loaded"
	@echo "  make docs-serve      Live-preview the mkdocs site"
	@echo "  make clean           Remove build artefacts"

install:
	pip install -e ".[test,docs]"

lint:
	ruff check netbox_aci
	ruff format --check netbox_aci
	yamllint -s .github

test:
	pytest

test-cov:
	pytest --cov-report=html

migrate:
	$(PY) $(NETBOX_MANAGE) migrate netbox_aci

makemigrations:
	$(PY) $(NETBOX_MANAGE) makemigrations netbox_aci

shell:
	$(PY) $(NETBOX_MANAGE) shell_plus || $(PY) $(NETBOX_MANAGE) shell

docs-serve:
	mkdocs serve

clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	find . -name __pycache__ -type d -exec rm -rf {} +
