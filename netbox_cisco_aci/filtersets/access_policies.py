"""FilterSets for the six per-policy interface refs (Phase 4)."""

import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from ..choices import (
    EnabledDisabledChoices,
    LACPModeChoices,
    LinkLevelAutoNegChoices,
    LinkLevelFECChoices,
    LinkLevelSpeedChoices,
)
from ..models.access import (
    ACICDPInterfacePolicy,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
)
from ..models.fabric import ACIFabric


def _name_search(queryset, value):
    return queryset.filter(
        Q(name__icontains=value) | Q(name_alias__icontains=value) | Q(description__icontains=value)
    )


def _fabric_id_filter():
    return django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )


class ACILinkLevelPolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = _fabric_id_filter()
    speed = django_filters.MultipleChoiceFilter(choices=LinkLevelSpeedChoices)
    auto_negotiation = django_filters.MultipleChoiceFilter(choices=LinkLevelAutoNegChoices)
    fec_mode = django_filters.MultipleChoiceFilter(choices=LinkLevelFECChoices)

    class Meta:
        model = ACILinkLevelPolicy
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACICDPInterfacePolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = _fabric_id_filter()
    admin_state = django_filters.MultipleChoiceFilter(choices=EnabledDisabledChoices)

    class Meta:
        model = ACICDPInterfacePolicy
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACILLDPInterfacePolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = _fabric_id_filter()
    receive_state = django_filters.MultipleChoiceFilter(choices=EnabledDisabledChoices)
    transmit_state = django_filters.MultipleChoiceFilter(choices=EnabledDisabledChoices)

    class Meta:
        model = ACILLDPInterfacePolicy
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACILACPInterfacePolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = _fabric_id_filter()
    mode = django_filters.MultipleChoiceFilter(choices=LACPModeChoices)

    class Meta:
        model = ACILACPInterfacePolicy
        fields = ("id", "name", "name_alias", "min_links", "max_links", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIMCPInterfacePolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = _fabric_id_filter()
    admin_state = django_filters.MultipleChoiceFilter(choices=EnabledDisabledChoices)

    class Meta:
        model = ACIMCPInterfacePolicy
        fields = ("id", "name", "name_alias", "strict_mode", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACISTPInterfacePolicyFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = _fabric_id_filter()

    class Meta:
        model = ACISTPInterfacePolicy
        fields = ("id", "name", "name_alias", "bpdu_filter", "bpdu_guard", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)
