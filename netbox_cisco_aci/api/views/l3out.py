"""DRF ViewSets for Phase 7 L3Out models."""

from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.l3out import (
    ACIBGPPeerFilterSet,
    ACIEIGRPInterfacePolicyFilterSet,
    ACIExternalEPGFilterSet,
    ACIExternalEPGSubnetFilterSet,
    ACIL3OutFilterSet,
    ACIL3OutInterfaceFilterSet,
    ACILogicalInterfaceProfileFilterSet,
    ACILogicalNodeFilterSet,
    ACILogicalNodeProfileFilterSet,
    ACIOSPFInterfaceAttachmentFilterSet,
    ACIOSPFInterfacePolicyFilterSet,
)
from ...models.l3out import (
    ACIBGPPeer,
    ACIEIGRPInterfacePolicy,
    ACIExternalEPG,
    ACIExternalEPGSubnet,
    ACIL3Out,
    ACIL3OutInterface,
    ACILogicalInterfaceProfile,
    ACILogicalNode,
    ACILogicalNodeProfile,
    ACIOSPFInterfaceAttachment,
    ACIOSPFInterfacePolicy,
)
from ..serializers.l3out import (
    ACIBGPPeerSerializer,
    ACIEIGRPInterfacePolicySerializer,
    ACIExternalEPGSerializer,
    ACIExternalEPGSubnetSerializer,
    ACIL3OutInterfaceSerializer,
    ACIL3OutSerializer,
    ACILogicalInterfaceProfileSerializer,
    ACILogicalNodeProfileSerializer,
    ACILogicalNodeSerializer,
    ACIOSPFInterfaceAttachmentSerializer,
    ACIOSPFInterfacePolicySerializer,
)


class ACIL3OutViewSet(NetBoxModelViewSet):
    queryset = ACIL3Out.objects.select_related("aci_tenant", "aci_vrf")
    serializer_class = ACIL3OutSerializer
    filterset_class = ACIL3OutFilterSet


class ACILogicalNodeProfileViewSet(NetBoxModelViewSet):
    queryset = ACILogicalNodeProfile.objects.select_related("aci_l3out", "aci_l3out__aci_tenant")
    serializer_class = ACILogicalNodeProfileSerializer
    filterset_class = ACILogicalNodeProfileFilterSet


class ACILogicalNodeViewSet(NetBoxModelViewSet):
    queryset = ACILogicalNode.objects.select_related(
        "aci_logical_node_profile",
        "aci_node",
        "aci_node__aci_pod",
    )
    serializer_class = ACILogicalNodeSerializer
    filterset_class = ACILogicalNodeFilterSet


class ACILogicalInterfaceProfileViewSet(NetBoxModelViewSet):
    queryset = ACILogicalInterfaceProfile.objects.select_related(
        "aci_logical_node_profile",
        "aci_logical_node_profile__aci_l3out",
    )
    serializer_class = ACILogicalInterfaceProfileSerializer
    filterset_class = ACILogicalInterfaceProfileFilterSet


class ACIL3OutInterfaceViewSet(NetBoxModelViewSet):
    queryset = ACIL3OutInterface.objects.select_related(
        "aci_logical_interface_profile",
        "dcim_interface",
        "dcim_interface__device",
    )
    serializer_class = ACIL3OutInterfaceSerializer
    filterset_class = ACIL3OutInterfaceFilterSet


class ACIBGPPeerViewSet(NetBoxModelViewSet):
    queryset = ACIBGPPeer.objects.select_related(
        "aci_logical_interface_profile",
        "aci_logical_node_profile",
    )
    serializer_class = ACIBGPPeerSerializer
    filterset_class = ACIBGPPeerFilterSet


class ACIOSPFInterfacePolicyViewSet(NetBoxModelViewSet):
    queryset = ACIOSPFInterfacePolicy.objects.select_related("aci_tenant")
    serializer_class = ACIOSPFInterfacePolicySerializer
    filterset_class = ACIOSPFInterfacePolicyFilterSet


class ACIOSPFInterfaceAttachmentViewSet(NetBoxModelViewSet):
    queryset = ACIOSPFInterfaceAttachment.objects.select_related(
        "aci_logical_interface_profile",
        "aci_ospf_interface_policy",
    )
    serializer_class = ACIOSPFInterfaceAttachmentSerializer
    filterset_class = ACIOSPFInterfaceAttachmentFilterSet


class ACIEIGRPInterfacePolicyViewSet(NetBoxModelViewSet):
    queryset = ACIEIGRPInterfacePolicy.objects.select_related("aci_tenant")
    serializer_class = ACIEIGRPInterfacePolicySerializer
    filterset_class = ACIEIGRPInterfacePolicyFilterSet


class ACIExternalEPGViewSet(NetBoxModelViewSet):
    queryset = ACIExternalEPG.objects.select_related("aci_l3out", "aci_l3out__aci_tenant")
    serializer_class = ACIExternalEPGSerializer
    filterset_class = ACIExternalEPGFilterSet


class ACIExternalEPGSubnetViewSet(NetBoxModelViewSet):
    queryset = ACIExternalEPGSubnet.objects.select_related("aci_external_epg")
    serializer_class = ACIExternalEPGSubnetSerializer
    filterset_class = ACIExternalEPGSubnetFilterSet
