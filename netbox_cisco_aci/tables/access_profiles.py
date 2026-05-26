"""Tables for Switch / Interface Profiles + selectors + attachments (Phase 4)."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from ..models.access import (
    ACIInterfaceProfile,
    ACIInterfaceProfileSelector,
    ACISwitchProfile,
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileSelector,
)


class ACISwitchProfileTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    selector_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:aciswitchprofileselector_list",
        url_params={"switch_profile_id": "pk"},
        verbose_name="Selectors",
    )
    attachment_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:aciswitchprofileinterfaceprofileattachment_list",
        url_params={"switch_profile_id": "pk"},
        verbose_name="Interface Profiles",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciswitchprofile_list")

    class Meta(NetBoxTable.Meta):
        model = ACISwitchProfile
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "selector_count",
            "attachment_count",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_fabric",
            "selector_count",
            "attachment_count",
        )


class ACISwitchProfileSelectorTable(NetBoxTable):
    name = tables.Column(linkify=True)
    switch_profile = tables.Column(linkify=True, verbose_name="Switch Profile")
    selector_type = ChoiceFieldColumn(verbose_name="Type")
    from_node_id = tables.Column(verbose_name="From node")
    to_node_id = tables.Column(verbose_name="To node")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciswitchprofileselector_list")

    class Meta(NetBoxTable.Meta):
        model = ACISwitchProfileSelector
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "switch_profile",
            "selector_type",
            "from_node_id",
            "to_node_id",
            "description",
            "tags",
        )
        default_columns = (
            "switch_profile",
            "selector_type",
            "from_node_id",
            "to_node_id",
        )


class ACIInterfaceProfileTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    selector_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:aciinterfaceprofileselector_list",
        url_params={"interface_profile_id": "pk"},
        verbose_name="Selectors",
    )
    attachment_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:aciswitchprofileinterfaceprofileattachment_list",
        url_params={"interface_profile_id": "pk"},
        verbose_name="Switch Profiles",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciinterfaceprofile_list")

    class Meta(NetBoxTable.Meta):
        model = ACIInterfaceProfile
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "selector_count",
            "attachment_count",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_fabric",
            "selector_count",
            "attachment_count",
        )


class ACIInterfaceProfileSelectorTable(NetBoxTable):
    name = tables.Column(linkify=True)
    interface_profile = tables.Column(linkify=True, verbose_name="Interface Profile")
    policy_group = tables.Column(linkify=True, verbose_name="Policy Group")
    from_module = tables.Column(verbose_name="From module")
    from_port = tables.Column(verbose_name="From port")
    to_module = tables.Column(verbose_name="To module")
    to_port = tables.Column(verbose_name="To port")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciinterfaceprofileselector_list")

    class Meta(NetBoxTable.Meta):
        model = ACIInterfaceProfileSelector
        fields = (
            "pk",
            "id",
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
        )
        default_columns = (
            "interface_profile",
            "policy_group",
            "from_module",
            "from_port",
            "to_module",
            "to_port",
        )


class ACISwitchProfileInterfaceProfileAttachmentTable(NetBoxTable):
    pk = columns.ToggleColumn()
    switch_profile = tables.Column(linkify=True, verbose_name="Switch Profile")
    interface_profile = tables.Column(linkify=True, verbose_name="Interface Profile")
    actions = columns.ActionsColumn(actions=("edit", "delete"))
    tags = columns.TagColumn(
        url_name="plugins:netbox_cisco_aci:aciswitchprofileinterfaceprofileattachment_list"
    )

    class Meta(NetBoxTable.Meta):
        model = ACISwitchProfileInterfaceProfileAttachment
        fields = ("pk", "id", "switch_profile", "interface_profile", "tags")
        default_columns = ("switch_profile", "interface_profile")
