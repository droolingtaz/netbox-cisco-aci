"""Forms for Phase 7 L3Out models."""

from dcim.models import Interface
from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField

from ..choices import (
    L3OutInterfaceTypeChoices,
    OSPFAreaTypeChoices,
    OSPFNetworkTypeChoices,
    QualityOfServiceClassChoices,
)
from ..models.fabric import ACINode
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
from ..models.tenant import ACIVRF, ACITenant

_TOKEN_LIST_HELP = _("JSON list of string tokens.")


# ---------------------------------------------------------------------------
# ACIL3Out
# ---------------------------------------------------------------------------


class ACIL3OutForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))
    aci_vrf = DynamicModelChoiceField(queryset=ACIVRF.objects.all(), label=_("VRF"))

    class Meta:
        model = ACIL3Out
        fields = (
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
        )


class ACIL3OutBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIL3Out
    target_dscp = forms.CharField(max_length=32, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "target_dscp")


class ACIL3OutFilterForm(NetBoxModelFilterSetForm):
    model = ACIL3Out
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )
    aci_vrf_id = DynamicModelMultipleChoiceField(
        queryset=ACIVRF.objects.all(), required=False, label=_("VRF")
    )
    protocol_bgp = forms.NullBooleanField(required=False)
    protocol_ospf = forms.NullBooleanField(required=False)
    protocol_eigrp = forms.NullBooleanField(required=False)
    protocol_static = forms.NullBooleanField(required=False)


class ACIL3OutImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")
    aci_vrf = forms.ModelChoiceField(queryset=ACIVRF.objects.all(), to_field_name="name")

    class Meta:
        model = ACIL3Out
        fields = (
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
        )


# ---------------------------------------------------------------------------
# ACILogicalNodeProfile
# ---------------------------------------------------------------------------


class ACILogicalNodeProfileForm(NetBoxModelForm):
    aci_l3out = DynamicModelChoiceField(queryset=ACIL3Out.objects.all(), label=_("L3Out"))

    class Meta:
        model = ACILogicalNodeProfile
        fields = (
            "name",
            "name_alias",
            "aci_l3out",
            "target_dscp",
            "description",
            "tags",
        )


class ACILogicalNodeProfileBulkEditForm(NetBoxModelBulkEditForm):
    model = ACILogicalNodeProfile
    target_dscp = forms.CharField(max_length=32, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "target_dscp")


class ACILogicalNodeProfileFilterForm(NetBoxModelFilterSetForm):
    model = ACILogicalNodeProfile
    aci_l3out_id = DynamicModelMultipleChoiceField(
        queryset=ACIL3Out.objects.all(), required=False, label=_("L3Out")
    )


class ACILogicalNodeProfileImportForm(NetBoxModelImportForm):
    aci_l3out = forms.ModelChoiceField(queryset=ACIL3Out.objects.all(), to_field_name="name")

    class Meta:
        model = ACILogicalNodeProfile
        fields = ("name", "name_alias", "aci_l3out", "target_dscp", "description", "tags")


# ---------------------------------------------------------------------------
# ACILogicalNode
# ---------------------------------------------------------------------------


class ACILogicalNodeForm(NetBoxModelForm):
    aci_logical_node_profile = DynamicModelChoiceField(
        queryset=ACILogicalNodeProfile.objects.all(), label=_("Logical Node Profile")
    )
    aci_node = DynamicModelChoiceField(queryset=ACINode.objects.all(), label=_("Node"))

    class Meta:
        model = ACILogicalNode
        fields = (
            "name",
            "name_alias",
            "aci_logical_node_profile",
            "aci_node",
            "router_id",
            "use_router_id_as_loopback",
            "loopback_address",
            "description",
            "tags",
        )


class ACILogicalNodeBulkEditForm(NetBoxModelBulkEditForm):
    model = ACILogicalNode
    use_router_id_as_loopback = forms.NullBooleanField(required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "loopback_address")


class ACILogicalNodeFilterForm(NetBoxModelFilterSetForm):
    model = ACILogicalNode
    aci_logical_node_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACILogicalNodeProfile.objects.all(), required=False, label=_("LNP")
    )
    aci_node_id = DynamicModelMultipleChoiceField(
        queryset=ACINode.objects.all(), required=False, label=_("Node")
    )


