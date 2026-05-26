"""FilterSet tests for Phase 6 binding models."""

from dcim.models import Interface
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from netbox_cisco_aci.choices import (
    InterfaceFabricRoleChoices,
    StaticPortBindingTypeChoices,
)
from netbox_cisco_aci.filtersets.bindings import (
    ACIDomainBindingFilterSet,
    ACIInterfaceFabricMembershipFilterSet,
    ACIStaticPortBindingFilterSet,
    ACIVPCBindingPairFilterSet,
)
from netbox_cisco_aci.models.access import ACIDomain
from netbox_cisco_aci.models.bindings import (
    ACIDomainBinding,
    ACIInterfaceFabricMembership,
    ACIStaticPortBinding,
    ACIVPCBindingPair,
)
from netbox_cisco_aci.models.fabric import ACIFabric, ACINode, ACIPod
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
)
from netbox_cisco_aci.tests.base import make_dcim_device


class Phase6FilterSetTests(TestCase):
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
        cls.epg_a = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-a",
        )
        cls.epg_b = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-b",
        )
        cls.dev_a = make_dcim_device("leaf-101")
        cls.dev_b = make_dcim_device("leaf-102")
        cls.iface_a = Interface.objects.create(device=cls.dev_a, name="eth1/1", type="10gbase-t")
        cls.iface_b = Interface.objects.create(device=cls.dev_b, name="eth1/1", type="10gbase-t")

        ct = ContentType.objects.get_for_model(cls.dev_a.__class__)
        cls.node_a = ACINode.objects.create(
            aci_pod=cls.pod,
            node_id=101,
            name="leaf-101",
            node_object_type=ct,
            node_object_id=cls.dev_a.pk,
        )
        cls.node_b = ACINode.objects.create(
            aci_pod=cls.pod,
            node_id=102,
            name="leaf-102",
            node_object_type=ct,
            node_object_id=cls.dev_b.pk,
        )

        cls.b1 = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=cls.epg_a, dcim_interface=cls.iface_a, encap_vlan=100
        )
        cls.b2 = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=cls.epg_b,
            dcim_interface=cls.iface_b,
            encap_vlan=200,
            binding_type=StaticPortBindingTypeChoices.PC,
        )

        cls.dom_a = ACIDomain.objects.create(
            aci_fabric=cls.fab, name="phys-a", domain_type="physical"
        )
        cls.dom_b = ACIDomain.objects.create(
            aci_fabric=cls.fab, name="phys-b", domain_type="physical"
        )
        cls.db1 = ACIDomainBinding.objects.create(
            aci_endpoint_group=cls.epg_a, aci_domain=cls.dom_a
        )
        cls.db2 = ACIDomainBinding.objects.create(
            aci_endpoint_group=cls.epg_b, aci_domain=cls.dom_b
        )

        cls.m1 = ACIInterfaceFabricMembership.objects.create(
            dcim_interface=cls.iface_a,
            aci_node=cls.node_a,
            interface_role=InterfaceFabricRoleChoices.HOST,
        )
        cls.m2 = ACIInterfaceFabricMembership.objects.create(
            dcim_interface=cls.iface_b,
            aci_node=cls.node_b,
            interface_role=InterfaceFabricRoleChoices.FABRIC,
        )

    # --- ACIStaticPortBinding ---

    def test_spb_filter_by_epg(self):
        qs = ACIStaticPortBindingFilterSet(
            {"aci_endpoint_group_id": [self.epg_a.pk]}, ACIStaticPortBinding.objects.all()
        ).qs
        self.assertSequenceEqual(list(qs), [self.b1])

    def test_spb_filter_by_interface(self):
        qs = ACIStaticPortBindingFilterSet(
            {"dcim_interface_id": [self.iface_b.pk]}, ACIStaticPortBinding.objects.all()
        ).qs
        self.assertSequenceEqual(list(qs), [self.b2])

    def test_spb_filter_by_binding_type(self):
        qs = ACIStaticPortBindingFilterSet(
            {"binding_type": [StaticPortBindingTypeChoices.PC]},
            ACIStaticPortBinding.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.b2])

    def test_spb_filter_by_encap(self):
        qs = ACIStaticPortBindingFilterSet(
            {"encap_vlan": [100]}, ACIStaticPortBinding.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.b1)

    # --- ACIVPCBindingPair ---

    def test_vpc_filter_by_binding_a(self):
        a = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg_a,
            dcim_interface=Interface.objects.create(
                device=self.dev_a, name="eth1/3", type="10gbase-t"
            ),
            encap_vlan=300,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )
        b = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg_a,
            dcim_interface=Interface.objects.create(
                device=self.dev_b, name="eth1/3", type="10gbase-t"
            ),
            encap_vlan=300,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )
        pair = ACIVPCBindingPair.objects.create(binding_a=a, binding_b=b)
        qs = ACIVPCBindingPairFilterSet(
            {"binding_a_id": [a.pk]}, ACIVPCBindingPair.objects.all()
        ).qs
        self.assertSequenceEqual(list(qs), [pair])

    # --- ACIDomainBinding ---

    def test_dom_filter_by_epg(self):
        qs = ACIDomainBindingFilterSet(
            {"aci_endpoint_group_id": [self.epg_a.pk]}, ACIDomainBinding.objects.all()
        ).qs
        self.assertSequenceEqual(list(qs), [self.db1])

    def test_dom_filter_by_domain(self):
        qs = ACIDomainBindingFilterSet(
            {"aci_domain_id": [self.dom_b.pk]}, ACIDomainBinding.objects.all()
        ).qs
        self.assertSequenceEqual(list(qs), [self.db2])

    # --- ACIInterfaceFabricMembership ---

    def test_ifm_filter_by_node(self):
        qs = ACIInterfaceFabricMembershipFilterSet(
            {"aci_node_id": [self.node_a.pk]},
            ACIInterfaceFabricMembership.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.m1])

    def test_ifm_filter_by_interface(self):
        qs = ACIInterfaceFabricMembershipFilterSet(
            {"dcim_interface_id": [self.iface_b.pk]},
            ACIInterfaceFabricMembership.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.m2])

    def test_ifm_filter_by_role(self):
        qs = ACIInterfaceFabricMembershipFilterSet(
            {"interface_role": [InterfaceFabricRoleChoices.FABRIC]},
            ACIInterfaceFabricMembership.objects.all(),
        ).qs
        self.assertSequenceEqual(list(qs), [self.m2])
