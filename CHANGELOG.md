# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/).

---

## [Unreleased]

> **Compatibility:** NetBox v4.5, NetBox v4.6

### Added

- **Phase 7 — L3Outs**:
  - `ACIL3Out` with per-protocol enablement (BGP / OSPF / EIGRP / Static),
    `ACILogicalNodeProfile` + `ACILogicalNode` (border-leaf pinning with
    router IDs and loopbacks), `ACILogicalInterfaceProfile` (routed /
    sub-interface / SVI / floating-SVI variants with encap and MTU),
    and `ACIL3OutInterface` binding logical interfaces to physical
    `dcim.Interface` rows with primary + secondary IP addresses.
  - `ACIBGPPeer` (at either LIP or LNP scope, with full BGP/peer/
    address-family/private-ASN control bitmaps and MD5 auth).
  - `ACIOSPFInterfacePolicy` + `ACIOSPFInterfaceAttachment` (reusable
    per-tenant OSPF policies attached to LIPs with area ID/type/cost).
  - `ACIEIGRPInterfacePolicy` (per-tenant EIGRP timers and controls).
  - `ACIExternalEPG` and `ACIExternalEPGSubnet` (route-leak/security
    scope controls per prefix).
  - `ACIContractRelation` extended with an XOR slot for External EPGs,
    so contracts can be applied to L3Out-facing endpoints.
  - Device and Interface "Cisco ACI Context" panels now also surface
    L3Out attachments.
- **L3Out static routes**: `ACIL3OutStaticRoute` (per-node static route
  with prefix, preference, track policy, and BFD control bit) and
  `ACIL3OutStaticRouteNextHop` (per-route next-hop entries supporting
  both prefix and null-route types, with per-hop preference for ECMP
  weighting). The Logical Node detail page and the device "Cisco ACI
  Context" template extension now also surface static routes.

### Changed

- `ACIContractRelation` gains an `aci_external_epg` FK (XOR slot alongside
  `aci_endpoint_group` and `aci_endpoint_security_group`), enabling contracts
  to be applied to External EPG endpoints on L3Outs.

### Added

- **Phase 6 — Static Port Bindings and Device/Interface visibility**:
  - `ACIStaticPortBinding` — binds an `ACIEndpointGroup` to a
    `dcim.Interface` with explicit encap VLAN, binding type
    (`regular` / `pc` / `vpc`), mode, primary encap VLAN (uSeg only),
    and deployment immediacy. APIC's `fvRsPathAtt` analog.
  - `ACIVPCBindingPair` — groups two `ACIStaticPortBinding`s as the
    two leaf sides of a single vPC, with check constraint that the
    two bindings differ and validation that both reference the same
    EPG, encap, and fabric while landing on distinct devices.
  - `ACIDomainBinding` — `fvRsDomAtt` analog binding an EPG to an
    `ACIDomain` with deployment / resolution immediacy and same-fabric
    enforcement.
  - `ACIInterfaceFabricMembership` — per-interface ACI Node attribution
    so a `dcim.Interface` resolves cleanly to its ACI fabric without
    walking through the device.
  - Auto-derived APIC-compatible `name` for all four binding models
    via `Model.save()` and matching API serializer logic — the name
    is generated from the FK relationships when not supplied, and
    sanitized to APIC's policy-name regex.
  - Device and Interface visibility panels (NetBox
    `PluginTemplateExtension`) that surface every binding on a
    `dcim.Device` or `dcim.Interface` detail page so operators can
    see which EPGs / domains / bridge-domains / subnets are attached
    without leaving NetBox's native pages.
  - Full UI, REST API, GraphQL, search index, navigation,
    NetBoxTable, and FilterSet coverage for all four new models.
  - 128 new tests covering models, forms, filtersets, API CRUD, and
    template-extension rendering — bringing the suite to 931 tests.

