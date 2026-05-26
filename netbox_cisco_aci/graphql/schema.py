"""Strawberry GraphQL schema for the plugin.

Each model gets a type plus a `list_*` resolver and a `*` (single-object)
resolver. NetBox merges this schema into its own at startup.
"""

import strawberry
import strawberry_django

from ..models.access import (
    ACIAAEP,
    ACIAAEPEPGMapping,
    ACICDPInterfacePolicy,
    ACIDomain,
    ACIInterfacePolicyGroup,
    ACIInterfaceProfile,
    ACIInterfaceProfileSelector,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
    ACISwitchProfile,
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileSelector,
    ACIVLANPool,
    ACIVLANPoolBlock,
)
from ..models.bindings import (
    ACIDomainBinding,
    ACIInterfaceFabricMembership,
    ACIStaticPortBinding,
    ACIVPCBindingPair,
)
from ..models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from ..models.fabric import ACIFabric, ACINode, ACIPod
from ..models.l3out import (
    ACIBGPPeer,
    ACIEIGRPInterfacePolicy,
    ACIExternalEPG,
    ACIExternalEPGSubnet,
    ACIL3Out,
    ACIL3OutInterface,
    ACIL3OutStaticRoute,
    ACIL3OutStaticRouteNextHop,
    ACILogicalInterfaceProfile,
    ACILogicalNode,
    ACILogicalNodeProfile,
    ACIOSPFInterfaceAttachment,
    ACIOSPFInterfacePolicy,
)
from ..models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
)

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


@strawberry_django.type(ACIFabric, fields="__all__")
class ACIFabricType:
    pass


@strawberry_django.type(ACIPod, fields="__all__")
class ACIPodType:
    pass


@strawberry_django.type(ACINode, fields="__all__")
class ACINodeType:
    pass


@strawberry_django.type(ACITenant, fields="__all__")
class ACITenantType:
    pass


@strawberry_django.type(ACIVRF, fields="__all__")
class ACIVRFType:
    pass


@strawberry_django.type(ACIBridgeDomain, fields="__all__")
class ACIBridgeDomainType:
    pass


@strawberry_django.type(ACIBridgeDomainSubnet, fields="__all__")
class ACIBridgeDomainSubnetType:
    pass


@strawberry_django.type(ACIAppProfile, fields="__all__")
class ACIAppProfileType:
    pass


@strawberry_django.type(ACIEndpointGroup, fields="__all__")
class ACIEndpointGroupType:
    pass


@strawberry_django.type(ACIUSegAttribute, fields="__all__")
class ACIUSegAttributeType:
    pass


@strawberry_django.type(ACIEndpointSecurityGroup, fields="__all__")
class ACIEndpointSecurityGroupType:
    pass


@strawberry_django.type(ACIVLANPool, fields="__all__")
class ACIVLANPoolType:
    pass


@strawberry_django.type(ACIVLANPoolBlock, fields="__all__")
class ACIVLANPoolBlockType:
    pass


@strawberry_django.type(ACIDomain, fields="__all__")
class ACIDomainType:
    pass


@strawberry_django.type(ACIAAEP, fields="__all__")
class ACIAAEPType:
    pass


@strawberry_django.type(ACIAAEPEPGMapping, fields="__all__")
class ACIAAEPEPGMappingType:
    pass


@strawberry_django.type(ACILinkLevelPolicy, fields="__all__")
class ACILinkLevelPolicyType:
    pass


@strawberry_django.type(ACICDPInterfacePolicy, fields="__all__")
class ACICDPInterfacePolicyType:
    pass


@strawberry_django.type(ACILLDPInterfacePolicy, fields="__all__")
class ACILLDPInterfacePolicyType:
    pass


@strawberry_django.type(ACILACPInterfacePolicy, fields="__all__")
class ACILACPInterfacePolicyType:
    pass


@strawberry_django.type(ACIMCPInterfacePolicy, fields="__all__")
class ACIMCPInterfacePolicyType:
    pass


@strawberry_django.type(ACISTPInterfacePolicy, fields="__all__")
class ACISTPInterfacePolicyType:
    pass


@strawberry_django.type(ACIInterfacePolicyGroup, fields="__all__")
class ACIInterfacePolicyGroupType:
    pass


@strawberry_django.type(ACISwitchProfile, fields="__all__")
class ACISwitchProfileType:
    pass


@strawberry_django.type(ACISwitchProfileSelector, fields="__all__")
class ACISwitchProfileSelectorType:
    pass


