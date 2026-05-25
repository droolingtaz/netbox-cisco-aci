# Development

## Quickstart

```bash
git clone https://github.com/bparker-e280/netbox-aci
cd netbox-aci
python -m venv .venv && source .venv/bin/activate
pip install -e ".[test,docs]"
```

You also need a working NetBox checkout (4.5.x or 4.6.x). Symlink the
plugin into it or `pip install -e` from the NetBox venv.

## Common loops

```bash
make lint        # ruff + yamllint
make test        # pytest with coverage gate
make migrate     # apply migrations to dev NetBox
make shell       # NetBox shell with plugin pre-loaded
```

## Adding a model

1. Add the model class under `netbox_aci/models/<domain>/`.
2. Register it in the domain's `__init__.py`.
3. Generate the migration: `make makemigrations`.
4. Add serializer, view, filterset, form, table, GraphQL type, search
   index, and navigation entry.
5. Add tests under `netbox_aci/tests/` mirroring the package layout.
6. Update `CHANGELOG.md`.

See [AGENTS.md](../AGENTS.md) for the full conventions list.
