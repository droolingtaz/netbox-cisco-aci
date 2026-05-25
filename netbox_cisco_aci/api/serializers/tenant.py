"""DRF serializers for tenancy models.

Uses the NetBox idiom of ``Serializer(nested=True)`` for FK fields (PK
on write, nested representation on read) and declares
``Meta.brief_fields`` so ``?brief=True`` works.
"""

from ipam.api.serializers import PrefixSerializer, VRFSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
)
from .fabric import ACIFabricSerializer


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_cisco_aci-api:{view}-detail"
    )


# ---------------------------------------------------------------------------
# Tenant
# ---------------------------------------------------------------------------


class ACITenantSerializer(NetBoxModelSerializer):
    url = _url("acitenant")
    aci_fabric = ACIFabricSerializer(nested=True)
    vrf_count = serializers.IntegerField(read_only=True)
    bd_count = serializers.IntegerField(read_only=True)
    app_profile_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ACITenant
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "description",
            "vrf_count",
            "bd_count",
            "app_profile_count",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "aci_fabric",
            "description",
        )


# ---------------------------------------------------------------------------
# VRF
# ---------------------------------------------------------------------------


class ACIVRFSerializer(NetBoxModelSerializer):
    url = _url("acivrf")
    aci_tenant = ACITenantSerializer(nested=True)
    nb_vrf = VRFSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACIVRF
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "nb_vrf",
            "policy_enforcement_preference",
            "policy_enforcement_direction",
            "bd_enforcement_enabled",
            "preferred_group_enabled",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "aci_tenant",
            "description",
        )


# ---------------------------------------------------------------------------
# Bridge Domain + Subnet
# ---------------------------------------------------------------------------


class ACIBridgeDomainSerializer(NetBoxModelSerializer):
    url = _url("acibridgedomain")
    aci_tenant = ACITenantSerializer(nested=True)
    aci_vrf = ACIVRFSerializer(nested=True)
    subnet_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ACIBridgeDomain
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_vrf",
            "unicast_routing_enabled",
            "arp_flooding_enabled",
            "limit_ip_learn_to_subnets",
            "l2_unknown_unicast",
            "l3_unknown_multicast",
            "multi_destination_flooding",
            "mac_address",
            "subnet_count",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "aci_tenant",
            "aci_vrf",
            "description",
        )


class ACIBridgeDomainSubnetSerializer(NetBoxModelSerializer):
    url = _url("acibridgedomainsubnet")
    aci_bridge_domain = ACIBridgeDomainSerializer(nested=True)
    nb_prefix = PrefixSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACIBridgeDomainSubnet
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_bridge_domain",
            "gateway_ip",
            "nb_prefix",
            "scope_public",
            "scope_shared",
            "scope_private",
            "is_primary",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "gateway_ip",
            "aci_bridge_domain",
            "description",
        )


# ---------------------------------------------------------------------------
# App Profile + EPG + uSeg
# ---------------------------------------------------------------------------


class ACIAppProfileSerializer(NetBoxModelSerializer):
    url = _url("aciappprofile")
    aci_tenant = ACITenantSerializer(nested=True)
    epg_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ACIAppProfile
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "epg_count",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "aci_tenant",
            "description",
        )


class ACIEndpointGroupSerializer(NetBoxModelSerializer):
    url = _url("aciendpointgroup")
    aci_tenant = ACITenantSerializer(nested=True)
    aci_app_profile = ACIAppProfileSerializer(nested=True)
    aci_bridge_domain = ACIBridgeDomainSerializer(nested=True)

    class Meta:
        model = ACIEndpointGroup
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_app_profile",
            "aci_bridge_domain",
            "admin_shutdown",
            "is_useg",
            "intra_epg_isolation",
            "preferred_group_member",
            "qos_class",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "aci_tenant",
            "aci_app_profile",
            "description",
        )


class ACIUSegAttributeSerializer(NetBoxModelSerializer):
    url = _url("aciusegattribute")
    aci_endpoint_group = ACIEndpointGroupSerializer(nested=True)

    class Meta:
        model = ACIUSegAttribute
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_endpoint_group",
            "attribute_type",
            "match_operator",
            "match_value",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "aci_endpoint_group",
            "attribute_type",
        )


# ---------------------------------------------------------------------------
# ESG
# ---------------------------------------------------------------------------


class ACIEndpointSecurityGroupSerializer(NetBoxModelSerializer):
    url = _url("aciendpointsecuritygroup")
    aci_tenant = ACITenantSerializer(nested=True)
    aci_vrf = ACIVRFSerializer(nested=True)
    aci_app_profile = ACIAppProfileSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACIEndpointSecurityGroup
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_vrf",
            "aci_app_profile",
            "admin_shutdown",
            "preferred_group_member",
            "intra_esg_isolation",
            "qos_class",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "aci_tenant",
            "aci_vrf",
            "description",
        )
