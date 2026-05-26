"""DRF serializers for Switch / Interface Profiles + selectors + attachments (Phase 4)."""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.access import (
    ACIInterfaceProfile,
    ACIInterfaceProfileSelector,
    ACISwitchProfile,
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileSelector,
)
from .access_groups import ACIInterfacePolicyGroupSerializer
from .fabric import ACIFabricSerializer


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_cisco_aci-api:{view}-detail"
    )


class ACISwitchProfileSerializer(NetBoxModelSerializer):
    url = _url("aciswitchprofile")
    aci_fabric = ACIFabricSerializer(nested=True)

    class Meta:
        model = ACISwitchProfile
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
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
            "url",
        )


class ACISwitchProfileSelectorSerializer(NetBoxModelSerializer):
    url = _url("aciswitchprofileselector")
    switch_profile = ACISwitchProfileSerializer(nested=True)

    class Meta:
        model = ACISwitchProfileSelector
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "switch_profile",
            "selector_type",
            "from_node_id",
            "to_node_id",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "description",
            "display",
            "from_node_id",
            "id",
            "name",
            "selector_type",
            "switch_profile",
            "to_node_id",
            "url",
        )


class ACIInterfaceProfileSerializer(NetBoxModelSerializer):
    url = _url("aciinterfaceprofile")
    aci_fabric = ACIFabricSerializer(nested=True)

    class Meta:
        model = ACIInterfaceProfile
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
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
            "url",
        )


class ACIInterfaceProfileSelectorSerializer(NetBoxModelSerializer):
    url = _url("aciinterfaceprofileselector")
    interface_profile = ACIInterfaceProfileSerializer(nested=True)
    policy_group = ACIInterfacePolicyGroupSerializer(
        nested=True, required=False, allow_null=True
    )

    class Meta:
        model = ACIInterfaceProfileSelector
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "interface_profile",
            "policy_group",
            "from_module",
            "from_port",
            "to_module",
            "to_port",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "description",
            "display",
            "from_module",
            "from_port",
            "id",
            "interface_profile",
            "name",
            "policy_group",
            "to_module",
            "to_port",
            "url",
        )


class ACISwitchProfileInterfaceProfileAttachmentSerializer(NetBoxModelSerializer):
    url = _url("aciswitchprofileinterfaceprofileattachment")
    switch_profile = ACISwitchProfileSerializer(nested=True)
    interface_profile = ACIInterfaceProfileSerializer(nested=True)

    class Meta:
        model = ACISwitchProfileInterfaceProfileAttachment
        fields = (
            "id",
            "url",
            "display",
            "switch_profile",
            "interface_profile",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "display",
            "id",
            "interface_profile",
            "switch_profile",
            "url",
        )
