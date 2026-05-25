# AGENTS.md

Conventions and guard-rails for AI assistants (Claude, Copilot, Cursor,
Codex, etc.) working in this repository. Human contributors should also
follow these — they exist to keep the plugin maintainable and on-spec
with the NetBox plugin catalogue standards.

## Project at a glance

- **Plugin name (Python package):** `netbox_cisco_aci`
- **PyPI name:** `netbox-cisco-aci`
- **License:** Apache-2.0
- **Supported NetBox:** 4.5.x and 4.6.x (single release supports both)
- **Supported Python:** 3.12 (NetBox 4.5+ requires Python 3.12)
- **Status:** Alpha — model and API may change between 0.x releases.

## Repository layout

```
netbox_cisco_aci/
├── __init__.py            # PluginConfig (min_version, max_version, etc.)
├── version.py             # __version__ — single source of truth
├── choices.py             # Django/NetBox ChoiceSet definitions
├── constants.py           # Magic numbers, regex, content-type tuples
├── validators.py          # Reusable model/field validators
├── navigation.py          # PluginMenu / PluginMenuItem entries
├── search.py              # SearchIndex registrations
├── urls.py                # URL routing for views
├── api/                   # DRF REST API (serializers, views, urls)
├── filtersets/            # django-filter FilterSets per model
├── forms/                 # NetBoxModelForm / BulkEdit / Filter forms
├── graphql/               # Strawberry GraphQL types and filters
├── migrations/            # Django migrations (one per phase, generally)
├── models/                # ORM models, grouped by ACI domain
│   ├── base.py            # Shared abstract base classes
│   ├── mixins.py          # Reusable mixins
│   ├── fabric/            # Fabric, Pod, Node
│   ├── tenant/            # Tenant, VRF, BD, AppProfile, EPG, ESG
│   ├── access/            # VLAN Pools, Domains, AAEP, Switch/Interface profiles
│   ├── contracts/         # Contract, Subject, Filter, Relations
│   ├── l3out/             # L3Out, LNP, LIP, peers, ExtEPG
│   └── bindings/          # Static port bindings (EPG ↔ dcim.Interface)
├── tables/                # django-tables2 tables
├── templates/netbox_cisco_aci/  # Object detail + list templates
├── template_content/      # PluginTemplateExtensions for core NetBox objects
└── tests/                 # Mirrors the package layout
```

## Conventions

### Naming

- **Model class:** `ACI<Object>` — `ACIFabric`, `ACITenant`, `ACIEndpointGroup`, etc.
- **DB table:** `netbox_cisco_aci_<snake>` (default Django naming is fine).
- **URL namespace:** `plugins:netbox_cisco_aci:<model>_list` / `_detail` / etc.
- **GraphQL type:** `ACI<Object>Type`.
- **Choice classes:** `<Domain>Choices` (e.g. `NodeRoleChoices`).

### Models

- All concrete models inherit from `NetBoxModel` (gives change logging,
  journal, custom fields, tags, RBAC out of the box).
- Use `ForeignKey(..., on_delete=models.PROTECT)` for hard parent
  references; `SET_NULL` only when nullability is meaningful.
- Cross-app references to `dcim.Device`, `dcim.Interface`, `ipam.VRF`,
  `ipam.Prefix`, `ipam.IPAddress` should use string FKs to avoid import
  cycles.
- Add field-level `verbose_name` and `help_text` for everything — these
  surface in the UI and API browsable docs.
- Honour `MinValueValidator` / `MaxValueValidator` for any field with a
  Cisco-documented range (Node ID, VLAN, ASN, etc.). Constants live in
  `constants.py`.

### DN parsing (carried over from the upstream aci-analyzer work)

If you ever parse APIC DNs (for example during a sync job), **always**
use bracket-aware helpers — never a naked `rsplit('/', 1)`. ACI embeds
full DNs in the last RN inside `[...]`, and naïve splits cut inside the
brackets and produce silent data loss. Helpers belong in
`netbox_cisco_aci/utils/dn.py` when sync code lands.

### Migrations

- One migration per phase of the build during 0.x — keeps partial
  deployments tractable.
- After 1.0, follow standard NetBox plugin practice: a migration per
  schema-changing PR, never edit migrations in-place after release.

### Tests

- Target **≥70% line coverage** across the package. CI fails if it
  drops below 65%.
- Mirror the package layout under `tests/`.
- Each model has, at minimum: a model test (validation, `__str__`,
  `clean`), a form test (valid + invalid cases), a filterset test, and
  an API test (list/detail/create/update/delete).

### Cloud / Kubernetes compatibility (HARD CONTRACT)

