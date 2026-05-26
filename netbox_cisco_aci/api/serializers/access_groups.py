"""DRF serializer for Interface Policy Groups (Phase 4)."""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.access import ACIInterfacePolicyGroup
from .access import ACIAAEPSerializer
from .access_policies import (
    ACICDPInterfacePolicySerializer,
    ACILACPInterfacePolicySerializer,
    ACILinkLevelPolicySerializer,
    ACILLDPInterfacePolicySerializer,
    ACIMCPInterfacePolicySerializer,
    ACISTPInterfacePolicySerializer,
)
from .fabric import ACIFabricSerializer


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_cisco_aci-api:{view}-detail"
    )


class ACIInterfacePolicyGroupSerializer(NetBoxModelSerializer):
    url = _url("aciinterfacepolicygroup")
    aci_fabric = ACIFabricSerializer(nested=True)
    link_level_policy = ACILinkLevelPolicySerializer(
        nested=True, required=False, allow_null=True
    )
    cdp_policy = ACICDPInterfacePolicySerializer(nested=True, required=False, allow_null=True)
    lldp_policy = ACILLDPInterfacePolicySerializer(nested=True, required=False, allow_null=True)
    lacp_policy = ACILACPInterfacePolicySerializer(nested=True, required=False, allow_null=True)
    mcp_policy = ACIMCPInterfacePolicySerializer(nested=True, required=False, allow_null=True)
    stp_policy = ACISTPInterfacePolicySerializer(nested=True, required=False, allow_null=True)
    aaep = ACIAAEPSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = ACIInterfacePolicyGroup
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "pg_type",
            "link_level_policy",
            "cdp_policy",
            "lldp_policy",
            "lacp_policy",
            "mcp_policy",
            "stp_policy",
            "aaep",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_fabric",
            "description",
            "display",
            "id",
            "name",
            "pg_type",
            "url",
        )
