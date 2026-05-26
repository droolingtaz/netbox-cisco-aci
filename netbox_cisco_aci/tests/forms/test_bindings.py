"""Form tests for Phase 6 binding models."""

from dcim.models import Interface
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from netbox_cisco_aci.choices import (
    InterfaceFabricRoleChoices,
    StaticPortBindingTypeChoices,
    StaticPortModeChoices,
)
from netbox_cisco_aci.forms.bindings import (
    ACIDomainBindingForm,
    ACIInterfaceFabricMembershipForm,
    ACIStaticPortBindingForm,
    ACIVPCBindingPairForm,
)
from netbox_cisco_aci.models.access import ACIDomain
from netbox_cisco_aci.models.bindings import ACIStaticPortBinding
from netbox_cisco_aci.models.fabric import ACIFabric, ACINode, ACIPod
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
)
from netbox_cisco_aci.tests.base import make_dcim_device


class Phase6FormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.fab2 = ACIFabric.objects.create(name="DC2")
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
        cls.device_a = make_dcim_device("leaf-101")
        cls.device_b = make_dcim_device("leaf-102")
        cls.iface_a = Interface.objects.create(device=cls.device_a, name="eth1/1", type="10gbase-t")
        cls.iface_b = Interface.objects.create(device=cls.device_b, name="eth1/1", type="10gbase-t")
        ct = ContentType.objects.get_for_model(cls.device_a.__class__)
        cls.node_a = ACINode.objects.create(
            aci_pod=cls.pod,
            node_id=101,
            name="leaf-101",
            node_object_type=ct,
            node_object_id=cls.device_a.pk,
        )

    def test_static_port_binding_form_valid(self):
        form = ACIStaticPortBindingForm(
            data={
                "aci_endpoint_group": self.epg.pk,
                "dcim_interface": self.iface_a.pk,
                "binding_type": StaticPortBindingTypeChoices.REGULAR,
                "encap_vlan": 100,
                "mode": StaticPortModeChoices.TRUNK,
                "deployment_immediacy": "lazy",
                "name": "spb-1",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_static_port_binding_form_invalid_encap_eq_primary(self):
        form = ACIStaticPortBindingForm(
            data={
                "aci_endpoint_group": self.epg.pk,
                "dcim_interface": self.iface_a.pk,
                "binding_type": StaticPortBindingTypeChoices.REGULAR,
                "encap_vlan": 100,
                "primary_encap_vlan": 100,
                "mode": StaticPortModeChoices.TRUNK,
                "deployment_immediacy": "lazy",
                "name": "spb-1",
            }
        )
        self.assertFalse(form.is_valid())

    def test_static_port_binding_form_requires_encap(self):
        form = ACIStaticPortBindingForm(
            data={
                "aci_endpoint_group": self.epg.pk,
                "dcim_interface": self.iface_a.pk,
                "binding_type": StaticPortBindingTypeChoices.REGULAR,
                "mode": StaticPortModeChoices.TRUNK,
                "deployment_immediacy": "lazy",
                "name": "spb-1",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("encap_vlan", form.errors)

    def test_vpc_binding_pair_form_valid(self):
        a = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg,
            dcim_interface=self.iface_a,
            encap_vlan=100,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )
        b = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg,
            dcim_interface=self.iface_b,
            encap_vlan=100,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )
        form = ACIVPCBindingPairForm(data={"binding_a": a.pk, "binding_b": b.pk, "name": "vpc-1"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_vpc_binding_pair_form_self_pair_invalid(self):
        a = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg,
            dcim_interface=self.iface_a,
            encap_vlan=100,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )
        form = ACIVPCBindingPairForm(data={"binding_a": a.pk, "binding_b": a.pk, "name": "vpc-1"})
        self.assertFalse(form.is_valid())

    def test_domain_binding_form_valid(self):
        dom = ACIDomain.objects.create(
            aci_fabric=self.fab, name="phys-dom-1", domain_type="physical"
        )
        form = ACIDomainBindingForm(
            data={
                "aci_endpoint_group": self.epg.pk,
                "aci_domain": dom.pk,
                "deployment_immediacy": "lazy",
                "resolution_immediacy": "lazy",
                "name": "db-1",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_domain_binding_form_cross_fabric_invalid(self):
        dom = ACIDomain.objects.create(
            aci_fabric=self.fab2, name="phys-dom-x", domain_type="physical"
        )
        form = ACIDomainBindingForm(
            data={
                "aci_endpoint_group": self.epg.pk,
                "aci_domain": dom.pk,
                "deployment_immediacy": "lazy",
                "resolution_immediacy": "lazy",
                "name": "db-x",
            }
        )
        self.assertFalse(form.is_valid())

    def test_interface_fabric_membership_form_valid(self):
        form = ACIInterfaceFabricMembershipForm(
            data={
                "dcim_interface": self.iface_a.pk,
                "aci_node": self.node_a.pk,
                "interface_role": InterfaceFabricRoleChoices.HOST,
                "name": "ifm-1",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_interface_fabric_membership_form_mismatched_device_invalid(self):
        # iface_b lives on device_b; node_a links device_a -> clean must reject
        form = ACIInterfaceFabricMembershipForm(
            data={
                "dcim_interface": self.iface_b.pk,
                "aci_node": self.node_a.pk,
                "interface_role": InterfaceFabricRoleChoices.HOST,
                "name": "ifm-bad",
            }
        )
        self.assertFalse(form.is_valid())