This plugin **must** run unmodified on NetBox Enterprise and NetBox
Cloud. Both run as immutable, horizontally-scalable Kubernetes pods.
That rules out a whole class of patterns that would work fine on a
classic VM install but silently break in a multi-pod environment.

A dedicated CI job (`cloud-compat` in `.github/workflows/ci.yml`)
scans the source tree for the forbidden patterns below and fails the
build on a hit. Treat any new finding as a release blocker — do not
`# noqa` it; fix the design.

**Forbidden — local filesystem and per-pod state**

- No `open(...)`, `pathlib.Path(...).write_*`, `os.makedirs`,
  `os.mkdir`, `os.remove`, `shutil.copy*` against arbitrary paths.
- No `tempfile.NamedTemporaryFile` / `mkdtemp` for anything that needs
  to survive the request that created it. Use the active
  `DEFAULT_FILE_STORAGE` backend instead (which is
  `django-storages` on Enterprise/Cloud).
- No hard-coded paths: `/tmp/...`, `/var/...`, `/opt/netbox/...`,
  `/home/...`. These don't exist (or aren't writeable) in the
  container image.
- No `FileField` / `ImageField` / `FilePathField` without explicit
  `storage=` kwarg routed through `default_storage`.
- No local SQLite, no `shelve`, no on-disk pickle caches.
- No `MEDIA_ROOT` / `STATIC_ROOT` direct access.

**Forbidden — process- and host-level assumptions**

- No Django management commands. Enterprise/Cloud cannot run them on
  demand. Use NetBox's `JobRunner` framework for long-running work
  (APIC sync, bulk import, audits, exports).
- No `threading.Thread`, `multiprocessing.*`, `asyncio.create_task`
  spawned from request paths. The pod can be killed mid-flight.
- No `subprocess.*`. The container has no shell-level tools we can
  depend on.
- No `APScheduler`, `schedule`, `crontab`, or other in-process
  schedulers. Recurring work goes through NetBox jobs + the
  Enterprise scheduler.
- No `socket.bind` / `listen`. Ingress is the platform's job.
- No `logging.FileHandler` / `RotatingFileHandler`. Logs go to stdout
  (Django default) so the platform can collect them.

**Forbidden — per-pod caching**

- No `django.core.cache.backends.locmem` or `filebased` assumptions.
  Anything cached must be safe to evict per-pod (Enterprise/Cloud run
  Redis behind the cache framework).
- No module-level mutable state that holds user/tenant data across
  requests.

**Required**

- Disk I/O goes through `django-storages` via `default_storage`. This
  routes to S3 (or equivalent) on Enterprise/Cloud and the local
  filesystem on a dev VM.
- Background work uses NetBox's `JobRunner` framework. The job
  payload is the state contract — assume the job may run on a
  different pod from the one that enqueued it.
- If you need a one-shot bootstrap (e.g. seed reference data), do it
  through a data migration, not a management command.

### Templates

- Detail templates extend `generic/object.html`.
- List templates extend `generic/object_list.html`.
- Re-usable partials live in `templates/netbox_cisco_aci/inc/`.
- Use NetBox's `htmx_partial` helpers for in-page updates.

### Template extensions

- Lives in `template_content/`. Each extension class targets exactly one
  core NetBox model (`dcim.Device`, `dcim.Interface`, ...).
- Register through `template_extensions` in `netbox_cisco_aci/__init__.py`.
- Keep queries small: prefetch related EPGs/BDs/Subnets in a single
  `select_related` chain and cap the queryset with `[:N]` before
  rendering.

## Working with AI

If you (the AI) are editing this repo:

1. **Read `CLAUDE.md` first** — it has the same content as this file
   plus per-tool overrides.
2. **Check `CHANGELOG.md`** before adding features — there may already
   be a planned entry that constrains the design.
3. **Run `make lint test`** before declaring work done. Both must pass.
4. **Don't add management commands.**
5. **Don't write to disk outside `django-storages`** — see the
   *Cloud / Kubernetes compatibility* section above for the full list
   of forbidden patterns. The `cloud-compat` CI job enforces this.
6. **Don't introduce new third-party deps** without first checking that
   they ship wheels for Python 3.11 and 3.12.
7. **Don't bump `min_version` or `max_version`** in a feature PR — that
   is reserved for explicit compat-bump PRs that also update
   `COMPATIBILITY.md`.

## Useful make targets

```bash
make lint        # ruff + yamllint (uses .yamllint.yml)
make test        # pytest with coverage
make migrate     # apply migrations against the dev NetBox
make shell       # NetBox shell with the plugin pre-loaded
make docs-serve  # mkdocs live preview
```

The ruff and yamllint versions are pinned (see `pyproject.toml`
`[project.optional-dependencies].test` and the CI workflow). Bump
them together to avoid the local/CI formatter drift that bit the
first Phase-2 PR.
