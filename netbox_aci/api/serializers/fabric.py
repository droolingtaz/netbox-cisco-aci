"""DRF serializers for fabric-topology models."""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.fabric import ACIFabric, ACINode, ACIPod


class ACIFabricSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_aci-api:acifabric-detail"
    )
    pod_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ACIFabric
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "fabric_id",
            "description",
            "pod_count",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )


class ACIPodSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_aci-api:acipod-detail")
    aci_fabric = ACIFabricSerializer(read_only=True)
    aci_fabric_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIFabric.objects.all(),
        source="aci_fabric",
        write_only=True,
    )
    node_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ACIPod
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_fabric",
            "aci_fabric_id",
            "pod_id",
            "description",
            "node_count",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )


class ACINodeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_aci-api:acinode-detail"
    )
    aci_pod = ACIPodSerializer(read_only=True)
    aci_pod_id = serializers.PrimaryKeyRelatedField(
        queryset=ACIPod.objects.all(),
        source="aci_pod",
        write_only=True,
    )
    node_object_type = serializers.SlugRelatedField(
        slug_field="model",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = ACINode
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_pod",
            "aci_pod_id",
            "node_id",
            "role",
            "node_type",
            "serial_number",
            "pod_tep_pool",
            "firmware_version",
            "node_object_type",
            "node_object_id",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