@strawberry_django.type(ACIInterfaceProfile, fields="__all__")
class ACIInterfaceProfileType:
    pass


@strawberry_django.type(ACIInterfaceProfileSelector, fields="__all__")
class ACIInterfaceProfileSelectorType:
    pass


@strawberry_django.type(ACISwitchProfileInterfaceProfileAttachment, fields="__all__")
class ACISwitchProfileInterfaceProfileAttachmentType:
    pass


@strawberry_django.type(ACIContract, fields="__all__")
class ACIContractType:
    pass


@strawberry_django.type(ACISubject, fields="__all__")
class ACISubjectType:
    pass


@strawberry_django.type(ACIFilter, fields="__all__")
class ACIFilterType:
    pass


@strawberry_django.type(ACIFilterEntry, fields="__all__")
class ACIFilterEntryType:
    pass


@strawberry_django.type(ACISubjectFilter, fields="__all__")
class ACISubjectFilterType:
    pass


@strawberry_django.type(ACIContractRelation, fields="__all__")
class ACIContractRelationType:
    pass


@strawberry_django.type(ACIStaticPortBinding, fields="__all__")
class ACIStaticPortBindingType:
    pass


@strawberry_django.type(ACIVPCBindingPair, fields="__all__")
class ACIVPCBindingPairType:
    pass


@strawberry_django.type(ACIDomainBinding, fields="__all__")
class ACIDomainBindingType:
    pass


@strawberry_django.type(ACIInterfaceFabricMembership, fields="__all__")
class ACIInterfaceFabricMembershipType:
    pass


@strawberry_django.type(ACIL3Out, fields="__all__")
class ACIL3OutType:
    pass


@strawberry_django.type(ACILogicalNodeProfile, fields="__all__")
class ACILogicalNodeProfileType:
    pass


@strawberry_django.type(ACILogicalNode, fields="__all__")
class ACILogicalNodeType:
    pass


@strawberry_django.type(ACILogicalInterfaceProfile, fields="__all__")
class ACILogicalInterfaceProfileType:
    pass


@strawberry_django.type(ACIL3OutInterface, fields="__all__")
class ACIL3OutInterfaceType:
    pass


@strawberry_django.type(ACIBGPPeer, fields="__all__")
class ACIBGPPeerType:
    pass


@strawberry_django.type(ACIOSPFInterfacePolicy, fields="__all__")
class ACIOSPFInterfacePolicyType:
    pass


@strawberry_django.type(ACIOSPFInterfaceAttachment, fields="__all__")
class ACIOSPFInterfaceAttachmentType:
    pass


@strawberry_django.type(ACIEIGRPInterfacePolicy, fields="__all__")
class ACIEIGRPInterfacePolicyType:
    pass


@strawberry_django.type(ACIL3OutStaticRoute, fields="__all__")
class ACIL3OutStaticRouteType:
    pass


@strawberry_django.type(ACIL3OutStaticRouteNextHop, fields="__all__")
class ACIL3OutStaticRouteNextHopType:
    pass


@strawberry_django.type(ACIExternalEPG, fields="__all__")
class ACIExternalEPGType:
    pass


@strawberry_django.type(ACIExternalEPGSubnet, fields="__all__")
class ACIExternalEPGSubnetType:
    pass


# ---------------------------------------------------------------------------
# Query root
# ---------------------------------------------------------------------------


