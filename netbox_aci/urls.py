"""Top-level URL routes for the plugin's UI views.

Each model gets a standard seven-route block (list, add, view, edit,
delete, bulk-import, bulk-edit, bulk-delete) following NetBox plugin
conventions.

NetBox includes this module at ``plugins/aci/`` with the instance
namespace ``netbox_aci`` (derived from ``app.label``) — see
netbox/plugins/urls.py. Setting an explicit ``app_name`` here would
clash with that namespace, so we deliberately don't.
"""

from django.urls import path

from .views import fabric as fab
from .views import tenant as tn


def _crud(prefix, slug, mod, view_cls_name, label):
    """Build the standard 8-URL CRUD block for a model.

    ``view_cls_name`` is the class-name *prefix* — e.g. for ``ACIFabric``
    we expect ``ACIFabricView``, ``ACIFabricListView``, etc., to exist
    on ``mod``.
    """

    return [
        path(
            f"{prefix}/",
            getattr(mod, f"{view_cls_name}ListView").as_view(),
            name=f"{label}_list",
        ),
        path(
            f"{prefix}/add/",
            getattr(mod, f"{view_cls_name}EditView").as_view(),
            name=f"{label}_add",
        ),
        path(
            f"{prefix}/import/",
            getattr(mod, f"{view_cls_name}BulkImportView").as_view(),
            name=f"{label}_import",
        ),
        path(
            f"{prefix}/edit/",
            getattr(mod, f"{view_cls_name}BulkEditView").as_view(),
            name=f"{label}_bulk_edit",
        ),
        path(
            f"{prefix}/delete/",
            getattr(mod, f"{view_cls_name}BulkDeleteView").as_view(),
            name=f"{label}_bulk_delete",
        ),
        path(
            f"{prefix}/<int:pk>/",
            getattr(mod, f"{view_cls_name}View").as_view(),
            name=label,
        ),
        path(
            f"{prefix}/<int:pk>/edit/",
            getattr(mod, f"{view_cls_name}EditView").as_view(),
            name=f"{label}_edit",
        ),
        path(
            f"{prefix}/<int:pk>/delete/",
            getattr(mod, f"{view_cls_name}DeleteView").as_view(),
            name=f"{label}_delete",
        ),
    ]


urlpatterns = []

# Phase 1 — Fabric topology
urlpatterns += _crud("fabrics", "fabric", fab, "ACIFabric", "acifabric")
urlpatterns += _crud("pods", "pod", fab, "ACIPod", "acipod")
urlpatterns += _crud("nodes", "node", fab, "ACINode", "acinode")

# Phase 2 — Tenancy
urlpatterns += _crud("tenants", "tenant", tn, "ACITenant", "acitenant")
urlpatterns += _crud("vrfs", "vrf", tn, "ACIVRF", "acivrf")
urlpatterns += _crud("bridge-domains", "bd", tn, "ACIBridgeDomain", "acibridgedomain")
urlpatterns += _crud(
    "bridge-domain-subnets", "bd-subnet", tn, "ACIBridgeDomainSubnet", "acibridgedomainsubnet"
)
urlpatterns += _crud("app-profiles", "ap", tn, "ACIAppProfile", "aciappprofile")
urlpatterns += _crud("endpoint-groups", "epg", tn, "ACIEndpointGroup", "aciendpointgroup")
urlpatterns += _crud("useg-attributes", "useg-attr", tn, "ACIUSegAttribute", "aciusegattribute")
urlpatterns += _crud(
    "endpoint-security-groups",
    "esg",
    tn,
    "ACIEndpointSecurityGroup",
    "aciendpointsecuritygroup",
)
