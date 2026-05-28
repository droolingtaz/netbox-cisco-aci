"""Tests for the Cisco ACI device/interface PluginTemplateExtensions."""

from dcim.models import Interface
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase

from netbox_cisco_aci.models.bindings import (
    ACIInterfaceFabricMembership,
    ACIStaticPortBinding,
)
from netbox_cisco_aci.models.fabric import ACIFabric, ACINode, ACIPod
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
)
from netbox_cisco_aci.template_content.device import ACIDeviceContextPanel
from netbox_cisco_aci.template_content.interface import ACIInterfaceContextPanel
from netbox_cisco_aci.tests.base import make_dcim_device


def _ctx(obj):
    request = RequestFactory().get("/")
    return {"object": obj, "request": request, "settings": {}, "config": {}}


class ACIDeviceContextPanelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.pod = ACIPod.objects.create(aci_fabric=cls.fab, pod_id=1, name="pod-1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="acme")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-prod")
        cls.bd = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd-web"
        )
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant, name="ap-web")
        cls.epg = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-web",
        )

    def test_returns_empty_for_unlinked_device(self):
        device = make_dcim_device("unlinked-leaf")
        ext = ACIDeviceContextPanel(_ctx(device))
        self.assertEqual(ext.full_width_page(), "")

    def test_renders_for_linked_device(self):
        device = make_dcim_device("linked-leaf")
        ct = ContentType.objects.get_for_model(device.__class__)
        ACINode.objects.create(
            aci_pod=self.pod,
            node_id=101,
            name="linked-leaf",
            node_object_type=ct,
            node_object_id=device.pk,
        )
        iface = Interface.objects.create(device=device, name="eth1/1", type="10gbase-t")
        ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg, dcim_interface=iface, encap_vlan=100
        )
        ext = ACIDeviceContextPanel(_ctx(device))
        out = ext.full_width_page()
        self.assertIn("Cisco ACI Context", out)
        self.assertIn("epg-web", out)
        self.assertIn("100", out)

    def test_renders_for_device_with_only_bindings_no_node(self):
        # Device has bindings but no ACINode link -> still render (binding
        # count > 0). The summary attr-table renders em-dashes for the
        # fabric/pod/node rows when those FKs aren't present, and the
        # bindings card still shows the encap so the operator sees the
        # ACI policy on the port.
        device = make_dcim_device("bindings-only")
        iface = Interface.objects.create(device=device, name="eth1/1", type="10gbase-t")
        ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg, dcim_interface=iface, encap_vlan=100
        )
        ext = ACIDeviceContextPanel(_ctx(device))
        out = ext.full_width_page()
        self.assertIn("Cisco ACI Context", out)
        # The encap from the binding is rendered in the bindings card.
        self.assertIn("100", out)
        # The ACI Node row in the summary table renders an em-dash because
        # there's no node linked. ``|placeholder`` outputs &mdash;.
        self.assertIn("&mdash;", out)


class ACIInterfaceContextPanelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.pod = ACIPod.objects.create(aci_fabric=cls.fab, pod_id=1, name="pod-1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="acme")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-prod")
        cls.bd = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd-web"
        )
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant, name="ap-web")
        cls.epg = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-web",
        )

    def test_returns_empty_when_no_aci_context(self):
        device = make_dcim_device("plain-leaf")
        iface = Interface.objects.create(device=device, name="eth1/1", type="10gbase-t")
        ext = ACIInterfaceContextPanel(_ctx(iface))
        self.assertEqual(ext.right_page(), "")

    def test_renders_for_interface_with_binding(self):
        device = make_dcim_device("bound-leaf")
        iface = Interface.objects.create(device=device, name="eth1/1", type="10gbase-t")
        ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg, dcim_interface=iface, encap_vlan=100
        )
        ext = ACIInterfaceContextPanel(_ctx(iface))
        out = ext.right_page()
        self.assertIn("Cisco ACI Context", out)
        self.assertIn("epg-web", out)

    def test_renders_for_interface_with_fabric_membership_only(self):
        device = make_dcim_device("memb-leaf")
        ct = ContentType.objects.get_for_model(device.__class__)
        node = ACINode.objects.create(
            aci_pod=self.pod,
            node_id=201,
            name="memb-leaf",
            node_object_type=ct,
            node_object_id=device.pk,
        )
        iface = Interface.objects.create(device=device, name="eth1/1", type="10gbase-t")
        ACIInterfaceFabricMembership.objects.create(dcim_interface=iface, aci_node=node)
        ext = ACIInterfaceContextPanel(_ctx(iface))
        out = ext.right_page()
        self.assertIn("Cisco ACI Context", out)
        self.assertIn("memb-leaf", out)


# ---------------------------------------------------------------------------
# Bucket D — empty-state early-return paths
# ---------------------------------------------------------------------------


class ACIDeviceContextPanelNoneObjectTests(TestCase):
    """Cover device.py L48, 51 — return '' when object is None."""

    def test_returns_empty_when_object_is_none(self):
        """device.py L48: `if device is None: return ""`."""
        ext = ACIDeviceContextPanel({"object": None, "request": None, "settings": {}, "config": {}})
        self.assertEqual(ext.full_width_page(), "")


class ACIInterfaceContextPanelNoneObjectTests(TestCase):
    """Cover interface.py L18 — return '' when object is None."""

    def test_returns_empty_when_object_is_none(self):
        """interface.py L18: `if interface is None: return ""`."""
        ext = ACIInterfaceContextPanel(
            {"object": None, "request": None, "settings": {}, "config": {}}
        )
        self.assertEqual(ext.right_page(), "")
