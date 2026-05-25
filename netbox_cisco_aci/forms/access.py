"""Forms for access-policy models (Phase 3)."""

from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

from ..choices import (
    DomainTypeChoices,
    StaticPortModeChoices,
    VLANPoolAllocationChoices,
)
from ..models.access import (
    ACIAAEP,
    ACIAAEPEPGMapping,
    ACIDomain,
    ACIVLANPool,
    ACIVLANPoolBlock,
)
from ..models.fabric import ACIFabric
from ..models.tenant import ACIEndpointGroup

# ---------------------------------------------------------------------------
# ACIVLANPool
# ---------------------------------------------------------------------------


class ACIVLANPoolForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))

    fieldsets = (
        FieldSet(
            "aci_fabric",
            "name",
            "name_alias",
            "allocation_mode",
            "description",
            name=_("VLAN Pool"),
        ),
    )

    class Meta:
        model = ACIVLANPool
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "allocation_mode",
            "description",
            "tags",
        )


class ACIVLANPoolBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIVLANPool
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    allocation_mode = forms.ChoiceField(choices=VLANPoolAllocationChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIVLANPoolFilterForm(NetBoxModelFilterSetForm):
    model = ACIVLANPool
    aci_fabric_id = DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )
    allocation_mode = forms.MultipleChoiceField(choices=VLANPoolAllocationChoices, required=False)


class ACIVLANPoolImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")
    allocation_mode = forms.ChoiceField(choices=VLANPoolAllocationChoices)

    class Meta:
        model = ACIVLANPool
        fields = ("aci_fabric", "name", "name_alias", "allocation_mode", "description", "tags")


# ---------------------------------------------------------------------------
# ACIVLANPoolBlock
# ---------------------------------------------------------------------------


class ACIVLANPoolBlockForm(NetBoxModelForm):
    aci_vlan_pool = DynamicModelChoiceField(
        queryset=ACIVLANPool.objects.all(), label=_("VLAN Pool")
    )

    class Meta:
        model = ACIVLANPoolBlock
        fields = (
            "aci_vlan_pool",
            "name",
            "name_alias",
            "from_vlan",
            "to_vlan",
            "allocation_mode_override",
            "description",
            "tags",
        )


class ACIVLANPoolBlockBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIVLANPoolBlock
    aci_vlan_pool = DynamicModelChoiceField(queryset=ACIVLANPool.objects.all(), required=False)
    allocation_mode_override = forms.ChoiceField(choices=VLANPoolAllocationChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "allocation_mode_override")


class ACIVLANPoolBlockFilterForm(NetBoxModelFilterSetForm):
    model = ACIVLANPoolBlock
    aci_vlan_pool_id = DynamicModelMultipleChoiceField(
        queryset=ACIVLANPool.objects.all(), required=False, label=_("VLAN Pool")
    )


class ACIVLANPoolBlockImportForm(NetBoxModelImportForm):
    aci_vlan_pool = forms.ModelChoiceField(queryset=ACIVLANPool.objects.all(), to_field_name="name")

    class Meta:
        model = ACIVLANPoolBlock
        fields = (
            "aci_vlan_pool",
            "name",
            "name_alias",
            "from_vlan",
            "to_vlan",
            "allocation_mode_override",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIDomain
# ---------------------------------------------------------------------------


class ACIDomainForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    aci_vlan_pool = DynamicModelChoiceField(
        queryset=ACIVLANPool.objects.all(),
        required=False,
        label=_("VLAN Pool"),
        query_params={"aci_fabric_id": "$aci_fabric"},
    )

    fieldsets = (
        FieldSet(
            "aci_fabric",
            "name",
            "name_alias",
            "domain_type",
            "aci_vlan_pool",
            "description",
            name=_("Domain"),
        ),
    )

    class Meta:
        model = ACIDomain
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "domain_type",
            "aci_vlan_pool",
            "description",
            "tags",
        )


class ACIDomainBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIDomain
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    domain_type = forms.ChoiceField(choices=DomainTypeChoices, required=False)
    aci_vlan_pool = DynamicModelChoiceField(queryset=ACIVLANPool.objects.all(), required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "aci_vlan_pool")


