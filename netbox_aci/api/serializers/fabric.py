"""DRF serializers for fabric-topology models.

We use the NetBox idiom for FK fields: a single ``Serializer(nested=True)``
field that accepts a PK on write and emits a nested representation on
read. The earlier write-only ``<field>_id`` pattern was rejected by
NetBox's standard APIViewTestCase, which asserts that every key in the
create payload echoes back in the response.

``Meta.brief_fields`` is also declared so the ``?brief=True`` URL flag
works as NetBox's test cases expect.
"""

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
        brief_fields = ("id", "url", "display", "name", "fabric_id", "description")


class ACIPodSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_aci-api:acipod-detail")
    aci_fabric = ACIFabricSerializer(nested=True)
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
            "pod_id",
            "description",
            "node_count",
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
            "pod_id",
            "description",
        )


class ACINodeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_aci-api:acinode-detail"
    )
    aci_pod = ACIPodSerializer(nested=True)
    node_object_type = serializers.SlugRelatedField(
        slug_field="model", read_only=True, allow_null=True
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
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "aci_pod",
            "node_id",
            "role",
            "description",
        )
