"""DRF ViewSets for tenancy models."""

from django.db.models import Count
from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.tenant import (
    ACIAppProfileFilterSet,
    ACIBridgeDomainFilterSet,
    ACIBridgeDomainSubnetFilterSet,
    ACIEndpointGroupFilterSet,
    ACIEndpointSecurityGroupFilterSet,
    ACITenantFilterSet,
    ACIUSegAttributeFilterSet,
    ACIVRFFilterSet,
)
from ...models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
)
from ..serializers.tenant import (
    ACIAppProfileSerializer,
    ACIBridgeDomainSerializer,
    ACIBridgeDomainSubnetSerializer,
    ACIEndpointGroupSerializer,
    ACIEndpointSecurityGroupSerializer,
    ACITenantSerializer,
    ACIUSegAttributeSerializer,
    ACIVRFSerializer,
)


class ACITenantViewSet(NetBoxModelViewSet):
    queryset = ACITenant.objects.select_related("aci_fabric").annotate(
        vrf_count=Count("vrfs", distinct=True),
        bd_count=Count("bridge_domains", distinct=True),
        app_profile_count=Count("app_profiles", distinct=True),
    )
    serializer_class = ACITenantSerializer
    filterset_class = ACITenantFilterSet


class ACIVRFViewSet(NetBoxModelViewSet):
    queryset = ACIVRF.objects.select_related("aci_tenant", "nb_vrf")
    serializer_class = ACIVRFSerializer
    filterset_class = ACIVRFFilterSet


class ACIBridgeDomainViewSet(NetBoxModelViewSet):
    queryset = ACIBridgeDomain.objects.select_related("aci_tenant", "aci_vrf").annotate(
        subnet_count=Count("subnets")
    )
    serializer_class = ACIBridgeDomainSerializer
    filterset_class = ACIBridgeDomainFilterSet


class ACIBridgeDomainSubnetViewSet(NetBoxModelViewSet):
    queryset = ACIBridgeDomainSubnet.objects.select_related("aci_bridge_domain", "nb_prefix")
    serializer_class = ACIBridgeDomainSubnetSerializer
    filterset_class = ACIBridgeDomainSubnetFilterSet


class ACIAppProfileViewSet(NetBoxModelViewSet):
    queryset = ACIAppProfile.objects.select_related("aci_tenant").annotate(
        epg_count=Count("endpoint_groups")
    )
    serializer_class = ACIAppProfileSerializer
    filterset_class = ACIAppProfileFilterSet


class ACIEndpointGroupViewSet(NetBoxModelViewSet):
    queryset = ACIEndpointGroup.objects.select_related(
        "aci_tenant", "aci_app_profile", "aci_bridge_domain"
    )
    serializer_class = ACIEndpointGroupSerializer
    filterset_class = ACIEndpointGroupFilterSet


class ACIUSegAttributeViewSet(NetBoxModelViewSet):
    queryset = ACIUSegAttribute.objects.select_related("aci_endpoint_group")
    serializer_class = ACIUSegAttributeSerializer
    filterset_class = ACIUSegAttributeFilterSet


class ACIEndpointSecurityGroupViewSet(NetBoxModelViewSet):
    queryset = ACIEndpointSecurityGroup.objects.select_related(
        "aci_tenant", "aci_vrf", "aci_app_profile"
    )
    serializer_class = ACIEndpointSecurityGroupSerializer
    filterset_class = ACIEndpointSecurityGroupFilterSet
