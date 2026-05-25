"""Tables for fabric-topology models."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from ..models.fabric import ACIFabric, ACINode, ACIPod


class ACIFabricTable(NetBoxTable):
    name = tables.Column(linkify=True)
    fabric_id = tables.Column(verbose_name="Fabric ID")
    pod_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:acipod_list",
        url_params={"aci_fabric_id": "pk"},
        verbose_name="Pods",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acifabric_list")

    class Meta(NetBoxTable.Meta):
        model = ACIFabric
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "fabric_id",
            "pod_count",
            "description",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("name", "fabric_id", "pod_count", "description")


class ACIPodTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    pod_id = tables.Column(verbose_name="Pod ID")
    node_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:acinode_list",
        url_params={"aci_pod_id": "pk"},
        verbose_name="Nodes",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acipod_list")

    class Meta(NetBoxTable.Meta):
        model = ACIPod
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "pod_id",
            "node_count",
            "description",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = ("name", "aci_fabric", "pod_id", "node_count", "description")


class ACINodeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_pod = tables.Column(linkify=True, verbose_name="Pod")
    node_id = tables.Column(verbose_name="Node ID")
    role = ChoiceFieldColumn()
    node_type = ChoiceFieldColumn(verbose_name="Type")
    node_object = tables.Column(linkify=True, verbose_name="Linked object")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acinode_list")

    class Meta(NetBoxTable.Meta):
        model = ACINode
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_pod",
            "node_id",
            "role",
            "node_type",
            "serial_number",
            "pod_tep_pool",
            "firmware_version",
            "node_object",
            "description",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = (
            "name",
            "aci_pod",
            "node_id",
            "role",
            "node_type",
            "serial_number",
            "node_object",
        )
