# Compatibility matrix

This page mirrors
[`COMPATIBILITY.md`](https://github.com/droolingtaz/netbox-cisco-aci/blob/main/COMPATIBILITY.md)
at the repo root, which is the source of truth checked by the NetBox
plugin catalogue.

| Plugin version | NetBox versions | Python | Status |
| --- | --- | --- | --- |
| `0.1.x` | 4.5.x, 4.6.x | 3.12 | Current |

## Why a single release line covers both NetBox 4.5 and 4.6

NetBox 4.5 and 4.6 share a compatible plugin API. The plugin's
`PluginConfig.min_version='4.5.0'` and `max_version='4.6.99'` declare
the support window explicitly, and the CI matrix runs the full test
suite against both NetBox versions on every push and pull request.

## Forward compatibility

Future NetBox 4.7+ support will require:

1. Bumping `max_version` in `netbox_cisco_aci/__init__.py`.
2. Adding the new NetBox version to the CI matrix.
3. Cutting a new release line.

Per [`AGENTS.md`](https://github.com/droolingtaz/netbox-cisco-aci/blob/main/AGENTS.md),
`min_version` and `max_version` must not be touched in feature PRs;
they are reserved for explicit compat-bump PRs that also update this
file and the test matrix.

## NetBox Enterprise and NetBox Cloud

The plugin runs unmodified on both. See
[Cloud / Kubernetes compatibility](cloud-compatibility.md) for the
hard contract this is built on.
