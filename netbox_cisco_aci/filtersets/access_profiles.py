"""FilterSets for Switch / Interface Profiles + selectors + attachments (Phase 4)."""

import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

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


def _name_search(queryset, value):
    return queryset.filter(
        Q(name__icontains=value) | Q(name_alias__icontains=value) | Q(description__icontains=value)
    )


class ACISwitchProfileFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )

    class Meta:
        model = ACISwitchProfile
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACISwitchProfileSelectorFilterSet(NetBoxModelFilterSet):
    switch_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISwitchProfile.objects.all(),
        field_name="switch_profile",
        label="Switch Profile (ID)",
    )
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(),
        field_name="switch_profile__aci_fabric",
        label="Fabric (ID)",
    )
    selector_type = django_filters.MultipleChoiceFilter(choices=RangeAllChoices)

    class Meta:
        model = ACISwitchProfileSelector
        fields = ("id", "name", "from_node_id", "to_node_id", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class ACIInterfaceProfileFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )

    class Meta:
        model = ACIInterfaceProfile
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIInterfaceProfileSelectorFilterSet(NetBoxModelFilterSet):
    interface_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIInterfaceProfile.objects.all(),
        field_name="interface_profile",
        label="Interface Profile (ID)",
    )
    policy_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIInterfacePolicyGroup.objects.all(),
        field_name="policy_group",
        label="Policy Group (ID)",
    )
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(),
        field_name="interface_profile__aci_fabric",
        label="Fabric (ID)",
    )

    class Meta:
        model = ACIInterfaceProfileSelector
        fields = (
            "id",
            "name",
            "from_module",
            "from_port",
            "to_module",
            "to_port",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class ACISwitchProfileInterfaceProfileAttachmentFilterSet(NetBoxModelFilterSet):
    switch_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACISwitchProfile.objects.all(),
        field_name="switch_profile",
        label="Switch Profile (ID)",
    )
    interface_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIInterfaceProfile.objects.all(),
        field_name="interface_profile",
        label="Interface Profile (ID)",
    )

    class Meta:
        model = ACISwitchProfileInterfaceProfileAttachment
        fields = ("id",)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(switch_profile__name__icontains=value) | Q(interface_profile__name__icontains=value)
        )
