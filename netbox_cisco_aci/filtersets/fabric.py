"""FilterSets for fabric-topology models."""

import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from ..choices import NodeRoleChoices, NodeTypeChoices
from ..models.fabric import ACIFabric, ACINode, ACIPod


class ACIFabricFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ACIFabric
        fields = ("id", "name", "name_alias", "fabric_id", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(name_alias__icontains=value)
            | Q(description__icontains=value)
        )


class ACIPodFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(),
        field_name="aci_fabric",
        label="Fabric (ID)",
    )
    aci_fabric = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(),
        field_name="aci_fabric__name",
        to_field_name="name",
        label="Fabric (name)",
    )

    class Meta:
        model = ACIPod
        fields = ("id", "name", "name_alias", "pod_id", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(name_alias__icontains=value)
            | Q(description__icontains=value)
        )


class ACINodeFilterSet(NetBoxModelFilterSet):
    aci_pod_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIPod.objects.all(),
        field_name="aci_pod",
        label="Pod (ID)",
    )
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(),
        field_name="aci_pod__aci_fabric",
        label="Fabric (ID)",
    )
    role = django_filters.MultipleChoiceFilter(choices=NodeRoleChoices)
    node_type = django_filters.MultipleChoiceFilter(choices=NodeTypeChoices)

    class Meta:
        model = ACINode
        fields = (
            "id",
            "name",
            "name_alias",
            "node_id",
            "serial_number",
            "pod_tep_pool",
            "firmware_version",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(name_alias__icontains=value)
            | Q(serial_number__icontains=value)
            | Q(description__icontains=value)
        )
