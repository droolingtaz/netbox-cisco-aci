"""FilterSets for Phase 5 contract / filter / relation models."""

import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from ..choices import (
    ContractFilterEntryEtherTypeChoices,
    ContractFilterEntryIPProtocolChoices,
    ContractRelationRoleChoices,
    ContractScopeChoices,
    SubjectFilterActionChoices,
    SubjectFilterDirectionChoices,
)
from ..models.l3out import ACIExternalEPG
from ..models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from ..models.tenant import (
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
)


class _NameAliasDescriptionSearchMixin:
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(name_alias__icontains=value)
            | Q(description__icontains=value)
        )


class ACIContractFilterSet(_NameAliasDescriptionSearchMixin, NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    scope = django_filters.MultipleChoiceFilter(choices=ContractScopeChoices)

    class Meta:
        model = ACIContract
        fields = ("id", "name", "name_alias", "description", "scope", "qos_class")


class ACISubjectFilterSet(_NameAliasDescriptionSearchMixin, NetBoxModelFilterSet):
    aci_contract_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIContract.objects.all(), field_name="aci_contract", label="Contract (ID)"
    )

    class Meta:
        model = ACISubject
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "apply_both_directions",
            "reverse_filter_ports",
        )


class ACIFilterFilterSet(_NameAliasDescriptionSearchMixin, NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )

    class Meta:
        model = ACIFilter
        fields = ("id", "name", "name_alias", "description")


class ACIFilterEntryFilterSet(_NameAliasDescriptionSearchMixin, NetBoxModelFilterSet):
    aci_filter_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFilter.objects.all(), field_name="aci_filter", label="Filter (ID)"
    )
    ether_type = django_filters.MultipleChoiceFilter(choices=ContractFilterEntryEtherTypeChoices)
    ip_protocol = django_filters.MultipleChoiceFilter(choices=ContractFilterEntryIPProtocolChoices)

    class Meta:
        model = ACIFilterEntry
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "ether_type",
            "ip_protocol",
            "stateful",
            "match_only_fragments",
        )


class ACISubjectFilterFilterSet(_NameAliasDescriptionSearchMixin, NetBoxModelFilterSet):
    aci_subject_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISubject.objects.all(), field_name="aci_subject", label="Subject (ID)"
    )
    aci_filter_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFilter.objects.all(), field_name="aci_filter", label="Filter (ID)"
    )
    direction = django_filters.MultipleChoiceFilter(choices=SubjectFilterDirectionChoices)
    action = django_filters.MultipleChoiceFilter(choices=SubjectFilterActionChoices)

    class Meta:
        model = ACISubjectFilter
        fields = ("id", "name", "name_alias", "description", "direction", "action", "priority")


class ACIContractRelationFilterSet(_NameAliasDescriptionSearchMixin, NetBoxModelFilterSet):
    aci_contract_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIContract.objects.all(), field_name="aci_contract", label="Contract (ID)"
    )
    aci_endpoint_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIEndpointGroup.objects.all(),
        field_name="aci_endpoint_group",
        label="EPG (ID)",
    )
    aci_endpoint_security_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIEndpointSecurityGroup.objects.all(),
        field_name="aci_endpoint_security_group",
        label="ESG (ID)",
    )
    aci_external_epg_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIExternalEPG.objects.all(),
        field_name="aci_external_epg",
        label="External EPG (ID)",
    )
    role = django_filters.MultipleChoiceFilter(choices=ContractRelationRoleChoices)

    class Meta:
        model = ACIContractRelation
        fields = ("id", "name", "name_alias", "description", "role")
