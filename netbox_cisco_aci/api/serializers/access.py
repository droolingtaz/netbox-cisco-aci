"""DRF serializers for access-policy models (Phase 3)."""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.access import (
    ACIAAEP,
    ACIAAEPEPGMapping,
    ACIDomain,
    ACIVLANPool,
    ACIVLANPoolBlock,
)
from .fabric import ACIFabricSerializer
from .tenant import ACIEndpointGroupSerializer


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_cisco_aci-api:{view}-detail"
    )


class ACIVLANPoolSerializer(NetBoxModelSerializer):
    url = _url("acivlanpool")
    aci_fabric = ACIFabricSerializer(nested=True)
    block_count = serializers.IntegerField(read_only=True)
    domain_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ACIVLANPool
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "allocation_mode",
            "block_count",
            "domain_count",
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
            "aci_fabric",
            "allocation_mode",
            "description",
        )


class ACIVLANPoolBlockSerializer(NetBoxModelSerializer):
    url = _url("acivlanpoolblock")
    aci_vlan_pool = ACIVLANPoolSerializer(nested=True)

    class Meta:
        model = ACIVLANPoolBlock
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_vlan_pool",
            "from_vlan",
            "to_vlan",
            "allocation_mode_override",
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
            "aci_vlan_pool",
            "from_vlan",
            "to_vlan",
            "description",
        )


class ACIDomainSerializer(NetBoxModelSerializer):
    url = _url("acidomain")
    aci_fabric = ACIFabricSerializer(nested=True)
    aci_vlan_pool = ACIVLANPoolSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACIDomain
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "domain_type",
            "aci_vlan_pool",
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
            "aci_fabric",
            "domain_type",
            "description",
        )


class ACIAAEPSerializer(NetBoxModelSerializer):
    url = _url("aciaaep")
    aci_fabric = ACIFabricSerializer(nested=True)
    domains = ACIDomainSerializer(nested=True, many=True, required=False)
    epg_mapping_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ACIAAEP
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "enable_infra_vlan",
            "domains",
            "epg_mapping_count",
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
            "aci_fabric",
            "enable_infra_vlan",
            "description",
        )


class ACIAAEPEPGMappingSerializer(NetBoxModelSerializer):
    url = _url("aciaaepepgmapping")
    aci_aaep = ACIAAEPSerializer(nested=True)
    aci_endpoint_group = ACIEndpointGroupSerializer(nested=True)

    class Meta:
        model = ACIAAEPEPGMapping
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_aaep",
            "aci_endpoint_group",
            "encap_vlan",
            "mode",
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
            "aci_aaep",
            "aci_endpoint_group",
            "encap_vlan",
            "mode",
        )
