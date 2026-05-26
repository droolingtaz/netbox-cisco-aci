"""FilterSets for Phase 7 L3Out models."""

import django_filters
from dcim.models import Interface
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from ..choices import (
    L3OutInterfaceTypeChoices,
    OSPFAreaTypeChoices,
    OSPFNetworkTypeChoices,
    QualityOfServiceClassChoices,
    StaticRouteNextHopTypeChoices,
)
from ..models.fabric import ACINode
from ..models.l3out import (
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
from ..models.tenant import ACIVRF, ACITenant


class _SearchMixin:
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(name_alias__icontains=value)
            | Q(description__icontains=value)
        )


class ACIL3OutFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    aci_vrf_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIVRF.objects.all(), field_name="aci_vrf", label="VRF (ID)"
    )
    protocol_bgp = django_filters.BooleanFilter()
    protocol_ospf = django_filters.BooleanFilter()
    protocol_eigrp = django_filters.BooleanFilter()
    protocol_static = django_filters.BooleanFilter()

    class Meta:
        model = ACIL3Out
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "protocol_bgp",
            "protocol_ospf",
            "protocol_eigrp",
            "protocol_static",
            "target_dscp",
        )


class ACILogicalNodeProfileFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_l3out_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIL3Out.objects.all(), field_name="aci_l3out", label="L3Out (ID)"
    )

    class Meta:
        model = ACILogicalNodeProfile
        fields = ("id", "name", "name_alias", "description", "target_dscp")


class ACILogicalNodeFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_logical_node_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACILogicalNodeProfile.objects.all(),
        field_name="aci_logical_node_profile",
        label="LNP (ID)",
    )
    aci_node_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACINode.objects.all(), field_name="aci_node", label="Node (ID)"
    )

    class Meta:
        model = ACILogicalNode
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "router_id",
            "use_router_id_as_loopback",
        )


class ACILogicalInterfaceProfileFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_logical_node_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACILogicalNodeProfile.objects.all(),
        field_name="aci_logical_node_profile",
        label="LNP (ID)",
    )
    interface_type = django_filters.MultipleChoiceFilter(choices=L3OutInterfaceTypeChoices)

    class Meta:
        model = ACILogicalInterfaceProfile
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "interface_type",
            "encap_vlan",
            "mtu",
        )


class ACIL3OutInterfaceFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_logical_interface_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACILogicalInterfaceProfile.objects.all(),
        field_name="aci_logical_interface_profile",
        label="LIP (ID)",
    )
    dcim_interface_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Interface.objects.all(),
        field_name="dcim_interface",
        label="Interface (ID)",
    )

    class Meta:
        model = ACIL3OutInterface
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "ip_address",
            "mac_address",
        )


class ACIBGPPeerFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_logical_interface_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACILogicalInterfaceProfile.objects.all(),
        field_name="aci_logical_interface_profile",
        label="LIP (ID)",
    )
    aci_logical_node_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACILogicalNodeProfile.objects.all(),
        field_name="aci_logical_node_profile",
        label="LNP (ID)",
    )
    remote_asn = django_filters.NumberFilter()
    local_asn = django_filters.NumberFilter()

    class Meta:
        model = ACIBGPPeer
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "peer_address",
            "remote_asn",
            "local_asn",
            "ebgp_multihop_ttl",
        )


class ACIOSPFInterfacePolicyFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    network_type = django_filters.MultipleChoiceFilter(choices=OSPFNetworkTypeChoices)

    class Meta:
        model = ACIOSPFInterfacePolicy
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "network_type",
            "priority",
            "cost",
            "hello_interval",
            "dead_interval",
        )


class ACIOSPFInterfaceAttachmentFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_logical_interface_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACILogicalInterfaceProfile.objects.all(),
        field_name="aci_logical_interface_profile",
        label="LIP (ID)",
    )
    aci_ospf_interface_policy_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIOSPFInterfacePolicy.objects.all(),
        field_name="aci_ospf_interface_policy",
        label="OSPF policy (ID)",
    )
    ospf_area_type = django_filters.MultipleChoiceFilter(choices=OSPFAreaTypeChoices)

    class Meta:
        model = ACIOSPFInterfaceAttachment
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "ospf_area_id",
            "ospf_area_type",
            "ospf_area_cost",
        )


class ACIEIGRPInterfacePolicyFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )

    class Meta:
        model = ACIEIGRPInterfacePolicy
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "hello_interval",
            "hold_interval",
        )


class ACIExternalEPGFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_l3out_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIL3Out.objects.all(), field_name="aci_l3out", label="L3Out (ID)"
    )
    qos_class = django_filters.MultipleChoiceFilter(choices=QualityOfServiceClassChoices)

    class Meta:
        model = ACIExternalEPG
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "qos_class",
            "target_dscp",
            "preferred_group_member",
        )


class ACIExternalEPGSubnetFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_external_epg_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIExternalEPG.objects.all(),
        field_name="aci_external_epg",
        label="External EPG (ID)",
    )

    class Meta:
        model = ACIExternalEPGSubnet
        fields = ("id", "name", "name_alias", "description", "prefix")


class ACIL3OutStaticRouteFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_logical_node_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACILogicalNode.objects.all(),
        field_name="aci_logical_node",
        label="Logical Node (ID)",
    )

    class Meta:
        model = ACIL3OutStaticRoute
        fields = ("id", "name", "name_alias", "description", "prefix", "preference")


class ACIL3OutStaticRouteNextHopFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_static_route_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIL3OutStaticRoute.objects.all(),
        field_name="aci_static_route",
        label="Static Route (ID)",
    )
    nexthop_type = django_filters.MultipleChoiceFilter(choices=StaticRouteNextHopTypeChoices)

    class Meta:
        model = ACIL3OutStaticRouteNextHop
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "nexthop_address",
            "nexthop_type",
            "preference",
        )
