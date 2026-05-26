"""REST API tests for Phase 7 L3Out models."""

from dcim.models import Interface
from utilities.testing import APITestCase, APIViewTestCases

from netbox_cisco_aci.choices import (
    L3OutInterfaceTypeChoices,
    OSPFNetworkTypeChoices,
)
from netbox_cisco_aci.models.fabric import ACIFabric, ACINode, ACIPod
from netbox_cisco_aci.models.l3out import (
    ACIBGPPeer,
    ACIEIGRPInterfacePolicy,
    ACIExternalEPG,
    ACIExternalEPGSubnet,
    ACIL3Out,
    ACIL3OutInterface,
    ACILogicalInterfaceProfile,
    ACILogicalNode,
    ACILogicalNodeProfile,
    ACIOSPFInterfaceAttachment,
    ACIOSPFInterfacePolicy,
)
from netbox_cisco_aci.models.tenant import ACIVRF, ACITenant
from netbox_cisco_aci.tests.base import make_dcim_device

PLUGIN_API_NAMESPACE = "plugins-api:netbox_cisco_aci"


def _build_l3out_fixture(prefix: str):
    """Build a common l3out fixture for test classes."""
    fab = ACIFabric.objects.create(name=f"{prefix}-fab")
    pod = ACIPod.objects.create(aci_fabric=fab, pod_id=1, name=f"{prefix}-pod")
    tenant = ACITenant.objects.create(aci_fabric=fab, name=f"{prefix}-t")
    vrf = ACIVRF.objects.create(aci_tenant=tenant, name=f"{prefix}-vrf")
    l3out = ACIL3Out.objects.create(
        aci_tenant=tenant,
        aci_vrf=vrf,
        name=f"{prefix}-l3out",
        protocol_static=True,
    )
    lnp = ACILogicalNodeProfile.objects.create(aci_l3out=l3out, name=f"{prefix}-lnp")
    lip = ACILogicalInterfaceProfile.objects.create(
        aci_logical_node_profile=lnp, name=f"{prefix}-lip"
    )
    return fab, pod, tenant, vrf, l3out, lnp, lip


# ---------------------------------------------------------------------------
# ACIL3Out
# ---------------------------------------------------------------------------


class ACIL3OutAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIL3Out
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_tenant",
        "aci_vrf",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-L3OutFab")
        tenant = ACITenant.objects.create(aci_fabric=fab, name="t-l3o-api")
        vrf = ACIVRF.objects.create(aci_tenant=tenant, name="vrf-l3o-api")
        for i in range(3):
            ACIL3Out.objects.create(
                aci_tenant=tenant,
                aci_vrf=vrf,
                name=f"l3out-{i}",
                protocol_static=True,
            )
        cls.create_data = [
            {
                "aci_tenant": tenant.pk,
                "aci_vrf": vrf.pk,
                "name": "l3out-a",
                "protocol_bgp": True,
            },
            {
                "aci_tenant": tenant.pk,
                "aci_vrf": vrf.pk,
                "name": "l3out-b",
                "protocol_ospf": True,
            },
        ]


# ---------------------------------------------------------------------------
# ACILogicalNodeProfile
# ---------------------------------------------------------------------------


class ACILogicalNodeProfileAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACILogicalNodeProfile
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_l3out",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip = _build_l3out_fixture("lnp-api")
        for i in range(2):
            ACILogicalNodeProfile.objects.create(aci_l3out=l3out, name=f"lnp-{i}")
        cls.create_data = [
            {"aci_l3out": l3out.pk, "name": "lnp-a"},
            {"aci_l3out": l3out.pk, "name": "lnp-b"},
        ]


# ---------------------------------------------------------------------------
# ACILogicalNode
#
# ACILogicalNode has unique constraint on (lnp, aci_node) and (lnp, router_id).
# Use distinct nodes / router IDs.
# ---------------------------------------------------------------------------


class ACILogicalNodeAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACILogicalNode
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_logical_node_profile",
        "aci_node",
        "description",
        "display",
        "id",
        "name",
        "router_id",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip = _build_l3out_fixture("ln-api")
        nodes = [
            ACINode.objects.create(
                aci_pod=pod, node_id=100 + i, name=f"leaf-{100 + i}", role="leaf"
            )
            for i in range(5)
        ]
        for i in range(3):
            ACILogicalNode.objects.create(
                aci_logical_node_profile=lnp,
                aci_node=nodes[i],
                name=f"ln-{i}",
                router_id=f"10.0.{i}.1",
            )
        cls.create_data = [
            {
                "aci_logical_node_profile": lnp.pk,
                "aci_node": nodes[3].pk,
                "name": "ln-a",
                "router_id": "10.0.10.1",
                "use_router_id_as_loopback": True,
            },
            {
                "aci_logical_node_profile": lnp.pk,
                "aci_node": nodes[4].pk,
                "name": "ln-b",
                "router_id": "10.0.11.1",
                "use_router_id_as_loopback": True,
            },
        ]


