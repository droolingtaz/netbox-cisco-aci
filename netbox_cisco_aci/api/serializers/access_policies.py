"""DRF serializers for the six per-policy interface refs (Phase 4)."""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.access import (
    ACICDPInterfacePolicy,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
)
from .fabric import ACIFabricSerializer


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_cisco_aci-api:{view}-detail"
    )


class ACILinkLevelPolicySerializer(NetBoxModelSerializer):
    url = _url("acilinklevelpolicy")
    aci_fabric = ACIFabricSerializer(nested=True)

    class Meta:
        model = ACILinkLevelPolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "speed",
            "auto_negotiation",
            "link_debounce_interval_ms",
            "fec_mode",
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
            "speed",
            "url",
        )


class ACICDPInterfacePolicySerializer(NetBoxModelSerializer):
    url = _url("acicdpinterfacepolicy")
    aci_fabric = ACIFabricSerializer(nested=True)

    class Meta:
        model = ACICDPInterfacePolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "admin_state",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_fabric",
            "admin_state",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


class ACILLDPInterfacePolicySerializer(NetBoxModelSerializer):
    url = _url("acilldpinterfacepolicy")
    aci_fabric = ACIFabricSerializer(nested=True)

    class Meta:
        model = ACILLDPInterfacePolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "receive_state",
            "transmit_state",
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
            "receive_state",
            "transmit_state",
            "url",
        )


class ACILACPInterfacePolicySerializer(NetBoxModelSerializer):
    url = _url("acilacpinterfacepolicy")
    aci_fabric = ACIFabricSerializer(nested=True)

    class Meta:
        model = ACILACPInterfacePolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "mode",
            "min_links",
            "max_links",
            "control_fast_select_hot_standby",
            "control_graceful_convergence",
            "control_load_defer",
            "control_suspend_individual_port",
            "control_symmetric_hashing",
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
            "mode",
            "name",
            "url",
        )


class ACIMCPInterfacePolicySerializer(NetBoxModelSerializer):
    url = _url("acimcpinterfacepolicy")
    aci_fabric = ACIFabricSerializer(nested=True)

    class Meta:
        model = ACIMCPInterfacePolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "admin_state",
            "strict_mode",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_fabric",
            "admin_state",
            "description",
            "display",
            "id",
            "name",
            "strict_mode",
            "url",
        )


class ACISTPInterfacePolicySerializer(NetBoxModelSerializer):
    url = _url("acistpinterfacepolicy")
    aci_fabric = ACIFabricSerializer(nested=True)

    class Meta:
        model = ACISTPInterfacePolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "bpdu_filter",
            "bpdu_guard",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_fabric",
            "bpdu_filter",
            "bpdu_guard",
            "description",
            "display",
            "id",
            "name",
            "url",
        )
