"""UI views for Phase 5 contract / filter / relation models."""

from ..filtersets.contracts import (
    ACIContractFilterSet,
    ACIContractRelationFilterSet,
    ACIFilterEntryFilterSet,
    ACIFilterFilterSet,
    ACISubjectFilterFilterSet,
    ACISubjectFilterSet,
)
from ..forms.contracts import (
    ACIContractBulkEditForm,
    ACIContractFilterForm,
    ACIContractForm,
    ACIContractImportForm,
    ACIContractRelationBulkEditForm,
    ACIContractRelationFilterForm,
    ACIContractRelationForm,
    ACIContractRelationImportForm,
    ACIFilterBulkEditForm,
    ACIFilterEntryBulkEditForm,
    ACIFilterEntryFilterForm,
    ACIFilterEntryForm,
    ACIFilterEntryImportForm,
    ACIFilterFilterForm,
    ACIFilterForm,
    ACIFilterImportForm,
    ACISubjectBulkEditForm,
    ACISubjectFilterBulkEditForm,
    ACISubjectFilterFilterSetForm,
    ACISubjectFilterForm,
    ACISubjectFilterImportForm,
    ACISubjectFilterSetForm,
    ACISubjectForm,
    ACISubjectImportForm,
)
from ..models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from ..tables.contracts import (
    ACIContractRelationTable,
    ACIContractTable,
    ACIFilterEntryTable,
    ACIFilterTable,
    ACISubjectFilterTable,
    ACISubjectTable,
)
from .access import _five_views

_contract = _five_views(
    ACIContract,
    ACIContractTable,
    ACIContractFilterSet,
    ACIContractFilterForm,
    ACIContractForm,
    ACIContractImportForm,
    ACIContractBulkEditForm,
    select=("aci_tenant",),
)
ACIContractView = _contract["view"]
ACIContractListView = _contract["list"]
ACIContractEditView = _contract["edit"]
ACIContractDeleteView = _contract["delete"]
ACIContractBulkImportView = _contract["bulk_import"]
ACIContractBulkEditView = _contract["bulk_edit"]
ACIContractBulkDeleteView = _contract["bulk_delete"]

_subject = _five_views(
    ACISubject,
    ACISubjectTable,
    ACISubjectFilterSet,
    ACISubjectFilterSetForm,
    ACISubjectForm,
    ACISubjectImportForm,
    ACISubjectBulkEditForm,
    select=("aci_contract", "aci_contract__aci_tenant"),
)
ACISubjectView = _subject["view"]
ACISubjectListView = _subject["list"]
ACISubjectEditView = _subject["edit"]
ACISubjectDeleteView = _subject["delete"]
ACISubjectBulkImportView = _subject["bulk_import"]
ACISubjectBulkEditView = _subject["bulk_edit"]
ACISubjectBulkDeleteView = _subject["bulk_delete"]

_filter = _five_views(
    ACIFilter,
    ACIFilterTable,
    ACIFilterFilterSet,
    ACIFilterFilterForm,
    ACIFilterForm,
    ACIFilterImportForm,
    ACIFilterBulkEditForm,
    select=("aci_tenant",),
)
ACIFilterView = _filter["view"]
ACIFilterListView = _filter["list"]
ACIFilterEditView = _filter["edit"]
ACIFilterDeleteView = _filter["delete"]
ACIFilterBulkImportView = _filter["bulk_import"]
ACIFilterBulkEditView = _filter["bulk_edit"]
ACIFilterBulkDeleteView = _filter["bulk_delete"]

_filter_entry = _five_views(
    ACIFilterEntry,
    ACIFilterEntryTable,
    ACIFilterEntryFilterSet,
    ACIFilterEntryFilterForm,
    ACIFilterEntryForm,
    ACIFilterEntryImportForm,
    ACIFilterEntryBulkEditForm,
    select=("aci_filter", "aci_filter__aci_tenant"),
)
ACIFilterEntryView = _filter_entry["view"]
ACIFilterEntryListView = _filter_entry["list"]
ACIFilterEntryEditView = _filter_entry["edit"]
ACIFilterEntryDeleteView = _filter_entry["delete"]
ACIFilterEntryBulkImportView = _filter_entry["bulk_import"]
ACIFilterEntryBulkEditView = _filter_entry["bulk_edit"]
ACIFilterEntryBulkDeleteView = _filter_entry["bulk_delete"]

_subject_filter = _five_views(
    ACISubjectFilter,
    ACISubjectFilterTable,
    ACISubjectFilterFilterSet,
    ACISubjectFilterFilterSetForm,
    ACISubjectFilterForm,
    ACISubjectFilterImportForm,
    ACISubjectFilterBulkEditForm,
    select=("aci_subject", "aci_filter"),
)
ACISubjectFilterView = _subject_filter["view"]
ACISubjectFilterListView = _subject_filter["list"]
ACISubjectFilterEditView = _subject_filter["edit"]
ACISubjectFilterDeleteView = _subject_filter["delete"]
ACISubjectFilterBulkImportView = _subject_filter["bulk_import"]
ACISubjectFilterBulkEditView = _subject_filter["bulk_edit"]
ACISubjectFilterBulkDeleteView = _subject_filter["bulk_delete"]

_relation = _five_views(
    ACIContractRelation,
    ACIContractRelationTable,
    ACIContractRelationFilterSet,
    ACIContractRelationFilterForm,
    ACIContractRelationForm,
    ACIContractRelationImportForm,
    ACIContractRelationBulkEditForm,
    select=(
        "aci_contract",
        "aci_endpoint_group",
        "aci_endpoint_security_group",
        "aci_external_epg",
    ),
)
ACIContractRelationView = _relation["view"]
ACIContractRelationListView = _relation["list"]
ACIContractRelationEditView = _relation["edit"]
ACIContractRelationDeleteView = _relation["delete"]
ACIContractRelationBulkImportView = _relation["bulk_import"]
ACIContractRelationBulkEditView = _relation["bulk_edit"]
ACIContractRelationBulkDeleteView = _relation["bulk_delete"]
