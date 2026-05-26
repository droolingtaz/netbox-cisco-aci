"""Forms for the Interface Policy Group (Phase 4)."""

from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField

from ..choices import InterfacePolicyGroupTypeChoices
from ..models.access import (
    ACIAAEP,
    ACICDPInterfacePolicy,
    ACIInterfacePolicyGroup,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
)
from ..models.fabric import ACIFabric


class ACIInterfacePolicyGroupForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    link_level_policy = DynamicModelChoiceField(
        queryset=ACILinkLevelPolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )
    cdp_policy = DynamicModelChoiceField(
        queryset=ACICDPInterfacePolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )
    lldp_policy = DynamicModelChoiceField(
        queryset=ACILLDPInterfacePolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )
    lacp_policy = DynamicModelChoiceField(
        queryset=ACILACPInterfacePolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )
    mcp_policy = DynamicModelChoiceField(
        queryset=ACIMCPInterfacePolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )
    stp_policy = DynamicModelChoiceField(
        queryset=ACISTPInterfacePolicy.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )
    aaep = DynamicModelChoiceField(
        queryset=ACIAAEP.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
    )

    class Meta:
        model = ACIInterfacePolicyGroup
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
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


class ACIInterfacePolicyGroupBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIInterfacePolicyGroup
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    pg_type = forms.ChoiceField(choices=InterfacePolicyGroupTypeChoices, required=False)
    aaep = DynamicModelChoiceField(queryset=ACIAAEP.objects.all(), required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "aaep")


class ACIInterfacePolicyGroupFilterForm(NetBoxModelFilterSetForm):
    model = ACIInterfacePolicyGroup
    aci_fabric_id = DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )
    pg_type = forms.MultipleChoiceField(choices=InterfacePolicyGroupTypeChoices, required=False)
    aaep_id = DynamicModelMultipleChoiceField(
        queryset=ACIAAEP.objects.all(), required=False, label=_("AAEP")
    )


class ACIInterfacePolicyGroupImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")
    link_level_policy = forms.ModelChoiceField(
        queryset=ACILinkLevelPolicy.objects.all(), to_field_name="name", required=False
    )
    cdp_policy = forms.ModelChoiceField(
        queryset=ACICDPInterfacePolicy.objects.all(), to_field_name="name", required=False
    )
    lldp_policy = forms.ModelChoiceField(
        queryset=ACILLDPInterfacePolicy.objects.all(), to_field_name="name", required=False
    )
    lacp_policy = forms.ModelChoiceField(
        queryset=ACILACPInterfacePolicy.objects.all(), to_field_name="name", required=False
    )
    mcp_policy = forms.ModelChoiceField(
        queryset=ACIMCPInterfacePolicy.objects.all(), to_field_name="name", required=False
    )
    stp_policy = forms.ModelChoiceField(
        queryset=ACISTPInterfacePolicy.objects.all(), to_field_name="name", required=False
    )
    aaep = forms.ModelChoiceField(
        queryset=ACIAAEP.objects.all(), to_field_name="name", required=False
    )

    class Meta:
        model = ACIInterfacePolicyGroup
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
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
