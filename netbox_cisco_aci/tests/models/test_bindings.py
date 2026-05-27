"""Model-level tests for Phase 6: Static Port Bindings + Template Extensions."""

from dcim.models import Interface
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from netbox_cisco_aci.choices import (
    DeploymentImmediacyChoices,
    InterfaceFabricRoleChoices,
    StaticPortBindingTypeChoices,
    StaticPortModeChoices,
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


class _BindingFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.fab2 = ACIFabric.objects.create(name="DC2")
        cls.pod = ACIPod.objects.create(aci_fabric=cls.fab, pod_id=1, name="pod-1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="acme")
        cls.tenant_other = ACITenant.objects.create(aci_fabric=cls.fab2, name="other")
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
        cls.epg_useg = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-useg",
            is_useg=True,
        )
        cls.device_a = make_dcim_device("leaf-101")
        cls.device_b = make_dcim_device("leaf-102")
        cls.iface_a = Interface.objects.create(device=cls.device_a, name="eth1/1", type="10gbase-t")
        cls.iface_b = Interface.objects.create(device=cls.device_b, name="eth1/1", type="10gbase-t")
        cls.iface_a2 = Interface.objects.create(
            device=cls.device_a, name="eth1/2", type="10gbase-t"
        )

        cls.device_ct = ContentType.objects.get_for_model(cls.device_a.__class__)
        cls.node_a = ACINode.objects.create(
            aci_pod=cls.pod,
            node_id=101,
            name="leaf-101",
            node_object_type=cls.device_ct,
            node_object_id=cls.device_a.pk,
        )
        cls.node_b = ACINode.objects.create(
            aci_pod=cls.pod,
            node_id=102,
            name="leaf-102",
            node_object_type=cls.device_ct,
            node_object_id=cls.device_b.pk,
        )


# ---------------------------------------------------------------------------
# ACIStaticPortBinding
# ---------------------------------------------------------------------------


class ACIStaticPortBindingTests(_BindingFixture):
    def test_create_defaults(self):
        b = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg, dcim_interface=self.iface_a, encap_vlan=100
        )
        self.assertEqual(b.binding_type, StaticPortBindingTypeChoices.REGULAR)
        self.assertEqual(b.mode, StaticPortModeChoices.TRUNK)
        self.assertEqual(b.deployment_immediacy, DeploymentImmediacyChoices.ON_DEMAND)

    def test_str(self):
        b = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg, dcim_interface=self.iface_a, encap_vlan=100
        )
        self.assertIn("epg-web", str(b))
        self.assertIn("VLAN 100", str(b))

    def test_unique_natural_key(self):
        ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg, dcim_interface=self.iface_a, encap_vlan=100
        )
        with self.assertRaises(IntegrityError):
            ACIStaticPortBinding.objects.create(
                aci_endpoint_group=self.epg, dcim_interface=self.iface_a, encap_vlan=100
            )

    def test_same_encap_different_interface_ok(self):
        ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg, dcim_interface=self.iface_a, encap_vlan=100
        )
        ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg, dcim_interface=self.iface_b, encap_vlan=100
        )

    def test_clean_encap_eq_primary_rejected(self):
        b = ACIStaticPortBinding(
            aci_endpoint_group=self.epg_useg,
            dcim_interface=self.iface_a,
            encap_vlan=100,
            primary_encap_vlan=100,
        )
        with self.assertRaises(ValidationError):
            b.clean()

    def test_clean_encap_neq_primary_ok(self):
        b = ACIStaticPortBinding(
            aci_endpoint_group=self.epg_useg,
            dcim_interface=self.iface_a,
            encap_vlan=100,
            primary_encap_vlan=200,
        )
        b.clean()

    def test_clean_access_untag_with_fex_rejected(self):
        b = ACIStaticPortBinding(
            aci_endpoint_group=self.epg,
            dcim_interface=self.iface_a,
            encap_vlan=100,
            mode=StaticPortModeChoices.ACCESS_UNTAG,
            binding_type=StaticPortBindingTypeChoices.FEX,
        )
        with self.assertRaises(ValidationError):
            b.clean()

    def test_clean_access_untag_with_regular_ok(self):
        b = ACIStaticPortBinding(
            aci_endpoint_group=self.epg,
            dcim_interface=self.iface_a,
            encap_vlan=100,
            mode=StaticPortModeChoices.ACCESS_UNTAG,
            binding_type=StaticPortBindingTypeChoices.REGULAR,
        )
        b.clean()

    def test_clean_primary_encap_non_useg_rejected(self):
        b = ACIStaticPortBinding(
            aci_endpoint_group=self.epg,
            dcim_interface=self.iface_a,
            encap_vlan=100,
            primary_encap_vlan=200,
        )
        with self.assertRaises(ValidationError):
            b.clean()

    def test_clean_primary_encap_useg_ok(self):
        b = ACIStaticPortBinding(
            aci_endpoint_group=self.epg_useg,
            dcim_interface=self.iface_a,
            encap_vlan=100,
            primary_encap_vlan=200,
        )
        b.clean()


