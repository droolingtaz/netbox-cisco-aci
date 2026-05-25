"""Tables for access-policy models (Phase 3)."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from ..models.access import (
    ACIAAEP,
    ACIAAEPEPGMapping,
    ACIDomain,
    ACIVLANPool,
    ACIVLANPoolBlock,
)


class ACIVLANPoolTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    allocation_mode = ChoiceFieldColumn(verbose_name="Mode")
    block_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:acivlanpoolblock_list",
        url_params={"aci_vlan_pool_id": "pk"},
        verbose_name="Blocks",
    )
    domain_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:acidomain_list",
        url_params={"aci_vlan_pool_id": "pk"},
        verbose_name="Domains",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acivlanpool_list")

    class Meta(NetBoxTable.Meta):
        model = ACIVLANPool
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "allocation_mode",
            "block_count",
            "domain_count",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_fabric",
            "allocation_mode",
            "block_count",
            "domain_count",
        )


class ACIVLANPoolBlockTable(NetBoxTable):
    aci_vlan_pool = tables.Column(linkify=True, verbose_name="VLAN Pool")
    from_vlan = tables.Column(verbose_name="From")
    to_vlan = tables.Column(verbose_name="To")
    allocation_mode_override = ChoiceFieldColumn(verbose_name="Mode override")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acivlanpoolblock_list")

    class Meta(NetBoxTable.Meta):
        model = ACIVLANPoolBlock
        fields = (
            "pk",
            "id",
            "aci_vlan_pool",
            "name",
            "from_vlan",
            "to_vlan",
            "allocation_mode_override",
            "description",
            "tags",
        )
        default_columns = (
            "aci_vlan_pool",
            "from_vlan",
            "to_vlan",
            "allocation_mode_override",
        )


class ACIDomainTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    domain_type = ChoiceFieldColumn(verbose_name="Type")
    aci_vlan_pool = tables.Column(linkify=True, verbose_name="VLAN Pool")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acidomain_list")

    class Meta(NetBoxTable.Meta):
        model = ACIDomain
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "domain_type",
            "aci_vlan_pool",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_fabric", "domain_type", "aci_vlan_pool")


class ACIAAEPTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    enable_infra_vlan = columns.BooleanColumn(verbose_name="Infra VLAN")
    domain_count = tables.Column(verbose_name="Domains", empty_values=())
    epg_mapping_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:aciaaepepgmapping_list",
        url_params={"aci_aaep_id": "pk"},
        verbose_name="EPG mappings",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciaaep_list")

    class Meta(NetBoxTable.Meta):
        model = ACIAAEP
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "enable_infra_vlan",
            "domain_count",
            "epg_mapping_count",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_fabric",
            "enable_infra_vlan",
            "domain_count",
            "epg_mapping_count",
        )

    def render_domain_count(self, record):
        return record.domains.count()


class ACIAAEPEPGMappingTable(NetBoxTable):
    aci_aaep = tables.Column(linkify=True, verbose_name="AAEP")
    aci_endpoint_group = tables.Column(linkify=True, verbose_name="EPG")
    encap_vlan = tables.Column(verbose_name="Encap VLAN")
    mode = ChoiceFieldColumn(verbose_name="Mode")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciaaepepgmapping_list")

    class Meta(NetBoxTable.Meta):
        model = ACIAAEPEPGMapping
        fields = (
            "pk",
            "id",
            "aci_aaep",
            "aci_endpoint_group",
            "encap_vlan",
            "mode",
            "name",
            "description",
            "tags",
        )
        default_columns = ("aci_aaep", "aci_endpoint_group", "encap_vlan", "mode")
