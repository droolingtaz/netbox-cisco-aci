"""FilterSets for tenancy models."""

import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from ..choices import (
    BDL2UnknownUnicastChoices,
    QualityOfServiceClassChoices,
    USegAttributeTypeChoices,
    VRFPolicyEnforcementChoices,
    VRFPolicyEnforcementPreferenceChoices,
)
from ..models.fabric import ACIFabric
from ..models.tenant import (
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
    ACIVRF,
)


def _name_search(queryset, value):
    return queryset.filter(
        Q(name__icontains=value)
        | Q(name_alias__icontains=value)
        | Q(description__icontains=value)
    )


class ACITenantFilterSet(NetBoxModelFilterSet):
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(), field_name="aci_fabric", label="Fabric (ID)"
    )

    class Meta:
        model = ACITenant
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIVRFFilterSet(NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    aci_fabric_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIFabric.objects.all(),
        field_name="aci_tenant__aci_fabric",
        label="Fabric (ID)",
    )
    policy_enforcement_preference = django_filters.MultipleChoiceFilter(
        choices=VRFPolicyEnforcementPreferenceChoices
    )
    policy_enforcement_direction = django_filters.MultipleChoiceFilter(
        choices=VRFPolicyEnforcementChoices
    )

    class Meta:
        model = ACIVRF
        fields = (
            "id",
            "name",
            "name_alias",
            "bd_enforcement_enabled",
            "preferred_group_enabled",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIBridgeDomainFilterSet(NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    aci_vrf_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIVRF.objects.all(), field_name="aci_vrf", label="VRF (ID)"
    )
    l2_unknown_unicast = django_filters.MultipleChoiceFilter(choices=BDL2UnknownUnicastChoices)

    class Meta:
        model = ACIBridgeDomain
        fields = (
            "id",
            "name",
            "name_alias",
            "unicast_routing_enabled",
            "arp_flooding_enabled",
            "limit_ip_learn_to_subnets",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIBridgeDomainSubnetFilterSet(NetBoxModelFilterSet):
    aci_bridge_domain_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIBridgeDomain.objects.all(),
        field_name="aci_bridge_domain",
        label="Bridge Domain (ID)",
    )

    class Meta:
        model = ACIBridgeDomainSubnet
        fields = (
            "id",
            "name",
            "gateway_ip",
            "scope_public",
            "scope_shared",
            "scope_private",
            "is_primary",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(gateway_ip__icontains=value)
            | Q(name__icontains=value)
            | Q(description__icontains=value)
        )


class ACIAppProfileFilterSet(NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )

    class Meta:
        model = ACIAppProfile
        fields = ("id", "name", "name_alias", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIEndpointGroupFilterSet(NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    aci_app_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIAppProfile.objects.all(),
        field_name="aci_app_profile",
        label="App Profile (ID)",
    )
    aci_bridge_domain_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIBridgeDomain.objects.all(),
        field_name="aci_bridge_domain",
        label="Bridge Domain (ID)",
    )
    qos_class = django_filters.MultipleChoiceFilter(choices=QualityOfServiceClassChoices)

    class Meta:
        model = ACIEndpointGroup
        fields = (
            "id",
            "name",
            "name_alias",
            "is_useg",
            "admin_shutdown",
            "intra_epg_isolation",
            "preferred_group_member",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)


class ACIUSegAttributeFilterSet(NetBoxModelFilterSet):
    aci_endpoint_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIEndpointGroup.objects.all(),
        field_name="aci_endpoint_group",
        label="EPG (ID)",
    )
    attribute_type = django_filters.MultipleChoiceFilter(choices=USegAttributeTypeChoices)

    class Meta:
        model = ACIUSegAttribute
        fields = ("id", "name", "match_value", "description")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(match_value__icontains=value)
            | Q(description__icontains=value)
        )


class ACIEndpointSecurityGroupFilterSet(NetBoxModelFilterSet):
    aci_tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACITenant.objects.all(), field_name="aci_tenant", label="Tenant (ID)"
    )
    aci_vrf_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIVRF.objects.all(), field_name="aci_vrf", label="VRF (ID)"
    )
    aci_app_profile_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ACIAppProfile.objects.all(),
        field_name="aci_app_profile",
        label="App Profile (ID)",
    )
    qos_class = django_filters.MultipleChoiceFilter(choices=QualityOfServiceClassChoices)

    class Meta:
        model = ACIEndpointSecurityGroup
        fields = (
            "id",
            "name",
            "name_alias",
            "admin_shutdown",
            "preferred_group_member",
            "intra_esg_isolation",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return _name_search(queryset, value)
