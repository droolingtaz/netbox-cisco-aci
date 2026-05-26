"""REST API tests for Phase 6: Static port bindings + device/interface."""

from dcim.models import Interface
from django.contrib.contenttypes.models import ContentType
from utilities.testing import APITestCase, APIViewTestCases

from netbox_cisco_aci.choices import (
    InterfaceFabricRoleChoices,
    StaticPortBindingTypeChoices,
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

PLUGIN_API_NAMESPACE = "plugins-api:netbox_cisco_aci"


def _build_common_fixture(prefix: str):
    """Build a tenant/epg/devices/interfaces fixture per test class."""

    fab = ACIFabric.objects.create(name=f"{prefix}-fab")
    pod = ACIPod.objects.create(aci_fabric=fab, pod_id=1, name=f"{prefix}-pod")
    tenant = ACITenant.objects.create(aci_fabric=fab, name=f"{prefix}-t")
    vrf = ACIVRF.objects.create(aci_tenant=tenant, name=f"{prefix}-vrf")
    bd = ACIBridgeDomain.objects.create(aci_tenant=tenant, aci_vrf=vrf, name=f"{prefix}-bd")
    ap = ACIAppProfile.objects.create(aci_tenant=tenant, name=f"{prefix}-ap")
    epg = ACIEndpointGroup.objects.create(
        aci_tenant=tenant,
        aci_app_profile=ap,
        aci_bridge_domain=bd,
        name=f"{prefix}-epg",
    )
    return fab, pod, tenant, epg


# ---------------------------------------------------------------------------
# ACIStaticPortBinding
#
# PROTECT-referenced from ACIVPCBindingPair (via binding_a / binding_b).
# Test_delete_object uses _get_queryset().first() ordered by
# (aci_endpoint_group, dcim_interface, encap_vlan) → the ordering-first row
# must be unprotected. Test_bulk_delete uses the top-3-by-`-id` rows → make
# the LAST 3 rows we create unprotected.
# ---------------------------------------------------------------------------


class ACIStaticPortBindingAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIStaticPortBinding
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_endpoint_group",
        "binding_type",
        "dcim_interface",
        "description",
        "display",
        "encap_vlan",
        "id",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, epg = _build_common_fixture("spb")
        # Create the devices & interfaces we will need.
        dev_a = make_dcim_device("spb-leaf-1")
        dev_b = make_dcim_device("spb-leaf-2")
        # First batch — 3 bindings (epg-first, ordered by interface id ASC,
        # then by encap). The middle row (encap 200) gets a PROTECT child via
        # a vPC pair — both bindings of the pair must be type vpc.
        iface_a1 = Interface.objects.create(device=dev_a, name="eth1/1", type="10gbase-t")
        iface_b1 = Interface.objects.create(device=dev_b, name="eth1/1", type="10gbase-t")
        b0 = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=epg, dcim_interface=iface_a1, encap_vlan=100
        )
        b_vpc_a = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=epg,
            dcim_interface=iface_a1,
            encap_vlan=200,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )
        b_vpc_b = ACIStaticPortBinding.objects.create(
            aci_endpoint_group=epg,
            dcim_interface=iface_b1,
            encap_vlan=200,
            binding_type=StaticPortBindingTypeChoices.VPC,
        )
        ACIVPCBindingPair.objects.create(binding_a=b_vpc_a, binding_b=b_vpc_b)
        # Second batch — 3 unprotected bindings created AFTER the vPC pair,
        # giving us the top-3-by-id safe for bulk_delete.
        iface_a2 = Interface.objects.create(device=dev_a, name="eth1/2", type="10gbase-t")
        iface_a3 = Interface.objects.create(device=dev_a, name="eth1/3", type="10gbase-t")
        iface_a4 = Interface.objects.create(device=dev_a, name="eth1/4", type="10gbase-t")
        ACIStaticPortBinding.objects.create(
            aci_endpoint_group=epg, dcim_interface=iface_a2, encap_vlan=300
        )
        ACIStaticPortBinding.objects.create(
            aci_endpoint_group=epg, dcim_interface=iface_a3, encap_vlan=300
        )
        ACIStaticPortBinding.objects.create(
            aci_endpoint_group=epg, dcim_interface=iface_a4, encap_vlan=300
        )
        # Just to nudge `b0` (ordering-first by EPG/iface ordering) to be
        # safe: it has no vPC pair. Verified above.
        _ = b0
        # New rows for create payloads
        iface_new_a = Interface.objects.create(device=dev_a, name="eth1/10", type="10gbase-t")
        iface_new_b = Interface.objects.create(device=dev_b, name="eth1/10", type="10gbase-t")
        cls.create_data = [
            {
                "aci_endpoint_group": epg.pk,
                "dcim_interface": iface_new_a.pk,
                "encap_vlan": 401,
            },
            {
                "aci_endpoint_group": epg.pk,
                "dcim_interface": iface_new_b.pk,
                "encap_vlan": 402,
            },
        ]


# ---------------------------------------------------------------------------
# ACIVPCBindingPair
# ---------------------------------------------------------------------------


class ACIVPCBindingPairAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIVPCBindingPair
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "binding_a",
        "binding_b",
        "description",
        "display",
        "id",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, epg = _build_common_fixture("vpc")
        dev_a = make_dcim_device("vpc-leaf-1")
        dev_b = make_dcim_device("vpc-leaf-2")

        def _mkpair(num):
            ia = Interface.objects.create(device=dev_a, name=f"eth1/{num}", type="10gbase-t")
            ib = Interface.objects.create(device=dev_b, name=f"eth1/{num}", type="10gbase-t")
            a = ACIStaticPortBinding.objects.create(
                aci_endpoint_group=epg,
                dcim_interface=ia,
                encap_vlan=100 + num,
                binding_type=StaticPortBindingTypeChoices.VPC,
            )
            b = ACIStaticPortBinding.objects.create(
                aci_endpoint_group=epg,
                dcim_interface=ib,
                encap_vlan=100 + num,
                binding_type=StaticPortBindingTypeChoices.VPC,
            )
            return a, b

        for n in range(1, 4):
            a, b = _mkpair(n)
            ACIVPCBindingPair.objects.create(binding_a=a, binding_b=b)

        a4, b4 = _mkpair(10)
        a5, b5 = _mkpair(11)
        cls.create_data = [
            {"binding_a": a4.pk, "binding_b": b4.pk, "name": "vpc-new-1"},
            {"binding_a": a5.pk, "binding_b": b5.pk, "name": "vpc-new-2"},
        ]


# ---------------------------------------------------------------------------
# ACIDomainBinding
# ---------------------------------------------------------------------------


class ACIDomainBindingAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIDomainBinding
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_domain",
        "aci_endpoint_group",
        "description",
        "display",
        "id",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, epg = _build_common_fixture("dom")
        # Need different EPGs so the natural-key (epg, domain) doesn't collide.
        ap2 = epg.aci_app_profile
        bd2 = epg.aci_bridge_domain
        epg2 = ACIEndpointGroup.objects.create(
            aci_tenant=tenant,
            aci_app_profile=ap2,
            aci_bridge_domain=bd2,
            name="dom-epg-2",
        )
        epg3 = ACIEndpointGroup.objects.create(
            aci_tenant=tenant,
            aci_app_profile=ap2,
            aci_bridge_domain=bd2,
            name="dom-epg-3",
        )
        epg4 = ACIEndpointGroup.objects.create(
            aci_tenant=tenant,
            aci_app_profile=ap2,
            aci_bridge_domain=bd2,
            name="dom-epg-4",
        )
        epg5 = ACIEndpointGroup.objects.create(
            aci_tenant=tenant,
            aci_app_profile=ap2,
            aci_bridge_domain=bd2,
            name="dom-epg-5",
        )
        dom = ACIDomain.objects.create(aci_fabric=fab, name="dom-phys", domain_type="physical")
        ACIDomainBinding.objects.create(aci_endpoint_group=epg, aci_domain=dom)
        ACIDomainBinding.objects.create(aci_endpoint_group=epg2, aci_domain=dom)
        ACIDomainBinding.objects.create(aci_endpoint_group=epg3, aci_domain=dom)

        dom2 = ACIDomain.objects.create(aci_fabric=fab, name="dom-phys-2", domain_type="physical")
        cls.create_data = [
            {"aci_endpoint_group": epg4.pk, "aci_domain": dom2.pk},
            {"aci_endpoint_group": epg5.pk, "aci_domain": dom2.pk},
        ]


# ---------------------------------------------------------------------------
# ACIInterfaceFabricMembership
# ---------------------------------------------------------------------------


class ACIInterfaceFabricMembershipAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIInterfaceFabricMembership
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_node",
        "dcim_interface",
        "description",
        "display",
        "id",
        "interface_role",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab, pod, tenant, epg = _build_common_fixture("ifm")
        dev = make_dcim_device("ifm-leaf")
        ct = ContentType.objects.get_for_model(dev.__class__)
        node = ACINode.objects.create(
            aci_pod=pod,
            node_id=101,
            name="ifm-leaf",
            node_object_type=ct,
            node_object_id=dev.pk,
        )

        for i in range(3):
            iface = Interface.objects.create(device=dev, name=f"eth1/{i + 1}", type="10gbase-t")
            ACIInterfaceFabricMembership.objects.create(
                dcim_interface=iface,
                aci_node=node,
                interface_role=InterfaceFabricRoleChoices.HOST,
            )

        # Extra interfaces for create payloads
        iface_new1 = Interface.objects.create(device=dev, name="eth1/20", type="10gbase-t")
        iface_new2 = Interface.objects.create(device=dev, name="eth1/21", type="10gbase-t")
        cls.create_data = [
            {
                "dcim_interface": iface_new1.pk,
                "aci_node": node.pk,
                "interface_role": InterfaceFabricRoleChoices.HOST,
            },
            {
                "dcim_interface": iface_new2.pk,
                "aci_node": node.pk,
                "interface_role": InterfaceFabricRoleChoices.FABRIC,
            },
        ]
