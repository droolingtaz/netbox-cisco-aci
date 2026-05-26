"""UI views for Interface Policy Groups (Phase 4)."""

from ..filtersets.access_groups import ACIInterfacePolicyGroupFilterSet
from ..forms.access_groups import (
    ACIInterfacePolicyGroupBulkEditForm,
    ACIInterfacePolicyGroupFilterForm,
    ACIInterfacePolicyGroupForm,
    ACIInterfacePolicyGroupImportForm,
)
from ..models.access import ACIInterfacePolicyGroup
from ..tables.access_groups import ACIInterfacePolicyGroupTable
from .access import _five_views

_pg = _five_views(
    ACIInterfacePolicyGroup,
    ACIInterfacePolicyGroupTable,
    ACIInterfacePolicyGroupFilterSet,
    ACIInterfacePolicyGroupFilterForm,
    ACIInterfacePolicyGroupForm,
    ACIInterfacePolicyGroupImportForm,
    ACIInterfacePolicyGroupBulkEditForm,
    select=(
        "aci_fabric",
        "link_level_policy",
        "cdp_policy",
        "lldp_policy",
        "lacp_policy",
        "mcp_policy",
        "stp_policy",
        "aaep",
    ),
)
ACIInterfacePolicyGroupView = _pg["view"]
ACIInterfacePolicyGroupListView = _pg["list"]
ACIInterfacePolicyGroupEditView = _pg["edit"]
ACIInterfacePolicyGroupDeleteView = _pg["delete"]
ACIInterfacePolicyGroupBulkImportView = _pg["bulk_import"]
ACIInterfacePolicyGroupBulkEditView = _pg["bulk_edit"]
ACIInterfacePolicyGroupBulkDeleteView = _pg["bulk_delete"]
