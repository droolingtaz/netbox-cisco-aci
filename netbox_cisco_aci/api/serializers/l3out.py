"""DRF serializers for Phase 7 L3Out models."""

from dcim.api.serializers import InterfaceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.l3out import (
    ACIBGPPeer,
    ACIEIGRPInterfacePolicy,
    ACIExternalEPG,
    ACIExternalEPGSubnet,
    ACIL3Out,
    ACIL3OutInterface,
    ACIL3OutStaticRoute,
    ACIL3OutStaticRouteNextHop,
    ACILogicalInterfaceProfile,
    ACILogicalNode,
    ACILogicalNodeProfile,
    ACIOSPFInterfaceAttachment,
    ACIOSPFInterfacePolicy,
)
from .bindings import _AutoNameMixin, _clean_name
from .fabric import ACINodeSerializer
from .tenant import ACITenantSerializer, ACIVRFSerializer


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_cisco_aci-api:{view}-detail"
    )


# ---------------------------------------------------------------------------
# ACIL3Out
# ---------------------------------------------------------------------------


class ACIL3OutSerializer(NetBoxModelSerializer):
    url = _url("acil3out")
    aci_tenant = ACITenantSerializer(nested=True)
    aci_vrf = ACIVRFSerializer(nested=True)

    class Meta:
        model = ACIL3Out
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_vrf",
            "protocol_bgp",
            "protocol_ospf",
            "protocol_eigrp",
            "protocol_static",
            "target_dscp",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_tenant",
            "aci_vrf",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


# ---------------------------------------------------------------------------
# ACILogicalNodeProfile
# ---------------------------------------------------------------------------


class ACILogicalNodeProfileSerializer(NetBoxModelSerializer):
    url = _url("acilogicalnodeprofile")
    aci_l3out = ACIL3OutSerializer(nested=True)

    class Meta:
        model = ACILogicalNodeProfile
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_l3out",
            "target_dscp",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_l3out",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


# ---------------------------------------------------------------------------
# ACILogicalNode
# ---------------------------------------------------------------------------


class ACILogicalNodeSerializer(NetBoxModelSerializer):
    url = _url("acilogicalnode")
    aci_logical_node_profile = ACILogicalNodeProfileSerializer(nested=True)
    aci_node = ACINodeSerializer(nested=True)

    class Meta:
        model = ACILogicalNode
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_logical_node_profile",
            "aci_node",
            "router_id",
            "use_router_id_as_loopback",
            "loopback_address",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_logical_node_profile",
            "aci_node",
            "description",
            "display",
            "id",
            "name",
            "router_id",
            "url",
        )


# ---------------------------------------------------------------------------
# ACILogicalInterfaceProfile
# ---------------------------------------------------------------------------


class ACILogicalInterfaceProfileSerializer(NetBoxModelSerializer):
    url = _url("acilogicalinterfaceprofile")
    aci_logical_node_profile = ACILogicalNodeProfileSerializer(nested=True)

    class Meta:
        model = ACILogicalInterfaceProfile
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_logical_node_profile",
            "interface_type",
            "encap_vlan",
            "mtu",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_logical_node_profile",
            "description",
            "display",
            "id",
            "interface_type",
            "name",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIL3OutInterface  (auto-name)
# ---------------------------------------------------------------------------


class ACIL3OutInterfaceSerializer(_AutoNameMixin, NetBoxModelSerializer):
    url = _url("acil3outinterface")
    aci_logical_interface_profile = ACILogicalInterfaceProfileSerializer(nested=True)
    dcim_interface = InterfaceSerializer(nested=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=64)

    def _derive_name(self, attrs: dict) -> str:
        lip = attrs.get("aci_logical_interface_profile")
        iface = attrs.get("dcim_interface")
        if not (lip and iface):
            return ""
        return _clean_name(f"l3if_{getattr(lip, 'name', '')}_{iface}")

    class Meta:
        model = ACIL3OutInterface
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_logical_interface_profile",
            "dcim_interface",
            "ip_address",
            "secondary_ip_addresses",
            "mac_address",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_logical_interface_profile",
            "dcim_interface",
            "description",
            "display",
            "id",
            "ip_address",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIBGPPeer
# ---------------------------------------------------------------------------


