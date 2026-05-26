"""Tables for the six per-policy interface refs (Phase 4)."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from ..models.access import (
    ACICDPInterfacePolicy,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
)


class ACILinkLevelPolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    speed = ChoiceFieldColumn()
    auto_negotiation = ChoiceFieldColumn(verbose_name="Auto-neg")
    fec_mode = ChoiceFieldColumn(verbose_name="FEC")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acilinklevelpolicy_list")

    class Meta(NetBoxTable.Meta):
        model = ACILinkLevelPolicy
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "speed",
            "auto_negotiation",
            "link_debounce_interval_ms",
            "fec_mode",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_fabric", "speed", "auto_negotiation", "fec_mode")


class ACICDPInterfacePolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    admin_state = ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acicdpinterfacepolicy_list")

    class Meta(NetBoxTable.Meta):
        model = ACICDPInterfacePolicy
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "admin_state",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_fabric", "admin_state")


class ACILLDPInterfacePolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    receive_state = ChoiceFieldColumn(verbose_name="Receive")
    transmit_state = ChoiceFieldColumn(verbose_name="Transmit")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acilldpinterfacepolicy_list")

    class Meta(NetBoxTable.Meta):
        model = ACILLDPInterfacePolicy
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "receive_state",
            "transmit_state",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_fabric", "receive_state", "transmit_state")


class ACILACPInterfacePolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    mode = ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acilacpinterfacepolicy_list")

    class Meta(NetBoxTable.Meta):
        model = ACILACPInterfacePolicy
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "mode",
            "min_links",
            "max_links",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_fabric", "mode", "min_links", "max_links")


class ACIMCPInterfacePolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    admin_state = ChoiceFieldColumn()
    strict_mode = columns.BooleanColumn(verbose_name="Strict")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acimcpinterfacepolicy_list")

    class Meta(NetBoxTable.Meta):
        model = ACIMCPInterfacePolicy
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "admin_state",
            "strict_mode",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_fabric", "admin_state", "strict_mode")


class ACISTPInterfacePolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    bpdu_filter = columns.BooleanColumn(verbose_name="BPDU Filter")
    bpdu_guard = columns.BooleanColumn(verbose_name="BPDU Guard")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acistpinterfacepolicy_list")

    class Meta(NetBoxTable.Meta):
        model = ACISTPInterfacePolicy
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "bpdu_filter",
            "bpdu_guard",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_fabric", "bpdu_filter", "bpdu_guard")
