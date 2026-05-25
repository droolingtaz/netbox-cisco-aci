"""API URL routes.

NetBox includes this module at ``api/plugins/aci/`` with the instance
namespace ``netbox_aci-api`` (see ``netbox/plugins/urls.py``). The
``app_name`` below is the *application* namespace; Django uses it as a
fallback when reverse() lookups don't specify an instance.
"""

from netbox.api.routers import NetBoxRouter

from .views.fabric import ACIFabricViewSet, ACINodeViewSet, ACIPodViewSet
from .views.tenant import (
    ACIAppProfileViewSet,
    ACIBridgeDomainSubnetViewSet,
    ACIBridgeDomainViewSet,
    ACIEndpointGroupViewSet,
    ACIEndpointSecurityGroupViewSet,
    ACITenantViewSet,
    ACIUSegAttributeViewSet,
    ACIVRFViewSet,
)

app_name = "netbox_aci"

router = NetBoxRouter()

# Phase 1 — Fabric topology
router.register("fabrics", ACIFabricViewSet)
router.register("pods", ACIPodViewSet)
router.register("nodes", ACINodeViewSet)

# Phase 2 — Tenancy
router.register("tenants", ACITenantViewSet)
router.register("vrfs", ACIVRFViewSet)
router.register("bridge-domains", ACIBridgeDomainViewSet)
router.register("bridge-domain-subnets", ACIBridgeDomainSubnetViewSet)
router.register("app-profiles", ACIAppProfileViewSet)
router.register("endpoint-groups", ACIEndpointGroupViewSet)
router.register("useg-attributes", ACIUSegAttributeViewSet)
router.register("endpoint-security-groups", ACIEndpointSecurityGroupViewSet)

urlpatterns = router.urls
