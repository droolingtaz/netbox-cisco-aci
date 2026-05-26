"""UI views for Phase 6 binding models."""

from ..filtersets.bindings import (
    ACIDomainBindingFilterSet,
    ACIInterfaceFabricMembershipFilterSet,
    ACIStaticPortBindingFilterSet,
    ACIVPCBindingPairFilterSet,
)
from ..forms.bindings import (
    ACIDomainBindingBulkEditForm,
    ACIDomainBindingFilterForm,
    ACIDomainBindingForm,
    ACIDomainBindingImportForm,
    ACIInterfaceFabricMembershipBulkEditForm,
    ACIInterfaceFabricMembershipFilterForm,
    ACIInterfaceFabricMembershipForm,
    ACIInterfaceFabricMembershipImportForm,
    ACIStaticPortBindingBulkEditForm,
    ACIStaticPortBindingFilterForm,
    ACIStaticPortBindingForm,
    ACIStaticPortBindingImportForm,
    ACIVPCBindingPairBulkEditForm,
    ACIVPCBindingPairFilterForm,
    ACIVPCBindingPairForm,
    ACIVPCBindingPairImportForm,
)
from ..models.bindings import (
    ACIDomainBinding,
    ACIInterfaceFabricMembership,
    ACIStaticPortBinding,
    ACIVPCBindingPair,
)
from ..tables.bindings import (
    ACIDomainBindingTable,
    ACIInterfaceFabricMembershipTable,
    ACIStaticPortBindingTable,
    ACIVPCBindingPairTable,
)
from .access import _five_views

_spb = _five_views(
    ACIStaticPortBinding,
    ACIStaticPortBindingTable,
    ACIStaticPortBindingFilterSet,
    ACIStaticPortBindingFilterForm,
    ACIStaticPortBindingForm,
    ACIStaticPortBindingImportForm,
    ACIStaticPortBindingBulkEditForm,
    select=(
        "aci_endpoint_group",
        "aci_endpoint_group__aci_tenant",
        "dcim_interface",
        "dcim_interface__device",
    ),
)
ACIStaticPortBindingView = _spb["view"]
ACIStaticPortBindingListView = _spb["list"]
ACIStaticPortBindingEditView = _spb["edit"]
ACIStaticPortBindingDeleteView = _spb["delete"]
ACIStaticPortBindingBulkImportView = _spb["bulk_import"]
ACIStaticPortBindingBulkEditView = _spb["bulk_edit"]
ACIStaticPortBindingBulkDeleteView = _spb["bulk_delete"]

_vpc = _five_views(
    ACIVPCBindingPair,
    ACIVPCBindingPairTable,
    ACIVPCBindingPairFilterSet,
    ACIVPCBindingPairFilterForm,
    ACIVPCBindingPairForm,
    ACIVPCBindingPairImportForm,
    ACIVPCBindingPairBulkEditForm,
    select=("binding_a", "binding_b"),
)
ACIVPCBindingPairView = _vpc["view"]
ACIVPCBindingPairListView = _vpc["list"]
ACIVPCBindingPairEditView = _vpc["edit"]
ACIVPCBindingPairDeleteView = _vpc["delete"]
ACIVPCBindingPairBulkImportView = _vpc["bulk_import"]
ACIVPCBindingPairBulkEditView = _vpc["bulk_edit"]
ACIVPCBindingPairBulkDeleteView = _vpc["bulk_delete"]

_dom = _five_views(
    ACIDomainBinding,
    ACIDomainBindingTable,
    ACIDomainBindingFilterSet,
    ACIDomainBindingFilterForm,
    ACIDomainBindingForm,
    ACIDomainBindingImportForm,
    ACIDomainBindingBulkEditForm,
    select=("aci_endpoint_group", "aci_domain"),
)
ACIDomainBindingView = _dom["view"]
ACIDomainBindingListView = _dom["list"]
ACIDomainBindingEditView = _dom["edit"]
ACIDomainBindingDeleteView = _dom["delete"]
ACIDomainBindingBulkImportView = _dom["bulk_import"]
ACIDomainBindingBulkEditView = _dom["bulk_edit"]
ACIDomainBindingBulkDeleteView = _dom["bulk_delete"]

_ifm = _five_views(
    ACIInterfaceFabricMembership,
    ACIInterfaceFabricMembershipTable,
    ACIInterfaceFabricMembershipFilterSet,
    ACIInterfaceFabricMembershipFilterForm,
    ACIInterfaceFabricMembershipForm,
    ACIInterfaceFabricMembershipImportForm,
    ACIInterfaceFabricMembershipBulkEditForm,
    select=("dcim_interface", "aci_node"),
)
ACIInterfaceFabricMembershipView = _ifm["view"]
ACIInterfaceFabricMembershipListView = _ifm["list"]
ACIInterfaceFabricMembershipEditView = _ifm["edit"]
ACIInterfaceFabricMembershipDeleteView = _ifm["delete"]
ACIInterfaceFabricMembershipBulkImportView = _ifm["bulk_import"]
ACIInterfaceFabricMembershipBulkEditView = _ifm["bulk_edit"]
ACIInterfaceFabricMembershipBulkDeleteView = _ifm["bulk_delete"]
