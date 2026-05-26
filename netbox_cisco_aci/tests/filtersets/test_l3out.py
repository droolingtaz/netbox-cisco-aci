"""FilterSet tests for Phase 7 L3Out models."""

from dcim.models import Interface
from django.test import TestCase

from netbox_cisco_aci.choices import (
    L3OutInterfaceTypeChoices,
    OSPFAreaTypeChoices,
    OSPFNetworkTypeChoices,
)
from netbox_cisco_aci.filtersets.l3out import (
    ACIBGPPeerFilterSet,
    ACIEIGRPInterfacePolicyFilterSet,
    ACIExternalEPGFilterSet,
    ACIExternalEPGSubnetFilterSet,
    ACIL3OutFilterSet,
    ACIL3OutInterfaceFilterSet,
    ACILogicalInterfaceProfileFilterSet,
    ACILogicalNodeFilterSet,
    ACILogicalNodeProfileFilterSet,
    ACIOSPFInterfaceAttachmentFilterSet,
    ACIOSPFInterfacePolicyFilterSet,
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


class L3OutFilterSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC-FS")
        cls.fab2 = ACIFabric.objects.create(name="DC-FS2")
        cls.pod = ACIPod.objects.create(aci_fabric=cls.fab, pod_id=1, name="pod-1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-fs")
        cls.tenant2 = ACITenant.objects.create(aci_fabric=cls.fab2, name="t-fs2")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-fs")
        cls.vrf2 = ACIVRF.objects.create(aci_tenant=cls.tenant2, name="vrf-fs2")

        # L3Outs – one BGP-enabled, one OSPF-enabled
        cls.l3out_bgp = ACIL3Out.objects.create(
            aci_tenant=cls.tenant,
            aci_vrf=cls.vrf,
            name="l3out-bgp",
            protocol_bgp=True,
            protocol_static=False,
        )
        cls.l3out_ospf = ACIL3Out.objects.create(
            aci_tenant=cls.tenant,
            aci_vrf=cls.vrf,
            name="l3out-ospf",
            protocol_ospf=True,
            protocol_static=False,
        )

        # LNPs
        cls.lnp_a = ACILogicalNodeProfile.objects.create(aci_l3out=cls.l3out_bgp, name="lnp-a")
        cls.lnp_b = ACILogicalNodeProfile.objects.create(aci_l3out=cls.l3out_ospf, name="lnp-b")

        # ACINodes for logical-node tests
        cls.aci_node = ACINode.objects.create(
            aci_pod=cls.pod, node_id=101, name="leaf-101", role="leaf"
        )
        cls.aci_node2 = ACINode.objects.create(
            aci_pod=cls.pod, node_id=102, name="leaf-102", role="leaf"
        )

        # LogicalNodes
        cls.ln_a = ACILogicalNode.objects.create(
            aci_logical_node_profile=cls.lnp_a,
            aci_node=cls.aci_node,
            name="ln-a",
            router_id="10.0.0.1",
        )
        cls.ln_b = ACILogicalNode.objects.create(
            aci_logical_node_profile=cls.lnp_b,
            aci_node=cls.aci_node2,
            name="ln-b",
            router_id="10.0.0.2",
        )

        # LIPs
        cls.lip_routed = ACILogicalInterfaceProfile.objects.create(
            aci_logical_node_profile=cls.lnp_a,
            name="lip-routed",
            interface_type=L3OutInterfaceTypeChoices.ROUTED,
        )
        cls.lip_svi = ACILogicalInterfaceProfile.objects.create(
            aci_logical_node_profile=cls.lnp_b,
            name="lip-svi",
            interface_type=L3OutInterfaceTypeChoices.SVI,
            encap_vlan=100,
        )

        # L3OutInterfaces
        cls.device = make_dcim_device("leaf-fs-1")
        cls.iface1 = Interface.objects.create(device=cls.device, name="eth1/1", type="10gbase-t")
        cls.iface2 = Interface.objects.create(device=cls.device, name="eth1/2", type="10gbase-t")
        cls.l3if_a = ACIL3OutInterface.objects.create(
            aci_logical_interface_profile=cls.lip_routed,
            dcim_interface=cls.iface1,
            ip_address="192.0.2.1/30",
        )
        cls.l3if_b = ACIL3OutInterface.objects.create(
            aci_logical_interface_profile=cls.lip_svi,
            dcim_interface=cls.iface2,
        )

        # BGP peers
        cls.bgp_peer_a = ACIBGPPeer.objects.create(
            aci_logical_interface_profile=cls.lip_routed,
            name="peer-a",
            peer_address="10.0.0.10",
            remote_asn=65001,
        )
        cls.bgp_peer_b = ACIBGPPeer.objects.create(
            aci_logical_node_profile=cls.lnp_a,
            name="peer-b",
            peer_address="10.0.0.11",
            remote_asn=65002,
        )

        # OSPF policies
        cls.ospf_pol_pt = ACIOSPFInterfacePolicy.objects.create(
            aci_tenant=cls.tenant,
            name="ospf-pt",
            network_type=OSPFNetworkTypeChoices.POINT_TO_POINT,
        )
        cls.ospf_pol_bcast = ACIOSPFInterfacePolicy.objects.create(
            aci_tenant=cls.tenant,
            name="ospf-bcast",
            network_type=OSPFNetworkTypeChoices.BROADCAST,
        )

        # OSPF attachment
        cls.ospf_att = ACIOSPFInterfaceAttachment.objects.create(
            aci_logical_interface_profile=cls.lip_routed,
            aci_ospf_interface_policy=cls.ospf_pol_pt,
            ospf_area_id="0",
            ospf_area_type=OSPFAreaTypeChoices.REGULAR,
            name="ospf-att-a",
        )

        # EIGRP policies
        cls.eigrp_pol_a = ACIEIGRPInterfacePolicy.objects.create(
            aci_tenant=cls.tenant, name="eigrp-a"
        )
        cls.eigrp_pol_b = ACIEIGRPInterfacePolicy.objects.create(
            aci_tenant=cls.tenant2, name="eigrp-b"
        )

        # External EPGs + subnets
        cls.eepg_a = ACIExternalEPG.objects.create(aci_l3out=cls.l3out_bgp, name="ext-a")
        cls.eepg_b = ACIExternalEPG.objects.create(aci_l3out=cls.l3out_ospf, name="ext-b")
        cls.subnet_a = ACIExternalEPGSubnet.objects.create(
            aci_external_epg=cls.eepg_a,
            name="sub-a",
            prefix="10.0.0.0/8",
        )
        cls.subnet_b = ACIExternalEPGSubnet.objects.create(
            aci_external_epg=cls.eepg_b,
            name="sub-b",
            prefix="172.16.0.0/12",
        )

    # -----------------------------------------------------------------------
    # ACIL3OutFilterSet
    # -----------------------------------------------------------------------

    def test_l3out_filter_by_tenant(self):
        qs = ACIL3OutFilterSet({"aci_tenant_id": [self.tenant.pk]}, ACIL3Out.objects.all()).qs
        self.assertIn(self.l3out_bgp, qs)
        self.assertIn(self.l3out_ospf, qs)

    def test_l3out_filter_by_protocol_bgp(self):
        qs = ACIL3OutFilterSet({"protocol_bgp": True}, ACIL3Out.objects.all()).qs
        self.assertIn(self.l3out_bgp, qs)
        self.assertNotIn(self.l3out_ospf, qs)

    def test_l3out_filter_by_protocol_ospf(self):
        qs = ACIL3OutFilterSet({"protocol_ospf": True}, ACIL3Out.objects.all()).qs
        self.assertIn(self.l3out_ospf, qs)
        self.assertNotIn(self.l3out_bgp, qs)

    # -----------------------------------------------------------------------
    # ACILogicalNodeProfileFilterSet
    # -----------------------------------------------------------------------

    def test_lnp_filter_by_l3out(self):
        qs = ACILogicalNodeProfileFilterSet(
            {"aci_l3out_id": [self.l3out_bgp.pk]},
            ACILogicalNodeProfile.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.lnp_a])

    # -----------------------------------------------------------------------
    # ACILogicalNodeFilterSet
    # -----------------------------------------------------------------------

    def test_logical_node_filter_by_lnp(self):
        qs = ACILogicalNodeFilterSet(
            {"aci_logical_node_profile_id": [self.lnp_a.pk]},
            ACILogicalNode.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.ln_a])

    def test_logical_node_filter_by_aci_node(self):
        qs = ACILogicalNodeFilterSet(
            {"aci_node_id": [self.aci_node2.pk]},
            ACILogicalNode.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.ln_b])

    # -----------------------------------------------------------------------
    # ACILogicalInterfaceProfileFilterSet
    # -----------------------------------------------------------------------

    def test_lip_filter_by_lnp(self):
        qs = ACILogicalInterfaceProfileFilterSet(
            {"aci_logical_node_profile_id": [self.lnp_a.pk]},
            ACILogicalInterfaceProfile.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.lip_routed])

    def test_lip_filter_by_interface_type(self):
        qs = ACILogicalInterfaceProfileFilterSet(
            {"interface_type": [L3OutInterfaceTypeChoices.SVI]},
            ACILogicalInterfaceProfile.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.lip_svi])

    # -----------------------------------------------------------------------
    # ACIL3OutInterfaceFilterSet
    # -----------------------------------------------------------------------

    def test_l3if_filter_by_lip(self):
        qs = ACIL3OutInterfaceFilterSet(
            {"aci_logical_interface_profile_id": [self.lip_routed.pk]},
            ACIL3OutInterface.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.l3if_a])

    def test_l3if_filter_by_dcim_interface(self):
        qs = ACIL3OutInterfaceFilterSet(
            {"dcim_interface_id": [self.iface2.pk]},
            ACIL3OutInterface.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.l3if_b])

    # -----------------------------------------------------------------------
    # ACIBGPPeerFilterSet
    # -----------------------------------------------------------------------

    def test_bgp_peer_filter_by_lip(self):
        qs = ACIBGPPeerFilterSet(
            {"aci_logical_interface_profile_id": [self.lip_routed.pk]},
            ACIBGPPeer.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.bgp_peer_a])

    def test_bgp_peer_filter_by_remote_asn(self):
        qs = ACIBGPPeerFilterSet(
            {"remote_asn": 65002},
            ACIBGPPeer.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.bgp_peer_b])

    # -----------------------------------------------------------------------
    # ACIOSPFInterfacePolicyFilterSet
    # -----------------------------------------------------------------------

    def test_ospf_policy_filter_by_tenant(self):
        qs = ACIOSPFInterfacePolicyFilterSet(
            {"aci_tenant_id": [self.tenant.pk]},
            ACIOSPFInterfacePolicy.objects.all(),
        ).qs
        self.assertIn(self.ospf_pol_pt, qs)
        self.assertIn(self.ospf_pol_bcast, qs)

    def test_ospf_policy_filter_by_network_type(self):
        qs = ACIOSPFInterfacePolicyFilterSet(
            {"network_type": [OSPFNetworkTypeChoices.POINT_TO_POINT]},
            ACIOSPFInterfacePolicy.objects.all(),
        ).qs
        self.assertIn(self.ospf_pol_pt, qs)
        self.assertNotIn(self.ospf_pol_bcast, qs)

    # -----------------------------------------------------------------------
    # ACIOSPFInterfaceAttachmentFilterSet
    # -----------------------------------------------------------------------

    def test_ospf_att_filter_by_lip(self):
        qs = ACIOSPFInterfaceAttachmentFilterSet(
            {"aci_logical_interface_profile_id": [self.lip_routed.pk]},
            ACIOSPFInterfaceAttachment.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.ospf_att])

    def test_ospf_att_filter_by_area_type(self):
        qs = ACIOSPFInterfaceAttachmentFilterSet(
            {"ospf_area_type": [OSPFAreaTypeChoices.REGULAR]},
            ACIOSPFInterfaceAttachment.objects.all(),
        ).qs
        self.assertIn(self.ospf_att, qs)

    # -----------------------------------------------------------------------
    # ACIEIGRPInterfacePolicyFilterSet
    # -----------------------------------------------------------------------

    def test_eigrp_filter_by_tenant(self):
        qs = ACIEIGRPInterfacePolicyFilterSet(
            {"aci_tenant_id": [self.tenant.pk]},
            ACIEIGRPInterfacePolicy.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.eigrp_pol_a])

    # -----------------------------------------------------------------------
    # ACIExternalEPGFilterSet
    # -----------------------------------------------------------------------

    def test_eepg_filter_by_l3out(self):
        qs = ACIExternalEPGFilterSet(
            {"aci_l3out_id": [self.l3out_bgp.pk]},
            ACIExternalEPG.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.eepg_a])

    # -----------------------------------------------------------------------
    # ACIExternalEPGSubnetFilterSet
    # -----------------------------------------------------------------------

    def test_subnet_filter_by_eepg(self):
        qs = ACIExternalEPGSubnetFilterSet(
            {"aci_external_epg_id": [self.eepg_a.pk]},
            ACIExternalEPGSubnet.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.subnet_a])