- **Phase 5 — Contracts, Subjects, Filters, and Contract Relations**:
  - `ACIContract` (per-tenant, with `scope` and optional `qos_class`)
  - `ACISubject` (children of a Contract) with a `reverse_filter_ports`
    guard that is only valid when `apply_both_directions` is true
  - `ACIFilter` (per-tenant) and `ACIFilterEntry` children with strict
    validation: TCP/UDP port pairs require both source and destination
    sides to be either fully specified or fully omitted; ARP opcode is
    only allowed when `ether_type='arp'`; ICMP type/code is only allowed
    when `ip_protocol` is `icmp` or `icmpv6`.
  - `ACISubjectFilter` through-model linking Subjects to Filters with
    optional per-binding `direction` / `action` / `priority` overrides.
  - `ACIContractRelation` through-model attaching a Contract as
    provider, consumer, or taboo to *either* an EPG **xor** an ESG
    (enforced via a check constraint plus `clean()`).
  - Cross-tenant carve-out: relations and bindings may reference
    objects in the same tenant or in the `common` tenant of the same
    fabric; everything else is rejected with a clear error.
  - Full UI, REST API, GraphQL, search index, navigation, and
    NetBoxTable coverage for all six new models.
  - 173 new tests covering models, forms, filtersets, and API CRUD.

- **Phase 4 — Switch & Interface Profiles and per-port policies**:
  - Six per-port policy templates: `ACILinkLevelPolicy`,
    `ACICDPInterfacePolicy`, `ACILLDPInterfacePolicy`,
    `ACILACPInterfacePolicy`, `ACIMCPInterfacePolicy`,
    `ACISTPInterfacePolicy`.
  - `ACIInterfacePolicyGroup` (Access / PC / vPC variants) with
    nullable FKs to each of the six policy templates plus AAEP, and a
    cross-fabric guard on every reference.
  - `ACISwitchProfile` with `ACISwitchProfileSelector` children
    (range or all-leaves selection).
  - `ACIInterfaceProfile` with `ACIInterfaceProfileSelector` children
    (module/port range, bound to an Interface Policy Group).
  - `ACISwitchProfileInterfaceProfileAttachment` through-model
    linking Switch Profiles to Interface Profiles, with a cross-fabric
    guard.
- **Cloud / Kubernetes compatibility contract.** Documented in
  `docs/cloud-compatibility.md` and `AGENTS.md`; enforced by a new
  `cloud-compat` CI job (`scripts/check_cloud_compat.py`) that fails
  the build on local-filesystem writes, in-process threading or
  schedulers, subprocess use, Django management commands, file-based
  caches, hard-coded host paths, and other patterns that would break
  on NetBox Enterprise / NetBox Cloud.

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
- **Phase 3 — Access policies** (this PR):
  - `ACIVLANPool` (`fvnsVlanInstP`) with `allocation_mode` static or
    dynamic. Unique per Fabric+name.
  - `ACIVLANPoolBlock` (`fvnsEncapBlk`) — `from_vlan`/`to_vlan` range
    inside a pool. Validates `to >= from`, refuses overlap with sibling
    blocks in the same pool, allows overlap across pools.
  - `ACIDomain` — single model for all five APIC domain types
    (Physical, L3, VMM, L2-Ext, FC) keyed by `domain_type`. Each Domain
    has an optional FK to one `ACIVLANPool`.
  - `ACIAAEP` (`infraAttEntityP`) with `enable_infra_vlan` flag and a
    M2M to Domains via the explicit `ACIAAEPDomainAssociation` through
    model (cross-fabric pairings are refused).
  - `ACIAAEPEPGMapping` (`infraRsFuncToEpg`) — binds an EPG onto an
    AAEP with encap VLAN and switching mode. Cross-fabric pairings
    are refused.
  - Full surface per model: form (edit + bulk-edit + filter + import),
    table, filterset, UI viewset, REST API serializer + viewset,
    GraphQL type, search index, navigation entry, detail template.
  - New "Access Policies" submenu groups all five UI entries.
  - Migration `0003_access_policies`.
  - Tests: model validation (overlap, cross-fabric, uniqueness),
    REST API CRUD, filterset (including `contains_vlan` numeric
    filter), form smoke tests — for every Phase 3 model.
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
