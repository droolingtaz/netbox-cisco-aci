"""Forms for Phase 6 binding models."""

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
    DeploymentImmediacyChoices,
    InterfaceFabricRoleChoices,
    ResolutionImmediacyChoices,
    StaticPortBindingTypeChoices,
    StaticPortModeChoices,
)
from ..models.access import ACIDomain
from ..models.bindings import (
    ACIDomainBinding,
    ACIInterfaceFabricMembership,
    ACIStaticPortBinding,
    ACIVPCBindingPair,
)
from ..models.fabric import ACINode
from ..models.tenant import ACIEndpointGroup

# ---------------------------------------------------------------------------
# ACIStaticPortBinding
# ---------------------------------------------------------------------------


class ACIStaticPortBindingForm(NetBoxModelForm):
    aci_endpoint_group = DynamicModelChoiceField(
        queryset=ACIEndpointGroup.objects.all(), label=_("EPG")
    )
    dcim_interface = DynamicModelChoiceField(queryset=Interface.objects.all(), label=_("Interface"))

    class Meta:
        model = ACIStaticPortBinding
        fields = (
            "aci_endpoint_group",
            "dcim_interface",
            "binding_type",
            "encap_vlan",
            "mode",
            "primary_encap_vlan",
            "deployment_immediacy",
            "name",
            "name_alias",
            "description",
            "tags",
        )


class ACIStaticPortBindingBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIStaticPortBinding
    binding_type = forms.ChoiceField(choices=StaticPortBindingTypeChoices, required=False)
    mode = forms.ChoiceField(choices=StaticPortModeChoices, required=False)
    deployment_immediacy = forms.ChoiceField(choices=DeploymentImmediacyChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "primary_encap_vlan")


class ACIStaticPortBindingFilterForm(NetBoxModelFilterSetForm):
    model = ACIStaticPortBinding
    aci_endpoint_group_id = DynamicModelMultipleChoiceField(
        queryset=ACIEndpointGroup.objects.all(), required=False, label=_("EPG")
    )
    dcim_interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(), required=False, label=_("Interface")
    )
    binding_type = forms.MultipleChoiceField(choices=StaticPortBindingTypeChoices, required=False)
    mode = forms.MultipleChoiceField(choices=StaticPortModeChoices, required=False)


