"""DRF ViewSets for Phase 6 binding models."""

from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.bindings import (
    ACIDomainBindingFilterSet,
    ACIInterfaceFabricMembershipFilterSet,
    ACIStaticPortBindingFilterSet,
    ACIVPCBindingPairFilterSet,
)
from ...models.bindings import (
    ACIDomainBinding,
    ACIInterfaceFabricMembership,
    ACIStaticPortBinding,
    ACIVPCBindingPair,
)
from ..serializers.bindings import (
    ACIDomainBindingSerializer,
    ACIInterfaceFabricMembershipSerializer,
    ACIStaticPortBindingSerializer,
    ACIVPCBindingPairSerializer,
)


class ACIStaticPortBindingViewSet(NetBoxModelViewSet):
    queryset = ACIStaticPortBinding.objects.select_related(
        "aci_endpoint_group",
        "aci_endpoint_group__aci_tenant",
        "dcim_interface",
        "dcim_interface__device",
    )
    serializer_class = ACIStaticPortBindingSerializer
    filterset_class = ACIStaticPortBindingFilterSet


class ACIVPCBindingPairViewSet(NetBoxModelViewSet):
    queryset = ACIVPCBindingPair.objects.select_related(
        "binding_a",
        "binding_a__aci_endpoint_group",
        "binding_a__dcim_interface",
        "binding_b",
        "binding_b__aci_endpoint_group",
        "binding_b__dcim_interface",
    )
    serializer_class = ACIVPCBindingPairSerializer
    filterset_class = ACIVPCBindingPairFilterSet


class ACIDomainBindingViewSet(NetBoxModelViewSet):
    queryset = ACIDomainBinding.objects.select_related(
        "aci_endpoint_group",
        "aci_endpoint_group__aci_tenant",
        "aci_domain",
    )
    serializer_class = ACIDomainBindingSerializer
    filterset_class = ACIDomainBindingFilterSet


class ACIInterfaceFabricMembershipViewSet(NetBoxModelViewSet):
    queryset = ACIInterfaceFabricMembership.objects.select_related(
        "dcim_interface",
        "dcim_interface__device",
        "aci_node",
        "aci_node__aci_pod",
        "aci_node__aci_pod__aci_fabric",
    )
    serializer_class = ACIInterfaceFabricMembershipSerializer
    filterset_class = ACIInterfaceFabricMembershipFilterSet
