"""SearchIndex registrations for the global NetBox search."""

from netbox.search import SearchIndex, register_search

from .models.access import (
    ACIAAEP,
    ACIAAEPEPGMapping,
    ACIDomain,
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
