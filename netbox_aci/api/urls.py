"""API URL routes.

NetBox includes this module at ``api/plugins/aci/`` with the instance
namespace ``netbox_aci-api`` — see netbox/plugins/urls.py in the NetBox
source. Setting an ``app_name`` here would clash with that namespace,
so we deliberately don't.
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
