"""Tables for Phase 6 binding models."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from ..models.bindings import (
    ACIDomainBinding,
    ACIInterfaceFabricMembership,
    ACIStaticPortBinding,
    ACIVPCBindingPair,
)


class ACIStaticPortBindingTable(NetBoxTable):
    aci_endpoint_group = tables.Column(linkify=True, verbose_name="EPG")
    dcim_interface = tables.Column(linkify=True, verbose_name="Interface")
    binding_type = ChoiceFieldColumn()
    mode = ChoiceFieldColumn()
    deployment_immediacy = ChoiceFieldColumn(verbose_name="Deploy")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acistaticportbinding_list")

    class Meta(NetBoxTable.Meta):
        model = ACIStaticPortBinding
        fields = (
            "pk",
            "id",
            "aci_endpoint_group",
            "dcim_interface",
            "binding_type",
            "encap_vlan",
            "mode",
            "primary_encap_vlan",
            "deployment_immediacy",
            "name",
            "description",
            "tags",
        )
        default_columns = (
            "aci_endpoint_group",
            "dcim_interface",
            "binding_type",
            "encap_vlan",
            "mode",
        )


class ACIVPCBindingPairTable(NetBoxTable):
    binding_a = tables.Column(linkify=True, verbose_name="Binding A")
    binding_b = tables.Column(linkify=True, verbose_name="Binding B")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acivpcbindingpair_list")

    class Meta(NetBoxTable.Meta):
        model = ACIVPCBindingPair
        fields = ("pk", "id", "binding_a", "binding_b", "name", "description", "tags")
        default_columns = ("binding_a", "binding_b", "name")


class ACIDomainBindingTable(NetBoxTable):
    aci_endpoint_group = tables.Column(linkify=True, verbose_name="EPG")
    aci_domain = tables.Column(linkify=True, verbose_name="Domain")
    deployment_immediacy = ChoiceFieldColumn(verbose_name="Deploy")
    resolution_immediacy = ChoiceFieldColumn(verbose_name="Resolve")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acidomainbinding_list")

    class Meta(NetBoxTable.Meta):
        model = ACIDomainBinding
        fields = (
            "pk",
            "id",
            "aci_endpoint_group",
            "aci_domain",
            "deployment_immediacy",
            "resolution_immediacy",
            "name",
            "description",
            "tags",
        )
        default_columns = (
            "aci_endpoint_group",
            "aci_domain",
            "deployment_immediacy",
            "resolution_immediacy",
        )


class ACIInterfaceFabricMembershipTable(NetBoxTable):
    dcim_interface = tables.Column(linkify=True, verbose_name="Interface")
    aci_node = tables.Column(linkify=True, verbose_name="ACI Node")
    interface_role = ChoiceFieldColumn(verbose_name="Role")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciinterfacefabricmembership_list")

    class Meta(NetBoxTable.Meta):
        model = ACIInterfaceFabricMembership
        fields = (
            "pk",
            "id",
            "dcim_interface",
            "aci_node",
            "interface_role",
            "name",
            "description",
            "tags",
        )
        default_columns = ("dcim_interface", "aci_node", "interface_role")
