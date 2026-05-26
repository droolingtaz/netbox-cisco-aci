"""Form tests for Phase 7 L3Out models."""

from dcim.models import Interface
from django.test import TestCase

from netbox_cisco_aci.choices import (
    L3OutInterfaceTypeChoices,
    OSPFAreaTypeChoices,
    OSPFNetworkTypeChoices,
)
from netbox_cisco_aci.forms.l3out import (
    ACIBGPPeerForm,
    ACIEIGRPInterfacePolicyForm,
    ACIExternalEPGForm,
    ACIExternalEPGSubnetForm,
    ACIL3OutForm,
    ACIL3OutInterfaceForm,
    ACILogicalInterfaceProfileForm,
    ACILogicalNodeForm,
    ACILogicalNodeProfileForm,
    ACIOSPFInterfaceAttachmentForm,
    ACIOSPFInterfacePolicyForm,
)
from netbox_cisco_aci.models.fabric import ACIFabric, ACINode, ACIPod
from netbox_cisco_aci.models.l3out import (
    ACIExternalEPG,
    ACIL3Out,
    ACILogicalInterfaceProfile,
    ACILogicalNodeProfile,
    ACIOSPFInterfacePolicy,
)
from netbox_cisco_aci.models.tenant import ACIVRF, ACITenant
from netbox_cisco_aci.tests.base import make_dcim_device


