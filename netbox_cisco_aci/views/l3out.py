"""UI views for Phase 7 L3Out models."""

from ..filtersets.l3out import (
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
from ..forms.l3out import (
    ACIBGPPeerBulkEditForm,
    ACIBGPPeerFilterForm,
    ACIBGPPeerForm,
    ACIBGPPeerImportForm,
    ACIEIGRPInterfacePolicyBulkEditForm,
    ACIEIGRPInterfacePolicyFilterForm,
    ACIEIGRPInterfacePolicyForm,
    ACIEIGRPInterfacePolicyImportForm,
    ACIExternalEPGBulkEditForm,
    ACIExternalEPGFilterForm,
    ACIExternalEPGForm,
    ACIExternalEPGImportForm,
    ACIExternalEPGSubnetBulkEditForm,
    ACIExternalEPGSubnetFilterForm,
    ACIExternalEPGSubnetForm,
    ACIExternalEPGSubnetImportForm,
    ACIL3OutBulkEditForm,
    ACIL3OutFilterForm,
    ACIL3OutForm,
    ACIL3OutImportForm,
    ACIL3OutInterfaceBulkEditForm,
    ACIL3OutInterfaceFilterForm,
    ACIL3OutInterfaceForm,
    ACIL3OutInterfaceImportForm,
    ACILogicalInterfaceProfileBulkEditForm,
    ACILogicalInterfaceProfileFilterForm,
    ACILogicalInterfaceProfileForm,
    ACILogicalInterfaceProfileImportForm,
    ACILogicalNodeBulkEditForm,
    ACILogicalNodeFilterForm,
    ACILogicalNodeForm,
    ACILogicalNodeImportForm,
    ACILogicalNodeProfileBulkEditForm,
    ACILogicalNodeProfileFilterForm,
    ACILogicalNodeProfileForm,
    ACILogicalNodeProfileImportForm,
    ACIOSPFInterfaceAttachmentBulkEditForm,
    ACIOSPFInterfaceAttachmentFilterForm,
    ACIOSPFInterfaceAttachmentForm,
    ACIOSPFInterfaceAttachmentImportForm,
    ACIOSPFInterfacePolicyBulkEditForm,
    ACIOSPFInterfacePolicyFilterForm,
    ACIOSPFInterfacePolicyForm,
    ACIOSPFInterfacePolicyImportForm,
)
from ..models.l3out import (
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
from ..tables.l3out import (
    ACIBGPPeerTable,
    ACIEIGRPInterfacePolicyTable,
    ACIExternalEPGSubnetTable,
    ACIExternalEPGTable,
    ACIL3OutInterfaceTable,
    ACIL3OutTable,
    ACILogicalInterfaceProfileTable,
    ACILogicalNodeProfileTable,
    ACILogicalNodeTable,
    ACIOSPFInterfaceAttachmentTable,
    ACIOSPFInterfacePolicyTable,
)
from .access import _five_views


def _bind(prefix, factory):
    """Bind the 7 standard view aliases into module namespace."""
    g = globals()
    g[f"{prefix}View"] = factory["view"]
    g[f"{prefix}ListView"] = factory["list"]
    g[f"{prefix}EditView"] = factory["edit"]
    g[f"{prefix}DeleteView"] = factory["delete"]
    g[f"{prefix}BulkImportView"] = factory["bulk_import"]
    g[f"{prefix}BulkEditView"] = factory["bulk_edit"]
    g[f"{prefix}BulkDeleteView"] = factory["bulk_delete"]


_bind(
    "ACIL3Out",
    _five_views(
        ACIL3Out,
        ACIL3OutTable,
        ACIL3OutFilterSet,
        ACIL3OutFilterForm,
        ACIL3OutForm,
        ACIL3OutImportForm,
        ACIL3OutBulkEditForm,
        select=("aci_tenant", "aci_vrf"),
    ),
)

_bind(
    "ACILogicalNodeProfile",
    _five_views(
        ACILogicalNodeProfile,
        ACILogicalNodeProfileTable,
        ACILogicalNodeProfileFilterSet,
        ACILogicalNodeProfileFilterForm,
        ACILogicalNodeProfileForm,
        ACILogicalNodeProfileImportForm,
        ACILogicalNodeProfileBulkEditForm,
        select=("aci_l3out", "aci_l3out__aci_tenant"),
    ),
)

_bind(
    "ACILogicalNode",
    _five_views(
        ACILogicalNode,
        ACILogicalNodeTable,
        ACILogicalNodeFilterSet,
        ACILogicalNodeFilterForm,
        ACILogicalNodeForm,
        ACILogicalNodeImportForm,
        ACILogicalNodeBulkEditForm,
        select=("aci_logical_node_profile", "aci_node"),
    ),
)

_bind(
    "ACILogicalInterfaceProfile",
    _five_views(
        ACILogicalInterfaceProfile,
        ACILogicalInterfaceProfileTable,
        ACILogicalInterfaceProfileFilterSet,
        ACILogicalInterfaceProfileFilterForm,
        ACILogicalInterfaceProfileForm,
        ACILogicalInterfaceProfileImportForm,
        ACILogicalInterfaceProfileBulkEditForm,
        select=("aci_logical_node_profile",),
    ),
)

_bind(
    "ACIL3OutInterface",
    _five_views(
        ACIL3OutInterface,
        ACIL3OutInterfaceTable,
        ACIL3OutInterfaceFilterSet,
        ACIL3OutInterfaceFilterForm,
        ACIL3OutInterfaceForm,
        ACIL3OutInterfaceImportForm,
        ACIL3OutInterfaceBulkEditForm,
        select=(
            "aci_logical_interface_profile",
            "dcim_interface",
            "dcim_interface__device",
        ),
    ),
)

_bind(
    "ACIBGPPeer",
    _five_views(
        ACIBGPPeer,
        ACIBGPPeerTable,
        ACIBGPPeerFilterSet,
        ACIBGPPeerFilterForm,
        ACIBGPPeerForm,
        ACIBGPPeerImportForm,
        ACIBGPPeerBulkEditForm,
        select=("aci_logical_interface_profile", "aci_logical_node_profile"),
    ),
)

_bind(
    "ACIOSPFInterfacePolicy",
    _five_views(
        ACIOSPFInterfacePolicy,
        ACIOSPFInterfacePolicyTable,
        ACIOSPFInterfacePolicyFilterSet,
        ACIOSPFInterfacePolicyFilterForm,
        ACIOSPFInterfacePolicyForm,
        ACIOSPFInterfacePolicyImportForm,
        ACIOSPFInterfacePolicyBulkEditForm,
        select=("aci_tenant",),
    ),
)

_bind(
    "ACIOSPFInterfaceAttachment",
    _five_views(
        ACIOSPFInterfaceAttachment,
        ACIOSPFInterfaceAttachmentTable,
        ACIOSPFInterfaceAttachmentFilterSet,
        ACIOSPFInterfaceAttachmentFilterForm,
        ACIOSPFInterfaceAttachmentForm,
        ACIOSPFInterfaceAttachmentImportForm,
        ACIOSPFInterfaceAttachmentBulkEditForm,
        select=("aci_logical_interface_profile", "aci_ospf_interface_policy"),
    ),
)

_bind(
    "ACIEIGRPInterfacePolicy",
    _five_views(
        ACIEIGRPInterfacePolicy,
        ACIEIGRPInterfacePolicyTable,
        ACIEIGRPInterfacePolicyFilterSet,
        ACIEIGRPInterfacePolicyFilterForm,
        ACIEIGRPInterfacePolicyForm,
        ACIEIGRPInterfacePolicyImportForm,
        ACIEIGRPInterfacePolicyBulkEditForm,
        select=("aci_tenant",),
    ),
)

_bind(
    "ACIExternalEPG",
    _five_views(
        ACIExternalEPG,
        ACIExternalEPGTable,
        ACIExternalEPGFilterSet,
        ACIExternalEPGFilterForm,
        ACIExternalEPGForm,
        ACIExternalEPGImportForm,
        ACIExternalEPGBulkEditForm,
        select=("aci_l3out", "aci_l3out__aci_tenant"),
    ),
)

_bind(
    "ACIExternalEPGSubnet",
    _five_views(
        ACIExternalEPGSubnet,
        ACIExternalEPGSubnetTable,
        ACIExternalEPGSubnetFilterSet,
        ACIExternalEPGSubnetFilterForm,
        ACIExternalEPGSubnetForm,
        ACIExternalEPGSubnetImportForm,
        ACIExternalEPGSubnetBulkEditForm,
        select=("aci_external_epg",),
    ),
)
