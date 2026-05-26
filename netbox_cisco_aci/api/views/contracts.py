"""DRF ViewSets for Phase 5 contract / filter / relation models."""

from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.contracts import (
    ACIContractFilterSet,
    ACIContractRelationFilterSet,
    ACIFilterEntryFilterSet,
    ACIFilterFilterSet,
    ACISubjectFilterFilterSet,
    ACISubjectFilterSet,
)
from ...models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from ..serializers.contracts import (
    ACIContractRelationSerializer,
    ACIContractSerializer,
    ACIFilterEntrySerializer,
    ACIFilterSerializer,
    ACISubjectFilterSerializer,
    ACISubjectSerializer,
)


class ACIContractViewSet(NetBoxModelViewSet):
    queryset = ACIContract.objects.select_related("aci_tenant")
    serializer_class = ACIContractSerializer
    filterset_class = ACIContractFilterSet


class ACIFilterViewSet(NetBoxModelViewSet):
    queryset = ACIFilter.objects.select_related("aci_tenant")
    serializer_class = ACIFilterSerializer
    filterset_class = ACIFilterFilterSet


class ACIFilterEntryViewSet(NetBoxModelViewSet):
    queryset = ACIFilterEntry.objects.select_related("aci_filter", "aci_filter__aci_tenant")
    serializer_class = ACIFilterEntrySerializer
    filterset_class = ACIFilterEntryFilterSet


class ACISubjectViewSet(NetBoxModelViewSet):
    queryset = ACISubject.objects.select_related("aci_contract", "aci_contract__aci_tenant")
    serializer_class = ACISubjectSerializer
    filterset_class = ACISubjectFilterSet


class ACISubjectFilterViewSet(NetBoxModelViewSet):
    queryset = ACISubjectFilter.objects.select_related("aci_subject", "aci_filter")
    serializer_class = ACISubjectFilterSerializer
    filterset_class = ACISubjectFilterFilterSet


class ACIContractRelationViewSet(NetBoxModelViewSet):
    queryset = ACIContractRelation.objects.select_related(
        "aci_contract", "aci_endpoint_group", "aci_endpoint_security_group"
    )
    serializer_class = ACIContractRelationSerializer
    filterset_class = ACIContractRelationFilterSet
