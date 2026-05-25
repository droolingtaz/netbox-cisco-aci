"""DRF ViewSets for access-policy models (Phase 3)."""

from django.db.models import Count
from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.access import (
    ACIAAEPEPGMappingFilterSet,
    ACIAAEPFilterSet,
    ACIDomainFilterSet,
    ACIVLANPoolBlockFilterSet,
    ACIVLANPoolFilterSet,
)
from ...models.access import (
    ACIAAEP,
    ACIAAEPEPGMapping,
    ACIDomain,
    ACIVLANPool,
    ACIVLANPoolBlock,
)
from ..serializers.access import (
    ACIAAEPEPGMappingSerializer,
    ACIAAEPSerializer,
    ACIDomainSerializer,
    ACIVLANPoolBlockSerializer,
    ACIVLANPoolSerializer,
)


class ACIVLANPoolViewSet(NetBoxModelViewSet):
    queryset = ACIVLANPool.objects.select_related("aci_fabric").annotate(
        block_count=Count("blocks", distinct=True),
        domain_count=Count("domains", distinct=True),
    )
    serializer_class = ACIVLANPoolSerializer
    filterset_class = ACIVLANPoolFilterSet


class ACIVLANPoolBlockViewSet(NetBoxModelViewSet):
    queryset = ACIVLANPoolBlock.objects.select_related("aci_vlan_pool")
    serializer_class = ACIVLANPoolBlockSerializer
    filterset_class = ACIVLANPoolBlockFilterSet


class ACIDomainViewSet(NetBoxModelViewSet):
    queryset = ACIDomain.objects.select_related("aci_fabric", "aci_vlan_pool")
    serializer_class = ACIDomainSerializer
    filterset_class = ACIDomainFilterSet


class ACIAAEPViewSet(NetBoxModelViewSet):
    queryset = (
        ACIAAEP.objects.select_related("aci_fabric")
        .prefetch_related("domains")
        .annotate(epg_mapping_count=Count("epg_mappings", distinct=True))
    )
    serializer_class = ACIAAEPSerializer
    filterset_class = ACIAAEPFilterSet


class ACIAAEPEPGMappingViewSet(NetBoxModelViewSet):
    queryset = ACIAAEPEPGMapping.objects.select_related("aci_aaep", "aci_endpoint_group")
    serializer_class = ACIAAEPEPGMappingSerializer
    filterset_class = ACIAAEPEPGMappingFilterSet
