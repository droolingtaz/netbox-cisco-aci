"""Forms for Phase 5 contract / filter / relation models."""

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
    ContractFilterEntryEtherTypeChoices,
    ContractFilterEntryIPProtocolChoices,
    ContractRelationRoleChoices,
    ContractScopeChoices,
    QualityOfServiceClassChoices,
    SubjectFilterActionChoices,
    SubjectFilterDirectionChoices,
    SubjectFilterPriorityChoices,
)
from ..models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from ..models.l3out import ACIExternalEPG
from ..models.tenant import (
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
)

# ---------------------------------------------------------------------------
# ACIContract
# ---------------------------------------------------------------------------


class ACIContractForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))

    fieldsets = (
        FieldSet(
            "aci_tenant",
            "name",
            "name_alias",
            "scope",
            "qos_class",
            "target_dscp",
            "description",
            name=_("Contract"),
        ),
    )

    class Meta:
        model = ACIContract
        fields = (
            "aci_tenant",
            "name",
            "name_alias",
            "scope",
            "qos_class",
            "target_dscp",
            "description",
            "tags",
        )


class ACIContractBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIContract
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), required=False)
    scope = forms.ChoiceField(choices=ContractScopeChoices, required=False)
    qos_class = forms.ChoiceField(choices=QualityOfServiceClassChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "qos_class", "target_dscp")


class ACIContractFilterForm(NetBoxModelFilterSetForm):
    model = ACIContract
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )
    scope = forms.MultipleChoiceField(choices=ContractScopeChoices, required=False)
    qos_class = forms.MultipleChoiceField(choices=QualityOfServiceClassChoices, required=False)


class ACIContractImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")
    scope = forms.ChoiceField(choices=ContractScopeChoices, required=False)

    class Meta:
        model = ACIContract
        fields = (
            "aci_tenant",
            "name",
            "name_alias",
            "scope",
            "qos_class",
            "target_dscp",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACISubject
# ---------------------------------------------------------------------------


class ACISubjectForm(NetBoxModelForm):
    aci_contract = DynamicModelChoiceField(queryset=ACIContract.objects.all(), label=_("Contract"))

    fieldsets = (
        FieldSet(
            "aci_contract",
            "name",
            "name_alias",
            "apply_both_directions",
            "reverse_filter_ports",
            "qos_class",
            "target_dscp",
            "description",
            name=_("Subject"),
        ),
    )

    class Meta:
        model = ACISubject
        fields = (
            "aci_contract",
            "name",
            "name_alias",
            "apply_both_directions",
            "reverse_filter_ports",
            "qos_class",
            "target_dscp",
            "description",
            "tags",
        )


class ACISubjectBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISubject
    aci_contract = DynamicModelChoiceField(queryset=ACIContract.objects.all(), required=False)
    apply_both_directions = forms.NullBooleanField(required=False)
    reverse_filter_ports = forms.NullBooleanField(required=False)
    qos_class = forms.ChoiceField(choices=QualityOfServiceClassChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "qos_class", "target_dscp")


class ACISubjectFilterSetForm(NetBoxModelFilterSetForm):
    model = ACISubject
    aci_contract_id = DynamicModelMultipleChoiceField(
        queryset=ACIContract.objects.all(), required=False, label=_("Contract")
    )


class ACISubjectImportForm(NetBoxModelImportForm):
    aci_contract = forms.ModelChoiceField(queryset=ACIContract.objects.all(), to_field_name="name")

    class Meta:
        model = ACISubject
        fields = (
            "aci_contract",
            "name",
            "name_alias",
            "apply_both_directions",
            "reverse_filter_ports",
            "qos_class",
            "target_dscp",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIFilter
# ---------------------------------------------------------------------------


class ACIFilterForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))

    class Meta:
        model = ACIFilter
        fields = ("aci_tenant", "name", "name_alias", "description", "tags")


class ACIFilterBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIFilter
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIFilterFilterForm(NetBoxModelFilterSetForm):
    model = ACIFilter
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )


class ACIFilterImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")

    class Meta:
        model = ACIFilter
        fields = ("aci_tenant", "name", "name_alias", "description", "tags")


# ---------------------------------------------------------------------------
# ACIFilterEntry
# ---------------------------------------------------------------------------


class ACIFilterEntryForm(NetBoxModelForm):
    aci_filter = DynamicModelChoiceField(queryset=ACIFilter.objects.all(), label=_("Filter"))

    fieldsets = (
        FieldSet(
            "aci_filter",
            "name",
            "name_alias",
            "ether_type",
            "ip_protocol",
            "description",
            name=_("Entry"),
        ),
        FieldSet(
            "source_port_from",
            "source_port_to",
            "destination_port_from",
            "destination_port_to",
            "tcp_rules",
            "stateful",
            name=_("L4"),
        ),
        FieldSet(
            "arp_opcode",
            "icmp_v4_type",
            "icmp_v6_type",
            "match_only_fragments",
            name=_("Other"),
        ),
    )

    class Meta:
        model = ACIFilterEntry
        fields = (
            "aci_filter",
            "name",
            "name_alias",
            "ether_type",
            "ip_protocol",
            "source_port_from",
            "source_port_to",
            "destination_port_from",
            "destination_port_to",
            "tcp_rules",
            "match_only_fragments",
            "arp_opcode",
            "stateful",
            "icmp_v4_type",
            "icmp_v6_type",
            "description",
            "tags",
        )


class ACIFilterEntryBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIFilterEntry
    aci_filter = DynamicModelChoiceField(queryset=ACIFilter.objects.all(), required=False)
    ether_type = forms.ChoiceField(choices=ContractFilterEntryEtherTypeChoices, required=False)
    ip_protocol = forms.ChoiceField(choices=ContractFilterEntryIPProtocolChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIFilterEntryFilterForm(NetBoxModelFilterSetForm):
    model = ACIFilterEntry
    aci_filter_id = DynamicModelMultipleChoiceField(
        queryset=ACIFilter.objects.all(), required=False, label=_("Filter")
    )
    ether_type = forms.MultipleChoiceField(
        choices=ContractFilterEntryEtherTypeChoices, required=False
    )
    ip_protocol = forms.MultipleChoiceField(
        choices=ContractFilterEntryIPProtocolChoices, required=False
    )


class ACIFilterEntryImportForm(NetBoxModelImportForm):
    aci_filter = forms.ModelChoiceField(queryset=ACIFilter.objects.all(), to_field_name="name")

    class Meta:
        model = ACIFilterEntry
        fields = (
            "aci_filter",
            "name",
            "name_alias",
            "ether_type",
            "ip_protocol",
            "source_port_from",
            "source_port_to",
            "destination_port_from",
            "destination_port_to",
            "tcp_rules",
            "match_only_fragments",
            "arp_opcode",
            "stateful",
            "icmp_v4_type",
            "icmp_v6_type",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACISubjectFilter (through-model)
# ---------------------------------------------------------------------------


class ACISubjectFilterForm(NetBoxModelForm):
    aci_subject = DynamicModelChoiceField(queryset=ACISubject.objects.all(), label=_("Subject"))
    aci_filter = DynamicModelChoiceField(queryset=ACIFilter.objects.all(), label=_("Filter"))

    class Meta:
        model = ACISubjectFilter
        fields = (
            "aci_subject",
            "aci_filter",
            "direction",
            "action",
            "priority",
            "name",
            "name_alias",
            "description",
            "tags",
        )


class ACISubjectFilterBulkEditForm(NetBoxModelBulkEditForm):
    model = ACISubjectFilter
    direction = forms.ChoiceField(choices=SubjectFilterDirectionChoices, required=False)
    action = forms.ChoiceField(choices=SubjectFilterActionChoices, required=False)
    priority = forms.ChoiceField(choices=SubjectFilterPriorityChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACISubjectFilterFilterSetForm(NetBoxModelFilterSetForm):
    model = ACISubjectFilter
    aci_subject_id = DynamicModelMultipleChoiceField(
        queryset=ACISubject.objects.all(), required=False, label=_("Subject")
    )
    aci_filter_id = DynamicModelMultipleChoiceField(
        queryset=ACIFilter.objects.all(), required=False, label=_("Filter")
    )
    direction = forms.MultipleChoiceField(choices=SubjectFilterDirectionChoices, required=False)
    action = forms.MultipleChoiceField(choices=SubjectFilterActionChoices, required=False)


class ACISubjectFilterImportForm(NetBoxModelImportForm):
    aci_subject = forms.ModelChoiceField(queryset=ACISubject.objects.all(), to_field_name="name")
    aci_filter = forms.ModelChoiceField(queryset=ACIFilter.objects.all(), to_field_name="name")

    class Meta:
        model = ACISubjectFilter
        fields = (
            "aci_subject",
            "aci_filter",
            "direction",
            "action",
            "priority",
            "name",
            "name_alias",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIContractRelation
# ---------------------------------------------------------------------------


class ACIContractRelationForm(NetBoxModelForm):
    aci_contract = DynamicModelChoiceField(queryset=ACIContract.objects.all(), label=_("Contract"))
    aci_endpoint_group = DynamicModelChoiceField(
        queryset=ACIEndpointGroup.objects.all(), required=False, label=_("EPG")
    )
    aci_endpoint_security_group = DynamicModelChoiceField(
        queryset=ACIEndpointSecurityGroup.objects.all(), required=False, label=_("ESG")
    )
    aci_external_epg = DynamicModelChoiceField(
        queryset=ACIExternalEPG.objects.all(), required=False, label=_("External EPG")
    )

    class Meta:
        model = ACIContractRelation
        fields = (
            "aci_contract",
            "aci_endpoint_group",
            "aci_endpoint_security_group",
            "aci_external_epg",
            "role",
            "name",
            "name_alias",
            "description",
            "tags",
        )


class ACIContractRelationBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIContractRelation
    role = forms.ChoiceField(choices=ContractRelationRoleChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIContractRelationFilterForm(NetBoxModelFilterSetForm):
    model = ACIContractRelation
    aci_contract_id = DynamicModelMultipleChoiceField(
        queryset=ACIContract.objects.all(), required=False, label=_("Contract")
    )
    aci_endpoint_group_id = DynamicModelMultipleChoiceField(
        queryset=ACIEndpointGroup.objects.all(), required=False, label=_("EPG")
    )
    aci_endpoint_security_group_id = DynamicModelMultipleChoiceField(
        queryset=ACIEndpointSecurityGroup.objects.all(), required=False, label=_("ESG")
    )
    aci_external_epg_id = DynamicModelMultipleChoiceField(
        queryset=ACIExternalEPG.objects.all(), required=False, label=_("External EPG")
    )
    role = forms.MultipleChoiceField(choices=ContractRelationRoleChoices, required=False)


class ACIContractRelationImportForm(NetBoxModelImportForm):
    aci_contract = forms.ModelChoiceField(queryset=ACIContract.objects.all(), to_field_name="name")
    aci_endpoint_group = forms.ModelChoiceField(
        queryset=ACIEndpointGroup.objects.all(), to_field_name="name", required=False
    )
    aci_endpoint_security_group = forms.ModelChoiceField(
        queryset=ACIEndpointSecurityGroup.objects.all(), to_field_name="name", required=False
    )
    aci_external_epg = forms.ModelChoiceField(
        queryset=ACIExternalEPG.objects.all(), to_field_name="name", required=False
    )
    role = forms.ChoiceField(choices=ContractRelationRoleChoices)

    class Meta:
        model = ACIContractRelation
        fields = (
            "aci_contract",
            "aci_endpoint_group",
            "aci_endpoint_security_group",
            "aci_external_epg",
            "role",
            "name",
            "name_alias",
            "description",
            "tags",
        )