class ACILogicalNodeImportForm(NetBoxModelImportForm):
    aci_logical_node_profile = forms.ModelChoiceField(
        queryset=ACILogicalNodeProfile.objects.all(), to_field_name="name"
    )
    aci_node = forms.ModelChoiceField(queryset=ACINode.objects.all(), to_field_name="name")

    class Meta:
        model = ACILogicalNode
        fields = (
            "name",
            "name_alias",
            "aci_logical_node_profile",
            "aci_node",
            "router_id",
            "use_router_id_as_loopback",
            "loopback_address",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACILogicalInterfaceProfile
# ---------------------------------------------------------------------------


class ACILogicalInterfaceProfileForm(NetBoxModelForm):
    aci_logical_node_profile = DynamicModelChoiceField(
        queryset=ACILogicalNodeProfile.objects.all(), label=_("LNP")
    )

    class Meta:
        model = ACILogicalInterfaceProfile
        fields = (
            "name",
            "name_alias",
            "aci_logical_node_profile",
            "interface_type",
            "encap_vlan",
            "mtu",
            "description",
            "tags",
        )


class ACILogicalInterfaceProfileBulkEditForm(NetBoxModelBulkEditForm):
    model = ACILogicalInterfaceProfile
    interface_type = forms.ChoiceField(choices=L3OutInterfaceTypeChoices, required=False)
    mtu = forms.IntegerField(required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "encap_vlan")


class ACILogicalInterfaceProfileFilterForm(NetBoxModelFilterSetForm):
    model = ACILogicalInterfaceProfile
    aci_logical_node_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACILogicalNodeProfile.objects.all(), required=False, label=_("LNP")
    )
    interface_type = forms.MultipleChoiceField(choices=L3OutInterfaceTypeChoices, required=False)


class ACILogicalInterfaceProfileImportForm(NetBoxModelImportForm):
    aci_logical_node_profile = forms.ModelChoiceField(
        queryset=ACILogicalNodeProfile.objects.all(), to_field_name="name"
    )
    interface_type = forms.ChoiceField(choices=L3OutInterfaceTypeChoices, required=False)

    class Meta:
        model = ACILogicalInterfaceProfile
        fields = (
            "name",
            "name_alias",
            "aci_logical_node_profile",
            "interface_type",
            "encap_vlan",
            "mtu",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIL3OutInterface
# ---------------------------------------------------------------------------


class ACIL3OutInterfaceForm(NetBoxModelForm):
    aci_logical_interface_profile = DynamicModelChoiceField(
        queryset=ACILogicalInterfaceProfile.objects.all(), label=_("LIP")
    )
    dcim_interface = DynamicModelChoiceField(queryset=Interface.objects.all(), label=_("Interface"))
    secondary_ip_addresses = forms.JSONField(
        required=False, initial=list, help_text=_("JSON list of IP/CIDR strings.")
    )

    class Meta:
        model = ACIL3OutInterface
        fields = (
            "name",
            "name_alias",
            "aci_logical_interface_profile",
            "dcim_interface",
            "ip_address",
            "secondary_ip_addresses",
            "mac_address",
            "description",
            "tags",
        )


class ACIL3OutInterfaceBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIL3OutInterface
    mac_address = forms.CharField(max_length=17, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "mac_address")


class ACIL3OutInterfaceFilterForm(NetBoxModelFilterSetForm):
    model = ACIL3OutInterface
    aci_logical_interface_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACILogicalInterfaceProfile.objects.all(), required=False, label=_("LIP")
    )
    dcim_interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(), required=False, label=_("Interface")
    )