# ---------------------------------------------------------------------------
# ACILogicalInterfaceProfile
# ---------------------------------------------------------------------------


class ACILogicalInterfaceProfileAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACILogicalInterfaceProfile
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_logical_node_profile",
        "description",
        "display",
        "id",
        "interface_type",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip = _build_l3out_fixture("lip-api")
        for i in range(2):
            ACILogicalInterfaceProfile.objects.create(aci_logical_node_profile=lnp, name=f"lip-{i}")
        cls.create_data = [
            {
                "aci_logical_node_profile": lnp.pk,
                "name": "lip-a",
                "interface_type": L3OutInterfaceTypeChoices.ROUTED,
            },
            {
                "aci_logical_node_profile": lnp.pk,
                "name": "lip-b",
                "interface_type": L3OutInterfaceTypeChoices.ROUTED,
            },
        ]


# ---------------------------------------------------------------------------
# ACIL3OutInterface  (auto-name; fixture isolation: OneToOne is on LIP side)
# ---------------------------------------------------------------------------


class ACIL3OutInterfaceAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIL3OutInterface
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_logical_interface_profile",
        "dcim_interface",
        "description",
        "display",
        "id",
        "ip_address",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip = _build_l3out_fixture("l3if-api")
        dev = make_dcim_device("leaf-l3if-api")
        # Create 3 existing rows
        ifaces = [
            Interface.objects.create(device=dev, name=f"eth1/{i + 1}", type="10gbase-t")
            for i in range(5)
        ]
        for i in range(3):
            ACIL3OutInterface.objects.create(
                aci_logical_interface_profile=lip,
                dcim_interface=ifaces[i],
            )
        # New rows for create_data (name derived automatically)
        cls.create_data = [
            {
                "aci_logical_interface_profile": lip.pk,
                "dcim_interface": ifaces[3].pk,
                "ip_address": "192.0.2.1/30",
            },
            {
                "aci_logical_interface_profile": lip.pk,
                "dcim_interface": ifaces[4].pk,
            },
        ]


# ---------------------------------------------------------------------------
# ACIBGPPeer
# ---------------------------------------------------------------------------


class ACIBGPPeerAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIBGPPeer
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "description",
        "display",
        "id",
        "name",
        "peer_address",
        "remote_asn",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip = _build_l3out_fixture("bgp-api")
        for i in range(3):
            ACIBGPPeer.objects.create(
                aci_logical_interface_profile=lip,
                name=f"peer-{i}",
                peer_address=f"10.0.0.{i + 1}",
                remote_asn=65000 + i,
            )
        cls.create_data = [
            {
                "aci_logical_interface_profile": lip.pk,
                "name": "peer-a",
                "peer_address": "10.0.1.1",
                "remote_asn": 65100,
            },
            {
                "aci_logical_node_profile": lnp.pk,
                "name": "peer-b",
                "peer_address": "10.0.1.2",
                "remote_asn": 65101,
            },
        ]


# ---------------------------------------------------------------------------
# ACIOSPFInterfacePolicy
#
# Referenced PROTECT by ACIOSPFInterfaceAttachment.
# Use the same pattern as ACIFilter: create 3 safe policies first, attach
# a PROTECT child to the middle one (pol-1), then create 3 more safe policies.
# - test_delete_object uses _get_queryset().first() ordered by (aci_tenant, name)
#   → first alphabetically = "pol-0" which has NO child.
# - test_bulk_delete_objects uses top-3-by-id → the last 3 created (pol-3,4,5)
#   are all safe.
# ---------------------------------------------------------------------------


class ACIOSPFInterfacePolicyAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIOSPFInterfacePolicy
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_tenant",
        "description",
        "display",
        "id",
        "name",
        "network_type",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip = _build_l3out_fixture("ospf-pol-api")
        # First batch: 3 policies (pol-0, pol-1, pol-2)
        for i in range(3):
            ACIOSPFInterfacePolicy.objects.create(aci_tenant=tenant, name=f"pol-{i}")
        # Attach a PROTECT child to pol-1 (NOT the first, NOT the last 3)
        pol1 = ACIOSPFInterfacePolicy.objects.get(aci_tenant=tenant, name="pol-1")
        ACIOSPFInterfaceAttachment.objects.create(
            aci_logical_interface_profile=lip,
            aci_ospf_interface_policy=pol1,
            ospf_area_id="0",
            name="att-protect",
        )
        # Second batch: 3 more policies (pol-3, pol-4, pol-5) — top-3-by-id, safe
        for i in range(3, 6):
            ACIOSPFInterfacePolicy.objects.create(aci_tenant=tenant, name=f"pol-{i}")
        cls.create_data = [
            {
                "aci_tenant": tenant.pk,
                "name": "pol-a",
                "network_type": OSPFNetworkTypeChoices.POINT_TO_POINT,
            },
            {
                "aci_tenant": tenant.pk,
                "name": "pol-b",
                "network_type": OSPFNetworkTypeChoices.BROADCAST,
            },
        ]


# ---------------------------------------------------------------------------
# ACIOSPFInterfaceAttachment
# (one-to-one with LIP — each LIP can have at most one attachment)
# ---------------------------------------------------------------------------


class ACIOSPFInterfaceAttachmentAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIOSPFInterfaceAttachment
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_logical_interface_profile",
        "aci_ospf_interface_policy",
        "description",
        "display",
        "id",
        "ospf_area_id",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip_seed = _build_l3out_fixture("ospf-att-api")
        ospf_pol = ACIOSPFInterfacePolicy.objects.create(aci_tenant=tenant, name="ospf-pol-att")
        # Need one LIP per attachment (one-to-one)
        lips = [lip_seed]
        for i in range(1, 5):
            lips.append(
                ACILogicalInterfaceProfile.objects.create(
                    aci_logical_node_profile=lnp, name=f"lip-att-{i}"
                )
            )
        for i in range(3):
            ACIOSPFInterfaceAttachment.objects.create(
                aci_logical_interface_profile=lips[i],
                aci_ospf_interface_policy=ospf_pol,
                ospf_area_id=str(i),
                name=f"att-{i}",
            )
        cls.create_data = [
            {
                "aci_logical_interface_profile": lips[3].pk,
                "aci_ospf_interface_policy": ospf_pol.pk,
                "ospf_area_id": "10",
                "name": "att-a",
            },
            {
                "aci_logical_interface_profile": lips[4].pk,
                "aci_ospf_interface_policy": ospf_pol.pk,
                "ospf_area_id": "11",
                "name": "att-b",
            },
        ]


# ---------------------------------------------------------------------------
# ACIEIGRPInterfacePolicy
# ---------------------------------------------------------------------------


class ACIEIGRPInterfacePolicyAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIEIGRPInterfacePolicy
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_tenant",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip = _build_l3out_fixture("eigrp-api")
        for i in range(3):
            ACIEIGRPInterfacePolicy.objects.create(aci_tenant=tenant, name=f"eigrp-{i}")
        cls.create_data = [
            {"aci_tenant": tenant.pk, "name": "eigrp-a"},
            {"aci_tenant": tenant.pk, "name": "eigrp-b"},
        ]


# ---------------------------------------------------------------------------
# ACIExternalEPG
# ---------------------------------------------------------------------------


class ACIExternalEPGAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIExternalEPG
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_l3out",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip = _build_l3out_fixture("eepg-api")
        for i in range(3):
            ACIExternalEPG.objects.create(aci_l3out=l3out, name=f"ext-{i}")
        cls.create_data = [
            {"aci_l3out": l3out.pk, "name": "ext-a"},
            {"aci_l3out": l3out.pk, "name": "ext-b"},
        ]


# ---------------------------------------------------------------------------
# ACIExternalEPGSubnet
# ---------------------------------------------------------------------------


class ACIExternalEPGSubnetAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIExternalEPGSubnet
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_external_epg",
        "description",
        "display",
        "id",
        "prefix",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, vrf, l3out, lnp, lip = _build_l3out_fixture("subnet-api")
        eepg = ACIExternalEPG.objects.create(aci_l3out=l3out, name="ext-subnet-api")
        prefixes = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
        for i, prefix in enumerate(prefixes):
            ACIExternalEPGSubnet.objects.create(
                aci_external_epg=eepg,
                name=f"sub-{i}",
                prefix=prefix,
            )
        cls.create_data = [
            {"aci_external_epg": eepg.pk, "name": "sub-a", "prefix": "203.0.113.0/24"},
            {"aci_external_epg": eepg.pk, "name": "sub-b", "prefix": "198.51.100.0/24"},
        ]
