"""NetBox/Django ChoiceSet definitions for the plugin.

Each grouping of choices lives in one class so it can be reused across
models, forms, filtersets, GraphQL types, and tests without duplicating
the literal strings.
"""

from django.utils.translation import gettext_lazy as _
from utilities.choices import ChoiceSet

# ---------------------------------------------------------------------------
# Fabric / Node
# ---------------------------------------------------------------------------


class NodeRoleChoices(ChoiceSet):
    """Functional role of an ACI Node."""

    key = "ACINode.role"

    ROLE_SPINE = "spine"
    ROLE_LEAF = "leaf"
    ROLE_APIC = "apic"
    ROLE_REMOTE_LEAF = "rleaf"
    ROLE_VIRTUAL_LEAF = "vleaf"
    ROLE_TIER2_LEAF = "tier2"

    CHOICES = [
        (ROLE_SPINE, _("Spine"), "blue"),
        (ROLE_LEAF, _("Leaf"), "green"),
        (ROLE_APIC, _("APIC controller"), "purple"),
        (ROLE_REMOTE_LEAF, _("Remote Leaf"), "teal"),
        (ROLE_VIRTUAL_LEAF, _("Virtual Leaf"), "cyan"),
        (ROLE_TIER2_LEAF, _("Tier-2 Leaf"), "orange"),
    ]


class NodeTypeChoices(ChoiceSet):
    """Hardware family of an ACI Node."""

    key = "ACINode.node_type"

    TYPE_UNKNOWN = "unknown"
    TYPE_PHYSICAL = "physical"
    TYPE_VIRTUAL = "virtual"
    TYPE_REMOTE = "remote"

    CHOICES = [
        (TYPE_PHYSICAL, _("Physical"), "blue"),
        (TYPE_VIRTUAL, _("Virtual"), "cyan"),
        (TYPE_REMOTE, _("Remote"), "orange"),
        (TYPE_UNKNOWN, _("Unknown"), "gray"),
    ]


# ---------------------------------------------------------------------------
# Tenancy / EPG
# ---------------------------------------------------------------------------


class QualityOfServiceClassChoices(ChoiceSet):
    """ACI QoS classes."""

    key = "QualityOfService.class"

    LEVEL_1 = "level1"
    LEVEL_2 = "level2"
    LEVEL_3 = "level3"
    LEVEL_4 = "level4"
    LEVEL_5 = "level5"
    LEVEL_6 = "level6"
    UNSPECIFIED = "unspecified"

    CHOICES = [
        (LEVEL_1, _("Level 1")),
        (LEVEL_2, _("Level 2")),
        (LEVEL_3, _("Level 3")),
        (LEVEL_4, _("Level 4")),
        (LEVEL_5, _("Level 5")),
        (LEVEL_6, _("Level 6")),
        (UNSPECIFIED, _("Unspecified")),
    ]


class VRFPolicyEnforcementChoices(ChoiceSet):
    """VRF policy-enforcement direction."""

    key = "ACIVRF.policy_enforcement_direction"

    INGRESS = "ingress"
    EGRESS = "egress"

    CHOICES = [
        (INGRESS, _("Ingress")),
        (EGRESS, _("Egress")),
    ]


class VRFPolicyEnforcementPreferenceChoices(ChoiceSet):
    """Whether VRF policy is actually enforced."""

    key = "ACIVRF.policy_enforcement_preference"

    ENFORCED = "enforced"
    UNENFORCED = "unenforced"

    CHOICES = [
        (ENFORCED, _("Enforced")),
        (UNENFORCED, _("Unenforced")),
    ]


# ---------------------------------------------------------------------------
# Bridge Domain
# ---------------------------------------------------------------------------


class BDL2UnknownUnicastChoices(ChoiceSet):
    """BD L2 unknown unicast forwarding mode."""

    key = "ACIBridgeDomain.l2_unknown_unicast"

    PROXY = "proxy"
    FLOOD = "flood"

    CHOICES = [
        (PROXY, _("Hardware Proxy")),
        (FLOOD, _("Flood")),
    ]