class ACIDomainFilterForm(NetBoxModelFilterSetForm):
    model = ACIDomain
    aci_fabric_id = DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )
    domain_type = forms.MultipleChoiceField(choices=DomainTypeChoices, required=False)
    aci_vlan_pool_id = DynamicModelMultipleChoiceField(
        queryset=ACIVLANPool.objects.all(), required=False, label=_("VLAN Pool")
    )


class ACIDomainImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")
    aci_vlan_pool = forms.ModelChoiceField(
        queryset=ACIVLANPool.objects.all(), to_field_name="name", required=False
    )
    domain_type = forms.ChoiceField(choices=DomainTypeChoices)

    class Meta:
        model = ACIDomain
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "domain_type",
            "aci_vlan_pool",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIAAEP
# ---------------------------------------------------------------------------


class ACIAAEPForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    domains = DynamicModelMultipleChoiceField(
        queryset=ACIDomain.objects.all(),
        required=False,
        query_params={"aci_fabric_id": "$aci_fabric"},
        label=_("Domains"),
        help_text=_("Domains this AAEP makes available. Must belong to the same Fabric."),
    )

    fieldsets = (
        FieldSet(
            "aci_fabric",
            "name",
            "name_alias",
            "enable_infra_vlan",
            "domains",
            "description",
            name=_("AAEP"),
        ),
    )

    class Meta:
        model = ACIAAEP
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "enable_infra_vlan",
            "domains",
            "description",
            "tags",
        )


class ACIAAEPBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIAAEP
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    enable_infra_vlan = forms.NullBooleanField(required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIAAEPFilterForm(NetBoxModelFilterSetForm):
    model = ACIAAEP
    aci_fabric_id = DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )
    enable_infra_vlan = forms.NullBooleanField(required=False)


class ACIAAEPImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACIAAEP
        fields = (
            "aci_fabric",
            "name",
            "name_alias",
            "enable_infra_vlan",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIAAEPEPGMapping
# ---------------------------------------------------------------------------


class ACIAAEPEPGMappingForm(NetBoxModelForm):
    aci_aaep = DynamicModelChoiceField(queryset=ACIAAEP.objects.all(), label=_("AAEP"))
    aci_endpoint_group = DynamicModelChoiceField(
        queryset=ACIEndpointGroup.objects.all(),
        label=_("Endpoint Group"),
    )

    fieldsets = (
        FieldSet(
            "aci_aaep",
            "aci_endpoint_group",
            "encap_vlan",
            "mode",
            "name",
            "name_alias",
            "description",
            name=_("AAEP \u2192 EPG"),
        ),
    )

    class Meta:
        model = ACIAAEPEPGMapping
        fields = (
            "aci_aaep",
            "aci_endpoint_group",
            "encap_vlan",
            "mode",
            "name",
            "name_alias",
            "description",
            "tags",
        )


class ACIAAEPEPGMappingBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIAAEPEPGMapping
    aci_aaep = DynamicModelChoiceField(queryset=ACIAAEP.objects.all(), required=False)
    aci_endpoint_group = DynamicModelChoiceField(
        queryset=ACIEndpointGroup.objects.all(), required=False
    )
    mode = forms.ChoiceField(choices=StaticPortModeChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIAAEPEPGMappingFilterForm(NetBoxModelFilterSetForm):
    model = ACIAAEPEPGMapping
    aci_aaep_id = DynamicModelMultipleChoiceField(
        queryset=ACIAAEP.objects.all(), required=False, label=_("AAEP")
    )
    aci_endpoint_group_id = DynamicModelMultipleChoiceField(
        queryset=ACIEndpointGroup.objects.all(), required=False, label=_("Endpoint Group")
    )
    mode = forms.MultipleChoiceField(choices=StaticPortModeChoices, required=False)


class ACIAAEPEPGMappingImportForm(NetBoxModelImportForm):
    aci_aaep = forms.ModelChoiceField(queryset=ACIAAEP.objects.all(), to_field_name="name")
    aci_endpoint_group = forms.ModelChoiceField(
        queryset=ACIEndpointGroup.objects.all(), to_field_name="name"
    )

    class Meta:
        model = ACIAAEPEPGMapping
        fields = (
            "aci_aaep",
            "aci_endpoint_group",
            "encap_vlan",
            "mode",
            "name",
            "name_alias",
            "description",
            "tags",
        )
