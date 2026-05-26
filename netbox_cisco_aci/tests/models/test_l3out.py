"""Model-level tests for Phase 7 L3Out objects."""

from dcim.models import Interface
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from netbox_cisco_aci.choices import OSPFAreaTypeChoices, OSPFNetworkTypeChoices
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


class _L3OutFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC-L3O")
        cls.pod = ACIPod.objects.create(aci_fabric=cls.fab, pod_id=1, name="pod-1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-l3o")
        cls.tenant_other = ACITenant.objects.create(
            aci_fabric=ACIFabric.objects.create(name="DC-Other"), name="other"
        )
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-l3o")
        cls.vrf_other = ACIVRF.objects.create(aci_tenant=cls.tenant_other, name="vrf-x")
        cls.device = make_dcim_device("leaf-l3o-1")
        cls.aci_node = ACINode.objects.create(
            aci_pod=cls.pod, node_id=101, name="leaf-101", role="leaf"
        )
        cls.l3out = ACIL3Out.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="l3out-core"
        )
        cls.lnp = ACILogicalNodeProfile.objects.create(aci_l3out=cls.l3out, name="lnp-a")
        cls.lip = ACILogicalInterfaceProfile.objects.create(
            aci_logical_node_profile=cls.lnp, name="lip-a"
        )


