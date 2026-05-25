"""DRF ViewSets for fabric-topology models."""

from django.db.models import Count
from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.fabric import ACIFabricFilterSet, ACINodeFilterSet, ACIPodFilterSet
from ...models.fabric import ACIFabric, ACINode, ACIPod
from ..serializers.fabric import (
    ACIFabricSerializer,
    ACINodeSerializer,
    ACIPodSerializer,
)


class ACIFabricViewSet(NetBoxModelViewSet):
    queryset = ACIFabric.objects.annotate(pod_count=Count("pods"))
    serializer_class = ACIFabricSerializer
    filterset_class = ACIFabricFilterSet


class ACIPodViewSet(NetBoxModelViewSet):
    queryset = ACIPod.objects.select_related("aci_fabric").annotate(node_count=Count("nodes"))
    serializer_class = ACIPodSerializer
    filterset_class = ACIPodFilterSet


class ACINodeViewSet(NetBoxModelViewSet):
    queryset = ACINode.objects.select_related("aci_pod", "aci_pod__aci_fabric")
    serializer_class = ACINodeSerializer
    filterset_class = ACINodeFilterSet
