# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/).

---

## [Unreleased]

> **Compatibility:** NetBox v4.5, NetBox v4.6

_No unreleased changes yet — next release will start here._

---

## [0.1.0] — 2026-05-26

First public release.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12 only
> (NetBox 4.5+ requires Python 3.12).

This release models every ACI construct needed for daily operations
across seven build phases, plus end-to-end NetBox plugin surface
(forms / tables / filtersets / UI views / REST API / GraphQL / search /
navigation / template extensions / migrations / 1,245+ tests) on a
Cloud / Kubernetes-friendly footprint.

### Added — Fabric topology (Phase 1)

- `ACIFabric`, `ACIPod`, `ACINode` (with optional generic foreign key to
  either `dcim.Device` or `virtualization.VirtualMachine`).
- Per-fabric uniqueness on pods; per-pod uniqueness on nodes; multi-fabric
  deployments and overlapping fabric IDs both supported.

### Added — Tenancy (Phase 2)

- `ACITenant`, `ACIVRF` (optional FK to `ipam.VRF`), `ACIBridgeDomain`
  with full L2/L3 forwarding policy and `ACIBridgeDomainSubnet`
  (gateway IP, scope flags, optional FK to `ipam.Prefix`).
- `ACIAppProfile`, `ACIEndpointGroup` (with `is_useg`, intra-EPG isolation,
  preferred-group, admin-shutdown, QoS), `ACIUSegAttribute` (only valid
  on uSeg EPGs), `ACIEndpointSecurityGroup` (VRF-scoped).
- BD-Tenant / VRF-Tenant / AP-Tenant agreement enforced; `common`-tenant
  carve-out for shared VRFs and contracts.

### Added — Access policies, Phase A (Phase 3)

- `ACIVLANPool` + `ACIVLANPoolBlock` (overlap refused inside a pool,
  allowed across pools).
- `ACIDomain` — single model for all five APIC domain types (Physical,
  L3, VMM, L2-Ext, FC) via `domain_type`.
- `ACIAAEP` + `ACIAAEPDomainAssociation` through-model + `ACIAAEPEPGMapping`,
  all cross-fabric guarded.

### Added — Access policies, Phase B (Phase 4)

- Six per-port policy templates: `ACILinkLevelPolicy`, `ACICDPInterfacePolicy`,
  `ACILLDPInterfacePolicy`, `ACILACPInterfacePolicy`, `ACIMCPInterfacePolicy`,
  `ACISTPInterfacePolicy`.
- `ACIInterfacePolicyGroup` (Access / PC / vPC) with nullable FKs to each
  of the six per-port policies plus AAEP, and a cross-fabric guard on
  every reference.
- `ACISwitchProfile` + `ACISwitchProfileSelector` (range or all-leaves).
- `ACIInterfaceProfile` + `ACIInterfaceProfileSelector` (module / port
  range, bound to a Policy Group).
- `ACISwitchProfileInterfaceProfileAttachment` linking the two profiles
  with a cross-fabric guard.

### Added — Contracts (Phase 5)

- `ACIContract` (per-tenant, `scope`, optional `qos_class`).
- `ACISubject` with a `reverse_filter_ports` guard active only when
  `apply_both_directions` is true.
- `ACIFilter` + `ACIFilterEntry` with strict validation: TCP/UDP port
  pairs require both sides, ARP opcode only on `ether_type='arp'`,
  ICMP type/code only on `ip_protocol in {'icmp','icmpv6'}`.
- `ACISubjectFilter` through-model with optional `direction` / `action` /
  `priority` overrides.
- `ACIContractRelation` through-model attaching a Contract as provider,
  consumer, or taboo to an EPG **xor** ESG **xor** External EPG.

### Added — Static port bindings + device/interface visibility (Phase 6)

- `ACIStaticPortBinding` — binds an EPG to a `dcim.Interface` with encap
  VLAN, binding type (`regular` / `pc` / `vpc`), mode, primary encap
  VLAN (uSeg only), and deployment immediacy.
- `ACIVPCBindingPair` — groups two `ACIStaticPortBinding`s as the two
  leaf sides of a single vPC with same-EPG / same-encap / different-device
  guards.