class BDL3UnknownMulticastChoices(ChoiceSet):
    """BD L3 unknown multicast flooding."""

    key = "ACIBridgeDomain.l3_unknown_multicast"

    FLOOD = "flood"
    OPT_FLOOD = "opt-flood"

    CHOICES = [
        (FLOOD, _("Flood")),
        (OPT_FLOOD, _("Optimized Flood")),
    ]


class BDMultiDestinationChoices(ChoiceSet):
    """BD multi-destination flooding scope."""

    key = "ACIBridgeDomain.multi_destination_flooding"

    BD_FLOOD = "bd-flood"
    ENCAP_FLOOD = "encap-flood"
    DROP = "drop"

    CHOICES = [
        (BD_FLOOD, _("Flood in BD")),
        (ENCAP_FLOOD, _("Flood in Encapsulation")),
        (DROP, _("Drop")),
    ]


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------


class ContractScopeChoices(ChoiceSet):
    """Contract enforcement scope."""

    key = "ACIContract.scope"

    SCOPE_GLOBAL = "global"
    SCOPE_TENANT = "tenant"
    SCOPE_VRF = "context"
    SCOPE_APP_PROFILE = "application-profile"

    CHOICES = [
        (SCOPE_GLOBAL, _("Global")),
        (SCOPE_TENANT, _("Tenant")),
        (SCOPE_VRF, _("VRF (Context)")),
        (SCOPE_APP_PROFILE, _("Application Profile")),
    ]


class ContractRelationRoleChoices(ChoiceSet):
    """Whether an EPG provides or consumes a contract."""

    key = "ACIContractRelation.role"

    PROVIDER = "provider"
    CONSUMER = "consumer"

    CHOICES = [
        (PROVIDER, _("Provider"), "green"),
        (CONSUMER, _("Consumer"), "blue"),
    ]


class SubjectFilterDirectionChoices(ChoiceSet):
    """Direction of a filter attached to a subject."""

    key = "ACISubjectFilter.direction"

    BOTH = "both"
    IN = "in"
    OUT = "out"

    CHOICES = [
        (BOTH, _("Both")),
        (IN, _("In (consumer-to-provider)")),
        (OUT, _("Out (provider-to-consumer)")),
    ]


class SubjectFilterActionChoices(ChoiceSet):
    """Action applied by a filter inside a subject."""

    key = "ACISubjectFilter.action"

    PERMIT = "permit"
    DENY = "deny"
    REDIRECT = "redirect"
    COPY = "copy"
    LOG = "log"

    CHOICES = [
        (PERMIT, _("Permit"), "green"),
        (DENY, _("Deny"), "red"),
        (REDIRECT, _("Redirect"), "blue"),
        (COPY, _("Copy"), "purple"),
        (LOG, _("Log"), "gray"),
    ]


class SubjectFilterPriorityChoices(ChoiceSet):
    """APIC subject-filter priority levels."""

    key = "ACISubjectFilter.priority"

    DEFAULT = "default"
    LEVEL1 = "level1"
    LEVEL2 = "level2"
    LEVEL3 = "level3"

    CHOICES = [
        (DEFAULT, _("Default")),
        (LEVEL1, _("Level 1")),
        (LEVEL2, _("Level 2")),
        (LEVEL3, _("Level 3")),
    ]


class ContractFilterEntryEtherTypeChoices(ChoiceSet):
    """Ethertype values supported by contract filter entries."""

    key = "ACIContractFilterEntry.ether_type"

    UNSPECIFIED = "unspecified"
    IP = "ip"
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    ARP = "arp"
    FCOE = "fcoe"
    MAC_SECURITY = "mac-security"
    MPLS_UCAST = "mpls-ucast"
    TRILL = "trill"

    CHOICES = [
        (UNSPECIFIED, _("Unspecified")),
        (IP, _("IP")),
        (IPV4, _("IPv4")),
        (IPV6, _("IPv6")),
        (ARP, _("ARP")),
        (FCOE, _("FCoE")),
        (MAC_SECURITY, _("MAC Security")),
        (MPLS_UCAST, _("MPLS Unicast")),
        (TRILL, _("TRILL")),
    ]


