"""Tables for Phase 7 L3Out models."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from ..models.l3out import (
    ACIBGPPeer,
    ACIEIGRPInterfacePolicy,
    ACIExternalEPG,
    ACIExternalEPGSubnet,
    ACIL3Out,
    ACIL3OutInterface,
    ACILogicalInterfaceProfile,
    ACILogicalNode,
    ACILogicalNodeProfile,
    ACIOSPFInterfaceAttachment,
    ACIOSPFInterfacePolicy,
)


class ACIL3OutTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    aci_vrf = tables.Column(linkify=True, verbose_name="VRF")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acil3out_list")

    class Meta(NetBoxTable.Meta):
        model = ACIL3Out
        fields = (
            "pk",
            "id",
            "name",
            "aci_tenant",
            "aci_vrf",
            "protocol_bgp",
            "protocol_ospf",
            "protocol_eigrp",
            "protocol_static",
            "target_dscp",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_tenant",
            "aci_vrf",
            "protocol_bgp",
            "protocol_ospf",
            "protocol_static",
        )


class ACILogicalNodeProfileTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_l3out = tables.Column(linkify=True, verbose_name="L3Out")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acilogicalnodeprofile_list")

    class Meta(NetBoxTable.Meta):
        model = ACILogicalNodeProfile
        fields = (
            "pk",
            "id",
            "name",
            "aci_l3out",
            "target_dscp",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_l3out", "description")


class ACILogicalNodeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_logical_node_profile = tables.Column(linkify=True, verbose_name="LNP")
    aci_node = tables.Column(linkify=True, verbose_name="Node")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acilogicalnode_list")

    class Meta(NetBoxTable.Meta):
        model = ACILogicalNode
        fields = (
            "pk",
            "id",
            "name",
            "aci_logical_node_profile",
            "aci_node",
            "router_id",
            "use_router_id_as_loopback",
            "loopback_address",
            "description",
            "tags",
        )
        default_columns = ("aci_logical_node_profile", "aci_node", "router_id")


class ACILogicalInterfaceProfileTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_logical_node_profile = tables.Column(linkify=True, verbose_name="LNP")
    interface_type = ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acilogicalinterfaceprofile_list")

    class Meta(NetBoxTable.Meta):
        model = ACILogicalInterfaceProfile
        fields = (
            "pk",
            "id",
            "name",
            "aci_logical_node_profile",
            "interface_type",
            "encap_vlan",
            "mtu",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_logical_node_profile",
            "interface_type",
            "encap_vlan",
        )


class ACIL3OutInterfaceTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_logical_interface_profile = tables.Column(linkify=True, verbose_name="LIP")
    dcim_interface = tables.Column(linkify=True, verbose_name="Interface")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acil3outinterface_list")

    class Meta(NetBoxTable.Meta):
        model = ACIL3OutInterface
        fields = (
            "pk",
            "id",
            "name",
            "aci_logical_interface_profile",
            "dcim_interface",
            "ip_address",
            "mac_address",
            "description",
            "tags",
        )
        default_columns = (
            "aci_logical_interface_profile",
            "dcim_interface",
            "ip_address",
        )


class ACIBGPPeerTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_logical_interface_profile = tables.Column(linkify=True, verbose_name="LIP")
    aci_logical_node_profile = tables.Column(linkify=True, verbose_name="LNP")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acibgppeer_list")

    class Meta(NetBoxTable.Meta):
        model = ACIBGPPeer
        fields = (
            "pk",
            "id",
            "name",
            "aci_logical_interface_profile",
            "aci_logical_node_profile",
            "peer_address",
            "remote_asn",
            "local_asn",
            "ebgp_multihop_ttl",
            "description",
            "tags",
        )
        default_columns = (
            "peer_address",
            "remote_asn",
            "aci_logical_interface_profile",
            "aci_logical_node_profile",
        )


class ACIOSPFInterfacePolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    network_type = ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciospfinterfacepolicy_list")

    class Meta(NetBoxTable.Meta):
        model = ACIOSPFInterfacePolicy
        fields = (
            "pk",
            "id",
            "name",
            "aci_tenant",
            "network_type",
            "priority",
            "cost",
            "hello_interval",
            "dead_interval",
            "retransmit_interval",
            "transmit_delay",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_tenant",
            "network_type",
            "priority",
            "hello_interval",
        )


class ACIOSPFInterfaceAttachmentTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_logical_interface_profile = tables.Column(linkify=True, verbose_name="LIP")
    aci_ospf_interface_policy = tables.Column(linkify=True, verbose_name="OSPF Policy")
    ospf_area_type = ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciospfinterfaceattachment_list")

    class Meta(NetBoxTable.Meta):
        model = ACIOSPFInterfaceAttachment
        fields = (
            "pk",
            "id",
            "name",
            "aci_logical_interface_profile",
            "aci_ospf_interface_policy",
            "ospf_area_id",
            "ospf_area_type",
            "ospf_area_cost",
            "description",
            "tags",
        )
        default_columns = (
            "aci_logical_interface_profile",
            "aci_ospf_interface_policy",
            "ospf_area_id",
            "ospf_area_type",
        )


class ACIEIGRPInterfacePolicyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acieigrpinterfacepolicy_list")

    class Meta(NetBoxTable.Meta):
        model = ACIEIGRPInterfacePolicy
        fields = (
            "pk",
            "id",
            "name",
            "aci_tenant",
            "hello_interval",
            "hold_interval",
            "bandwidth",
            "delay",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_tenant", "hello_interval", "hold_interval")


class ACIExternalEPGTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_l3out = tables.Column(linkify=True, verbose_name="L3Out")
    qos_class = ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciexternalepg_list")

    class Meta(NetBoxTable.Meta):
        model = ACIExternalEPG
        fields = (
            "pk",
            "id",
            "name",
            "aci_l3out",
            "qos_class",
            "target_dscp",
            "preferred_group_member",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_l3out", "preferred_group_member")


class ACIExternalEPGSubnetTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_external_epg = tables.Column(linkify=True, verbose_name="External EPG")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:aciexternalepgsubnet_list")

    class Meta(NetBoxTable.Meta):
        model = ACIExternalEPGSubnet
        fields = (
            "pk",
            "id",
            "name",
            "aci_external_epg",
            "prefix",
            "description",
            "tags",
        )
        default_columns = ("aci_external_epg", "prefix")