@strawberry.type
class Query:
    aci_fabric: ACIFabricType | None = strawberry_django.field()
    aci_fabric_list: list[ACIFabricType] = strawberry_django.field()

    aci_pod: ACIPodType | None = strawberry_django.field()
    aci_pod_list: list[ACIPodType] = strawberry_django.field()

    aci_node: ACINodeType | None = strawberry_django.field()
    aci_node_list: list[ACINodeType] = strawberry_django.field()

    aci_tenant: ACITenantType | None = strawberry_django.field()
    aci_tenant_list: list[ACITenantType] = strawberry_django.field()

    aci_vrf: ACIVRFType | None = strawberry_django.field()
    aci_vrf_list: list[ACIVRFType] = strawberry_django.field()

    aci_bridge_domain: ACIBridgeDomainType | None = strawberry_django.field()
    aci_bridge_domain_list: list[ACIBridgeDomainType] = strawberry_django.field()

    aci_bridge_domain_subnet: ACIBridgeDomainSubnetType | None = strawberry_django.field()
    aci_bridge_domain_subnet_list: list[ACIBridgeDomainSubnetType] = strawberry_django.field()

    aci_app_profile: ACIAppProfileType | None = strawberry_django.field()
    aci_app_profile_list: list[ACIAppProfileType] = strawberry_django.field()

    aci_endpoint_group: ACIEndpointGroupType | None = strawberry_django.field()
    aci_endpoint_group_list: list[ACIEndpointGroupType] = strawberry_django.field()

    aci_useg_attribute: ACIUSegAttributeType | None = strawberry_django.field()
    aci_useg_attribute_list: list[ACIUSegAttributeType] = strawberry_django.field()

    aci_endpoint_security_group: ACIEndpointSecurityGroupType | None = strawberry_django.field()
    aci_endpoint_security_group_list: list[ACIEndpointSecurityGroupType] = strawberry_django.field()

    aci_vlan_pool: ACIVLANPoolType | None = strawberry_django.field()
    aci_vlan_pool_list: list[ACIVLANPoolType] = strawberry_django.field()

    aci_vlan_pool_block: ACIVLANPoolBlockType | None = strawberry_django.field()
    aci_vlan_pool_block_list: list[ACIVLANPoolBlockType] = strawberry_django.field()

    aci_domain: ACIDomainType | None = strawberry_django.field()
    aci_domain_list: list[ACIDomainType] = strawberry_django.field()

    aci_aaep: ACIAAEPType | None = strawberry_django.field()
    aci_aaep_list: list[ACIAAEPType] = strawberry_django.field()

    aci_aaep_epg_mapping: ACIAAEPEPGMappingType | None = strawberry_django.field()
    aci_aaep_epg_mapping_list: list[ACIAAEPEPGMappingType] = strawberry_django.field()

    aci_link_level_policy: ACILinkLevelPolicyType | None = strawberry_django.field()
    aci_link_level_policy_list: list[ACILinkLevelPolicyType] = strawberry_django.field()

    aci_cdp_interface_policy: ACICDPInterfacePolicyType | None = strawberry_django.field()
    aci_cdp_interface_policy_list: list[ACICDPInterfacePolicyType] = strawberry_django.field()

    aci_lldp_interface_policy: ACILLDPInterfacePolicyType | None = strawberry_django.field()
    aci_lldp_interface_policy_list: list[ACILLDPInterfacePolicyType] = strawberry_django.field()

    aci_lacp_interface_policy: ACILACPInterfacePolicyType | None = strawberry_django.field()
    aci_lacp_interface_policy_list: list[ACILACPInterfacePolicyType] = strawberry_django.field()

    aci_mcp_interface_policy: ACIMCPInterfacePolicyType | None = strawberry_django.field()
    aci_mcp_interface_policy_list: list[ACIMCPInterfacePolicyType] = strawberry_django.field()

    aci_stp_interface_policy: ACISTPInterfacePolicyType | None = strawberry_django.field()
    aci_stp_interface_policy_list: list[ACISTPInterfacePolicyType] = strawberry_django.field()

    aci_interface_policy_group: ACIInterfacePolicyGroupType | None = strawberry_django.field()
    aci_interface_policy_group_list: list[ACIInterfacePolicyGroupType] = strawberry_django.field()

    aci_switch_profile: ACISwitchProfileType | None = strawberry_django.field()
    aci_switch_profile_list: list[ACISwitchProfileType] = strawberry_django.field()

    aci_switch_profile_selector: ACISwitchProfileSelectorType | None = strawberry_django.field()
    aci_switch_profile_selector_list: list[ACISwitchProfileSelectorType] = strawberry_django.field()

    aci_interface_profile: ACIInterfaceProfileType | None = strawberry_django.field()
    aci_interface_profile_list: list[ACIInterfaceProfileType] = strawberry_django.field()

    aci_interface_profile_selector: ACIInterfaceProfileSelectorType | None = (
        strawberry_django.field()
    )
    aci_interface_profile_selector_list: list[ACIInterfaceProfileSelectorType] = (
        strawberry_django.field()
    )

    aci_switch_profile_interface_profile_attachment: (
        ACISwitchProfileInterfaceProfileAttachmentType | None
    ) = strawberry_django.field()
    aci_switch_profile_interface_profile_attachment_list: list[
        ACISwitchProfileInterfaceProfileAttachmentType
    ] = strawberry_django.field()

    aci_contract: ACIContractType | None = strawberry_django.field()
    aci_contract_list: list[ACIContractType] = strawberry_django.field()

    aci_subject: ACISubjectType | None = strawberry_django.field()
    aci_subject_list: list[ACISubjectType] = strawberry_django.field()

    aci_filter: ACIFilterType | None = strawberry_django.field()
    aci_filter_list: list[ACIFilterType] = strawberry_django.field()

    aci_filter_entry: ACIFilterEntryType | None = strawberry_django.field()
    aci_filter_entry_list: list[ACIFilterEntryType] = strawberry_django.field()

    aci_subject_filter: ACISubjectFilterType | None = strawberry_django.field()
    aci_subject_filter_list: list[ACISubjectFilterType] = strawberry_django.field()

    aci_contract_relation: ACIContractRelationType | None = strawberry_django.field()
    aci_contract_relation_list: list[ACIContractRelationType] = strawberry_django.field()

    aci_static_port_binding: ACIStaticPortBindingType | None = strawberry_django.field()
    aci_static_port_binding_list: list[ACIStaticPortBindingType] = strawberry_django.field()

    aci_vpc_binding_pair: ACIVPCBindingPairType | None = strawberry_django.field()
    aci_vpc_binding_pair_list: list[ACIVPCBindingPairType] = strawberry_django.field()

    aci_domain_binding: ACIDomainBindingType | None = strawberry_django.field()
    aci_domain_binding_list: list[ACIDomainBindingType] = strawberry_django.field()

    aci_interface_fabric_membership: ACIInterfaceFabricMembershipType | None = (
        strawberry_django.field()
    )
    aci_interface_fabric_membership_list: list[ACIInterfaceFabricMembershipType] = (
        strawberry_django.field()
    )

    aci_l3out: ACIL3OutType | None = strawberry_django.field()
    aci_l3out_list: list[ACIL3OutType] = strawberry_django.field()

    aci_logical_node_profile: ACILogicalNodeProfileType | None = strawberry_django.field()
    aci_logical_node_profile_list: list[ACILogicalNodeProfileType] = strawberry_django.field()

    aci_logical_node: ACILogicalNodeType | None = strawberry_django.field()
    aci_logical_node_list: list[ACILogicalNodeType] = strawberry_django.field()

    aci_logical_interface_profile: ACILogicalInterfaceProfileType | None = strawberry_django.field()
    aci_logical_interface_profile_list: list[ACILogicalInterfaceProfileType] = (
        strawberry_django.field()
    )

    aci_l3out_interface: ACIL3OutInterfaceType | None = strawberry_django.field()
    aci_l3out_interface_list: list[ACIL3OutInterfaceType] = strawberry_django.field()

    aci_bgp_peer: ACIBGPPeerType | None = strawberry_django.field()
    aci_bgp_peer_list: list[ACIBGPPeerType] = strawberry_django.field()

    aci_ospf_interface_policy: ACIOSPFInterfacePolicyType | None = strawberry_django.field()
    aci_ospf_interface_policy_list: list[ACIOSPFInterfacePolicyType] = strawberry_django.field()

    aci_ospf_interface_attachment: ACIOSPFInterfaceAttachmentType | None = strawberry_django.field()
    aci_ospf_interface_attachment_list: list[ACIOSPFInterfaceAttachmentType] = (
        strawberry_django.field()
    )

    aci_eigrp_interface_policy: ACIEIGRPInterfacePolicyType | None = strawberry_django.field()
    aci_eigrp_interface_policy_list: list[ACIEIGRPInterfacePolicyType] = strawberry_django.field()

    aci_external_epg: ACIExternalEPGType | None = strawberry_django.field()
    aci_external_epg_list: list[ACIExternalEPGType] = strawberry_django.field()

    aci_external_epg_subnet: ACIExternalEPGSubnetType | None = strawberry_django.field()
    aci_external_epg_subnet_list: list[ACIExternalEPGSubnetType] = strawberry_django.field()

    aci_l3out_static_route: ACIL3OutStaticRouteType | None = strawberry_django.field()
    aci_l3out_static_route_list: list[ACIL3OutStaticRouteType] = strawberry_django.field()

    aci_l3out_static_route_next_hop: ACIL3OutStaticRouteNextHopType | None = (
        strawberry_django.field()
    )
    aci_l3out_static_route_next_hop_list: list[ACIL3OutStaticRouteNextHopType] = (
        strawberry_django.field()
    )


schema = [Query]