class ContractFilterEntryIPProtocolChoices(ChoiceSet):
    """IP protocol values supported by contract filter entries."""

    key = "ACIContractFilterEntry.ip_protocol"

    UNSPECIFIED = "unspecified"
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ICMPV6 = "icmpv6"
    IGMP = "igmp"
    EIGRP = "eigrp"
    OSPF = "ospfigp"
    PIM = "pim"
    L2TP = "l2tp"

    CHOICES = [
        (UNSPECIFIED, _("Unspecified")),
        (TCP, _("TCP")),
        (UDP, _("UDP")),
        (ICMP, _("ICMP")),
        (ICMPV6, _("ICMPv6")),
        (IGMP, _("IGMP")),
        (EIGRP, _("EIGRP")),
        (OSPF, _("OSPF")),
        (PIM, _("PIM")),
        (L2TP, _("L2TP")),
    ]


# ---------------------------------------------------------------------------
# Domains / VLAN Pools / AAEP
# ---------------------------------------------------------------------------


class DomainTypeChoices(ChoiceSet):
    """ACI Domain type."""

    key = "ACIDomain.domain_type"

    PHYSICAL = "physical"
    L3 = "l3"
    VMM = "vmm"
    L2 = "l2"
    FC = "fc"

    CHOICES = [
        (PHYSICAL, _("Physical")),
        (L3, _("L3")),
        (VMM, _("VMM")),
        (L2, _("L2 External")),
        (FC, _("Fibre Channel")),
    ]


class VLANPoolAllocationChoices(ChoiceSet):
    """VLAN Pool allocation mode."""

    key = "ACIVLANPool.allocation_mode"

    STATIC = "static"
    DYNAMIC = "dynamic"

    CHOICES = [
        (STATIC, _("Static")),
        (DYNAMIC, _("Dynamic")),
    ]


# ---------------------------------------------------------------------------
# Static Port Bindings
# ---------------------------------------------------------------------------


class StaticPortModeChoices(ChoiceSet):
    """Static port binding switching mode."""

    key = "ACIEPGStaticPortBinding.mode"

    TRUNK = "regular"
    ACCESS_TAG = "native"
    ACCESS_UNTAG = "untagged"

    CHOICES = [
        (TRUNK, _("Trunk (802.1q)")),
        (ACCESS_TAG, _("Access (802.1p)")),
        (ACCESS_UNTAG, _("Access (untagged)")),
    ]


class DeploymentImmediacyChoices(ChoiceSet):
    """Deployment immediacy for EPG-to-leaf programming."""

    key = "ACIEPGStaticPortBinding.deployment_immediacy"

    IMMEDIATE = "immediate"
    ON_DEMAND = "lazy"

    CHOICES = [
        (IMMEDIATE, _("Immediate")),
        (ON_DEMAND, _("On Demand")),
    ]


class ResolutionImmediacyChoices(ChoiceSet):
    """Resolution immediacy."""

    key = "ACIEPGStaticPortBinding.resolution_immediacy"

    IMMEDIATE = "immediate"
    ON_DEMAND = "lazy"
    PRE_PROVISION = "pre-provision"

    CHOICES = [
        (IMMEDIATE, _("Immediate")),
        (ON_DEMAND, _("On Demand")),
        (PRE_PROVISION, _("Pre-provision")),
    ]


class StaticPortBindingTypeChoices(ChoiceSet):
    """How an EPG is bound to a physical interface (``fvRsPathAtt.tDn``)."""

    key = "ACIStaticPortBinding.binding_type"

    REGULAR = "regular"
    PC = "pc"
    VPC = "vpc"
    DIRECT_PC = "direct-port-channel"
    FEX = "fex"

    CHOICES = [
        (REGULAR, _("Access port"), "gray"),
        (PC, _("Port Channel member"), "blue"),
        (VPC, _("vPC member"), "purple"),
        (DIRECT_PC, _("Direct Port Channel"), "cyan"),
        (FEX, _("FEX host port"), "orange"),
    ]


class InterfaceFabricRoleChoices(ChoiceSet):
    """Role of a physical interface inside an ACI fabric."""

    key = "ACIInterfaceFabricMembership.interface_role"

    FABRIC = "fabric"
    HOST = "host"
    PEER_LINK = "peer-link"
    MGMT = "mgmt"

    CHOICES = [
        (FABRIC, _("Fabric uplink"), "blue"),
        (HOST, _("Host downlink"), "green"),
        (PEER_LINK, _("vPC peer-link"), "purple"),
        (MGMT, _("Management"), "gray"),
    ]


