# netbox-cisco-aci

A [NetBox](https://netboxlabs.com/oss/netbox/) plugin for **operational
visibility and documentation of Cisco ACI** fabrics.

Models every ACI construct needed for daily operations — Fabrics, Pods,
Nodes (linked to existing `dcim.Device` records), Tenants, VRFs, Bridge
Domains and subnets, Application Profiles, EPGs / ESGs (including uSeg),
Contracts / Subjects / Filters, AAEPs, Domains, VLAN Pools, Switch and
Interface profiles, L3Outs (with BGP / OSPF / EIGRP peers and External
EPGs), and **per-interface EPG/BD/Subnet bindings** so you can see the
ACI policy applied to any device or port at a glance.

[![CI](https://github.com/droolingtaz/netbox-cisco-aci/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/droolingtaz/netbox-cisco-aci/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/droolingtaz/netbox-cisco-aci/branch/main/graph/badge.svg)](https://codecov.io/gh/droolingtaz/netbox-cisco-aci)
[![PyPI](https://img.shields.io/pypi/v/netbox-cisco-aci.svg?label=pypi)](https://pypi.org/project/netbox-cisco-aci/)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://pypi.org/project/netbox-cisco-aci/)
[![NetBox](https://img.shields.io/badge/netbox-4.5%20%7C%204.6-26a69a.svg)](COMPATIBILITY.md)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-526CFE.svg)](https://droolingtaz.github.io/netbox-cisco-aci/)

## Compatibility

See the [compatibility matrix](COMPATIBILITY.md) for supported NetBox versions.

The plugin is designed to run unmodified on **NetBox Enterprise** and
**NetBox Cloud** (both Kubernetes-based, multi-pod, immutable
filesystems) as well as classic single-VM installs. The contract is
documented in [`docs/cloud-compatibility.md`](docs/cloud-compatibility.md)
and enforced by the `cloud-compat` CI job.

## Features

- **Fabric topology** — Fabric → Pod → Node, with each Node optionally
  linked to a `dcim.Device` so existing inventory remains the source of
  truth for hardware.
- **Tenancy model** — Tenant → VRF, Bridge Domain (+ Subnets),
  Application Profile → EPG / ESG, including uSeg attributes.
- **Access policies** — VLAN Pools, Physical / L3 / VMM Domains, AAEPs
  with EPG mappings, Switch Profiles, Interface Profiles, Interface
  Policy Groups, and per-policy refs (CDP / LLDP / LACP / MCP / STP /
  Link Level).
- **Contracts** — Contracts, Subjects, Filters with entries, and
  Provider / Consumer relations (including `common`-tenant imports and
  inter-VRF / shared-services patterns).
- **L3Outs** — Logical Node Profiles, Logical Interface Profiles
  (routed / SVI / sub-interface), BGP / OSPF / EIGRP peers, External
  EPGs with subnets and contract bindings.
- **Device & interface visibility** — every static port binding links
  an EPG to a `dcim.Interface`. The plugin injects panels on both the
  Device and Interface detail views showing the EPGs, BDs, Subnets, and
  VRFs that touch that hardware.
- **Full NetBox surface** — REST API, GraphQL, search, navigation,
  change-logging, journal, custom fields, tags, and per-object RBAC.

## Installation

```bash
source /opt/netbox/venv/bin/activate
pip install netbox-cisco-aci
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`:

```python
PLUGINS = ['netbox_cisco_aci']
```

Run migrations and restart NetBox:

```bash
python /opt/netbox/netbox/manage.py migrate
sudo systemctl restart netbox netbox-rq
```

Add `netbox-cisco-aci` to `local_requirements.txt`.

## Configuration

The plugin works with sensible defaults. Optional settings live under
`PLUGINS_CONFIG['netbox_cisco_aci']` — see the [configuration docs](docs/configuration.md).

## Development

See [AGENTS.md](AGENTS.md) for repository conventions and
[docs/development.md](docs/development.md) for the dev-loop quickstart.

## Licensing

Apache License 2.0 — see [LICENSE](LICENSE).
