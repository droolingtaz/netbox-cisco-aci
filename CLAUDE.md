# CLAUDE.md

Claude-specific guidance for this repository. The general rules live in
[AGENTS.md](AGENTS.md); this file only adds Claude-specific overrides.

## Read first

1. [AGENTS.md](AGENTS.md) — full repo conventions.
2. [COMPATIBILITY.md](COMPATIBILITY.md) — supported NetBox versions.
3. [CHANGELOG.md](CHANGELOG.md) — what is planned vs. shipped.
4. The relevant model file under `netbox_cisco_aci/models/<domain>/` before
   touching anything in `forms/`, `filtersets/`, `api/`, or `tables/`.

## Workflow

- Make changes in small, reviewable commits. One model per commit when
  possible.
- After any model change, immediately also update:
  the matching serializer, filterset, form, table, view, GraphQL type,
  search index, navigation entry, and tests. Missing one of these is the
  #1 source of regressions in NetBox plugins.
- Generate migrations with `make migrate` (which calls
  `manage.py makemigrations netbox_cisco_aci`); never hand-edit migration
  files after they have been committed.

## Things to avoid

- **`rsplit('/', 1)` on ACI DNs.** Use bracket-aware helpers.
- **`management/commands/` directories.** Use NetBox's `JobRunner`.
- **Direct file I/O.** Go through `django-storages`.
- **`features.updateFields = true`** in any docx generation (carried
  over from the aci-analyzer report — same Word popup applies if we
  ever ship a docx exporter).

## Useful context

The plugin's design grew out of the `aci-analyzer` project (a Python
CLI that pulls APIC config and renders Word as-builts). Some helpers —
particularly DN parsing and the EPG context resolution logic — will
eventually be lifted from there when the APIC-sync background job lands
in a later release.