# ---------------------------------------------------------------------------
# L3Out
# ---------------------------------------------------------------------------


class L3OutInterfaceTypeChoices(ChoiceSet):
    """Logical Interface Profile sub-type."""

    key = "ACILogicalInterfaceProfile.interface_type"

    ROUTED = "routed"
    SUB_INTERFACE = "sub-interface"
    SVI = "svi"
    FLOATING_SVI = "floating-svi"

    CHOICES = [
        (ROUTED, _("Routed")),
        (SUB_INTERFACE, _("Sub-interface")),
        (SVI, _("SVI")),
        (FLOATING_SVI, _("Floating SVI")),
    ]


class RoutingProtocolChoices(ChoiceSet):
    """Routing protocol used by an L3Out peer/neighbor."""

    key = "ACIL3Out.routing_protocol"

    BGP = "bgp"
    OSPF = "ospf"
    EIGRP = "eigrp"
    STATIC = "static"

    CHOICES = [
        (BGP, _("BGP")),
        (OSPF, _("OSPF")),
        (EIGRP, _("EIGRP")),
        (STATIC, _("Static")),
    ]


class OSPFNetworkTypeChoices(ChoiceSet):
    """OSPF interface network type (``ospfIfPol.nwT``)."""

    key = "ACIOSPFInterfacePolicy.network_type"

    UNSPECIFIED = "unspecified"
    POINT_TO_POINT = "pt-to-pt"
    BROADCAST = "bcast"

    CHOICES = [
        (UNSPECIFIED, _("Unspecified")),
        (POINT_TO_POINT, _("Point-to-point")),
        (BROADCAST, _("Broadcast")),
    ]


class OSPFAreaTypeChoices(ChoiceSet):
    """OSPF area type used by an L3Out OSPF interface attachment."""

    key = "ACIOSPFInterfaceAttachment.ospf_area_type"

    REGULAR = "regular"
    STUB = "stub"
    NSSA = "nssa"

    CHOICES = [
        (REGULAR, _("Regular")),
        (STUB, _("Stub")),
        (NSSA, _("NSSA")),
    ]


class StaticRouteNextHopTypeChoices(ChoiceSet):
    """Type of next hop on an L3Out static route entry (``ipNexthopP.nhType``)."""

    key = "ACIL3OutStaticRouteNextHop.nexthop_type"

    PREFIX = "prefix"
    NONE = "none"

    CHOICES = [
        (PREFIX, _("Prefix (normal next-hop)")),
        (NONE, _("None (null route)")),
    ]


# ---------------------------------------------------------------------------
# uSeg EPG attributes
# ---------------------------------------------------------------------------


class USegAttributeTypeChoices(ChoiceSet):
    """uSeg EPG attribute type."""

    key = "USegAttribute.type"

    IP = "ip"
    MAC = "mac"
    DNS = "dns"
    VM_NAME = "vm-name"
    VM_TAG = "vm-tag"
    VNIC_DN = "vnic-dn"
    GUEST_OS = "guest-os"

    CHOICES = [
        (IP, _("IP")),
        (MAC, _("MAC")),
        (DNS, _("DNS")),
        (VM_NAME, _("VM Name")),
        (VM_TAG, _("VM Tag")),
        (VNIC_DN, _("vNIC DN")),
        (GUEST_OS, _("Guest OS")),
    ]


class USegAttributeMatchOperatorChoices(ChoiceSet):
    """uSeg attribute match operator."""

    key = "USegAttribute.match_operator"

    EQUALS = "equals"
    CONTAINS = "contains"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"

    CHOICES = [
        (EQUALS, _("Equals")),
        (CONTAINS, _("Contains")),
        (STARTSWITH, _("Starts with")),
        (ENDSWITH, _("Ends with")),
    ]


# ---------------------------------------------------------------------------
# Access policies — interface policies (Phase 4)
# ---------------------------------------------------------------------------


