"""DRF serializers for tenancy models."""

from ipam.api.serializers import PrefixSerializer, VRFSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.fabric import ACIFabric
from ...models.tenant import (
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
    ACIVRF,
)
from .fabric import ACIFabricSerializer


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_aci-api:{view}-detail"
    )


# ---------------------------------------------------------------------------
# Tenant
# ---------------------------------------------------------------------------

class ACITenantSerializer(NetBoxModelSerializer):
    url = _url("acitenant")
    aci_fabric = ACIFabricSerializer(read_only=True)
    aci_fabric_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIFabric.objects.all(),
        source="aci_fabric",
        write_only=True,
    )
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
            "aci_fabric_id",
            "description",
            "vrf_count",
            "bd_count",
            "app_profile_count",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )


# ---------------------------------------------------------------------------
# VRF
# ---------------------------------------------------------------------------

class ACIVRFSerializer(NetBoxModelSerializer):
    url = _url("acivrf")
    aci_tenant = ACITenantSerializer(read_only=True)
    aci_tenant_id = serializers.PrimaryKeyRelatedField(
        queryset=ACITenant.objects.all(), source="aci_tenant", write_only=True
    )
    nb_vrf = VRFSerializer(read_only=True, nested=True)

    class Meta:
        model = ACIVRF
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_tenant_id",
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


# ---------------------------------------------------------------------------
# Bridge Domain + Subnet
# ---------------------------------------------------------------------------

class ACIBridgeDomainSerializer(NetBoxModelSerializer):
    url = _url("acibridgedomain")
    aci_tenant = ACITenantSerializer(read_only=True)
    aci_tenant_id = serializers.PrimaryKeyRelatedField(
        queryset=ACITenant.objects.all(), source="aci_tenant", write_only=True
    )
    aci_vrf = ACIVRFSerializer(read_only=True)
    aci_vrf_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIVRF.objects.all(), source="aci_vrf", write_only=True
    )
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
            "aci_tenant_id",
            "aci_vrf",
            "aci_vrf_id",
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


class ACIBridgeDomainSubnetSerializer(NetBoxModelSerializer):
    url = _url("acibridgedomainsubnet")
    aci_bridge_domain = ACIBridgeDomainSerializer(read_only=True)
    aci_bridge_domain_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIBridgeDomain.objects.all(), source="aci_bridge_domain", write_only=True
    )
    nb_prefix = PrefixSerializer(read_only=True, nested=True)

    class Meta:
        model = ACIBridgeDomainSubnet
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_bridge_domain",
            "aci_bridge_domain_id",
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


# ---------------------------------------------------------------------------
# App Profile + EPG + uSeg
# ---------------------------------------------------------------------------

class ACIAppProfileSerializer(NetBoxModelSerializer):
    url = _url("aciappprofile")
    aci_tenant = ACITenantSerializer(read_only=True)
    aci_tenant_id = serializers.PrimaryKeyRelatedField(
        queryset=ACITenant.objects.all(), source="aci_tenant", write_only=True
    )
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
            "aci_tenant_id",
            "epg_count",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )


class ACIEndpointGroupSerializer(NetBoxModelSerializer):
    url = _url("aciendpointgroup")
    aci_tenant = ACITenantSerializer(read_only=True)
    aci_tenant_id = serializers.PrimaryKeyRelatedField(
        queryset=ACITenant.objects.all(), source="aci_tenant", write_only=True
    )
    aci_app_profile = ACIAppProfileSerializer(read_only=True)
    aci_app_profile_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIAppProfile.objects.all(), source="aci_app_profile", write_only=True
    )
    aci_bridge_domain = ACIBridgeDomainSerializer(read_only=True)
    aci_bridge_domain_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIBridgeDomain.objects.all(), source="aci_bridge_domain", write_only=True
    )

    class Meta:
        model = ACIEndpointGroup
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_tenant_id",
            "aci_app_profile",
            "aci_app_profile_id",
            "aci_bridge_domain",
            "aci_bridge_domain_id",
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


class ACIUSegAttributeSerializer(NetBoxModelSerializer):
    url = _url("aciusegattribute")
    aci_endpoint_group = ACIEndpointGroupSerializer(read_only=True)
    aci_endpoint_group_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIEndpointGroup.objects.filter(is_useg=True),
        source="aci_endpoint_group",
        write_only=True,
    )

    class Meta:
        model = ACIUSegAttribute
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_endpoint_group",
            "aci_endpoint_group_id",
            "attribute_type",
            "match_operator",
            "match_value",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )


# ---------------------------------------------------------------------------
# ESG
# ---------------------------------------------------------------------------

class ACIEndpointSecurityGroupSerializer(NetBoxModelSerializer):
    url = _url("aciendpointsecuritygroup")
    aci_tenant = ACITenantSerializer(read_only=True)
    aci_tenant_id = serializers.PrimaryKeyRelatedField(
        queryset=ACITenant.objects.all(), source="aci_tenant", write_only=True
    )
    aci_vrf = ACIVRFSerializer(read_only=True)
    aci_vrf_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIVRF.objects.all(), source="aci_vrf", write_only=True
    )
    aci_app_profile = ACIAppProfileSerializer(read_only=True)
    aci_app_profile_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIAppProfile.objects.all(),
        source="aci_app_profile",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = ACIEndpointSecurityGroup
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_tenant_id",
            "aci_vrf",
            "aci_vrf_id",
            "aci_app_profile",
            "aci_app_profile_id",
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