- `ACIDomainBinding` — APIC `fvRsDomAtt` equivalent binding an EPG to an
  `ACIDomain` with deployment / resolution immediacy.
- `ACIInterfaceFabricMembership` — per-interface ACI Node attribution.
- Auto-derived APIC-policy-safe `name` for all binding models via
  `Model.save()` and matching API serializer logic.
- **PluginTemplateExtensions** on `dcim.Device` and `dcim.Interface`
  inject "Cisco ACI Context" panels surfacing the EPGs, BDs, subnets,
  VRFs, and contracts touching the hardware.

### Added — L3Outs (Phase 7)

- `ACIL3Out` with per-protocol enablement (BGP / OSPF / EIGRP / Static).
- `ACILogicalNodeProfile` + `ACILogicalNode` (border-leaf pinning with
  router IDs and loopbacks).
- `ACILogicalInterfaceProfile` (routed / sub-interface / SVI / floating-SVI
  variants with encap and MTU) + `ACIL3OutInterface` binding logical
  interfaces to physical `dcim.Interface` rows with primary and secondary
  IP addresses.
- `ACIBGPPeer` (attaches at either LIP or LNP scope; full BGP / peer /
  address-family / private-ASN control bitmaps and MD5 auth).
- `ACIOSPFInterfacePolicy` + `ACIOSPFInterfaceAttachment` (reusable
  per-tenant OSPF policies attached to LIPs with area ID / type / cost).
- `ACIEIGRPInterfacePolicy` (per-tenant EIGRP timers + controls).
- `ACIExternalEPG` + `ACIExternalEPGSubnet` (route-leak / security scope
  controls per prefix).
- `ACIL3OutStaticRoute` + `ACIL3OutStaticRouteNextHop` (per-node static
  routes with prefix / preference / track policy / BFD; per-route
  next-hop entries supporting both prefix and null-route types, with
  per-hop preference for ECMP weighting).
- Device and Interface "Cisco ACI Context" panels extended to surface
  L3Out attachments and static routes.

### Added — Infrastructure and governance

- **Cloud / Kubernetes compatibility contract.** Documented in
  `docs/cloud-compatibility.md` and `AGENTS.md`; enforced by the
  `cloud-compat` CI job (`scripts/check_cloud_compat.py`) — local
  filesystem writes, in-process threading or schedulers, subprocess use,
  Django management commands, file-based caches, and hard-coded host
  paths all fail the build.
- `AGENTS.md` and `CLAUDE.md` for AI-assisted development.
- `COMPATIBILITY.md` per the NetBox plugin catalogue standard.
- `MkDocs Material` documentation site built from `docs/` and deployed
  to GitHub Pages on every push to `main`.
- GitHub Actions release workflow (`.github/workflows/release.yml`)
  that publishes to PyPI on tag push, supporting both trusted publishing
  (OIDC) and `PYPI_API_TOKEN` flows, and creates a GitHub Release from
  the matching CHANGELOG section.
- Codecov upload integrated into the test matrix.

### CI

- Matrix: NetBox 4.5 × Python 3.12 and NetBox 4.6 × Python 3.12.
  (NetBox 4.5+ requires Python 3.12, so a 3.11 matrix entry would only
  re-run the lint paths and is intentionally omitted.)
- `cloud-compat`, `lint` (ruff `0.15.14` pinned), and the two NetBox
  test jobs are all required checks on `main`.
- Coverage reporting via `coverage[toml]` with an initial gate of 65%
  (`--cov-fail-under=65` re-enabled now that the model surface is stable
  at v0.1.0).

### Notes

- 1,245+ tests across models, forms, filtersets, REST API, and template
  extensions; all green on NetBox 4.5 and 4.6.
- `netbox-aci` was already taken on PyPI by an unrelated v0.0.7 project,
  so this plugin ships under the **`netbox-cisco-aci`** distribution
  name. Python package, Django app label, URL base, and constraint
  names all use the matching `netbox_cisco_aci` / `cisco-aci` prefixes.

[Unreleased]: https://github.com/droolingtaz/netbox-cisco-aci/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.0