# ---------------------------------------------------------------------------
# Phase 7.1 — Static Route filterset tests
# ---------------------------------------------------------------------------

from netbox_cisco_aci.choices import StaticRouteNextHopTypeChoices  # noqa: E402
from netbox_cisco_aci.filtersets.l3out import (  # noqa: E402
    ACIL3OutStaticRouteFilterSet,
    ACIL3OutStaticRouteNextHopFilterSet,
)
from netbox_cisco_aci.models.l3out import (  # noqa: E402
    ACIL3OutStaticRoute,
    ACIL3OutStaticRouteNextHop,
)


class StaticRouteFilterSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from netbox_cisco_aci.models.fabric import ACIFabric, ACINode, ACIPod

        fab = ACIFabric.objects.create(name="DC-SRFS")
        pod = ACIPod.objects.create(aci_fabric=fab, pod_id=1, name="pod-1")
        tenant = ACITenant.objects.create(aci_fabric=fab, name="t-srfs")
        vrf = ACIVRF.objects.create(aci_tenant=tenant, name="vrf-srfs")
        from netbox_cisco_aci.models.l3out import ACIL3Out, ACILogicalNode, ACILogicalNodeProfile

        l3out = ACIL3Out.objects.create(aci_tenant=tenant, aci_vrf=vrf, name="l3out-srfs")
        lnp = ACILogicalNodeProfile.objects.create(aci_l3out=l3out, name="lnp-srfs")
        node_a = ACINode.objects.create(aci_pod=pod, node_id=301, name="leaf-301", role="leaf")
        node_b = ACINode.objects.create(aci_pod=pod, node_id=302, name="leaf-302", role="leaf")
        cls.ln_a = ACILogicalNode.objects.create(
            aci_logical_node_profile=lnp, aci_node=node_a, name="ln-a", router_id="10.6.0.1"
        )
        cls.ln_b = ACILogicalNode.objects.create(
            aci_logical_node_profile=lnp, aci_node=node_b, name="ln-b", router_id="10.6.0.2"
        )
        cls.route_a = ACIL3OutStaticRoute.objects.create(
            aci_logical_node=cls.ln_a, prefix="10.0.0.0/8"
        )
        cls.route_b = ACIL3OutStaticRoute.objects.create(
            aci_logical_node=cls.ln_b, prefix="172.16.0.0/12"
        )
        cls.nh_prefix = ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=cls.route_a,
            nexthop_address="10.0.0.1",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        cls.nh_null = ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=cls.route_a,
            nexthop_address="",
            nexthop_type=StaticRouteNextHopTypeChoices.NONE,
        )

    def test_filter_by_logical_node(self):
        qs = ACIL3OutStaticRouteFilterSet({"aci_logical_node_id": [self.ln_a.pk]}).qs
        self.assertIn(self.route_a, qs)
        self.assertNotIn(self.route_b, qs)

    def test_filter_by_prefix(self):
        qs = ACIL3OutStaticRouteFilterSet({"prefix": ["10.0.0.0/8"]}).qs
        self.assertIn(self.route_a, qs)
        self.assertNotIn(self.route_b, qs)

    def test_filter_nexthop_by_static_route(self):
        qs = ACIL3OutStaticRouteNextHopFilterSet({"aci_static_route_id": [self.route_a.pk]}).qs
        self.assertIn(self.nh_prefix, qs)
        self.assertIn(self.nh_null, qs)
        self.assertEqual(qs.count(), 2)

    def test_filter_nexthop_by_type_prefix(self):
        qs = ACIL3OutStaticRouteNextHopFilterSet(
            {"nexthop_type": [StaticRouteNextHopTypeChoices.PREFIX]}
        ).qs
        self.assertIn(self.nh_prefix, qs)
        self.assertNotIn(self.nh_null, qs)

    def test_filter_nexthop_by_type_none(self):
        qs = ACIL3OutStaticRouteNextHopFilterSet(
            {"nexthop_type": [StaticRouteNextHopTypeChoices.NONE]}
        ).qs
        self.assertIn(self.nh_null, qs)
        self.assertNotIn(self.nh_prefix, qs)
