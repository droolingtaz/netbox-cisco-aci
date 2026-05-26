"""DRF ViewSets for the six per-policy interface refs (Phase 4)."""

from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.access_policies import (
    ACICDPInterfacePolicyFilterSet,
    ACILACPInterfacePolicyFilterSet,
    ACILinkLevelPolicyFilterSet,
    ACILLDPInterfacePolicyFilterSet,
    ACIMCPInterfacePolicyFilterSet,
    ACISTPInterfacePolicyFilterSet,
)
from ...models.access import (
    ACICDPInterfacePolicy,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
)
from ..serializers.access_policies import (
    ACICDPInterfacePolicySerializer,
    ACILACPInterfacePolicySerializer,
    ACILinkLevelPolicySerializer,
    ACILLDPInterfacePolicySerializer,
    ACIMCPInterfacePolicySerializer,
    ACISTPInterfacePolicySerializer,
)


class ACILinkLevelPolicyViewSet(NetBoxModelViewSet):
    queryset = ACILinkLevelPolicy.objects.select_related("aci_fabric")
    serializer_class = ACILinkLevelPolicySerializer
    filterset_class = ACILinkLevelPolicyFilterSet


class ACICDPInterfacePolicyViewSet(NetBoxModelViewSet):
    queryset = ACICDPInterfacePolicy.objects.select_related("aci_fabric")
    serializer_class = ACICDPInterfacePolicySerializer
    filterset_class = ACICDPInterfacePolicyFilterSet


class ACILLDPInterfacePolicyViewSet(NetBoxModelViewSet):
    queryset = ACILLDPInterfacePolicy.objects.select_related("aci_fabric")
    serializer_class = ACILLDPInterfacePolicySerializer
    filterset_class = ACILLDPInterfacePolicyFilterSet


class ACILACPInterfacePolicyViewSet(NetBoxModelViewSet):
    queryset = ACILACPInterfacePolicy.objects.select_related("aci_fabric")
    serializer_class = ACILACPInterfacePolicySerializer
    filterset_class = ACILACPInterfacePolicyFilterSet


class ACIMCPInterfacePolicyViewSet(NetBoxModelViewSet):
    queryset = ACIMCPInterfacePolicy.objects.select_related("aci_fabric")
    serializer_class = ACIMCPInterfacePolicySerializer
    filterset_class = ACIMCPInterfacePolicyFilterSet


class ACISTPInterfacePolicyViewSet(NetBoxModelViewSet):
    queryset = ACISTPInterfacePolicy.objects.select_related("aci_fabric")
    serializer_class = ACISTPInterfacePolicySerializer
    filterset_class = ACISTPInterfacePolicyFilterSet
