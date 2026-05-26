"""Top-level URL routes for the plugin's UI views.

Each model gets a standard seven-route block (list, add, view, edit,
delete, bulk-import, bulk-edit, bulk-delete) following NetBox plugin
conventions.

NetBox includes this module at ``plugins/aci/`` with the instance
namespace ``netbox_cisco_aci`` (derived from ``app.label``) — see
netbox/plugins/urls.py. The ``app_name`` below is the *application*
namespace; reverse() lookups against ``plugins:netbox_cisco_aci:...`` use it.
"""

from django.urls import path

from .views import access as acc
from .views import access_groups as acg
from .views import access_policies as acp
from .views import access_profiles as apr
from .views import bindings as bnd
from .views import contracts as ctr
from .views import fabric as fab
from .views import l3out as l3o
from .views import tenant as tn

app_name = "netbox_cisco_aci"


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

# Phase 3 — Access policies
urlpatterns += _crud("vlan-pools", "pool", acc, "ACIVLANPool", "acivlanpool")
urlpatterns += _crud("vlan-pool-blocks", "block", acc, "ACIVLANPoolBlock", "acivlanpoolblock")
urlpatterns += _crud("domains", "domain", acc, "ACIDomain", "acidomain")
urlpatterns += _crud("aaeps", "aaep", acc, "ACIAAEP", "aciaaep")
urlpatterns += _crud(
    "aaep-epg-mappings",
    "aaep-map",
    acc,
    "ACIAAEPEPGMapping",
    "aciaaepepgmapping",
)

# Phase 4 — Interface policies, policy groups, profiles
urlpatterns += _crud("link-level-policies", "link", acp, "ACILinkLevelPolicy", "acilinklevelpolicy")
urlpatterns += _crud("cdp-policies", "cdp", acp, "ACICDPInterfacePolicy", "acicdpinterfacepolicy")
urlpatterns += _crud(
    "lldp-policies", "lldp", acp, "ACILLDPInterfacePolicy", "acilldpinterfacepolicy"
)
urlpatterns += _crud(
    "lacp-policies", "lacp", acp, "ACILACPInterfacePolicy", "acilacpinterfacepolicy"
)
urlpatterns += _crud("mcp-policies", "mcp", acp, "ACIMCPInterfacePolicy", "acimcpinterfacepolicy")
urlpatterns += _crud("stp-policies", "stp", acp, "ACISTPInterfacePolicy", "acistpinterfacepolicy")
urlpatterns += _crud(
    "interface-policy-groups",
    "pg",
    acg,
    "ACIInterfacePolicyGroup",
    "aciinterfacepolicygroup",
)
urlpatterns += _crud("switch-profiles", "sp", apr, "ACISwitchProfile", "aciswitchprofile")
urlpatterns += _crud(
    "switch-profile-selectors",
    "sps",
    apr,
    "ACISwitchProfileSelector",
    "aciswitchprofileselector",
)
urlpatterns += _crud("interface-profiles", "ip", apr, "ACIInterfaceProfile", "aciinterfaceprofile")
urlpatterns += _crud(
    "interface-profile-selectors",
    "ips",
    apr,
    "ACIInterfaceProfileSelector",
    "aciinterfaceprofileselector",
)
urlpatterns += _crud(
    "switch-interface-profile-attachments",
    "swip-attach",
    apr,
    "ACISwitchProfileInterfaceProfileAttachment",
    "aciswitchprofileinterfaceprofileattachment",
)

# Phase 5 — Contracts / Subjects / Filters / Relations
urlpatterns += _crud("contracts", "contract", ctr, "ACIContract", "acicontract")
urlpatterns += _crud("subjects", "subject", ctr, "ACISubject", "acisubject")
urlpatterns += _crud("filters", "filter", ctr, "ACIFilter", "acifilter")
urlpatterns += _crud("filter-entries", "filter-entry", ctr, "ACIFilterEntry", "acifilterentry")
urlpatterns += _crud(
    "subject-filters", "subject-filter", ctr, "ACISubjectFilter", "acisubjectfilter"
)
urlpatterns += _crud(
    "contract-relations",
    "contract-relation",
    ctr,
    "ACIContractRelation",
    "acicontractrelation",
)

# Phase 6 — Static Port Bindings
urlpatterns += _crud(
    "static-port-bindings",
    "spb",
    bnd,
    "ACIStaticPortBinding",
    "acistaticportbinding",
)
urlpatterns += _crud(
    "vpc-binding-pairs",
    "vpc-pair",
    bnd,
    "ACIVPCBindingPair",
    "acivpcbindingpair",
)
urlpatterns += _crud(
    "domain-bindings",
    "dom-binding",
    bnd,
    "ACIDomainBinding",
    "acidomainbinding",
)
urlpatterns += _crud(
    "interface-fabric-memberships",
    "ifm",
    bnd,
    "ACIInterfaceFabricMembership",
    "aciinterfacefabricmembership",
)

# Phase 7 — L3Outs
urlpatterns += _crud("l3outs", "l3out", l3o, "ACIL3Out", "acil3out")
urlpatterns += _crud(
    "logical-node-profiles",
    "lnp",
    l3o,
    "ACILogicalNodeProfile",
    "acilogicalnodeprofile",
)
urlpatterns += _crud(
    "logical-nodes", "ln", l3o, "ACILogicalNode", "acilogicalnode"
)
urlpatterns += _crud(
    "logical-interface-profiles",
    "lip",
    l3o,
    "ACILogicalInterfaceProfile",
    "acilogicalinterfaceprofile",
)
urlpatterns += _crud(
    "l3out-interfaces", "l3if", l3o, "ACIL3OutInterface", "acil3outinterface"
)
urlpatterns += _crud("bgp-peers", "bgp", l3o, "ACIBGPPeer", "acibgppeer")
urlpatterns += _crud(
    "ospf-interface-policies",
    "ospf-pol",
    l3o,
    "ACIOSPFInterfacePolicy",
    "aciospfinterfacepolicy",
)
urlpatterns += _crud(
    "ospf-interface-attachments",
    "ospf-att",
    l3o,
    "ACIOSPFInterfaceAttachment",
    "aciospfinterfaceattachment",
)
urlpatterns += _crud(
    "eigrp-interface-policies",
    "eigrp-pol",
    l3o,
    "ACIEIGRPInterfacePolicy",
    "acieigrpinterfacepolicy",
)
urlpatterns += _crud(
    "external-epgs", "ext-epg", l3o, "ACIExternalEPG", "aciexternalepg"
)
urlpatterns += _crud(
    "external-epg-subnets",
    "ext-epg-sub",
    l3o,
    "ACIExternalEPGSubnet",
    "aciexternalepgsubnet",
)
