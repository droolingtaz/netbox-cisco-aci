"""FilterSets for access-policy models (Phase 3)."""

import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

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


def _name_search(queryset, value):
    return queryset.filter(
        Q(name__icontains=value) | Q(name_alias__icontains=value) | Q(description__icontains=value)
    )


class ACIVLANPoolFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )
    allocation_mode = django_filters.MultipleChoiceFilter(choices=VLANPoolAllocationChoices)

    class Meta:
        model = ACIVLANPool
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIVLANPoolBlockFilterSet(NetBoxModelFilterSet):
    aci_vlan_pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIVLANPool.objects.all(),
        field_name="aci_vlan_pool",
        label="VLAN Pool (ID)",
    )
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(),
        field_name="aci_vlan_pool__aci_fabric",
        label="Fabric (ID)",
    )
    contains_vlan = django_filters.NumberFilter(method="filter_contains_vlan")

    class Meta:
        model = ACIVLANPoolBlock
        fields = ("id", "name", "from_vlan", "to_vlan", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    def filter_contains_vlan(self, queryset, name, value):
        """Filter blocks whose range covers the given VLAN ID."""
        return queryset.filter(from_vlan__lte=value, to_vlan__gte=value)


class ACIDomainFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )
    aci_vlan_pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIVLANPool.objects.all(),
        field_name="aci_vlan_pool",
        label="VLAN Pool (ID)",
    )
    domain_type = django_filters.MultipleChoiceFilter(choices=DomainTypeChoices)

    class Meta:
        model = ACIDomain
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIAAEPFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )
    aci_domain_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIDomain.objects.all(), field_name="domains", label="Domain (ID)"
    )

    class Meta:
        model = ACIAAEP
        fields = ("id", "name", "name_alias", "enable_infra_vlan", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIAAEPEPGMappingFilterSet(NetBoxModelFilterSet):
    aci_aaep_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIAAEP.objects.all(), field_name="aci_aaep", label="AAEP (ID)"
    )
    aci_endpoint_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIEndpointGroup.objects.all(),
        field_name="aci_endpoint_group",
        label="EPG (ID)",
    )
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(),
        field_name="aci_aaep__aci_fabric",
        label="Fabric (ID)",
    )
    mode = django_filters.MultipleChoiceFilter(choices=StaticPortModeChoices)

    class Meta:
        model = ACIAAEPEPGMapping
        fields = ("id", "name", "encap_vlan", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
