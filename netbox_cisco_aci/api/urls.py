"""API URL routes.

NetBox includes this module at ``api/plugins/aci/`` with the instance
namespace ``netbox_cisco_aci-api`` (see ``netbox/plugins/urls.py``). The
``app_name`` below is the *application* namespace; Django uses it as a
fallback when reverse() lookups don't specify an instance.
"""

from netbox.api.routers import NetBoxRouter

from .views.access import (
    ACIAAEPEPGMappingViewSet,
    ACIAAEPViewSet,
    ACIDomainViewSet,
    ACIVLANPoolBlockViewSet,
    ACIVLANPoolViewSet,
)
from .views.access_groups import ACIInterfacePolicyGroupViewSet
from .views.access_policies import (
    ACICDPInterfacePolicyViewSet,
    ACILACPInterfacePolicyViewSet,
    ACILinkLevelPolicyViewSet,
    ACILLDPInterfacePolicyViewSet,
    ACIMCPInterfacePolicyViewSet,
    ACISTPInterfacePolicyViewSet,
)
from .views.access_profiles import (
    ACIInterfaceProfileSelectorViewSet,
    ACIInterfaceProfileViewSet,
    ACISwitchProfileInterfaceProfileAttachmentViewSet,
    ACISwitchProfileSelectorViewSet,
    ACISwitchProfileViewSet,
)
from .views.bindings import (
    ACIDomainBindingViewSet,
    ACIInterfaceFabricMembershipViewSet,
    ACIStaticPortBindingViewSet,
    ACIVPCBindingPairViewSet,
)
from .views.contracts import (
    ACIContractRelationViewSet,
    ACIContractViewSet,
    ACIFilterEntryViewSet,
    ACIFilterViewSet,
    ACISubjectFilterViewSet,
    ACISubjectViewSet,
)
from .views.fabric import ACIFabricViewSet, ACINodeViewSet, ACIPodViewSet
from .views.l3out import (
    ACIBGPPeerViewSet,
    ACIEIGRPInterfacePolicyViewSet,
    ACIExternalEPGSubnetViewSet,
    ACIExternalEPGViewSet,
    ACIL3OutInterfaceViewSet,
    ACIL3OutViewSet,
    ACILogicalInterfaceProfileViewSet,
    ACILogicalNodeProfileViewSet,
    ACILogicalNodeViewSet,
    ACIOSPFInterfaceAttachmentViewSet,
    ACIOSPFInterfacePolicyViewSet,
)
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

app_name = "netbox_cisco_aci"

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

# Phase 3 — Access policies
router.register("vlan-pools", ACIVLANPoolViewSet)
router.register("vlan-pool-blocks", ACIVLANPoolBlockViewSet)
router.register("domains", ACIDomainViewSet)
router.register("aaeps", ACIAAEPViewSet)
router.register("aaep-epg-mappings", ACIAAEPEPGMappingViewSet)

# Phase 4 — Interface policies, policy groups, profiles
router.register("link-level-policies", ACILinkLevelPolicyViewSet)
router.register("cdp-policies", ACICDPInterfacePolicyViewSet)
router.register("lldp-policies", ACILLDPInterfacePolicyViewSet)
router.register("lacp-policies", ACILACPInterfacePolicyViewSet)
router.register("mcp-policies", ACIMCPInterfacePolicyViewSet)
router.register("stp-policies", ACISTPInterfacePolicyViewSet)
router.register("interface-policy-groups", ACIInterfacePolicyGroupViewSet)
router.register("switch-profiles", ACISwitchProfileViewSet)
router.register("switch-profile-selectors", ACISwitchProfileSelectorViewSet)
router.register("interface-profiles", ACIInterfaceProfileViewSet)
router.register("interface-profile-selectors", ACIInterfaceProfileSelectorViewSet)
router.register(
    "switch-interface-profile-attachments",
    ACISwitchProfileInterfaceProfileAttachmentViewSet,
)

# Phase 5 — Contracts / Subjects / Filters / Relations
router.register("contracts", ACIContractViewSet)
router.register("subjects", ACISubjectViewSet)
router.register("filters", ACIFilterViewSet)
router.register("filter-entries", ACIFilterEntryViewSet)
router.register("subject-filters", ACISubjectFilterViewSet)
router.register("contract-relations", ACIContractRelationViewSet)

# Phase 6 — Static Port Bindings
router.register("static-port-bindings", ACIStaticPortBindingViewSet)
router.register("vpc-binding-pairs", ACIVPCBindingPairViewSet)
router.register("domain-bindings", ACIDomainBindingViewSet)
router.register("interface-fabric-memberships", ACIInterfaceFabricMembershipViewSet)

# Phase 7 — L3Outs
router.register("l3outs", ACIL3OutViewSet)
router.register("logical-node-profiles", ACILogicalNodeProfileViewSet)
router.register("logical-nodes", ACILogicalNodeViewSet)
router.register("logical-interface-profiles", ACILogicalInterfaceProfileViewSet)
router.register("l3out-interfaces", ACIL3OutInterfaceViewSet)
router.register("bgp-peers", ACIBGPPeerViewSet)
router.register("ospf-interface-policies", ACIOSPFInterfacePolicyViewSet)
router.register("ospf-interface-attachments", ACIOSPFInterfaceAttachmentViewSet)
router.register("eigrp-interface-policies", ACIEIGRPInterfacePolicyViewSet)
router.register("external-epgs", ACIExternalEPGViewSet)
router.register("external-epg-subnets", ACIExternalEPGSubnetViewSet)

urlpatterns = router.urls
