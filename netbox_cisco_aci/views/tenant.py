"""UI views for tenancy models."""

from netbox.views import generic

from ..filtersets.tenant import (
    ACIAppProfileFilterSet,
    ACIBridgeDomainFilterSet,
    ACIBridgeDomainSubnetFilterSet,
    ACIEndpointGroupFilterSet,
    ACIEndpointSecurityGroupFilterSet,
    ACITenantFilterSet,
    ACIUSegAttributeFilterSet,
    ACIVRFFilterSet,
)
from ..forms.tenant import (
    ACIAppProfileBulkEditForm,
    ACIAppProfileFilterForm,
    ACIAppProfileForm,
    ACIAppProfileImportForm,
    ACIBridgeDomainBulkEditForm,
    ACIBridgeDomainFilterForm,
    ACIBridgeDomainForm,
    ACIBridgeDomainImportForm,
    ACIBridgeDomainSubnetBulkEditForm,
    ACIBridgeDomainSubnetFilterForm,
    ACIBridgeDomainSubnetForm,
    ACIBridgeDomainSubnetImportForm,
    ACIEndpointGroupBulkEditForm,
    ACIEndpointGroupFilterForm,
    ACIEndpointGroupForm,
    ACIEndpointGroupImportForm,
    ACIEndpointSecurityGroupBulkEditForm,
    ACIEndpointSecurityGroupFilterForm,
    ACIEndpointSecurityGroupForm,
    ACIEndpointSecurityGroupImportForm,
    ACITenantBulkEditForm,
    ACITenantFilterForm,
    ACITenantForm,
    ACITenantImportForm,
    ACIUSegAttributeBulkEditForm,
    ACIUSegAttributeFilterForm,
    ACIUSegAttributeForm,
    ACIUSegAttributeImportForm,
    ACIVRFBulkEditForm,
    ACIVRFFilterForm,
    ACIVRFForm,
    ACIVRFImportForm,
)
from ..models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
)
from ..tables.tenant import (
    ACIAppProfileTable,
    ACIBridgeDomainSubnetTable,
    ACIBridgeDomainTable,
    ACIEndpointGroupTable,
    ACIEndpointSecurityGroupTable,
    ACITenantTable,
    ACIUSegAttributeTable,
    ACIVRFTable,
)


def _five_views(
    model,
    table,
    filterset,
    filter_form,
    form,
    import_form,
    bulk_edit_form,
    select=(),
):
    """Build a standard ObjectView/List/Edit/Delete bundle for a model.

    Returns a dict keyed by `view`, `list`, `edit`, `delete`,
    `bulk_import`, `bulk_edit`, `bulk_delete` so callers can register
    them by name.
    """

    base_qs = model.objects.all()
    if select:
        base_qs = model.objects.select_related(*select)

    detail_view = type(
        f"{model.__name__}View",
        (generic.ObjectView,),
        {"queryset": base_qs},
    )
    list_view = type(
        f"{model.__name__}ListView",
        (generic.ObjectListView,),
        {
            "queryset": base_qs,
            "table": table,
            "filterset": filterset,
            "filterset_form": filter_form,
        },
    )
    edit_view = type(
        f"{model.__name__}EditView",
        (generic.ObjectEditView,),
        {"queryset": model.objects.all(), "form": form},
    )
    delete_view = type(
        f"{model.__name__}DeleteView",
        (generic.ObjectDeleteView,),
        {"queryset": model.objects.all()},
    )
    bulk_import_view = type(
        f"{model.__name__}BulkImportView",
        (generic.BulkImportView,),
        {"queryset": model.objects.all(), "model_form": import_form},
    )
    bulk_edit_view = type(
        f"{model.__name__}BulkEditView",
        (generic.BulkEditView,),
        {
            "queryset": model.objects.all(),
            "filterset": filterset,
            "table": table,
            "form": bulk_edit_form,
        },
    )
    bulk_delete_view = type(
        f"{model.__name__}BulkDeleteView",
        (generic.BulkDeleteView,),
        {
            "queryset": model.objects.all(),
            "filterset": filterset,
            "table": table,
        },
    )

    return {
        "view": detail_view,
        "list": list_view,
        "edit": edit_view,
        "delete": delete_view,
        "bulk_import": bulk_import_view,
        "bulk_edit": bulk_edit_view,
        "bulk_delete": bulk_delete_view,
    }


# ---------------------------------------------------------------------------
# Generate one bundle per tenancy model. The dynamic class generation
# keeps this file readable; ``urls.py`` references each class by name.
# ---------------------------------------------------------------------------

_tenant = _five_views(
    ACITenant,
    ACITenantTable,
    ACITenantFilterSet,
    ACITenantFilterForm,
    ACITenantForm,
    ACITenantImportForm,
    ACITenantBulkEditForm,
    select=("aci_fabric",),
)
ACITenantView = _tenant["view"]
ACITenantListView = _tenant["list"]
ACITenantEditView = _tenant["edit"]
ACITenantDeleteView = _tenant["delete"]
ACITenantBulkImportView = _tenant["bulk_import"]
ACITenantBulkEditView = _tenant["bulk_edit"]
ACITenantBulkDeleteView = _tenant["bulk_delete"]

_vrf = _five_views(
    ACIVRF,
    ACIVRFTable,
    ACIVRFFilterSet,
    ACIVRFFilterForm,
    ACIVRFForm,
    ACIVRFImportForm,
    ACIVRFBulkEditForm,
    select=("aci_tenant", "aci_tenant__aci_fabric", "nb_vrf"),
)
ACIVRFView = _vrf["view"]
ACIVRFListView = _vrf["list"]
ACIVRFEditView = _vrf["edit"]
ACIVRFDeleteView = _vrf["delete"]
ACIVRFBulkImportView = _vrf["bulk_import"]
ACIVRFBulkEditView = _vrf["bulk_edit"]
ACIVRFBulkDeleteView = _vrf["bulk_delete"]

