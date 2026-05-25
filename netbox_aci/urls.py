"""Top-level URL routes for the plugin's UI views.

Each model gets a five-route block (list, add, view, edit, delete)
following standard NetBox plugin conventions. As models land in later
phases they slot in here.
"""

from django.urls import include, path

from .views import fabric as fabric_views

app_name = "netbox_aci"

urlpatterns = [
    # ----- Fabric topology -----
    path(
        "fabrics/",
        include(
            [
                path("", fabric_views.ACIFabricListView.as_view(), name="acifabric_list"),
                path(
                    "add/",
                    fabric_views.ACIFabricEditView.as_view(),
                    name="acifabric_add",
                ),
                path(
                    "<int:pk>/",
                    fabric_views.ACIFabricView.as_view(),
                    name="acifabric",
                ),
                path(
                    "<int:pk>/edit/",
                    fabric_views.ACIFabricEditView.as_view(),
                    name="acifabric_edit",
                ),
                path(
                    "<int:pk>/delete/",
                    fabric_views.ACIFabricDeleteView.as_view(),
                    name="acifabric_delete",
                ),
            ]
        ),
    ),
    path(
        "pods/",
        include(
            [
                path("", fabric_views.ACIPodListView.as_view(), name="acipod_list"),
                path("add/", fabric_views.ACIPodEditView.as_view(), name="acipod_add"),
                path("<int:pk>/", fabric_views.ACIPodView.as_view(), name="acipod"),
                path(
                    "<int:pk>/edit/",
                    fabric_views.ACIPodEditView.as_view(),
                    name="acipod_edit",
                ),
                path(
                    "<int:pk>/delete/",
                    fabric_views.ACIPodDeleteView.as_view(),
                    name="acipod_delete",
                ),
            ]
        ),
    ),
    path(
        "nodes/",
        include(
            [
                path("", fabric_views.ACINodeListView.as_view(), name="acinode_list"),
                path("add/", fabric_views.ACINodeEditView.as_view(), name="acinode_add"),
                path("<int:pk>/", fabric_views.ACINodeView.as_view(), name="acinode"),
                path(
                    "<int:pk>/edit/",
                    fabric_views.ACINodeEditView.as_view(),
                    name="acinode_edit",
                ),
                path(
                    "<int:pk>/delete/",
                    fabric_views.ACINodeDeleteView.as_view(),
                    name="acinode_delete",
                ),
            ]
        ),
    ),
]
