# Cloud / Kubernetes compatibility

`netbox-cisco-aci` runs unmodified on **NetBox Enterprise** and
**NetBox Cloud**, in addition to classic single-VM NetBox installs.

Both Enterprise and Cloud run NetBox as immutable, horizontally-scalable
Kubernetes pods with an ephemeral filesystem and a shared Redis + S3
backplane. That puts hard limits on what a plugin can do safely.

## What the plugin does

- **All disk I/O routed through `default_storage` (django-storages).**
  When (and only when) a future phase needs to persist files
  (e.g. exported APIC config snapshots), it will use Django's storage
  abstraction. On Enterprise/Cloud this resolves to the platform's S3
  backend automatically — no plugin-side config required.

- **Background work uses NetBox's `JobRunner` framework.** When the
  APIC sync layer lands, every long-running task (sync, audit, bulk
  import, export) goes through the same job queue NetBox itself uses.
  Jobs are durable, observable in the NetBox UI, and survive pod
  restarts.

- **No Django management commands.** Enterprise/Cloud cannot invoke
  them on demand. Any one-shot bootstrap work happens through a data
  migration; recurring work happens through the platform scheduler.

- **No per-pod state.** No in-process caches, no file-backed
  scratchpads, no module-level mutable state holding tenant data.

## What the plugin will never do

The full forbidden-pattern list lives in
[`AGENTS.md`](https://github.com/droolingtaz/netbox-cisco-aci/blob/main/AGENTS.md) under
*"Cloud / Kubernetes compatibility (HARD CONTRACT)"*. The short
version:

- No `open()` for writes, no `tempfile`, no `pathlib` write/mutate
  methods, no `shutil` file ops, no hard-coded host paths
  (`/tmp`, `/var`, `/opt/netbox`, ...).
- No `FileField` / `ImageField` without an explicit `storage=` kwarg
  routed through `default_storage`.
- No `threading.Thread`, `multiprocessing`, `subprocess`, or
  `socket.bind` in request paths.
- No in-process schedulers (`APScheduler`, `schedule`, `sched`).
- No `locmem` / `filebased` cache assumptions — the platform's Redis
  cache is the single source of truth.
- No `FileHandler` / `RotatingFileHandler` — logs go to stdout for
  the platform to collect.

## How the contract is enforced

A dedicated CI job (`cloud-compat`) runs
[`scripts/check_cloud_compat.py`](https://github.com/droolingtaz/netbox-cisco-aci/blob/main/scripts/check_cloud_compat.py) on
every push and pull request. The job is part of the required check set
on `main` — a violation fails the build and blocks the merge.

If you genuinely need an exception (rare — usually means reading a
package-shipped data file via `importlib.resources`), add a
`# cloud-compat: ok` comment on the offending line. Each exemption
must be justified in the PR description.

## Why this matters

NetBox Cloud is the simplest path to running the plugin without
operating any infrastructure yourself, and a plugin that silently
misbehaves there is effectively unmaintained for that audience. By
treating the contract as a CI gate rather than a style guideline, we
keep the plugin shippable to Cloud and Enterprise from day one.