class L3OutFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC-Form")
        cls.pod = ACIPod.objects.create(aci_fabric=cls.fab, pod_id=1, name="pod-1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-form")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-form")
        cls.l3out = ACIL3Out.objects.create(
            aci_tenant=cls.tenant,
            aci_vrf=cls.vrf,
            name="l3out-form",
            protocol_static=True,
        )
        cls.lnp = ACILogicalNodeProfile.objects.create(aci_l3out=cls.l3out, name="lnp-form")
        cls.lip = ACILogicalInterfaceProfile.objects.create(
            aci_logical_node_profile=cls.lnp, name="lip-form"
        )
        cls.device = make_dcim_device("leaf-form-1")
        cls.iface = Interface.objects.create(device=cls.device, name="eth1/1", type="10gbase-t")
        cls.aci_node = ACINode.objects.create(
            aci_pod=cls.pod, node_id=101, name="leaf-101", role="leaf"
        )
        cls.ospf_pol = ACIOSPFInterfacePolicy.objects.create(
            aci_tenant=cls.tenant, name="ospf-pol-form"
        )
        cls.eepg = ACIExternalEPG.objects.create(aci_l3out=cls.l3out, name="ext-form")

    # -----------------------------------------------------------------------
    # ACIL3Out
    # -----------------------------------------------------------------------

    def test_l3out_form_valid(self):
        form = ACIL3OutForm(
            data={
                "name": "l3out-new",
                "aci_tenant": self.tenant.pk,
                "aci_vrf": self.vrf.pk,
                "protocol_static": True,
                "protocol_bgp": False,
                "protocol_ospf": False,
                "protocol_eigrp": False,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_l3out_form_no_protocol_invalid(self):
        """At least one routing protocol must be True."""
        form = ACIL3OutForm(
            data={
                "name": "l3out-noprot",
                "aci_tenant": self.tenant.pk,
                "aci_vrf": self.vrf.pk,
                "protocol_static": False,
                "protocol_bgp": False,
                "protocol_ospf": False,
                "protocol_eigrp": False,
            }
        )
        # The clean() raises on the model; Django forms pass model clean through
        self.assertFalse(form.is_valid())

    # -----------------------------------------------------------------------
    # ACILogicalNodeProfile
    # -----------------------------------------------------------------------

    def test_lnp_form_valid(self):
        form = ACILogicalNodeProfileForm(
            data={
                "name": "lnp-new",
                "aci_l3out": self.l3out.pk,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    # -----------------------------------------------------------------------
    # ACILogicalNode
    # -----------------------------------------------------------------------

    def test_logical_node_form_valid(self):
        form = ACILogicalNodeForm(
            data={
                "name": "ln-new",
                "aci_logical_node_profile": self.lnp.pk,
                "aci_node": self.aci_node.pk,
                "router_id": "10.0.0.1",
                "use_router_id_as_loopback": True,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_logical_node_form_loopback_required_when_no_rid_loopback(self):
        """use_router_id_as_loopback=False requires loopback_address."""
        form = ACILogicalNodeForm(
            data={
                "name": "ln-nolb",
                "aci_logical_node_profile": self.lnp.pk,
                "aci_node": self.aci_node.pk,
                "router_id": "10.0.0.2",
                "use_router_id_as_loopback": False,
                "loopback_address": "",
            }
        )
        self.assertFalse(form.is_valid())

    # -----------------------------------------------------------------------
    # ACILogicalInterfaceProfile
    # -----------------------------------------------------------------------

    def test_lip_form_valid_routed(self):
        form = ACILogicalInterfaceProfileForm(
            data={
                "name": "lip-new",
                "aci_logical_node_profile": self.lnp.pk,
                "interface_type": L3OutInterfaceTypeChoices.ROUTED,
                "mtu": 9000,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_lip_form_svi_requires_encap(self):
        """SVI type requires encap_vlan."""
        form = ACILogicalInterfaceProfileForm(
            data={
                "name": "lip-svi-nenc",
                "aci_logical_node_profile": self.lnp.pk,
                "interface_type": L3OutInterfaceTypeChoices.SVI,
                "mtu": 9000,
            }
        )
        self.assertFalse(form.is_valid())

    def test_lip_form_sub_interface_valid(self):
        form = ACILogicalInterfaceProfileForm(
            data={
                "name": "lip-sub",
                "aci_logical_node_profile": self.lnp.pk,
                "interface_type": L3OutInterfaceTypeChoices.SUB_INTERFACE,
                "encap_vlan": 100,
                "mtu": 9000,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    # -----------------------------------------------------------------------
    # ACIL3OutInterface
    # -----------------------------------------------------------------------

    def test_l3out_interface_form_valid(self):
        form = ACIL3OutInterfaceForm(
            data={
                "name": "l3if-new",
                "aci_logical_interface_profile": self.lip.pk,
                "dcim_interface": self.iface.pk,
                "ip_address": "192.0.2.1/30",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    # -----------------------------------------------------------------------
    # ACIBGPPeer
    # -----------------------------------------------------------------------

    def test_bgp_peer_form_valid_lip(self):
        form = ACIBGPPeerForm(
            data={
                "name": "bgp-peer-new",
                "aci_logical_interface_profile": self.lip.pk,
                "peer_address": "10.0.0.2",
                "remote_asn": 65001,
                "ebgp_multihop_ttl": 1,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_bgp_peer_form_xor_invalid_both(self):
        """Both LIP and LNP set → invalid."""
        form = ACIBGPPeerForm(
            data={
                "name": "bgp-peer-bad",
                "aci_logical_interface_profile": self.lip.pk,
                "aci_logical_node_profile": self.lnp.pk,
                "peer_address": "10.0.0.3",
                "remote_asn": 65002,
                "ebgp_multihop_ttl": 1,
            }
        )
        self.assertFalse(form.is_valid())

    def test_bgp_peer_form_xor_invalid_neither(self):
        """Neither LIP nor LNP set → invalid."""
        form = ACIBGPPeerForm(
            data={
                "name": "bgp-peer-empty",
                "peer_address": "10.0.0.4",
                "remote_asn": 65003,
                "ebgp_multihop_ttl": 1,
            }
        )
        self.assertFalse(form.is_valid())

    # -----------------------------------------------------------------------
    # ACIOSPFInterfacePolicy
    # -----------------------------------------------------------------------

    def test_ospf_policy_form_valid(self):
        form = ACIOSPFInterfacePolicyForm(
            data={
                "name": "ospf-pol-new",
                "aci_tenant": self.tenant.pk,
                "network_type": OSPFNetworkTypeChoices.UNSPECIFIED,
                "priority": 1,
                "cost": 0,
                "hello_interval": 10,
                "dead_interval": 40,
                "retransmit_interval": 5,
                "transmit_delay": 1,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    # -----------------------------------------------------------------------
    # ACIOSPFInterfaceAttachment
    # -----------------------------------------------------------------------

    def test_ospf_attachment_form_valid(self):
        form = ACIOSPFInterfaceAttachmentForm(
            data={
                "name": "ospf-att-new",
                "aci_logical_interface_profile": self.lip.pk,
                "aci_ospf_interface_policy": self.ospf_pol.pk,
                "ospf_area_id": "0",
                "ospf_area_type": OSPFAreaTypeChoices.REGULAR,
                "ospf_area_cost": 1,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    # -----------------------------------------------------------------------
    # ACIEIGRPInterfacePolicy
    # -----------------------------------------------------------------------

    def test_eigrp_policy_form_valid(self):
        form = ACIEIGRPInterfacePolicyForm(
            data={
                "name": "eigrp-pol-new",
                "aci_tenant": self.tenant.pk,
                "hello_interval": 5,
                "hold_interval": 15,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    # -----------------------------------------------------------------------
    # ACIExternalEPG
    # -----------------------------------------------------------------------

    def test_external_epg_form_valid(self):
        form = ACIExternalEPGForm(
            data={
                "name": "ext-epg-new",
                "aci_l3out": self.l3out.pk,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    # -----------------------------------------------------------------------
    # ACIExternalEPGSubnet
    # -----------------------------------------------------------------------

    def test_external_epg_subnet_form_valid(self):
        form = ACIExternalEPGSubnetForm(
            data={
                "name": "subnet-new",
                "aci_external_epg": self.eepg.pk,
                "prefix": "10.0.0.0/8",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_external_epg_subnet_form_invalid_prefix(self):
        form = ACIExternalEPGSubnetForm(
            data={
                "name": "subnet-bad",
                "aci_external_epg": self.eepg.pk,
                "prefix": "not-a-prefix",
            }
        )
        self.assertFalse(form.is_valid())


# ---------------------------------------------------------------------------
# Phase 7.1 — Static Route form tests
# ---------------------------------------------------------------------------

from netbox_cisco_aci.choices import StaticRouteNextHopTypeChoices  # noqa: E402
from netbox_cisco_aci.forms.l3out import (  # noqa: E402
    ACIL3OutStaticRouteForm,
    ACIL3OutStaticRouteNextHopForm,
)
from netbox_cisco_aci.models.l3out import (  # noqa: E402
    ACIL3OutStaticRoute,
    ACILogicalNode,
)


class StaticRouteFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from netbox_cisco_aci.models.fabric import ACIFabric, ACINode, ACIPod

        cls.fab = ACIFabric.objects.create(name="DC-SRForm")
        cls.pod = ACIPod.objects.create(aci_fabric=cls.fab, pod_id=1, name="pod-1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-srform")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-srform")
        from netbox_cisco_aci.models.l3out import ACIL3Out, ACILogicalNodeProfile

        cls.l3out = ACIL3Out.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="l3out-srform"
        )
        cls.lnp = ACILogicalNodeProfile.objects.create(aci_l3out=cls.l3out, name="lnp-srform")
        cls.aci_node = ACINode.objects.create(
            aci_pod=cls.pod, node_id=201, name="leaf-201", role="leaf"
        )
        cls.ln = ACILogicalNode.objects.create(
            aci_logical_node_profile=cls.lnp,
            aci_node=cls.aci_node,
            name="ln-srform",
            router_id="10.5.0.1",
        )

    def test_valid_static_route_form(self):
        form = ACIL3OutStaticRouteForm(
            data={
                "name": "test-route",
                "aci_logical_node": self.ln.pk,
                "prefix": "192.168.1.0/24",
                "preference": 1,
                "route_controls": "[]",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_static_route_form_missing_prefix(self):
        form = ACIL3OutStaticRouteForm(
            data={
                "name": "bad-route",
                "aci_logical_node": self.ln.pk,
                "preference": 1,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("prefix", form.errors)

    def test_valid_nexthop_form(self):
        route = ACIL3OutStaticRoute.objects.create(aci_logical_node=self.ln, prefix="10.20.0.0/16")
        form = ACIL3OutStaticRouteNextHopForm(
            data={
                "name": "nh-test",
                "aci_static_route": route.pk,
                "nexthop_address": "10.0.0.1",
                "nexthop_type": StaticRouteNextHopTypeChoices.PREFIX,
                "preference": 0,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_nexthop_form_missing_route(self):
        form = ACIL3OutStaticRouteNextHopForm(
            data={
                "name": "nh-bad",
                "nexthop_address": "10.0.0.1",
                "nexthop_type": StaticRouteNextHopTypeChoices.PREFIX,
                "preference": 0,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("aci_static_route", form.errors)