class ACIBGPPeerSerializer(NetBoxModelSerializer):
    url = _url("acibgppeer")
    aci_logical_interface_profile = ACILogicalInterfaceProfileSerializer(
        nested=True, required=False, allow_null=True
    )
    aci_logical_node_profile = ACILogicalNodeProfileSerializer(
        nested=True, required=False, allow_null=True
    )

    class Meta:
        model = ACIBGPPeer
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_logical_interface_profile",
            "aci_logical_node_profile",
            "peer_address",
            "remote_asn",
            "local_asn",
            "ebgp_multihop_ttl",
            "password",
            "bgp_controls",
            "peer_controls",
            "address_family_controls",
            "private_asn_controls",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "description",
            "display",
            "id",
            "name",
            "peer_address",
            "remote_asn",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIOSPFInterfacePolicy
# ---------------------------------------------------------------------------


class ACIOSPFInterfacePolicySerializer(NetBoxModelSerializer):
    url = _url("aciospfinterfacepolicy")
    aci_tenant = ACITenantSerializer(nested=True)

    class Meta:
        model = ACIOSPFInterfacePolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "network_type",
            "priority",
            "cost",
            "hello_interval",
            "dead_interval",
            "retransmit_interval",
            "transmit_delay",
            "controls",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_tenant",
            "description",
            "display",
            "id",
            "name",
            "network_type",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIOSPFInterfaceAttachment
# ---------------------------------------------------------------------------


class ACIOSPFInterfaceAttachmentSerializer(NetBoxModelSerializer):
    url = _url("aciospfinterfaceattachment")
    aci_logical_interface_profile = ACILogicalInterfaceProfileSerializer(nested=True)
    aci_ospf_interface_policy = ACIOSPFInterfacePolicySerializer(nested=True)

    class Meta:
        model = ACIOSPFInterfaceAttachment
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_logical_interface_profile",
            "aci_ospf_interface_policy",
            "ospf_area_id",
            "ospf_area_type",
            "ospf_area_cost",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_logical_interface_profile",
            "aci_ospf_interface_policy",
            "description",
            "display",
            "id",
            "ospf_area_id",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIEIGRPInterfacePolicy
# ---------------------------------------------------------------------------


class ACIEIGRPInterfacePolicySerializer(NetBoxModelSerializer):
    url = _url("acieigrpinterfacepolicy")
    aci_tenant = ACITenantSerializer(nested=True)

    class Meta:
        model = ACIEIGRPInterfacePolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "hello_interval",
            "hold_interval",
            "bandwidth",
            "delay",
            "controls",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_tenant",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIExternalEPG
# ---------------------------------------------------------------------------


class ACIExternalEPGSerializer(NetBoxModelSerializer):
    url = _url("aciexternalepg")
    aci_l3out = ACIL3OutSerializer(nested=True)

    class Meta:
        model = ACIExternalEPG
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_l3out",
            "qos_class",
            "target_dscp",
            "preferred_group_member",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_l3out",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIExternalEPGSubnet
# ---------------------------------------------------------------------------


class ACIExternalEPGSubnetSerializer(NetBoxModelSerializer):
    url = _url("aciexternalepgsubnet")
    aci_external_epg = ACIExternalEPGSerializer(nested=True)

    class Meta:
        model = ACIExternalEPGSubnet
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_external_epg",
            "prefix",
            "scope_controls",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_external_epg",
            "description",
            "display",
            "id",
            "prefix",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIL3OutStaticRoute
# ---------------------------------------------------------------------------


class ACIL3OutStaticRouteSerializer(_AutoNameMixin, NetBoxModelSerializer):
    url = _url("acil3outstaticroute")
    aci_logical_node = ACILogicalNodeSerializer(nested=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=64)

    def _derive_name(self, attrs: dict) -> str:
        node = attrs.get("aci_logical_node")
        prefix = attrs.get("prefix", "")
        if not node:
            return ""
        return _clean_name(f"route_{getattr(node, 'name', '')}_{prefix}")

    class Meta:
        model = ACIL3OutStaticRoute
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_logical_node",
            "prefix",
            "preference",
            "track_policy",
            "route_controls",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_logical_node",
            "description",
            "display",
            "id",
            "preference",
            "prefix",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIL3OutStaticRouteNextHop
# ---------------------------------------------------------------------------


class ACIL3OutStaticRouteNextHopSerializer(_AutoNameMixin, NetBoxModelSerializer):
    url = _url("acil3outstaticroutenexthop")
    aci_static_route = ACIL3OutStaticRouteSerializer(nested=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=64)

    def _derive_name(self, attrs: dict) -> str:
        addr = attrs.get("nexthop_address") or "null"
        return _clean_name(f"nh_{addr}")

    class Meta:
        model = ACIL3OutStaticRouteNextHop
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_static_route",
            "nexthop_address",
            "nexthop_type",
            "preference",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_static_route",
            "description",
            "display",
            "id",
            "nexthop_address",
            "nexthop_type",
            "url",
        )
