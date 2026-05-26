"""FilterSets for Phase 6 binding models."""

import django_filters
from dcim.models import Interface
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from ..choices import (
    InterfaceFabricRoleChoices,
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


class _SearchMixin:
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(name_alias__icontains=value)
            | Q(description__icontains=value)
        )


class ACIStaticPortBindingFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_endpoint_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIEndpointGroup.objects.all(),
        field_name="aci_endpoint_group",
        label="EPG (ID)",
    )
    dcim_interface_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Interface.objects.all(),
        field_name="dcim_interface",
        label="Interface (ID)",
    )
    binding_type = django_filters.MultipleChoiceFilter(choices=StaticPortBindingTypeChoices)
    mode = django_filters.MultipleChoiceFilter(choices=StaticPortModeChoices)

    class Meta:
        model = ACIStaticPortBinding
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "binding_type",
            "encap_vlan",
            "mode",
            "primary_encap_vlan",
            "deployment_immediacy",
        )


class ACIVPCBindingPairFilterSet(_SearchMixin, NetBoxModelFilterSet):
    binding_a_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIStaticPortBinding.objects.all(),
        field_name="binding_a",
        label="Binding A (ID)",
    )
    binding_b_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIStaticPortBinding.objects.all(),
        field_name="binding_b",
        label="Binding B (ID)",
    )

    class Meta:
        model = ACIVPCBindingPair
        fields = ("id", "name", "name_alias", "description")


class ACIDomainBindingFilterSet(_SearchMixin, NetBoxModelFilterSet):
    aci_endpoint_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIEndpointGroup.objects.all(),
        field_name="aci_endpoint_group",
        label="EPG (ID)",
    )
    aci_domain_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIDomain.objects.all(), field_name="aci_domain", label="Domain (ID)"
    )

    class Meta:
        model = ACIDomainBinding
        fields = (
            "id",
            "name",
            "name_alias",
            "description",
            "deployment_immediacy",
            "resolution_immediacy",
        )


class ACIInterfaceFabricMembershipFilterSet(_SearchMixin, NetBoxModelFilterSet):
    dcim_interface_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Interface.objects.all(),
        field_name="dcim_interface",
        label="Interface (ID)",
    )
    aci_node_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACINode.objects.all(), field_name="aci_node", label="Node (ID)"
    )
    interface_role = django_filters.MultipleChoiceFilter(choices=InterfaceFabricRoleChoices)

    class Meta:
        model = ACIInterfaceFabricMembership
        fields = ("id", "name", "name_alias", "description", "interface_role")