class EnabledDisabledChoices(ChoiceSet):
    """Generic enabled/disabled admin state used by several APIC policies."""

    key = "ACIPolicy.enabled_disabled"

    ENABLED = "enabled"
    DISABLED = "disabled"

    CHOICES = [
        (ENABLED, _("Enabled"), "green"),
        (DISABLED, _("Disabled"), "gray"),
    ]


class LinkLevelSpeedChoices(ChoiceSet):
    """Link Level interface speeds (``fabricHIfPol.speed``)."""

    key = "ACILinkLevelPolicy.speed"

    INHERIT = "inherit"
    SPEED_100M = "100M"
    SPEED_1G = "1G"
    SPEED_10G = "10G"
    SPEED_25G = "25G"
    SPEED_40G = "40G"
    SPEED_100G = "100G"
    SPEED_400G = "400G"

    CHOICES = [
        (INHERIT, _("Inherit")),
        (SPEED_100M, _("100 Mbps")),
        (SPEED_1G, _("1 Gbps")),
        (SPEED_10G, _("10 Gbps")),
        (SPEED_25G, _("25 Gbps")),
        (SPEED_40G, _("40 Gbps")),
        (SPEED_100G, _("100 Gbps")),
        (SPEED_400G, _("400 Gbps")),
    ]


class LinkLevelAutoNegChoices(ChoiceSet):
    """Auto-negotiation state on a Link Level policy."""

    key = "ACILinkLevelPolicy.auto_negotiation"

    ON = "on"
    OFF = "off"

    CHOICES = [
        (ON, _("On")),
        (OFF, _("Off")),
    ]


class LinkLevelFECChoices(ChoiceSet):
    """FEC modes available on a Link Level policy."""

    key = "ACILinkLevelPolicy.fec_mode"

    INHERIT = "inherit"
    CL74_FC_FEC = "cl74-fc-fec"
    CL91_RS_FEC = "cl91-rs-fec"
    CONS16_RS_FEC = "cons16-rs-fec"
    IEEE_RS_FEC = "ieee-rs-fec"
    KP_FEC = "kp-fec"
    DISABLE_FEC = "disable-fec"

    CHOICES = [
        (INHERIT, _("Inherit")),
        (CL74_FC_FEC, _("CL74 FC-FEC")),
        (CL91_RS_FEC, _("CL91 RS-FEC")),
        (CONS16_RS_FEC, _("Consortium-16 RS-FEC")),
        (IEEE_RS_FEC, _("IEEE RS-FEC")),
        (KP_FEC, _("KP-FEC")),
        (DISABLE_FEC, _("Disabled")),
    ]


class LACPModeChoices(ChoiceSet):
    """LACP / port-channel modes (``lacpLagPol.mode``)."""

    key = "ACILACPInterfacePolicy.mode"

    OFF = "off"
    ACTIVE = "active"
    PASSIVE = "passive"
    MAC_PIN = "mac-pin"
    MAC_PIN_NIC_LOAD = "mac-pin-nic-load"
    EXPLICIT_FAILOVER = "explicit-failover"

    CHOICES = [
        (OFF, _("Off (static)")),
        (ACTIVE, _("LACP Active")),
        (PASSIVE, _("LACP Passive")),
        (MAC_PIN, _("MAC Pinning")),
        (MAC_PIN_NIC_LOAD, _("MAC Pinning + NIC Load Balancing")),
        (EXPLICIT_FAILOVER, _("Explicit Failover Order")),
    ]


class InterfacePolicyGroupTypeChoices(ChoiceSet):
    """Interface Policy Group variant (access / PC / vPC)."""

    key = "ACIInterfacePolicyGroup.pg_type"

    ACCESS = "access"
    PC = "pc"
    VPC = "vpc"

    CHOICES = [
        (ACCESS, _("Access"), "gray"),
        (PC, _("Port Channel"), "blue"),
        (VPC, _("Virtual Port Channel"), "purple"),
    ]


class RangeAllChoices(ChoiceSet):
    """Selector mode: explicit range vs. \u201call\u201d."""

    key = "ACISelector.selector_type"

    RANGE = "range"
    ALL = "all"

    CHOICES = [
        (RANGE, _("Range")),
        (ALL, _("All")),
    ]