# ---------------------------------------------------------------------------
# ACIVPCBindingPair
# ---------------------------------------------------------------------------


class ACIVPCBindingPairTests(_BindingFixture):
    def _make_vpc_binding(self, iface, encap=100, epg=None):
        return ACIStaticPortBinding.objects.create(
            aci_endpoint_group=epg or self.epg,
            dcim_interface=iface,
            encap_vlan=encap,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )

    def test_create_valid_pair(self):
        a = self._make_vpc_binding(self.iface_a)
        b = self._make_vpc_binding(self.iface_b)
        pair = ACIVPCBindingPair.objects.create(binding_a=a, binding_b=b)
        self.assertIn("vPC", str(pair))

    def test_clean_distinct_bindings(self):
        a = self._make_vpc_binding(self.iface_a)
        pair = ACIVPCBindingPair(binding_a=a, binding_b=a)
        with self.assertRaises(ValidationError):
            pair.clean()

    def test_clean_both_must_be_vpc(self):
        a = self._make_vpc_binding(self.iface_a)
        b = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg,
            dcim_interface=self.iface_b,
            encap_vlan=100,
            binding_type=StaticPortBindingTypeChoices.REGULAR,
        )
        pair = ACIVPCBindingPair(binding_a=a, binding_b=b)
        with self.assertRaises(ValidationError):
            pair.clean()

    def test_clean_same_epg(self):
        a = self._make_vpc_binding(self.iface_a, epg=self.epg)
        b = self._make_vpc_binding(self.iface_b, epg=self.epg_useg)
        pair = ACIVPCBindingPair(binding_a=a, binding_b=b)
        with self.assertRaises(ValidationError):
            pair.clean()

    def test_clean_same_encap(self):
        a = self._make_vpc_binding(self.iface_a, encap=100)
        b = self._make_vpc_binding(self.iface_b, encap=200)
        pair = ACIVPCBindingPair(binding_a=a, binding_b=b)
        with self.assertRaises(ValidationError):
            pair.clean()

    def test_clean_different_devices(self):
        a = self._make_vpc_binding(self.iface_a)
        # same device, different interface
        b = self._make_vpc_binding(self.iface_a2)
        pair = ACIVPCBindingPair(binding_a=a, binding_b=b)
        with self.assertRaises(ValidationError):
            pair.clean()

    def test_check_constraint_blocks_db_self_pair(self):
        a = self._make_vpc_binding(self.iface_a)
        with self.assertRaises(IntegrityError):
            ACIVPCBindingPair.objects.create(binding_a=a, binding_b=a)


# ---------------------------------------------------------------------------
# ACIDomainBinding
# ---------------------------------------------------------------------------


