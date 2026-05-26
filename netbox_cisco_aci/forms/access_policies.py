"""Forms for the six per-policy interface refs (Phase 4)."""

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
    EnabledDisabledChoices,
    LACPModeChoices,
    LinkLevelAutoNegChoices,
    LinkLevelFECChoices,
    LinkLevelSpeedChoices,
)
from ..models.access import (
    ACICDPInterfacePolicy,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
)
from ..models.fabric import ACIFabric


def _fabric_field():
    return DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))


def _fabric_filter_field():
    return DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )


# ---------------------------------------------------------------------------
# Link Level
# ---------------------------------------------------------------------------


class ACILinkLevelPolicyForm(NetBoxModelForm):
    aci_fabric = _fabric_field()

    class Meta:
        model = ACILinkLevelPolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "speed",
            "auto_negotiation",
            "link_debounce_interval_ms",
            "fec_mode",
            "description",
            "tags",
        )


class ACILinkLevelPolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACILinkLevelPolicy
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    speed = forms.ChoiceField(choices=LinkLevelSpeedChoices, required=False)
    auto_negotiation = forms.ChoiceField(choices=LinkLevelAutoNegChoices, required=False)
    fec_mode = forms.ChoiceField(choices=LinkLevelFECChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACILinkLevelPolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACILinkLevelPolicy
    aci_fabric_id = _fabric_filter_field()
    speed = forms.MultipleChoiceField(choices=LinkLevelSpeedChoices, required=False)
    auto_negotiation = forms.MultipleChoiceField(choices=LinkLevelAutoNegChoices, required=False)
    fec_mode = forms.MultipleChoiceField(choices=LinkLevelFECChoices, required=False)


class ACILinkLevelPolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACILinkLevelPolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "speed",
            "auto_negotiation",
            "link_debounce_interval_ms",
            "fec_mode",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# CDP
# ---------------------------------------------------------------------------


class ACICDPInterfacePolicyForm(NetBoxModelForm):
    aci_fabric = _fabric_field()

    class Meta:
        model = ACICDPInterfacePolicy
        fields = ("aci_fabric", "name", "name_alias", "admin_state", "description", "tags")


class ACICDPInterfacePolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACICDPInterfacePolicy
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    admin_state = forms.ChoiceField(choices=EnabledDisabledChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACICDPInterfacePolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACICDPInterfacePolicy
    aci_fabric_id = _fabric_filter_field()
    admin_state = forms.MultipleChoiceField(choices=EnabledDisabledChoices, required=False)


class ACICDPInterfacePolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACICDPInterfacePolicy
        fields = ("aci_fabric", "name", "name_alias", "admin_state", "description", "tags")


# ---------------------------------------------------------------------------
# LLDP
# ---------------------------------------------------------------------------


class ACILLDPInterfacePolicyForm(NetBoxModelForm):
    aci_fabric = _fabric_field()

    class Meta:
        model = ACILLDPInterfacePolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "receive_state",
            "transmit_state",
            "description",
            "tags",
        )


class ACILLDPInterfacePolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACILLDPInterfacePolicy
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    receive_state = forms.ChoiceField(choices=EnabledDisabledChoices, required=False)
    transmit_state = forms.ChoiceField(choices=EnabledDisabledChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACILLDPInterfacePolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACILLDPInterfacePolicy
    aci_fabric_id = _fabric_filter_field()
    receive_state = forms.MultipleChoiceField(choices=EnabledDisabledChoices, required=False)
    transmit_state = forms.MultipleChoiceField(choices=EnabledDisabledChoices, required=False)


class ACILLDPInterfacePolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACILLDPInterfacePolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "receive_state",
            "transmit_state",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# LACP
# ---------------------------------------------------------------------------


class ACILACPInterfacePolicyForm(NetBoxModelForm):
    aci_fabric = _fabric_field()

    class Meta:
        model = ACILACPInterfacePolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "mode",
            "min_links",
            "max_links",
            "control_fast_select_hot_standby",
            "control_graceful_convergence",
            "control_load_defer",
            "control_suspend_individual_port",
            "control_symmetric_hashing",
            "description",
            "tags",
        )


class ACILACPInterfacePolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACILACPInterfacePolicy
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    mode = forms.ChoiceField(choices=LACPModeChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACILACPInterfacePolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACILACPInterfacePolicy
    aci_fabric_id = _fabric_filter_field()
    mode = forms.MultipleChoiceField(choices=LACPModeChoices, required=False)


class ACILACPInterfacePolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACILACPInterfacePolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "mode",
            "min_links",
            "max_links",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# MCP
# ---------------------------------------------------------------------------


class ACIMCPInterfacePolicyForm(NetBoxModelForm):
    aci_fabric = _fabric_field()

    class Meta:
        model = ACIMCPInterfacePolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "admin_state",
            "strict_mode",
            "description",
            "tags",
        )


class ACIMCPInterfacePolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIMCPInterfacePolicy
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    admin_state = forms.ChoiceField(choices=EnabledDisabledChoices, required=False)
    strict_mode = forms.NullBooleanField(required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIMCPInterfacePolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACIMCPInterfacePolicy
    aci_fabric_id = _fabric_filter_field()
    admin_state = forms.MultipleChoiceField(choices=EnabledDisabledChoices, required=False)


class ACIMCPInterfacePolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACIMCPInterfacePolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "admin_state",
            "strict_mode",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# STP
# ---------------------------------------------------------------------------


class ACISTPInterfacePolicyForm(NetBoxModelForm):
    aci_fabric = _fabric_field()

    class Meta:
        model = ACISTPInterfacePolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "bpdu_filter",
            "bpdu_guard",
            "description",
            "tags",
        )


class ACISTPInterfacePolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISTPInterfacePolicy
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    bpdu_filter = forms.NullBooleanField(required=False)
    bpdu_guard = forms.NullBooleanField(required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACISTPInterfacePolicyFilterForm(NetBoxModelFilterSetForm):
    model = ACISTPInterfacePolicy
    aci_fabric_id = _fabric_filter_field()
    bpdu_filter = forms.NullBooleanField(required=False)
    bpdu_guard = forms.NullBooleanField(required=False)


class ACISTPInterfacePolicyImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACISTPInterfacePolicy
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "bpdu_filter",
            "bpdu_guard",
            "description",
            "tags",
        )
