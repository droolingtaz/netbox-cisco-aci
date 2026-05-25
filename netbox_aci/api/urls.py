"""API URL routes."""

from netbox.api.routers import NetBoxRouter

from .views.fabric import ACIFabricViewSet, ACINodeViewSet, ACIPodViewSet

app_name = "netbox_aci"

router = NetBoxRouter()
router.register("fabrics", ACIFabricViewSet)
router.register("pods", ACIPodViewSet)
router.register("nodes", ACINodeViewSet)

urlpatterns = router.urls