class ACIDomainBindingTests(_BindingFixture):
    def test_create_and_str(self):
        dom = ACIDomain.objects.create(
            aci_fabric=self.fab, name="phys-dom-1", domain_type="physical"
        )
        b = ACIDomainBinding.objects.create(aci_endpoint_group=self.epg, aci_domain=dom)
        self.assertIn("epg-web", str(b))
        self.assertIn("phys-dom-1", str(b))

    def test_unique(self):
        dom = ACIDomain.objects.create(
            aci_fabric=self.fab, name="phys-dom-1", domain_type="physical"
        )
        ACIDomainBinding.objects.create(aci_endpoint_group=self.epg, aci_domain=dom)
        with self.assertRaises(IntegrityError):
            ACIDomainBinding.objects.create(aci_endpoint_group=self.epg, aci_domain=dom)

    def test_cross_fabric_rejected(self):
        # Domain in fab2, EPG in fab1
        dom = ACIDomain.objects.create(
            aci_fabric=self.fab2, name="phys-dom-x", domain_type="physical"
        )
        b = ACIDomainBinding(aci_endpoint_group=self.epg, aci_domain=dom)
        with self.assertRaises(ValidationError):
            b.clean()

    def test_same_fabric_ok(self):
        dom = ACIDomain.objects.create(
            aci_fabric=self.fab, name="phys-dom-1", domain_type="physical"
        )
        b = ACIDomainBinding(aci_endpoint_group=self.epg, aci_domain=dom)
        b.clean()


# ---------------------------------------------------------------------------
# ACIInterfaceFabricMembership
# ---------------------------------------------------------------------------


class ACIInterfaceFabricMembershipTests(_BindingFixture):
    def test_create_default_role(self):
        m = ACIInterfaceFabricMembership.objects.create(
            dcim_interface=self.iface_a, aci_node=self.node_a
        )
        self.assertEqual(m.interface_role, InterfaceFabricRoleChoices.HOST)

    def test_str(self):
        m = ACIInterfaceFabricMembership.objects.create(
            dcim_interface=self.iface_a, aci_node=self.node_a
        )
        self.assertIn("leaf-101", str(m))

    def test_one_membership_per_interface(self):
        ACIInterfaceFabricMembership.objects.create(
            dcim_interface=self.iface_a, aci_node=self.node_a
        )
        with self.assertRaises(IntegrityError):
            ACIInterfaceFabricMembership.objects.create(
                dcim_interface=self.iface_a, aci_node=self.node_b
            )

    def test_clean_device_node_mismatch_rejected(self):
        # node_a links device_a; trying to attach iface_b (which is on device_b) -> error
        m = ACIInterfaceFabricMembership(dcim_interface=self.iface_b, aci_node=self.node_a)
        with self.assertRaises(ValidationError):
            m.clean()

    def test_clean_device_node_match_ok(self):
        m = ACIInterfaceFabricMembership(dcim_interface=self.iface_a, aci_node=self.node_a)
        m.clean()

    def test_clean_node_without_gfk_link_ok(self):
        node_orphan = ACINode.objects.create(aci_pod=self.pod, node_id=999, name="orphan")
        m = ACIInterfaceFabricMembership(dcim_interface=self.iface_a, aci_node=node_orphan)
        m.clean()


# ---------------------------------------------------------------------------
# Extra coverage (Bucket B) — missed lines in binding models
# ---------------------------------------------------------------------------


