"""FilterSet for ACI Interface Policy Groups (Phase 4)."""

import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from ..choices import InterfacePolicyGroupTypeChoices
from ..models.access import ACIAAEP, ACIInterfacePolicyGroup
from ..models.fabric import ACIFabric


class ACIInterfacePolicyGroupFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )
    pg_type = django_filters.MultipleChoiceFilter(choices=InterfacePolicyGroupTypeChoices)
    aaep_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIAAEP.objects.all(), field_name="aaep", label="AAEP (ID)"
    )

    class Meta:
        model = ACIInterfacePolicyGroup
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(name_alias__icontains=value)
            | Q(description__icontains=value)
        )
