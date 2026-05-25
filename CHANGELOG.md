# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/).

---

## [Unreleased]

> **Compatibility:** NetBox v4.5, NetBox v4.6

### Changed

- **BREAKING (pre-release): renamed plugin to `netbox-cisco-aci`.**
  The PyPI name `netbox-aci` was already taken by an unrelated
  project (Marc-Aurel Mohr-Lenné, v0.0.7). New names:
  - PyPI distribution: `netbox-cisco-aci`
  - Python package: `netbox_cisco_aci`
  - Django app label: `netbox_cisco_aci`
  - URL base: `/plugins/cisco-aci/` and `/api/plugins/cisco-aci/`
  - URL namespaces: `plugins:netbox_cisco_aci:*`, `plugins-api:netbox_cisco_aci-api:*`
  - Constraint names: `netbox_cisco_aci_*`
  No releases have shipped under the old name, so no migration path
  is required; the old name is simply unused.

### Added

- Initial plugin scaffold targeting NetBox 4.5.x and 4.6.x in a single
  release.
- Phase 1 — Fabric topology models: `ACIFabric`, `ACIPod`, `ACINode`
  (with optional FK to `dcim.Device`).
- **Phase 2 — Tenancy models** (this PR):
  - `ACITenant` (fabric-scoped, name-unique inside its Fabric).
  - `ACIVRF` with policy-enforcement preference + direction, BD
    enforcement, and preferred-group flag. Optional FK to `ipam.VRF`.
  - `ACIBridgeDomain` with full L2/L3 forwarding policy (unicast
    routing, ARP flooding, L2-unknown-unicast, L3-unknown-multicast,
    multi-destination flooding, custom MAC, limit-IP-learn). VRF may
    live in the same tenant or in `common`; the model enforces that.
  - `ACIBridgeDomainSubnet` (gateway IP, scope flags, primary flag,
    optional FK to `ipam.Prefix`).
  - `ACIAppProfile`.
  - `ACIEndpointGroup` with `is_useg`, intra-EPG isolation,
    preferred-group membership, admin-shutdown, and QoS class. AP-Tenant
    and BD-Tenant/`common` agreement is enforced in `clean()`.
  - `ACIUSegAttribute` (type / operator / value triplet, only valid on
    EPGs with `is_useg=True` — enforced in `clean()`).
  - `ACIEndpointSecurityGroup` (VRF-scoped, optional AP, with admin-
    shutdown, preferred-group, intra-ESG isolation, QoS).
  - Full surface per model: form (edit + bulk-edit + filter + import),
    table, filterset, UI viewset, REST API serializer + viewset,
    GraphQL type, search index, navigation entry, detail template.
  - Migration `0002_tenancy`.
  - Tests: model validation/uniqueness/clean, REST API CRUD,
    filterset behaviour, form valid/invalid — for every Phase 2 model.
- Phase 3 (planned) — Access policies: `ACIVLANPool` + encap blocks,
  `ACIDomain` (physical / L3 / VMM), `ACIAAEP` with domain and EPG
  mappings.
- Phase 4 — Switch / Interface Profiles, Interface Policy Groups,
  per-policy refs (CDP, LLDP, LACP, MCP, STP, Link Level).
- Phase 5 — `ACIContract`, `ACIContractSubject`, `ACIContractFilter`
  with entries, and provider/consumer relations.
- Phase 6 — `ACIEPGStaticPortBinding` (links an EPG to a `dcim.Interface`
  with encap VLAN, mode, and immediacy). Device and Interface detail
  views gain ACI context panels.
- Phase 7 — L3Outs: `ACIL3Out`, `ACILogicalNodeProfile`,
  `ACILogicalInterfaceProfile`, `ACIBGPPeer`, `ACIOSPFPeer`,
  `ACIEIGRPNeighbor`, `ACIExternalEPG`.
- AGENTS.md / CLAUDE.md for AI-assisted development.
- COMPATIBILITY.md per NetBox plugin catalogue standards.
- CI matrix across NetBox 4.5 / 4.6 × Python 3.11 / 3.12 with coverage
  upload (target ≥70%, gate at 65%).
