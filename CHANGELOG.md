# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning 2.0.0](https://semver.org/).

---

## [Unreleased]

> **Compatibility:** NetBox v4.5, NetBox v4.6

### Added

- Initial plugin scaffold targeting NetBox 4.5.x and 4.6.x in a single
  release.
- Phase 1 — Fabric topology models: `ACIFabric`, `ACIPod`, `ACINode`
  (with optional FK to `dcim.Device`).
- Phase 2 — Tenancy models: `ACITenant`, `ACIVRF`, `ACIBridgeDomain`,
  `ACIBridgeDomainSubnet`, `ACIAppProfile`, `ACIEndpointGroup`,
  `ACIEndpointSecurityGroup` (incl. uSeg attributes).
- Phase 3 — Access policies: `ACIVLANPool` + encap blocks,
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
