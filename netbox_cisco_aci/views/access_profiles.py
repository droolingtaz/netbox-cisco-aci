"""UI views for Switch / Interface Profiles + selectors + attachments (Phase 4)."""

from ..filtersets.access_profiles import (
    ACIInterfaceProfileFilterSet,
    ACIInterfaceProfileSelectorFilterSet,
    ACISwitchProfileFilterSet,
    ACISwitchProfileInterfaceProfileAttachmentFilterSet,
    ACISwitchProfileSelectorFilterSet,
)
from ..forms.access_profiles import (
    ACIInterfaceProfileBulkEditForm,
    ACIInterfaceProfileFilterForm,
    ACIInterfaceProfileForm,
    ACIInterfaceProfileImportForm,
    ACIInterfaceProfileSelectorBulkEditForm,
    ACIInterfaceProfileSelectorFilterForm,
    ACIInterfaceProfileSelectorForm,
    ACIInterfaceProfileSelectorImportForm,
    ACISwitchProfileBulkEditForm,
    ACISwitchProfileFilterForm,
    ACISwitchProfileForm,
    ACISwitchProfileImportForm,
    ACISwitchProfileInterfaceProfileAttachmentBulkEditForm,
    ACISwitchProfileInterfaceProfileAttachmentFilterForm,
    ACISwitchProfileInterfaceProfileAttachmentForm,
    ACISwitchProfileInterfaceProfileAttachmentImportForm,
    ACISwitchProfileSelectorBulkEditForm,
    ACISwitchProfileSelectorFilterForm,
    ACISwitchProfileSelectorForm,
    ACISwitchProfileSelectorImportForm,
)
from ..models.access import (
    ACIInterfaceProfile,
    ACIInterfaceProfileSelector,
    ACISwitchProfile,
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileSelector,
)
from ..tables.access_profiles import (
    ACIInterfaceProfileSelectorTable,
    ACIInterfaceProfileTable,
    ACISwitchProfileInterfaceProfileAttachmentTable,
    ACISwitchProfileSelectorTable,
    ACISwitchProfileTable,
)
from .access import _five_views

_sp = _five_views(
    ACISwitchProfile,
    ACISwitchProfileTable,
    ACISwitchProfileFilterSet,
    ACISwitchProfileFilterForm,
    ACISwitchProfileForm,
    ACISwitchProfileImportForm,
    ACISwitchProfileBulkEditForm,
    select=("aci_fabric",),
)
ACISwitchProfileView = _sp["view"]
ACISwitchProfileListView = _sp["list"]
ACISwitchProfileEditView = _sp["edit"]
ACISwitchProfileDeleteView = _sp["delete"]
ACISwitchProfileBulkImportView = _sp["bulk_import"]
ACISwitchProfileBulkEditView = _sp["bulk_edit"]
ACISwitchProfileBulkDeleteView = _sp["bulk_delete"]

_sps = _five_views(
    ACISwitchProfileSelector,
    ACISwitchProfileSelectorTable,
    ACISwitchProfileSelectorFilterSet,
    ACISwitchProfileSelectorFilterForm,
    ACISwitchProfileSelectorForm,
    ACISwitchProfileSelectorImportForm,
    ACISwitchProfileSelectorBulkEditForm,
    select=("switch_profile",),
)
ACISwitchProfileSelectorView = _sps["view"]
ACISwitchProfileSelectorListView = _sps["list"]
ACISwitchProfileSelectorEditView = _sps["edit"]
ACISwitchProfileSelectorDeleteView = _sps["delete"]
ACISwitchProfileSelectorBulkImportView = _sps["bulk_import"]
ACISwitchProfileSelectorBulkEditView = _sps["bulk_edit"]
ACISwitchProfileSelectorBulkDeleteView = _sps["bulk_delete"]

_ip = _five_views(
    ACIInterfaceProfile,
    ACIInterfaceProfileTable,
    ACIInterfaceProfileFilterSet,
    ACIInterfaceProfileFilterForm,
    ACIInterfaceProfileForm,
    ACIInterfaceProfileImportForm,
    ACIInterfaceProfileBulkEditForm,
    select=("aci_fabric",),
)
ACIInterfaceProfileView = _ip["view"]
ACIInterfaceProfileListView = _ip["list"]
ACIInterfaceProfileEditView = _ip["edit"]
ACIInterfaceProfileDeleteView = _ip["delete"]
ACIInterfaceProfileBulkImportView = _ip["bulk_import"]
ACIInterfaceProfileBulkEditView = _ip["bulk_edit"]
ACIInterfaceProfileBulkDeleteView = _ip["bulk_delete"]

_ips = _five_views(
    ACIInterfaceProfileSelector,
    ACIInterfaceProfileSelectorTable,
    ACIInterfaceProfileSelectorFilterSet,
    ACIInterfaceProfileSelectorFilterForm,
    ACIInterfaceProfileSelectorForm,
    ACIInterfaceProfileSelectorImportForm,
    ACIInterfaceProfileSelectorBulkEditForm,
    select=("interface_profile", "policy_group"),
)
ACIInterfaceProfileSelectorView = _ips["view"]
ACIInterfaceProfileSelectorListView = _ips["list"]
ACIInterfaceProfileSelectorEditView = _ips["edit"]
ACIInterfaceProfileSelectorDeleteView = _ips["delete"]
ACIInterfaceProfileSelectorBulkImportView = _ips["bulk_import"]
ACIInterfaceProfileSelectorBulkEditView = _ips["bulk_edit"]
ACIInterfaceProfileSelectorBulkDeleteView = _ips["bulk_delete"]

_att = _five_views(
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileInterfaceProfileAttachmentTable,
    ACISwitchProfileInterfaceProfileAttachmentFilterSet,
    ACISwitchProfileInterfaceProfileAttachmentFilterForm,
    ACISwitchProfileInterfaceProfileAttachmentForm,
    ACISwitchProfileInterfaceProfileAttachmentImportForm,
    ACISwitchProfileInterfaceProfileAttachmentBulkEditForm,
    select=("switch_profile", "interface_profile"),
)
ACISwitchProfileInterfaceProfileAttachmentView = _att["view"]
ACISwitchProfileInterfaceProfileAttachmentListView = _att["list"]
ACISwitchProfileInterfaceProfileAttachmentEditView = _att["edit"]
ACISwitchProfileInterfaceProfileAttachmentDeleteView = _att["delete"]
ACISwitchProfileInterfaceProfileAttachmentBulkImportView = _att["bulk_import"]
ACISwitchProfileInterfaceProfileAttachmentBulkEditView = _att["bulk_edit"]
ACISwitchProfileInterfaceProfileAttachmentBulkDeleteView = _att["bulk_delete"]
