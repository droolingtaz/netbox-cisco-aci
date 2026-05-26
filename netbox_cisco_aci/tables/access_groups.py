"""Table for the Interface Policy Group (Phase 4)."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from ..models.access import ACIInterfacePolicyGroup


class ACIInterfacePolicyGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    pg_type = ChoiceFieldColumn(verbose_name="Type")
    link_level_policy = tables.Column(linkify=True, verbose_name="Link Level")
    cdp_policy = tables.Column(linkify=True, verbose_name="CDP")
    lldp_policy = tables.Column(linkify=True, verbose_name="LLDP")
    lacp_policy = tables.Column(linkify=True, verbose_name="LACP")
    mcp_policy = tables.Column(linkify=True, verbose_name="MCP")
    stp_policy = tables.Column(linkify=True, verbose_name="STP")
    aaep = tables.Column(linkify=True, verbose_name="AAEP")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciinterfacepolicygroup_list")

    class Meta(NetBoxTable.Meta):
        model = ACIInterfacePolicyGroup
        fields = (
            "pk",
            "id",
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
        )
        default_columns = ("name", "aci_fabric", "pg_type", "lacp_policy", "aaep")