class ACIL3OutModelTests(_L3OutFixture):
    def test_string_and_url(self):
        self.assertEqual(str(self.l3out), "t-l3o / l3out-core")
        self.assertIn("/l3outs/", self.l3out.get_absolute_url())

    def test_tenant_vrf_cross_tenant_blocked(self):
        bad = ACIL3Out(aci_tenant=self.tenant, aci_vrf=self.vrf_other, name="bad")
        with self.assertRaises(ValidationError):
            bad.full_clean()

    def test_unique_per_tenant(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIL3Out.objects.create(aci_tenant=self.tenant, aci_vrf=self.vrf, name="l3out-core")

    def test_same_name_different_tenant_ok(self):
        ACIL3Out.objects.create(
            aci_tenant=self.tenant_other, aci_vrf=self.vrf_other, name="l3out-core"
        )


class ACILogicalNodeProfileModelTests(_L3OutFixture):
    def test_string(self):
        self.assertIn("lnp-a", str(self.lnp))

    def test_unique_per_l3out(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACILogicalNodeProfile.objects.create(aci_l3out=self.l3out, name="lnp-a")


class ACILogicalNodeModelTests(_L3OutFixture):
    def test_create_with_router_id(self):
        ln = ACILogicalNode.objects.create(
            aci_logical_node_profile=self.lnp,
            aci_node=self.aci_node,
            name="node-101",
            router_id="10.0.0.1",
        )
        self.assertEqual(ln.router_id, "10.0.0.1")
        self.assertIn("/logical-nodes/", ln.get_absolute_url())

    def test_unique_per_lnp_node(self):
        ACILogicalNode.objects.create(
            aci_logical_node_profile=self.lnp,
            aci_node=self.aci_node,
            name="n1",
            router_id="10.0.0.10",
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACILogicalNode.objects.create(
                aci_logical_node_profile=self.lnp,
                aci_node=self.aci_node,
                name="dup",
                router_id="10.0.0.11",
            )


class ACILogicalInterfaceProfileModelTests(_L3OutFixture):
    def test_string_and_unique(self):
        self.assertIn("lip-a", str(self.lip))
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACILogicalInterfaceProfile.objects.create(
                aci_logical_node_profile=self.lnp, name="lip-a"
            )


class ACIL3OutInterfaceModelTests(_L3OutFixture):
    def test_autoname_on_save(self):
        iface = Interface.objects.create(device=self.device, name="eth1/1", type="10gbase-t")
        i = ACIL3OutInterface.objects.create(
            aci_logical_interface_profile=self.lip,
            dcim_interface=iface,
            ip_address="192.0.2.1/30",
        )
        self.assertTrue(i.name.startswith("l3if_lip-a"))

    def test_invalid_ip_rejected(self):
        iface = Interface.objects.create(device=self.device, name="eth1/2", type="10gbase-t")
        i = ACIL3OutInterface(
            aci_logical_interface_profile=self.lip,
            dcim_interface=iface,
            ip_address="not-an-ip",
        )
        with self.assertRaises(ValidationError):
            i.full_clean()

    def test_secondary_ip_list_validated(self):
        iface = Interface.objects.create(device=self.device, name="eth1/3", type="10gbase-t")
        i = ACIL3OutInterface(
            aci_logical_interface_profile=self.lip,
            dcim_interface=iface,
            ip_address="192.0.2.1/30",
            secondary_ip_addresses=["nope"],
        )
        with self.assertRaises(ValidationError):
            i.full_clean()

    def test_unique_lip_iface(self):
        iface = Interface.objects.create(device=self.device, name="eth1/4", type="10gbase-t")
        ACIL3OutInterface.objects.create(
            aci_logical_interface_profile=self.lip, dcim_interface=iface
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIL3OutInterface.objects.create(
                aci_logical_interface_profile=self.lip, dcim_interface=iface
            )


class ACIBGPPeerModelTests(_L3OutFixture):
    def test_xor_lip_lnp(self):
        peer = ACIBGPPeer(
            aci_logical_interface_profile=self.lip,
            aci_logical_node_profile=self.lnp,
            peer_address="10.0.0.2",
            remote_asn=65001,
        )
        with self.assertRaises(ValidationError):
            peer.full_clean()
        peer2 = ACIBGPPeer(peer_address="10.0.0.3", remote_asn=65002)
        with self.assertRaises(ValidationError):
            peer2.full_clean()

    def test_lip_peer_ok(self):
        peer = ACIBGPPeer.objects.create(
            aci_logical_interface_profile=self.lip,
            peer_address="10.0.0.2",
            remote_asn=65001,
        )
        self.assertEqual(str(peer), "10.0.0.2 AS65001")

    def test_invalid_address(self):
        peer = ACIBGPPeer(
            aci_logical_node_profile=self.lnp,
            peer_address="not-ip",
            remote_asn=65001,
        )
        with self.assertRaises(ValidationError):
            peer.full_clean()


class ACIOSPFInterfacePolicyModelTests(_L3OutFixture):
    def test_create_and_str(self):
        p = ACIOSPFInterfacePolicy.objects.create(
            aci_tenant=self.tenant,
            name="ospf-pol",
            network_type=OSPFNetworkTypeChoices.POINT_TO_POINT,
        )
        self.assertIn("ospf-pol", str(p))

    def test_unique_per_tenant(self):
        ACIOSPFInterfacePolicy.objects.create(aci_tenant=self.tenant, name="ospf-pol")
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIOSPFInterfacePolicy.objects.create(aci_tenant=self.tenant, name="ospf-pol")


class ACIOSPFInterfaceAttachmentModelTests(_L3OutFixture):
    def setUp(self):
        self.pol = ACIOSPFInterfacePolicy.objects.create(aci_tenant=self.tenant, name="op")

    def test_decimal_area_ok(self):
        att = ACIOSPFInterfaceAttachment(
            aci_logical_interface_profile=self.lip,
            aci_ospf_interface_policy=self.pol,
            ospf_area_id="0",
            ospf_area_type=OSPFAreaTypeChoices.REGULAR,
            name="ospf-att-0",
        )
        att.full_clean()
        att.save()
        self.assertIn("OSPF area 0", str(att))

    def test_dotted_quad_area_ok(self):
        att = ACIOSPFInterfaceAttachment(
            aci_logical_interface_profile=self.lip,
            aci_ospf_interface_policy=self.pol,
            ospf_area_id="0.0.0.1",
            name="ospf-att-dq",
        )
        att.full_clean()

    def test_invalid_area(self):
        att = ACIOSPFInterfaceAttachment(
            aci_logical_interface_profile=self.lip,
            aci_ospf_interface_policy=self.pol,
            ospf_area_id="garbage",
            name="ospf-att-bad",
        )
        with self.assertRaises(ValidationError):
            att.full_clean()

    def test_lip_one_to_one(self):
        ACIOSPFInterfaceAttachment.objects.create(
            aci_logical_interface_profile=self.lip,
            aci_ospf_interface_policy=self.pol,
            ospf_area_id="0",
            name="ospf-att-1to1-a",
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIOSPFInterfaceAttachment.objects.create(
                aci_logical_interface_profile=self.lip,
                aci_ospf_interface_policy=self.pol,
                ospf_area_id="1",
                name="ospf-att-1to1-b",
            )


class ACIEIGRPInterfacePolicyModelTests(_L3OutFixture):
    def test_create(self):
        e = ACIEIGRPInterfacePolicy.objects.create(aci_tenant=self.tenant, name="eigrp1")
        self.assertEqual(str(e), "t-l3o / eigrp1")

    def test_unique_per_tenant(self):
        ACIEIGRPInterfacePolicy.objects.create(aci_tenant=self.tenant, name="e1")
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIEIGRPInterfacePolicy.objects.create(aci_tenant=self.tenant, name="e1")


class ACIExternalEPGModelTests(_L3OutFixture):
    def test_str_and_tenant_property(self):
        eepg = ACIExternalEPG.objects.create(aci_l3out=self.l3out, name="ext-1")
        self.assertIn("ext-1", str(eepg))
        self.assertEqual(eepg.aci_tenant, self.tenant)

    def test_unique_per_l3out(self):
        ACIExternalEPG.objects.create(aci_l3out=self.l3out, name="ext-1")
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIExternalEPG.objects.create(aci_l3out=self.l3out, name="ext-1")


class ACIExternalEPGSubnetModelTests(_L3OutFixture):
    def setUp(self):
        self.eepg = ACIExternalEPG.objects.create(aci_l3out=self.l3out, name="ext-net")

    def test_valid_prefix(self):
        s = ACIExternalEPGSubnet(aci_external_epg=self.eepg, name="any", prefix="0.0.0.0/0")
        s.full_clean()
        s.save()
        self.assertIn("0.0.0.0/0", str(s))

    def test_invalid_prefix(self):
        s = ACIExternalEPGSubnet(aci_external_epg=self.eepg, name="bad", prefix="not-a-prefix")
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test_unique_per_extepg(self):
        ACIExternalEPGSubnet.objects.create(
            aci_external_epg=self.eepg, name="a", prefix="10.0.0.0/8"
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIExternalEPGSubnet.objects.create(
                aci_external_epg=self.eepg, name="b", prefix="10.0.0.0/8"
            )


# ---------------------------------------------------------------------------
# Phase 7.1 — Static Routes
# ---------------------------------------------------------------------------

from netbox_cisco_aci.choices import StaticRouteNextHopTypeChoices  # noqa: E402
from netbox_cisco_aci.models.l3out import (  # noqa: E402
    ACIL3OutStaticRoute,
    ACIL3OutStaticRouteNextHop,
)


class ACIL3OutStaticRouteModelTests(_L3OutFixture):
    """Tests for ACIL3OutStaticRoute."""

    def setUp(self):
        self.ln = ACILogicalNode.objects.create(
            aci_logical_node_profile=self.lnp,
            aci_node=self.aci_node,
            name="ln-sr-1",
            router_id="10.1.0.1",
        )

    def test_create_and_str(self):
        route = ACIL3OutStaticRoute.objects.create(
            aci_logical_node=self.ln,
            prefix="10.50.0.0/16",
            preference=1,
        )
        self.assertIn("10.50.0.0/16", str(route))
        self.assertIn("ln-sr-1", str(route))
        self.assertIn("->", str(route))

    def test_auto_name_on_save(self):
        route = ACIL3OutStaticRoute.objects.create(
            aci_logical_node=self.ln,
            prefix="0.0.0.0/0",
        )
        self.assertTrue(route.name.startswith("route_"))
        # dots are legal in ACI policy names so regex keeps them;
        # slash becomes underscore → "0.0.0.0_0" is present in the name
        self.assertIn("0.0.0.0_0", route.name)

    def test_explicit_name_preserved(self):
        route = ACIL3OutStaticRoute.objects.create(
            aci_logical_node=self.ln,
            prefix="192.168.0.0/24",
            name="my-custom-name",
        )
        self.assertEqual(route.name, "my-custom-name")

    def test_get_absolute_url(self):
        route = ACIL3OutStaticRoute.objects.create(
            aci_logical_node=self.ln,
            prefix="10.10.0.0/16",
        )
        self.assertIn("/static-routes/", route.get_absolute_url())

    def test_invalid_prefix_raises_validation_error(self):
        route = ACIL3OutStaticRoute(
            aci_logical_node=self.ln,
            prefix="not-a-prefix",
        )
        with self.assertRaises(ValidationError):
            route.full_clean()

    def test_ipv6_prefix_valid(self):
        route = ACIL3OutStaticRoute.objects.create(
            aci_logical_node=self.ln,
            prefix="2001:db8::/32",
        )
        self.assertEqual(route.prefix, "2001:db8::/32")

    def test_unique_constraint_node_prefix(self):
        ACIL3OutStaticRoute.objects.create(
            aci_logical_node=self.ln,
            prefix="10.0.0.0/8",
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIL3OutStaticRoute.objects.create(
                aci_logical_node=self.ln,
                prefix="10.0.0.0/8",
            )

    def test_same_prefix_different_node_ok(self):
        ln2 = ACILogicalNode.objects.create(
            aci_logical_node_profile=self.lnp,
            aci_node=ACINode.objects.create(
                aci_pod=self.pod, node_id=202, name="leaf-202", role="leaf"
            ),
            name="ln-sr-2",
            router_id="10.2.0.1",
        )
        ACIL3OutStaticRoute.objects.create(aci_logical_node=self.ln, prefix="172.16.0.0/12")
        ACIL3OutStaticRoute.objects.create(aci_logical_node=ln2, prefix="172.16.0.0/12")


class ACIL3OutStaticRouteNextHopModelTests(_L3OutFixture):
    """Tests for ACIL3OutStaticRouteNextHop."""

    def setUp(self):
        self.ln = ACILogicalNode.objects.create(
            aci_logical_node_profile=self.lnp,
            aci_node=self.aci_node,
            name="ln-nh-1",
            router_id="10.3.0.1",
        )
        self.route = ACIL3OutStaticRoute.objects.create(
            aci_logical_node=self.ln,
            prefix="10.100.0.0/16",
        )

    def test_create_prefix_type(self):
        nh = ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=self.route,
            nexthop_address="192.0.2.1",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        self.assertIn("192.0.2.1", str(nh))
        self.assertIn("via", str(nh))

    def test_create_none_type_blank_address(self):
        nh = ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=self.route,
            nexthop_address="",
            nexthop_type=StaticRouteNextHopTypeChoices.NONE,
        )
        self.assertIn("null", str(nh))

    def test_none_type_with_address_raises(self):
        nh = ACIL3OutStaticRouteNextHop(
            aci_static_route=self.route,
            nexthop_address="10.0.0.1",
            nexthop_type=StaticRouteNextHopTypeChoices.NONE,
        )
        with self.assertRaises(ValidationError):
            nh.full_clean()

    def test_prefix_type_without_address_raises(self):
        nh = ACIL3OutStaticRouteNextHop(
            aci_static_route=self.route,
            nexthop_address="",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        with self.assertRaises(ValidationError):
            nh.full_clean()

    def test_invalid_address_raises(self):
        nh = ACIL3OutStaticRouteNextHop(
            aci_static_route=self.route,
            nexthop_address="not-an-ip",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        with self.assertRaises(ValidationError):
            nh.full_clean()

    def test_ipv6_nexthop_valid(self):
        nh = ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=self.route,
            nexthop_address="2001:db8::1",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        self.assertEqual(nh.nexthop_address, "2001:db8::1")

    def test_auto_name_on_save(self):
        nh = ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=self.route,
            nexthop_address="10.0.0.5",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        self.assertTrue(nh.name.startswith("nh_"))

    def test_get_absolute_url(self):
        nh = ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=self.route,
            nexthop_address="10.0.0.9",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        self.assertIn("/static-route-next-hops/", nh.get_absolute_url())

    def test_uniqueness_route_address_positive(self):
        ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=self.route,
            nexthop_address="10.0.0.1",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIL3OutStaticRouteNextHop.objects.create(
                aci_static_route=self.route,
                nexthop_address="10.0.0.1",
                nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
            )

    def test_different_address_same_route_ok(self):
        ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=self.route,
            nexthop_address="10.0.0.1",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        nh2 = ACIL3OutStaticRouteNextHop.objects.create(
            aci_static_route=self.route,
            nexthop_address="10.0.0.2",
            nexthop_type=StaticRouteNextHopTypeChoices.PREFIX,
        )
        self.assertEqual(nh2.nexthop_address, "10.0.0.2")
