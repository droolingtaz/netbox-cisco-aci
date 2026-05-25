"""Strawberry GraphQL schema for the plugin.

Each model gets a type plus a `list_*` resolver and a `*` (single-object)
resolver. NetBox merges this schema into its own at startup.
"""

import strawberry
import strawberry_django

from ..models.fabric import ACIFabric, ACINode, ACIPod
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


schema = [Query]
