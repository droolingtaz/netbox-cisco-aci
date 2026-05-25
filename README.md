# netbox-aci

A [NetBox](https://netboxlabs.com/oss/netbox/) plugin for **operational
visibility and documentation of Cisco ACI** fabrics.

Models every ACI construct needed for daily operations — Fabrics, Pods,
Nodes (linked to existing `dcim.Device` records), Tenants, VRFs, Bridge
Domains and subnets, Application Profiles, EPGs / ESGs (including uSeg),
Contracts / Subjects / Filters, AAEPs, Domains, VLAN Pools, Switch and
Interface profiles, L3Outs (with BGP / OSPF / EIGRP peers and External
EPGs), and **per-interface EPG/BD/Subnet bindings** so you can see the
ACI policy applied to any device or port at a glance.

[![PyPI](https://img.shields.io/pypi/v/netbox-aci.svg)](https://pypi.org/project/netbox-aci/)
[![Python versions](https://img.shields.io/pypi/pyversions/netbox-aci.svg)](https://pypi.org/project/netbox-aci/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

## Compatibility

See the [compatibility matrix](COMPATIBILITY.md) for supported NetBox versions.

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
pip install netbox-aci
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`:

```python
PLUGINS = ['netbox_aci']
```

Run migrations and restart NetBox:

```bash
python /opt/netbox/netbox/manage.py migrate
sudo systemctl restart netbox netbox-rq
```

Add `netbox-aci` to `local_requirements.txt`.

## Configuration

The plugin works with sensible defaults. Optional settings live under
`PLUGINS_CONFIG['netbox_aci']` — see the [configuration docs](docs/configuration.md).

## Development

See [AGENTS.md](AGENTS.md) for repository conventions and
[docs/development.md](docs/development.md) for the dev-loop quickstart.

## Licensing

Apache License 2.0 — see [LICENSE](LICENSE).