_bd = _five_views(
    ACIBridgeDomain,
    ACIBridgeDomainTable,
    ACIBridgeDomainFilterSet,
    ACIBridgeDomainFilterForm,
    ACIBridgeDomainForm,
    ACIBridgeDomainImportForm,
    ACIBridgeDomainBulkEditForm,
    select=("aci_tenant", "aci_vrf"),
)
ACIBridgeDomainView = _bd["view"]
ACIBridgeDomainListView = _bd["list"]
ACIBridgeDomainEditView = _bd["edit"]
ACIBridgeDomainDeleteView = _bd["delete"]
ACIBridgeDomainBulkImportView = _bd["bulk_import"]
ACIBridgeDomainBulkEditView = _bd["bulk_edit"]
ACIBridgeDomainBulkDeleteView = _bd["bulk_delete"]

_bd_subnet = _five_views(
    ACIBridgeDomainSubnet,
    ACIBridgeDomainSubnetTable,
    ACIBridgeDomainSubnetFilterSet,
    ACIBridgeDomainSubnetFilterForm,
    ACIBridgeDomainSubnetForm,
    ACIBridgeDomainSubnetImportForm,
    ACIBridgeDomainSubnetBulkEditForm,
    select=("aci_bridge_domain", "nb_prefix"),
)
ACIBridgeDomainSubnetView = _bd_subnet["view"]
ACIBridgeDomainSubnetListView = _bd_subnet["list"]
ACIBridgeDomainSubnetEditView = _bd_subnet["edit"]
ACIBridgeDomainSubnetDeleteView = _bd_subnet["delete"]
ACIBridgeDomainSubnetBulkImportView = _bd_subnet["bulk_import"]
ACIBridgeDomainSubnetBulkEditView = _bd_subnet["bulk_edit"]
ACIBridgeDomainSubnetBulkDeleteView = _bd_subnet["bulk_delete"]

_ap = _five_views(
    ACIAppProfile,
    ACIAppProfileTable,
    ACIAppProfileFilterSet,
    ACIAppProfileFilterForm,
    ACIAppProfileForm,
    ACIAppProfileImportForm,
    ACIAppProfileBulkEditForm,
    select=("aci_tenant",),
)
ACIAppProfileView = _ap["view"]
ACIAppProfileListView = _ap["list"]
ACIAppProfileEditView = _ap["edit"]
ACIAppProfileDeleteView = _ap["delete"]
ACIAppProfileBulkImportView = _ap["bulk_import"]
ACIAppProfileBulkEditView = _ap["bulk_edit"]
ACIAppProfileBulkDeleteView = _ap["bulk_delete"]

_epg = _five_views(
    ACIEndpointGroup,
    ACIEndpointGroupTable,
    ACIEndpointGroupFilterSet,
    ACIEndpointGroupFilterForm,
    ACIEndpointGroupForm,
    ACIEndpointGroupImportForm,
    ACIEndpointGroupBulkEditForm,
    select=("aci_tenant", "aci_app_profile", "aci_bridge_domain"),
)
ACIEndpointGroupView = _epg["view"]
ACIEndpointGroupListView = _epg["list"]
ACIEndpointGroupEditView = _epg["edit"]
ACIEndpointGroupDeleteView = _epg["delete"]
ACIEndpointGroupBulkImportView = _epg["bulk_import"]
ACIEndpointGroupBulkEditView = _epg["bulk_edit"]
ACIEndpointGroupBulkDeleteView = _epg["bulk_delete"]

_useg = _five_views(
    ACIUSegAttribute,
    ACIUSegAttributeTable,
    ACIUSegAttributeFilterSet,
    ACIUSegAttributeFilterForm,
    ACIUSegAttributeForm,
    ACIUSegAttributeImportForm,
    ACIUSegAttributeBulkEditForm,
    select=("aci_endpoint_group",),
)
ACIUSegAttributeView = _useg["view"]
ACIUSegAttributeListView = _useg["list"]
ACIUSegAttributeEditView = _useg["edit"]
ACIUSegAttributeDeleteView = _useg["delete"]
ACIUSegAttributeBulkImportView = _useg["bulk_import"]
ACIUSegAttributeBulkEditView = _useg["bulk_edit"]
ACIUSegAttributeBulkDeleteView = _useg["bulk_delete"]

_esg = _five_views(
    ACIEndpointSecurityGroup,
    ACIEndpointSecurityGroupTable,
    ACIEndpointSecurityGroupFilterSet,
    ACIEndpointSecurityGroupFilterForm,
    ACIEndpointSecurityGroupForm,
    ACIEndpointSecurityGroupImportForm,
    ACIEndpointSecurityGroupBulkEditForm,
    select=("aci_tenant", "aci_vrf", "aci_app_profile"),
)
ACIEndpointSecurityGroupView = _esg["view"]
ACIEndpointSecurityGroupListView = _esg["list"]
ACIEndpointSecurityGroupEditView = _esg["edit"]
ACIEndpointSecurityGroupDeleteView = _esg["delete"]
ACIEndpointSecurityGroupBulkImportView = _esg["bulk_import"]
ACIEndpointSecurityGroupBulkEditView = _esg["bulk_edit"]
ACIEndpointSecurityGroupBulkDeleteView = _esg["bulk_delete"]
