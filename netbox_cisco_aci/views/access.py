"""UI views for access-policy models (Phase 3)."""

from netbox.views import generic

from ..filtersets.access import (
    ACIAAEPEPGMappingFilterSet,
    ACIAAEPFilterSet,
    ACIDomainFilterSet,
    ACIVLANPoolBlockFilterSet,
    ACIVLANPoolFilterSet,
)
from ..forms.access import (
    ACIAAEPBulkEditForm,
    ACIAAEPEPGMappingBulkEditForm,
    ACIAAEPEPGMappingFilterForm,
    ACIAAEPEPGMappingForm,
    ACIAAEPEPGMappingImportForm,
    ACIAAEPFilterForm,
    ACIAAEPForm,
    ACIAAEPImportForm,
    ACIDomainBulkEditForm,
    ACIDomainFilterForm,
    ACIDomainForm,
    ACIDomainImportForm,
    ACIVLANPoolBlockBulkEditForm,
    ACIVLANPoolBlockFilterForm,
    ACIVLANPoolBlockForm,
    ACIVLANPoolBlockImportForm,
    ACIVLANPoolBulkEditForm,
    ACIVLANPoolFilterForm,
    ACIVLANPoolForm,
    ACIVLANPoolImportForm,
)
from ..models.access import (
    ACIAAEP,
    ACIAAEPEPGMapping,
    ACIDomain,
    ACIVLANPool,
    ACIVLANPoolBlock,
)
from ..tables.access import (
    ACIAAEPEPGMappingTable,
    ACIAAEPTable,
    ACIDomainTable,
    ACIVLANPoolBlockTable,
    ACIVLANPoolTable,
)


def _five_views(model, table, filterset, filter_form, form, import_form, bulk_edit_form, select=()):
    """Build standard list / detail / edit / delete / bulk views for a model."""

    base_qs = model.objects.all()
    if select:
        base_qs = model.objects.select_related(*select)
    return {
        "view": type(f"{model.__name__}View", (generic.ObjectView,), {"queryset": base_qs}),
        "list": type(
            f"{model.__name__}ListView",
            (generic.ObjectListView,),
            {
                "queryset": base_qs,
                "table": table,
                "filterset": filterset,
                "filterset_form": filter_form,
            },
        ),
        "edit": type(
            f"{model.__name__}EditView",
            (generic.ObjectEditView,),
            {"queryset": model.objects.all(), "form": form},
        ),
        "delete": type(
            f"{model.__name__}DeleteView",
            (generic.ObjectDeleteView,),
            {"queryset": model.objects.all()},
        ),
        "bulk_import": type(
            f"{model.__name__}BulkImportView",
            (generic.BulkImportView,),
            {"queryset": model.objects.all(), "model_form": import_form},
        ),
        "bulk_edit": type(
            f"{model.__name__}BulkEditView",
            (generic.BulkEditView,),
            {
                "queryset": model.objects.all(),
                "filterset": filterset,
                "table": table,
                "form": bulk_edit_form,
            },
        ),
        "bulk_delete": type(
            f"{model.__name__}BulkDeleteView",
            (generic.BulkDeleteView,),
            {"queryset": model.objects.all(), "filterset": filterset, "table": table},
        ),
    }


_pool = _five_views(
    ACIVLANPool,
    ACIVLANPoolTable,
    ACIVLANPoolFilterSet,
    ACIVLANPoolFilterForm,
    ACIVLANPoolForm,
    ACIVLANPoolImportForm,
    ACIVLANPoolBulkEditForm,
    select=("aci_fabric",),
)
ACIVLANPoolView = _pool["view"]
ACIVLANPoolListView = _pool["list"]
ACIVLANPoolEditView = _pool["edit"]
ACIVLANPoolDeleteView = _pool["delete"]
ACIVLANPoolBulkImportView = _pool["bulk_import"]
ACIVLANPoolBulkEditView = _pool["bulk_edit"]
ACIVLANPoolBulkDeleteView = _pool["bulk_delete"]

_block = _five_views(
    ACIVLANPoolBlock,
    ACIVLANPoolBlockTable,
    ACIVLANPoolBlockFilterSet,
    ACIVLANPoolBlockFilterForm,
    ACIVLANPoolBlockForm,
    ACIVLANPoolBlockImportForm,
    ACIVLANPoolBlockBulkEditForm,
    select=("aci_vlan_pool",),
)
ACIVLANPoolBlockView = _block["view"]
ACIVLANPoolBlockListView = _block["list"]
ACIVLANPoolBlockEditView = _block["edit"]
ACIVLANPoolBlockDeleteView = _block["delete"]
ACIVLANPoolBlockBulkImportView = _block["bulk_import"]
ACIVLANPoolBlockBulkEditView = _block["bulk_edit"]
ACIVLANPoolBlockBulkDeleteView = _block["bulk_delete"]

_domain = _five_views(
    ACIDomain,
    ACIDomainTable,
    ACIDomainFilterSet,
    ACIDomainFilterForm,
    ACIDomainForm,
    ACIDomainImportForm,
    ACIDomainBulkEditForm,
    select=("aci_fabric", "aci_vlan_pool"),
)
ACIDomainView = _domain["view"]
ACIDomainListView = _domain["list"]
ACIDomainEditView = _domain["edit"]
ACIDomainDeleteView = _domain["delete"]
ACIDomainBulkImportView = _domain["bulk_import"]
ACIDomainBulkEditView = _domain["bulk_edit"]
ACIDomainBulkDeleteView = _domain["bulk_delete"]

_aaep = _five_views(
    ACIAAEP,
    ACIAAEPTable,
    ACIAAEPFilterSet,
    ACIAAEPFilterForm,
    ACIAAEPForm,
    ACIAAEPImportForm,
    ACIAAEPBulkEditForm,
    select=("aci_fabric",),
)
ACIAAEPView = _aaep["view"]
ACIAAEPListView = _aaep["list"]
ACIAAEPEditView = _aaep["edit"]
ACIAAEPDeleteView = _aaep["delete"]
ACIAAEPBulkImportView = _aaep["bulk_import"]
ACIAAEPBulkEditView = _aaep["bulk_edit"]
ACIAAEPBulkDeleteView = _aaep["bulk_delete"]

_mapping = _five_views(
    ACIAAEPEPGMapping,
    ACIAAEPEPGMappingTable,
    ACIAAEPEPGMappingFilterSet,
    ACIAAEPEPGMappingFilterForm,
    ACIAAEPEPGMappingForm,
    ACIAAEPEPGMappingImportForm,
    ACIAAEPEPGMappingBulkEditForm,
    select=("aci_aaep", "aci_endpoint_group"),
)
ACIAAEPEPGMappingView = _mapping["view"]
ACIAAEPEPGMappingListView = _mapping["list"]
ACIAAEPEPGMappingEditView = _mapping["edit"]
ACIAAEPEPGMappingDeleteView = _mapping["delete"]
ACIAAEPEPGMappingBulkImportView = _mapping["bulk_import"]
ACIAAEPEPGMappingBulkEditView = _mapping["bulk_edit"]
ACIAAEPEPGMappingBulkDeleteView = _mapping["bulk_delete"]
