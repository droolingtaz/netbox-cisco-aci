"""SearchIndex registrations for the global NetBox search."""

from netbox.search import SearchIndex, register_search

from .models.access import (
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
from .models.fabric import ACIFabric, ACINode, ACIPod
from .models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
)


@register_search
class ACIFabricIndex(SearchIndex):
    model = ACIFabric
    fields = (("name", 100), ("description", 500), ("fabric_id", 100))


@register_search
class ACIPodIndex(SearchIndex):
    model = ACIPod
    fields = (("name", 100), ("description", 500), ("pod_id", 100))


@register_search
class ACINodeIndex(SearchIndex):
    model = ACINode
    fields = (
        ("name", 100),
        ("description", 500),
        ("node_id", 100),
        ("serial_number", 200),
    )


@register_search
class ACITenantIndex(SearchIndex):
    model = ACITenant
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIVRFIndex(SearchIndex):
    model = ACIVRF
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIBridgeDomainIndex(SearchIndex):
    model = ACIBridgeDomain
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIBridgeDomainSubnetIndex(SearchIndex):
    model = ACIBridgeDomainSubnet
    fields = (("gateway_ip", 100), ("name", 200), ("description", 500))


@register_search
class ACIAppProfileIndex(SearchIndex):
    model = ACIAppProfile
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIEndpointGroupIndex(SearchIndex):
    model = ACIEndpointGroup
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIUSegAttributeIndex(SearchIndex):
    model = ACIUSegAttribute
    fields = (("name", 100), ("match_value", 200), ("description", 500))


@register_search
class ACIEndpointSecurityGroupIndex(SearchIndex):
    model = ACIEndpointSecurityGroup
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIVLANPoolIndex(SearchIndex):
    model = ACIVLANPool
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIVLANPoolBlockIndex(SearchIndex):
    model = ACIVLANPoolBlock
    fields = (("name", 100), ("description", 500))


@register_search
class ACIDomainIndex(SearchIndex):
    model = ACIDomain
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIAAEPIndex(SearchIndex):
    model = ACIAAEP
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIAAEPEPGMappingIndex(SearchIndex):
    model = ACIAAEPEPGMapping
    fields = (("name", 100), ("description", 500))


# Phase 4 — Interface policies, policy groups, profiles


@register_search
class ACILinkLevelPolicyIndex(SearchIndex):
    model = ACILinkLevelPolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACICDPInterfacePolicyIndex(SearchIndex):
    model = ACICDPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACILLDPInterfacePolicyIndex(SearchIndex):
    model = ACILLDPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACILACPInterfacePolicyIndex(SearchIndex):
    model = ACILACPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIMCPInterfacePolicyIndex(SearchIndex):
    model = ACIMCPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISTPInterfacePolicyIndex(SearchIndex):
    model = ACISTPInterfacePolicy
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIInterfacePolicyGroupIndex(SearchIndex):
    model = ACIInterfacePolicyGroup
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISwitchProfileIndex(SearchIndex):
    model = ACISwitchProfile
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISwitchProfileSelectorIndex(SearchIndex):
    model = ACISwitchProfileSelector
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIInterfaceProfileIndex(SearchIndex):
    model = ACIInterfaceProfile
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACIInterfaceProfileSelectorIndex(SearchIndex):
    model = ACIInterfaceProfileSelector
    fields = (("name", 100), ("name_alias", 200), ("description", 500))


@register_search
class ACISwitchProfileInterfaceProfileAttachmentIndex(SearchIndex):
    model = ACISwitchProfileInterfaceProfileAttachment
    fields = ()
