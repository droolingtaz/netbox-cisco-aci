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
        cls.lnp = ACILogicalNodeProfile.objects.create(
            aci_l3out=cls.l3out, name="lnp-a"
        )
        cls.lip = ACILogicalInterfaceProfile.objects.create(
            aci_logical_node_profile=cls.lnp, name="lip-a"
        )


class ACIL3OutModelTests(_L3OutFixture):
    def test_string_and_url(self):
        self.assertEqual(str(self.l3out), "l3out-core")
        self.assertIn("/l3outs/", self.l3out.get_absolute_url())

    def test_tenant_vrf_cross_tenant_blocked(self):
        bad = ACIL3Out(
            aci_tenant=self.tenant, aci_vrf=self.vrf_other, name="bad"
        )
        with self.assertRaises(ValidationError):
            bad.full_clean()

    def test_unique_per_tenant(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIL3Out.objects.create(
                aci_tenant=self.tenant, aci_vrf=self.vrf, name="l3out-core"
            )

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
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACILogicalNode.objects.create(
                aci_logical_node_profile=self.lnp,
                aci_node=self.aci_node,
                name="dup",
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
        iface = Interface.objects.create(
            device=self.device, name="eth1/1", type="10gbase-t"
        )
        i = ACIL3OutInterface.objects.create(
            aci_logical_interface_profile=self.lip,
            dcim_interface=iface,
            ip_address="192.0.2.1/30",
        )
        self.assertTrue(i.name.startswith("l3if_lip-a"))

    def test_invalid_ip_rejected(self):
        iface = Interface.objects.create(
            device=self.device, name="eth1/2", type="10gbase-t"
        )
        i = ACIL3OutInterface(
            aci_logical_interface_profile=self.lip,
            dcim_interface=iface,
            ip_address="not-an-ip",
        )
        with self.assertRaises(ValidationError):
            i.full_clean()

    def test_secondary_ip_list_validated(self):
        iface = Interface.objects.create(
            device=self.device, name="eth1/3", type="10gbase-t"
        )
        i = ACIL3OutInterface(
            aci_logical_interface_profile=self.lip,
            dcim_interface=iface,
            ip_address="192.0.2.1/30",
            secondary_ip_addresses=["nope"],
        )
        with self.assertRaises(ValidationError):
            i.full_clean()

    def test_unique_lip_iface(self):
        iface = Interface.objects.create(
            device=self.device, name="eth1/4", type="10gbase-t"
        )
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
            network_type=OSPFNetworkTypeChoices.P2P,
        )
        self.assertIn("ospf-pol", str(p))

    def test_unique_per_tenant(self):
        ACIOSPFInterfacePolicy.objects.create(
            aci_tenant=self.tenant, name="ospf-pol"
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIOSPFInterfacePolicy.objects.create(
                aci_tenant=self.tenant, name="ospf-pol"
            )


class ACIOSPFInterfaceAttachmentModelTests(_L3OutFixture):
    def setUp(self):
        self.pol = ACIOSPFInterfacePolicy.objects.create(
            aci_tenant=self.tenant, name="op"
        )

    def test_decimal_area_ok(self):
        att = ACIOSPFInterfaceAttachment(
            aci_logical_interface_profile=self.lip,
            aci_ospf_interface_policy=self.pol,
            ospf_area_id="0",
            ospf_area_type=OSPFAreaTypeChoices.REGULAR,
        )
        att.full_clean()
        att.save()
        self.assertIn("OSPF area 0", str(att))

    def test_dotted_quad_area_ok(self):
        att = ACIOSPFInterfaceAttachment(
            aci_logical_interface_profile=self.lip,
            aci_ospf_interface_policy=self.pol,
            ospf_area_id="0.0.0.1",
        )
        att.full_clean()

    def test_invalid_area(self):
        att = ACIOSPFInterfaceAttachment(
            aci_logical_interface_profile=self.lip,
            aci_ospf_interface_policy=self.pol,
            ospf_area_id="garbage",
        )
        with self.assertRaises(ValidationError):
            att.full_clean()

    def test_lip_one_to_one(self):
        ACIOSPFInterfaceAttachment.objects.create(
            aci_logical_interface_profile=self.lip,
            aci_ospf_interface_policy=self.pol,
            ospf_area_id="0",
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIOSPFInterfaceAttachment.objects.create(
                aci_logical_interface_profile=self.lip,
                aci_ospf_interface_policy=self.pol,
                ospf_area_id="1",
            )


class ACIEIGRPInterfacePolicyModelTests(_L3OutFixture):
    def test_create(self):
        e = ACIEIGRPInterfacePolicy.objects.create(
            aci_tenant=self.tenant, name="eigrp1"
        )
        self.assertEqual(str(e), "eigrp1")

    def test_unique_per_tenant(self):
        ACIEIGRPInterfacePolicy.objects.create(aci_tenant=self.tenant, name="e1")
        with self.assertRaises(IntegrityError), transaction.atomic():
            ACIEIGRPInterfacePolicy.objects.create(
                aci_tenant=self.tenant, name="e1"
            )


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
        self.eepg = ACIExternalEPG.objects.create(
            aci_l3out=self.l3out, name="ext-net"
        )

    def test_valid_prefix(self):
        s = ACIExternalEPGSubnet(
            aci_external_epg=self.eepg, name="any", prefix="0.0.0.0/0"
        )
        s.full_clean()
        s.save()
        self.assertIn("0.0.0.0/0", str(s))

    def test_invalid_prefix(self):
        s = ACIExternalEPGSubnet(
            aci_external_epg=self.eepg, name="bad", prefix="not-a-prefix"
        )
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
