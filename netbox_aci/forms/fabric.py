"""Forms for fabric-topology models."""

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

from ..choices import NodeRoleChoices, NodeTypeChoices
from ..models.fabric import ACIFabric, ACINode, ACIPod


# ---------------------------------------------------------------------------
# ACIFabric
# ---------------------------------------------------------------------------

class ACIFabricForm(NetBoxModelForm):
    fieldsets = (
        FieldSet("name", "name_alias", "fabric_id", "description", name=_("Fabric")),
    )

    class Meta:
        model = ACIFabric
        fields = ("name", "name_alias", "fabric_id", "description", "tags")


class ACIFabricBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIFabric
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIFabricFilterForm(NetBoxModelFilterSetForm):
    model = ACIFabric
    fabric_id = forms.IntegerField(required=False)


class ACIFabricImportForm(NetBoxModelImportForm):
    class Meta:
        model = ACIFabric
        fields = ("name", "name_alias", "fabric_id", "description", "tags")


# ---------------------------------------------------------------------------
# ACIPod
# ---------------------------------------------------------------------------

class ACIPodForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    fieldsets = (
        FieldSet("aci_fabric", "name", "name_alias", "pod_id", "description", name=_("Pod")),
    )

    class Meta:
        model = ACIPod
        fields = ("aci_fabric", "name", "name_alias", "pod_id", "description", "tags")


class ACIPodBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIPod
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIPodFilterForm(NetBoxModelFilterSetForm):
    model = ACIPod
    aci_fabric_id = DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )
    pod_id = forms.IntegerField(required=False)


class ACIPodImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACIPod
        fields = ("aci_fabric", "name", "name_alias", "pod_id", "description", "tags")


# ---------------------------------------------------------------------------
# ACINode
# ---------------------------------------------------------------------------

class ACINodeForm(NetBoxModelForm):
    aci_pod = DynamicModelChoiceField(queryset=ACIPod.objects.all(), label=_("Pod"))

    fieldsets = (
        FieldSet(
            "aci_pod",
            "name",
            "name_alias",
            "node_id",
            "role",
            "node_type",
            "serial_number",
            "pod_tep_pool",
            "firmware_version",
            "description",
            name=_("Node"),
        ),
        FieldSet("node_object_type", "node_object_id", name=_("Linked NetBox object")),
    )

    class Meta:
        model = ACINode
        fields = (
            "aci_pod",
            "name",
            "name_alias",
            "node_id",
            "role",
            "node_type",
            "serial_number",
            "pod_tep_pool",
            "firmware_version",
            "node_object_type",
            "node_object_id",
            "description",
            "tags",
        )


class ACINodeBulkEditForm(NetBoxModelBulkEditForm):
    model = ACINode
    aci_pod = DynamicModelChoiceField(queryset=ACIPod.objects.all(), required=False)
    role = forms.ChoiceField(choices=NodeRoleChoices, required=False)
    node_type = forms.ChoiceField(choices=NodeTypeChoices, required=False)
    firmware_version = forms.CharField(max_length=64, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "firmware_version", "pod_tep_pool")


class ACINodeFilterForm(NetBoxModelFilterSetForm):
    model = ACINode
    aci_pod_id = DynamicModelMultipleChoiceField(
        queryset=ACIPod.objects.all(), required=False, label=_("Pod")
    )
    role = forms.MultipleChoiceField(choices=NodeRoleChoices, required=False)
    node_type = forms.MultipleChoiceField(choices=NodeTypeChoices, required=False)
    node_id = forms.IntegerField(required=False)


class ACINodeImportForm(NetBoxModelImportForm):
    aci_pod = forms.ModelChoiceField(queryset=ACIPod.objects.all(), to_field_name="name")
    role = forms.ChoiceField(choices=NodeRoleChoices)
    node_type = forms.ChoiceField(choices=NodeTypeChoices, required=False)

    class Meta:
        model = ACINode
        fields = (
            "aci_pod",
            "name",
            "name_alias",
            "node_id",
            "role",
            "node_type",
            "serial_number",
            "pod_tep_pool",
            "firmware_version",
            "description",
            "tags",
        )