class ACIVPCBindingPairExtraTests(_BindingFixture):
    """Cover missed lines L55, 66, 109-112 in vpc.py."""

    def _make_vpc_binding(self, iface, encap=100, epg=None):
        return ACIStaticPortBinding.objects.create(
            aci_endpoint_group=epg or self.epg,
            dcim_interface=iface,
            encap_vlan=encap,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )

    def test_distinct_bindings_error_message(self):
        a = self._make_vpc_binding(self.iface_a)
        pair = ACIVPCBindingPair(binding_a=a, binding_b=a)
        with self.assertRaisesRegex(ValidationError, "distinct"):
            pair.clean()

    def test_vpc_type_required_error_message(self):
        a = self._make_vpc_binding(self.iface_a)
        b = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg,
            dcim_interface=self.iface_b,
            encap_vlan=100,
            binding_type=StaticPortBindingTypeChoices.REGULAR,
        )
        pair = ACIVPCBindingPair(binding_a=a, binding_b=b)
        with self.assertRaisesRegex(ValidationError, "vpc"):
            pair.clean()

    def test_same_epg_required_error_message(self):
        a = self._make_vpc_binding(self.iface_a, epg=self.epg)
        b = self._make_vpc_binding(self.iface_b, epg=self.epg_useg)
        pair = ACIVPCBindingPair(binding_a=a, binding_b=b)
        with self.assertRaisesRegex(ValidationError, "EPG"):
            pair.clean()

    def test_same_encap_required_error_message(self):
        a = self._make_vpc_binding(self.iface_a, encap=100)
        b = self._make_vpc_binding(self.iface_b, encap=200)
        pair = ACIVPCBindingPair(binding_a=a, binding_b=b)
        with self.assertRaisesRegex(ValidationError, "VLAN"):
            pair.clean()

    def test_cross_fabric_vpc_pair_rejected(self):
        """vPC peers on nodes in different fabrics must be rejected."""
        from netbox_cisco_aci.models.bindings import ACIInterfaceFabricMembership

        pod_b = ACIPod.objects.create(aci_fabric=self.fab2, pod_id=1, name="pod-dc2")
        node_dc2 = ACINode.objects.create(aci_pod=pod_b, node_id=301, name="leaf-dc2")
        device_c = make_dcim_device("leaf-dc2-dev")
        iface_c = Interface.objects.create(device=device_c, name="eth1/1", type="10gbase-t")
        ACIInterfaceFabricMembership.objects.create(
            dcim_interface=self.iface_a, aci_node=self.node_a
        )
        ACIInterfaceFabricMembership.objects.create(dcim_interface=iface_c, aci_node=node_dc2)
        a = self._make_vpc_binding(self.iface_a)
        b_dc2 = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg,
            dcim_interface=iface_c,
            encap_vlan=100,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )
        pair = ACIVPCBindingPair(binding_a=a, binding_b=b_dc2)
        with self.assertRaisesRegex(ValidationError, "fabric"):
            pair.clean()


class ACIStaticPortBindingExtraTests(_BindingFixture):
    """Cover get_absolute_url (L91 in static_port_bindings.py)."""

    def test_get_absolute_url(self):
        b = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=self.epg, dcim_interface=self.iface_a, encap_vlan=999
        )
        self.assertIn(str(b.pk), b.get_absolute_url())


class ACIDomainBindingExtraTests(_BindingFixture):
    """Cover get_absolute_url (L62 in domain_bindings.py)."""

    def test_get_absolute_url(self):
        dom = ACIDomain.objects.create(
            aci_fabric=self.fab, name="phys-dom-url", domain_type="physical"
        )
        b = ACIDomainBinding.objects.create(aci_endpoint_group=self.epg, aci_domain=dom)
        self.assertIn(str(b.pk), b.get_absolute_url())


class ACIInterfaceFabricMembershipExtraTests(_BindingFixture):
    """Cover missed lines L52, 71, 86 in fabric_membership.py."""

    def test_get_absolute_url(self):
        m = ACIInterfaceFabricMembership.objects.create(
            dcim_interface=self.iface_a, aci_node=self.node_a
        )
        self.assertIn(str(m.pk), m.get_absolute_url())

    def test_clean_skips_when_no_fk(self):
        """Line 71: return early when dcim_interface_id or aci_node_id is None."""
        m = ACIInterfaceFabricMembership(dcim_interface=None, aci_node=None, name="empty")
        # Should not raise; early return path
        m.clean()

    def test_clean_skips_non_device_node(self):
        """Line 86: skip consistency check when node points at non-device object."""
        from django.contrib.contenttypes.models import ContentType

        from netbox_cisco_aci.models.fabric import ACINode

        # Create a node whose GFK points at a non-dcim.Device content type (e.g. ACIFabric)
        fab_ct = ContentType.objects.get_for_model(self.fab.__class__)
        node_vm = ACINode.objects.create(
            aci_pod=self.pod,
            node_id=998,
            name="vm-like-node",
            node_object_type=fab_ct,
            node_object_id=self.fab.pk,
        )
        # iface_b belongs to device_b, but node is a "non-device" type → should not raise
        m = ACIInterfaceFabricMembership(dcim_interface=self.iface_b, aci_node=node_vm)
        m.clean()