class ACIStaticPortBindingImportForm(NetBoxModelImportForm):
    aci_endpoint_group = forms.ModelChoiceField(
        queryset=ACIEndpointGroup.objects.all(), to_field_name="name"
    )
    dcim_interface = forms.ModelChoiceField(queryset=Interface.objects.all())
    binding_type = forms.ChoiceField(choices=StaticPortBindingTypeChoices, required=False)
    mode = forms.ChoiceField(choices=StaticPortModeChoices, required=False)

    class Meta:
        model = ACIStaticPortBinding
        fields = (
            "aci_endpoint_group",
            "dcim_interface",
            "binding_type",
            "encap_vlan",
            "mode",
            "primary_encap_vlan",
            "deployment_immediacy",
            "name",
            "name_alias",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIVPCBindingPair
# ---------------------------------------------------------------------------


class ACIVPCBindingPairForm(NetBoxModelForm):
    binding_a = DynamicModelChoiceField(
        queryset=ACIStaticPortBinding.objects.all(), label=_("Binding A")
    )
    binding_b = DynamicModelChoiceField(
        queryset=ACIStaticPortBinding.objects.all(), label=_("Binding B")
    )

    class Meta:
        model = ACIVPCBindingPair
        fields = ("binding_a", "binding_b", "name", "name_alias", "description", "tags")


class ACIVPCBindingPairBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIVPCBindingPair
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIVPCBindingPairFilterForm(NetBoxModelFilterSetForm):
    model = ACIVPCBindingPair
    binding_a_id = DynamicModelMultipleChoiceField(
        queryset=ACIStaticPortBinding.objects.all(), required=False, label=_("Binding A")
    )
    binding_b_id = DynamicModelMultipleChoiceField(
        queryset=ACIStaticPortBinding.objects.all(), required=False, label=_("Binding B")
    )


class ACIVPCBindingPairImportForm(NetBoxModelImportForm):
    binding_a = forms.ModelChoiceField(queryset=ACIStaticPortBinding.objects.all())
    binding_b = forms.ModelChoiceField(queryset=ACIStaticPortBinding.objects.all())

    class Meta:
        model = ACIVPCBindingPair
        fields = ("binding_a", "binding_b", "name", "name_alias", "description", "tags")


# ---------------------------------------------------------------------------
# ACIDomainBinding
# ---------------------------------------------------------------------------


class ACIDomainBindingForm(NetBoxModelForm):
    aci_endpoint_group = DynamicModelChoiceField(
        queryset=ACIEndpointGroup.objects.all(), label=_("EPG")
    )
    aci_domain = DynamicModelChoiceField(queryset=ACIDomain.objects.all(), label=_("Domain"))

    class Meta:
        model = ACIDomainBinding
        fields = (
            "aci_endpoint_group",
            "aci_domain",
            "deployment_immediacy",
            "resolution_immediacy",
            "name",
            "name_alias",
            "description",
            "tags",
        )


class ACIDomainBindingBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIDomainBinding
    deployment_immediacy = forms.ChoiceField(choices=DeploymentImmediacyChoices, required=False)
    resolution_immediacy = forms.ChoiceField(choices=ResolutionImmediacyChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIDomainBindingFilterForm(NetBoxModelFilterSetForm):
    model = ACIDomainBinding
    aci_endpoint_group_id = DynamicModelMultipleChoiceField(
        queryset=ACIEndpointGroup.objects.all(), required=False, label=_("EPG")
    )
    aci_domain_id = DynamicModelMultipleChoiceField(
        queryset=ACIDomain.objects.all(), required=False, label=_("Domain")
    )


class ACIDomainBindingImportForm(NetBoxModelImportForm):
    aci_endpoint_group = forms.ModelChoiceField(
        queryset=ACIEndpointGroup.objects.all(), to_field_name="name"
    )
    aci_domain = forms.ModelChoiceField(queryset=ACIDomain.objects.all(), to_field_name="name")

    class Meta:
        model = ACIDomainBinding
        fields = (
            "aci_endpoint_group",
            "aci_domain",
            "deployment_immediacy",
            "resolution_immediacy",
            "name",
            "name_alias",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIInterfaceFabricMembership
# ---------------------------------------------------------------------------


class ACIInterfaceFabricMembershipForm(NetBoxModelForm):
    dcim_interface = DynamicModelChoiceField(queryset=Interface.objects.all(), label=_("Interface"))
    aci_node = DynamicModelChoiceField(queryset=ACINode.objects.all(), label=_("ACI Node"))

    class Meta:
        model = ACIInterfaceFabricMembership
        fields = (
            "dcim_interface",
            "aci_node",
            "interface_role",
            "name",
            "name_alias",
            "description",
            "tags",
        )


class ACIInterfaceFabricMembershipBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIInterfaceFabricMembership
    interface_role = forms.ChoiceField(choices=InterfaceFabricRoleChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIInterfaceFabricMembershipFilterForm(NetBoxModelFilterSetForm):
    model = ACIInterfaceFabricMembership
    dcim_interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(), required=False, label=_("Interface")
    )
    aci_node_id = DynamicModelMultipleChoiceField(
        queryset=ACINode.objects.all(), required=False, label=_("ACI Node")
    )
    interface_role = forms.MultipleChoiceField(choices=InterfaceFabricRoleChoices, required=False)


class ACIInterfaceFabricMembershipImportForm(NetBoxModelImportForm):
    dcim_interface = forms.ModelChoiceField(queryset=Interface.objects.all())
    aci_node = forms.ModelChoiceField(queryset=ACINode.objects.all(), to_field_name="name")
    interface_role = forms.ChoiceField(choices=InterfaceFabricRoleChoices, required=False)

    class Meta:
        model = ACIInterfaceFabricMembership
        fields = (
            "dcim_interface",
            "aci_node",
            "interface_role",
            "name",
            "name_alias",
            "description",
            "tags",
        )
