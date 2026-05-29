# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/).

---

## [Unreleased]

> **Compatibility:** NetBox v4.5, NetBox v4.6

_No unreleased changes yet — next release will start here._

---

## [0.1.5] — 2026-05-29

Patch release finishing the device ACI Context restyle: the **L3Out
Logical Nodes** sub-card now follows the same per-attribute
`attr-table` layout as the rest of the panel.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Changed

- **L3Out Logical Nodes sub-card restyled to per-node `attr-table`**
  (PR #21). The v0.1.4 restyle missed one section: each logical node
  on the device ACI Context panel was rendered as a single attr-table
  row whose right cell stuffed three pieces of data inline
  (`L3Out: ... · Router ID: 1.1.1.1` and a `No static routes.`
  sentence). Each logical node now renders as its own per-attribute
  attr-table inside the section card, with explicit rows for **Logical
  Node**, **L3Out**, **Logical Node Profile**, **Router ID**,
  **Loopback Address**, and **Static Routes**. Consecutive nodes are
  separated by a thin `<hr>` and the card header gains a count badge.
  Empty values render as em-dashes; FK references render as links.
  Pure template + test change.

---

## [0.1.4] — 2026-05-28

Patch release restyling the **Cisco ACI Context** panel on the
`dcim.Device` and `dcim.Interface` detail pages to match NetBox's
stock card layout.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Changed

- **"Cisco ACI Context" panel restyled to NetBox `attr-table`**
  (PR #19). Both the device and interface PluginTemplateExtensions
  now render the same compact two-column label-to-value definition
  list NetBox uses for stock cards like "Device Type" — link-colored
  FK values via `|linkify` and em-dashes for empty fields via
  `|placeholder`. Subordinate sections (Static Port Bindings, L3Out
  Logical Nodes, Reachable Subnets, Contracts, L3Out Interfaces, BGP
  Peers) split into their own cards stacked beneath the summary,
  each with a count badge in the header. Same data density, same
  links, but the panels now blend seamlessly into the surrounding
  NetBox UI. Pure template-layer change; no model, migration, API,
  or serializer impact.

---

## [0.1.3] — 2026-05-27

Patch release adding the AAEP→EPG encap-VLAN reachability check and
fixing a cosmetic em-dash render on the VLAN Pool detail page.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Added

- **AAEP→EPG encap VLAN must be reachable through the AAEP's domains**
  (PR #17). `ACIAAEPEPGMapping.clean()` now resolves the chain
  `AAEP → ACIAAEPDomainAssociation → ACIDomain → ACIVLANPool` and
  asserts the encap is contained in at least one `ACIVLANPoolBlock`
  under those pools. Mirrors APIC's deployment-time behaviour: the
  leaves refuse to program a mapping whose encap isn't covered by any
  bound pool. The check is intentionally permissive while the AAEP is
  still being built (no domains attached, or attached domains have no
  pool yet) so users aren't blocked during incremental config. Eight
  new test cases cover the empty-domain, no-pool, in-range,
  boundary, multi-block, and multi-domain branches.

### Fixed

- **`\u2014` rendering as literal text on the VLAN Pool detail page**
  (PR #17). `templates/netbox_cisco_aci/acivlanpool.html` had a
  `default:"\u2014"` filter call that I'd written assuming the Django
  template engine would interpret the Python escape. It doesn't, so
  the page rendered the literal six characters next to each VLAN
  block. Replaced with the canonical NetBox `|placeholder` filter
  which renders an em-dash in the muted class. Spot-audited the rest
  of the templates — no other instance of this shape.

---

## [0.1.2] — 2026-05-27

Patch release fixing the **Add USeg Attribute** form. All v0.1.x users
who use uSeg EPGs should upgrade.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Fixed

- **"Select a valid choice" on the Add USeg Attribute form (PR #15).**
  `ACIUSegAttributeForm.aci_endpoint_group` restricted the form's
  validation queryset to `ACIEndpointGroup.objects.filter(is_useg=True)`,
  but NetBox's `DynamicModelChoiceField` typeahead fetches candidates
  from the REST API, which had no `is_useg` default. Users saw every
  EPG in the dropdown, picked one that wasn't uSeg, and the form
  rejected the choice on submit. Fixed by adding
  `query_params={"is_useg": True}` to the three affected fields
  (`ACIUSegAttributeForm`, `ACIUSegAttributeBulkEditForm`,
  `ACIUSegAttributeFilterForm`).

### Added

- **`tests/test_form_dropdown_filters.py`** — regression guard. A pure
  static scan that walks every `forms/*.py` and asserts every
  `DynamicModelChoiceField` / `DynamicModelMultipleChoiceField` with a
  filtered queryset (`.filter(…)`) also passes `query_params={…}`. The
  check runs in ~15 ms with no DB setup, and the failure message
  points the next maintainer at the offending field. Designed to
  catch the same class of bug across all future forms.

---

## [0.1.1] — 2026-05-27

Patch release fixing a production-blocking 500 on every list / detail
page in v0.1.0. All v0.1.0 users should upgrade.

> **Compatibility:** NetBox v4.5, NetBox v4.6 · Python 3.12.

### Fixed

- **`NoReverseMatch` 500 on every UI page.** NetBox 4.x's object detail
  and list-row templates reverse `<label>_changelog` and
  `<label>_journal` unconditionally for every model, but the plugin's
  `_crud()` URL factory only registered the eight basic CRUD verbs.
  The first time a logged-in user opened any list or detail page,
  NetBox tried to render the per-row dropdown, hit
  `django.urls.exceptions.NoReverseMatch`, and produced a red 500. The
  factory now registers the two missing routes (`changelog`, `journal`)
  for every model, backed by NetBox's stock `ObjectChangeLogView` and
  `ObjectJournalView` (PR #13). The bug existed for every model in
  v0.1.0 — not just `ACIFabric`.

### Added

- **`tests/test_urls.py`** — regression guard. Enumerates every
  UI-bearing model in the plugin and asserts every route in the
  ten-route block (list / add / import / bulk-edit / bulk-delete /
  detail / edit / delete / changelog / journal) reverses cleanly. The
  test class explicitly checks `changelog` and `journal` so a future
  regression of this exact bug fails the build with an obvious error.
  CI did not catch the original failure because NetBox's
  `ViewTestCases` and `APIViewTestCases` only reverse the explicit
  verbs they cover — they never touch `*_changelog` or `*_journal`.

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

[Unreleased]: https://github.com/droolingtaz/netbox-cisco-aci/compare/v0.1.5...HEAD
[0.1.5]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.5
[0.1.4]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.4
[0.1.3]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.3
[0.1.2]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.2
[0.1.1]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.1
[0.1.0]: https://github.com/droolingtaz/netbox-cisco-aci/releases/tag/v0.1.0
