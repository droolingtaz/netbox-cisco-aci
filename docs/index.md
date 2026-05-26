# netbox-cisco-aci

A [NetBox](https://netboxlabs.com/oss/netbox/) plugin for **operational
visibility and documentation of Cisco ACI** fabrics.

Models every ACI construct needed for daily operations — Fabrics, Pods,
Nodes (linked to existing `dcim.Device` records), Tenants, VRFs, Bridge
Domains and subnets, Application Profiles, EPGs / ESGs (including uSeg),
Contracts / Subjects / Filters, AAEPs, Domains, VLAN Pools, Switch and
Interface profiles, L3Outs (with BGP / OSPF / EIGRP / Static routes and
External EPGs), and **per-interface EPG/BD/Subnet bindings** so you can
see the ACI policy applied to any device or port at a glance.

## Quick links

- [GitHub repo](https://github.com/droolingtaz/netbox-cisco-aci)
- [PyPI release](https://pypi.org/project/netbox-cisco-aci/)
- [Issue tracker](https://github.com/droolingtaz/netbox-cisco-aci/issues)
- [Changelog](changelog.md)

## Highlights

### Fabric topology

`ACIFabric` → `ACIPod` → `ACINode`, where each Node optionally links to
an existing `dcim.Device` or `virtualization.VirtualMachine`. Multi-fabric
and overlapping fabric-ID deployments are first-class.

### Tenancy and policy

`ACITenant`, `ACIVRF`, `ACIBridgeDomain` (+ subnets), `ACIAppProfile`,
`ACIEndpointGroup` (with full uSeg attribute support),
`ACIEndpointSecurityGroup`, all with the `common`-tenant carve-out and
cross-tenant agreement enforcement APIC requires.

### Access policies

Full Switch / Interface profile stack with selectors, Interface Policy
Groups (Access / PC / vPC), and the six per-port policy templates
(Link Level, CDP, LLDP, LACP, MCP, STP), all with cross-fabric guards.

### Contracts

`ACIContract`, `ACISubject`, `ACIFilter` with strict port-pair / ARP /
ICMP validation, `ACISubjectFilter` overrides, and `ACIContractRelation`
attaching contracts to EPGs, ESGs, **or** External EPGs.

### L3Outs

`ACIL3Out` → `LogicalNodeProfile` → `LogicalInterfaceProfile` →
`L3OutInterface` (with primary + secondary IPs on `dcim.Interface`).
BGP / OSPF / EIGRP / Static routing fully modelled, with route entries
and per-route next-hop ECMP weighting.

### Operational visibility

PluginTemplateExtensions inject a "Cisco ACI Context" panel into the
`dcim.Device` and `dcim.Interface` detail pages, surfacing every
binding, L3Out attachment, static route, and contract relation touching
the hardware — without ever leaving NetBox.

## Compatibility

- **NetBox**: 4.5.x and 4.6.x in a single release
  ([compatibility matrix](compatibility.md)).
- **Python**: 3.12 (NetBox 4.5+ requirement).
- **NetBox Enterprise / NetBox Cloud**: yes — see
  [Cloud / Kubernetes compatibility](cloud-compatibility.md). The
  contract is enforced by a CI gate.

## Install

```bash
pip install netbox-cisco-aci
```

Then add to your NetBox `configuration.py`:

```python
PLUGINS = ['netbox_cisco_aci']
```

…and run migrations:

```bash
python manage.py migrate
```

See [Configuration](configuration.md) for tunable settings.