class ACIL3OutInterfaceImportForm(NetBoxModelImportForm):
    aci_logical_interface_profile = forms.ModelChoiceField(
        queryset=ACILogicalInterfaceProfile.objects.all(), to_field_name="name"
    )
    dcim_interface = forms.ModelChoiceField(queryset=Interface.objects.all())

    class Meta:
        model = ACIL3OutInterface
        fields = (
            "name",
            "name_alias",
            "aci_logical_interface_profile",
            "dcim_interface",
            "ip_address",
            "mac_address",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIBGPPeer
# ---------------------------------------------------------------------------


class ACIBGPPeerForm(NetBoxModelForm):
    aci_logical_interface_profile = DynamicModelChoiceField(
        queryset=ACILogicalInterfaceProfile.objects.all(), required=False, label=_("LIP")
    )
    aci_logical_node_profile = DynamicModelChoiceField(
        queryset=ACILogicalNodeProfile.objects.all(), required=False, label=_("LNP")
    )
    bgp_controls = forms.JSONField(required=False, initial=list, help_text=_TOKEN_LIST_HELP)
    peer_controls = forms.JSONField(required=False, initial=list, help_text=_TOKEN_LIST_HELP)
    address_family_controls = forms.JSONField(
        required=False, initial=list, help_text=_TOKEN_LIST_HELP
    )
    private_asn_controls = forms.JSONField(required=False, initial=list, help_text=_TOKEN_LIST_HELP)

    class Meta:
        model = ACIBGPPeer
        fields = (
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
        )


class ACIBGPPeerBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIBGPPeer
    ebgp_multihop_ttl = forms.IntegerField(required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "password")


class ACIBGPPeerFilterForm(NetBoxModelFilterSetForm):
    model = ACIBGPPeer
    aci_logical_interface_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACILogicalInterfaceProfile.objects.all(), required=False, label=_("LIP")
    )
    aci_logical_node_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACILogicalNodeProfile.objects.all(), required=False, label=_("LNP")
    )


class ACIBGPPeerImportForm(NetBoxModelImportForm):
    aci_logical_interface_profile = forms.ModelChoiceField(
        queryset=ACILogicalInterfaceProfile.objects.all(), required=False, to_field_name="name"
    )
    aci_logical_node_profile = forms.ModelChoiceField(
        queryset=ACILogicalNodeProfile.objects.all(), required=False, to_field_name="name"
    )

    class Meta:
        model = ACIBGPPeer
        fields = (
            "name",
            "name_alias",
            "aci_logical_interface_profile",
            "aci_logical_node_profile",
            "peer_address",
            "remote_asn",
            "local_asn",
            "ebgp_multihop_ttl",
            "password",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIOSPFInterfacePolicy
# ---------------------------------------------------------------------------


class ACIOSPFInterfacePolicyForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))
    controls = forms.JSONField(required=False, initial=list, help_text=_TOKEN_LIST_HELP)

    class Meta:
        model = ACIOSPFInterfacePolicy
        fields = (
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
        )


class ACIOSPFInterfacePolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIOSPFInterfacePolicy
    network_type = forms.ChoiceField(choices=OSPFNetworkTypeChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIOSPFInterfacePolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACIOSPFInterfacePolicy
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )
    network_type = forms.MultipleChoiceField(choices=OSPFNetworkTypeChoices, required=False)


class ACIOSPFInterfacePolicyImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")
    network_type = forms.ChoiceField(choices=OSPFNetworkTypeChoices, required=False)

    class Meta:
        model = ACIOSPFInterfacePolicy
        fields = (
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
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIOSPFInterfaceAttachment
# ---------------------------------------------------------------------------


class ACIOSPFInterfaceAttachmentForm(NetBoxModelForm):
    aci_logical_interface_profile = DynamicModelChoiceField(
        queryset=ACILogicalInterfaceProfile.objects.all(), label=_("LIP")
    )
    aci_ospf_interface_policy = DynamicModelChoiceField(
        queryset=ACIOSPFInterfacePolicy.objects.all(), label=_("OSPF Policy")
    )

    class Meta:
        model = ACIOSPFInterfaceAttachment
        fields = (
            "name",
            "name_alias",
            "aci_logical_interface_profile",
            "aci_ospf_interface_policy",
            "ospf_area_id",
            "ospf_area_type",
            "ospf_area_cost",
            "description",
            "tags",
        )


class ACIOSPFInterfaceAttachmentBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIOSPFInterfaceAttachment
    ospf_area_type = forms.ChoiceField(choices=OSPFAreaTypeChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIOSPFInterfaceAttachmentFilterForm(NetBoxModelFilterSetForm):
    model = ACIOSPFInterfaceAttachment
    aci_logical_interface_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACILogicalInterfaceProfile.objects.all(), required=False, label=_("LIP")
    )
    aci_ospf_interface_policy_id = DynamicModelMultipleChoiceField(
        queryset=ACIOSPFInterfacePolicy.objects.all(), required=False, label=_("OSPF Policy")
    )
    ospf_area_type = forms.MultipleChoiceField(choices=OSPFAreaTypeChoices, required=False)


class ACIOSPFInterfaceAttachmentImportForm(NetBoxModelImportForm):
    aci_logical_interface_profile = forms.ModelChoiceField(
        queryset=ACILogicalInterfaceProfile.objects.all(), to_field_name="name"
    )
    aci_ospf_interface_policy = forms.ModelChoiceField(
        queryset=ACIOSPFInterfacePolicy.objects.all(), to_field_name="name"
    )
    ospf_area_type = forms.ChoiceField(choices=OSPFAreaTypeChoices, required=False)

    class Meta:
        model = ACIOSPFInterfaceAttachment
        fields = (
            "name",
            "name_alias",
            "aci_logical_interface_profile",
            "aci_ospf_interface_policy",
            "ospf_area_id",
            "ospf_area_type",
            "ospf_area_cost",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIEIGRPInterfacePolicy
# ---------------------------------------------------------------------------


class ACIEIGRPInterfacePolicyForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))
    controls = forms.JSONField(required=False, initial=list, help_text=_TOKEN_LIST_HELP)

    class Meta:
        model = ACIEIGRPInterfacePolicy
        fields = (
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
        )


class ACIEIGRPInterfacePolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIEIGRPInterfacePolicy
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "bandwidth", "delay")


class ACIEIGRPInterfacePolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACIEIGRPInterfacePolicy
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )


class ACIEIGRPInterfacePolicyImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")

    class Meta:
        model = ACIEIGRPInterfacePolicy
        fields = (
            "name",
            "name_alias",
            "aci_tenant",
            "hello_interval",
            "hold_interval",
            "bandwidth",
            "delay",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIExternalEPG
# ---------------------------------------------------------------------------


class ACIExternalEPGForm(NetBoxModelForm):
    aci_l3out = DynamicModelChoiceField(queryset=ACIL3Out.objects.all(), label=_("L3Out"))

    class Meta:
        model = ACIExternalEPG
        fields = (
            "name",
            "name_alias",
            "aci_l3out",
            "qos_class",
            "target_dscp",
            "preferred_group_member",
            "description",
            "tags",
        )


class ACIExternalEPGBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIExternalEPG
    qos_class = forms.ChoiceField(choices=QualityOfServiceClassChoices, required=False)
    target_dscp = forms.CharField(max_length=32, required=False)
    preferred_group_member = forms.NullBooleanField(required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "qos_class", "target_dscp")


class ACIExternalEPGFilterForm(NetBoxModelFilterSetForm):
    model = ACIExternalEPG
    aci_l3out_id = DynamicModelMultipleChoiceField(
        queryset=ACIL3Out.objects.all(), required=False, label=_("L3Out")
    )
    qos_class = forms.MultipleChoiceField(choices=QualityOfServiceClassChoices, required=False)


class ACIExternalEPGImportForm(NetBoxModelImportForm):
    aci_l3out = forms.ModelChoiceField(queryset=ACIL3Out.objects.all(), to_field_name="name")
    qos_class = forms.ChoiceField(choices=QualityOfServiceClassChoices, required=False)

    class Meta:
        model = ACIExternalEPG
        fields = (
            "name",
            "name_alias",
            "aci_l3out",
            "qos_class",
            "target_dscp",
            "preferred_group_member",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIExternalEPGSubnet
# ---------------------------------------------------------------------------


class ACIExternalEPGSubnetForm(NetBoxModelForm):
    aci_external_epg = DynamicModelChoiceField(
        queryset=ACIExternalEPG.objects.all(), label=_("External EPG")
    )
    scope_controls = forms.JSONField(required=False, initial=list, help_text=_TOKEN_LIST_HELP)

    class Meta:
        model = ACIExternalEPGSubnet
        fields = (
            "name",
            "name_alias",
            "aci_external_epg",
            "prefix",
            "scope_controls",
            "description",
            "tags",
        )


class ACIExternalEPGSubnetBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIExternalEPGSubnet
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIExternalEPGSubnetFilterForm(NetBoxModelFilterSetForm):
    model = ACIExternalEPGSubnet
    aci_external_epg_id = DynamicModelMultipleChoiceField(
        queryset=ACIExternalEPG.objects.all(), required=False, label=_("External EPG")
    )


class ACIExternalEPGSubnetImportForm(NetBoxModelImportForm):
    aci_external_epg = forms.ModelChoiceField(
        queryset=ACIExternalEPG.objects.all(), to_field_name="name"
    )

    class Meta:
        model = ACIExternalEPGSubnet
        fields = (
            "name",
            "name_alias",
            "aci_external_epg",
            "prefix",
            "description",
            "tags",
        )
