"""UI views for the six per-policy interface refs (Phase 4)."""

from ..filtersets.access_policies import (
    ACICDPInterfacePolicyFilterSet,
    ACILACPInterfacePolicyFilterSet,
    ACILinkLevelPolicyFilterSet,
    ACILLDPInterfacePolicyFilterSet,
    ACIMCPInterfacePolicyFilterSet,
    ACISTPInterfacePolicyFilterSet,
)
from ..forms.access_policies import (
    ACICDPInterfacePolicyBulkEditForm,
    ACICDPInterfacePolicyFilterForm,
    ACICDPInterfacePolicyForm,
    ACICDPInterfacePolicyImportForm,
    ACILACPInterfacePolicyBulkEditForm,
    ACILACPInterfacePolicyFilterForm,
    ACILACPInterfacePolicyForm,
    ACILACPInterfacePolicyImportForm,
    ACILinkLevelPolicyBulkEditForm,
    ACILinkLevelPolicyFilterForm,
    ACILinkLevelPolicyForm,
    ACILinkLevelPolicyImportForm,
    ACILLDPInterfacePolicyBulkEditForm,
    ACILLDPInterfacePolicyFilterForm,
    ACILLDPInterfacePolicyForm,
    ACILLDPInterfacePolicyImportForm,
    ACIMCPInterfacePolicyBulkEditForm,
    ACIMCPInterfacePolicyFilterForm,
    ACIMCPInterfacePolicyForm,
    ACIMCPInterfacePolicyImportForm,
    ACISTPInterfacePolicyBulkEditForm,
    ACISTPInterfacePolicyFilterForm,
    ACISTPInterfacePolicyForm,
    ACISTPInterfacePolicyImportForm,
)
from ..models.access import (
    ACICDPInterfacePolicy,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
)
from ..tables.access_policies import (
    ACICDPInterfacePolicyTable,
    ACILACPInterfacePolicyTable,
    ACILinkLevelPolicyTable,
    ACILLDPInterfacePolicyTable,
    ACIMCPInterfacePolicyTable,
    ACISTPInterfacePolicyTable,
)
from .access import _five_views

_link = _five_views(
    ACILinkLevelPolicy,
    ACILinkLevelPolicyTable,
    ACILinkLevelPolicyFilterSet,
    ACILinkLevelPolicyFilterForm,
    ACILinkLevelPolicyForm,
    ACILinkLevelPolicyImportForm,
    ACILinkLevelPolicyBulkEditForm,
    select=("aci_fabric",),
)
ACILinkLevelPolicyView = _link["view"]
ACILinkLevelPolicyListView = _link["list"]
ACILinkLevelPolicyEditView = _link["edit"]
ACILinkLevelPolicyDeleteView = _link["delete"]
ACILinkLevelPolicyBulkImportView = _link["bulk_import"]
ACILinkLevelPolicyBulkEditView = _link["bulk_edit"]
ACILinkLevelPolicyBulkDeleteView = _link["bulk_delete"]

_cdp = _five_views(
    ACICDPInterfacePolicy,
    ACICDPInterfacePolicyTable,
    ACICDPInterfacePolicyFilterSet,
    ACICDPInterfacePolicyFilterForm,
    ACICDPInterfacePolicyForm,
    ACICDPInterfacePolicyImportForm,
    ACICDPInterfacePolicyBulkEditForm,
    select=("aci_fabric",),
)
ACICDPInterfacePolicyView = _cdp["view"]
ACICDPInterfacePolicyListView = _cdp["list"]
ACICDPInterfacePolicyEditView = _cdp["edit"]
ACICDPInterfacePolicyDeleteView = _cdp["delete"]
ACICDPInterfacePolicyBulkImportView = _cdp["bulk_import"]
ACICDPInterfacePolicyBulkEditView = _cdp["bulk_edit"]
ACICDPInterfacePolicyBulkDeleteView = _cdp["bulk_delete"]

_lldp = _five_views(
    ACILLDPInterfacePolicy,
    ACILLDPInterfacePolicyTable,
    ACILLDPInterfacePolicyFilterSet,
    ACILLDPInterfacePolicyFilterForm,
    ACILLDPInterfacePolicyForm,
    ACILLDPInterfacePolicyImportForm,
    ACILLDPInterfacePolicyBulkEditForm,
    select=("aci_fabric",),
)
ACILLDPInterfacePolicyView = _lldp["view"]
ACILLDPInterfacePolicyListView = _lldp["list"]
ACILLDPInterfacePolicyEditView = _lldp["edit"]
ACILLDPInterfacePolicyDeleteView = _lldp["delete"]
ACILLDPInterfacePolicyBulkImportView = _lldp["bulk_import"]
ACILLDPInterfacePolicyBulkEditView = _lldp["bulk_edit"]
ACILLDPInterfacePolicyBulkDeleteView = _lldp["bulk_delete"]

_lacp = _five_views(
    ACILACPInterfacePolicy,
    ACILACPInterfacePolicyTable,
    ACILACPInterfacePolicyFilterSet,
    ACILACPInterfacePolicyFilterForm,
    ACILACPInterfacePolicyForm,
    ACILACPInterfacePolicyImportForm,
    ACILACPInterfacePolicyBulkEditForm,
    select=("aci_fabric",),
)
ACILACPInterfacePolicyView = _lacp["view"]
ACILACPInterfacePolicyListView = _lacp["list"]
ACILACPInterfacePolicyEditView = _lacp["edit"]
ACILACPInterfacePolicyDeleteView = _lacp["delete"]
ACILACPInterfacePolicyBulkImportView = _lacp["bulk_import"]
ACILACPInterfacePolicyBulkEditView = _lacp["bulk_edit"]
ACILACPInterfacePolicyBulkDeleteView = _lacp["bulk_delete"]

_mcp = _five_views(
    ACIMCPInterfacePolicy,
    ACIMCPInterfacePolicyTable,
    ACIMCPInterfacePolicyFilterSet,
    ACIMCPInterfacePolicyFilterForm,
    ACIMCPInterfacePolicyForm,
    ACIMCPInterfacePolicyImportForm,
    ACIMCPInterfacePolicyBulkEditForm,
    select=("aci_fabric",),
)
ACIMCPInterfacePolicyView = _mcp["view"]
ACIMCPInterfacePolicyListView = _mcp["list"]
ACIMCPInterfacePolicyEditView = _mcp["edit"]
ACIMCPInterfacePolicyDeleteView = _mcp["delete"]
ACIMCPInterfacePolicyBulkImportView = _mcp["bulk_import"]
ACIMCPInterfacePolicyBulkEditView = _mcp["bulk_edit"]
ACIMCPInterfacePolicyBulkDeleteView = _mcp["bulk_delete"]

_stp = _five_views(
    ACISTPInterfacePolicy,
    ACISTPInterfacePolicyTable,
    ACISTPInterfacePolicyFilterSet,
    ACISTPInterfacePolicyFilterForm,
    ACISTPInterfacePolicyForm,
    ACISTPInterfacePolicyImportForm,
    ACISTPInterfacePolicyBulkEditForm,
    select=("aci_fabric",),
)
ACISTPInterfacePolicyView = _stp["view"]
ACISTPInterfacePolicyListView = _stp["list"]
ACISTPInterfacePolicyEditView = _stp["edit"]
ACISTPInterfacePolicyDeleteView = _stp["delete"]
ACISTPInterfacePolicyBulkImportView = _stp["bulk_import"]
ACISTPInterfacePolicyBulkEditView = _stp["bulk_edit"]
ACISTPInterfacePolicyBulkDeleteView = _stp["bulk_delete"]
