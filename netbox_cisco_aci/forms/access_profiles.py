"""Forms for Switch / Interface Profiles + selectors + attachments (Phase 4)."""

from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField

from ..choices import RangeAllChoices
from ..models.access import (
    ACIInterfacePolicyGroup,
    ACIInterfaceProfile,
    ACIInterfaceProfileSelector,
    ACISwitchProfile,
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileSelector,
)
from ..models.fabric import ACIFabric

# ---------------------------------------------------------------------------
# Switch Profile
# ---------------------------------------------------------------------------


class ACISwitchProfileForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))

    class Meta:
        model = ACISwitchProfile
        fields = ("aci_fabric", "name", "name_alias", "description", "tags")


class ACISwitchProfileBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISwitchProfile
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACISwitchProfileFilterForm(NetBoxModelFilterSetForm):
    model = ACISwitchProfile
    aci_fabric_id = DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )


class ACISwitchProfileImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACISwitchProfile
        fields = ("aci_fabric", "name", "name_alias", "description", "tags")


# ---------------------------------------------------------------------------
# Switch Profile Selector
# ---------------------------------------------------------------------------


class ACISwitchProfileSelectorForm(NetBoxModelForm):
    switch_profile = DynamicModelChoiceField(
        queryset=ACISwitchProfile.objects.all(), label=_("Switch Profile")
    )

    class Meta:
        model = ACISwitchProfileSelector
        fields = (
            "switch_profile",
            "name",
            "name_alias",
            "selector_type",
            "from_node_id",
            "to_node_id",
            "description",
            "tags",
        )


class ACISwitchProfileSelectorBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISwitchProfileSelector
    switch_profile = DynamicModelChoiceField(
        queryset=ACISwitchProfile.objects.all(), required=False
    )
    selector_type = forms.ChoiceField(choices=RangeAllChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACISwitchProfileSelectorFilterForm(NetBoxModelFilterSetForm):
    model = ACISwitchProfileSelector
    switch_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACISwitchProfile.objects.all(), required=False, label=_("Switch Profile")
    )
    selector_type = forms.MultipleChoiceField(choices=RangeAllChoices, required=False)


class ACISwitchProfileSelectorImportForm(NetBoxModelImportForm):
    switch_profile = forms.ModelChoiceField(
        queryset=ACISwitchProfile.objects.all(), to_field_name="name"
    )

    class Meta:
        model = ACISwitchProfileSelector
        fields = (
            "switch_profile",
            "name",
            "name_alias",
            "selector_type",
            "from_node_id",
            "to_node_id",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# Interface Profile
# ---------------------------------------------------------------------------


class ACIInterfaceProfileForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))

    class Meta:
        model = ACIInterfaceProfile
        fields = ("aci_fabric", "name", "name_alias", "description", "tags")


class ACIInterfaceProfileBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIInterfaceProfile
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIInterfaceProfileFilterForm(NetBoxModelFilterSetForm):
    model = ACIInterfaceProfile
    aci_fabric_id = DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )


class ACIInterfaceProfileImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACIInterfaceProfile
        fields = ("aci_fabric", "name", "name_alias", "description", "tags")


# ---------------------------------------------------------------------------
# Interface Profile Selector
# ---------------------------------------------------------------------------


class ACIInterfaceProfileSelectorForm(NetBoxModelForm):
    interface_profile = DynamicModelChoiceField(
        queryset=ACIInterfaceProfile.objects.all(), label=_("Interface Profile")
    )
    policy_group = DynamicModelChoiceField(
        queryset=ACIInterfacePolicyGroup.objects.all(),
        required=False,
        label=_("Policy Group"),
    )

    class Meta:
        model = ACIInterfaceProfileSelector
        fields = (
            "interface_profile",
            "name",
            "name_alias",
            "policy_group",
            "from_module",
            "from_port",
            "to_module",
            "to_port",
            "description",
            "tags",
        )


class ACIInterfaceProfileSelectorBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIInterfaceProfileSelector
    interface_profile = DynamicModelChoiceField(
        queryset=ACIInterfaceProfile.objects.all(), required=False
    )
    policy_group = DynamicModelChoiceField(
        queryset=ACIInterfacePolicyGroup.objects.all(), required=False
    )
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "policy_group")


class ACIInterfaceProfileSelectorFilterForm(NetBoxModelFilterSetForm):
    model = ACIInterfaceProfileSelector
    interface_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACIInterfaceProfile.objects.all(), required=False, label=_("Interface Profile")
    )
    policy_group_id = DynamicModelMultipleChoiceField(
        queryset=ACIInterfacePolicyGroup.objects.all(), required=False, label=_("Policy Group")
    )


class ACIInterfaceProfileSelectorImportForm(NetBoxModelImportForm):
    interface_profile = forms.ModelChoiceField(
        queryset=ACIInterfaceProfile.objects.all(), to_field_name="name"
    )
    policy_group = forms.ModelChoiceField(
        queryset=ACIInterfacePolicyGroup.objects.all(), to_field_name="name", required=False
    )

    class Meta:
        model = ACIInterfaceProfileSelector
        fields = (
            "interface_profile",
            "name",
            "name_alias",
            "policy_group",
            "from_module",
            "from_port",
            "to_module",
            "to_port",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# Switch \u2194 Interface Profile attachment
# ---------------------------------------------------------------------------


class ACISwitchProfileInterfaceProfileAttachmentForm(NetBoxModelForm):
    switch_profile = DynamicModelChoiceField(
        queryset=ACISwitchProfile.objects.all(), label=_("Switch Profile")
    )
    interface_profile = DynamicModelChoiceField(
        queryset=ACIInterfaceProfile.objects.all(), label=_("Interface Profile")
    )

    class Meta:
        model = ACISwitchProfileInterfaceProfileAttachment
        fields = ("switch_profile", "interface_profile")


class ACISwitchProfileInterfaceProfileAttachmentBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISwitchProfileInterfaceProfileAttachment
    switch_profile = DynamicModelChoiceField(
        queryset=ACISwitchProfile.objects.all(), required=False
    )
    interface_profile = DynamicModelChoiceField(
        queryset=ACIInterfaceProfile.objects.all(), required=False
    )


class ACISwitchProfileInterfaceProfileAttachmentFilterForm(NetBoxModelFilterSetForm):
    model = ACISwitchProfileInterfaceProfileAttachment
    switch_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACISwitchProfile.objects.all(), required=False, label=_("Switch Profile")
    )
    interface_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACIInterfaceProfile.objects.all(), required=False, label=_("Interface Profile")
    )


class ACISwitchProfileInterfaceProfileAttachmentImportForm(NetBoxModelImportForm):
    switch_profile = forms.ModelChoiceField(
        queryset=ACISwitchProfile.objects.all(), to_field_name="name"
    )
    interface_profile = forms.ModelChoiceField(
        queryset=ACIInterfaceProfile.objects.all(), to_field_name="name"
    )

    class Meta:
        model = ACISwitchProfileInterfaceProfileAttachment
        fields = ("switch_profile", "interface_profile")
