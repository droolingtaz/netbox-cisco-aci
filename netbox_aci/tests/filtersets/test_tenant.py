"""FilterSet tests for Phase 2."""

from django.test import TestCase

from netbox_aci.filtersets.tenant import (
    ACIBridgeDomainFilterSet,
    ACIEndpointGroupFilterSet,
    ACITenantFilterSet,
    ACIVRFFilterSet,
)
from netbox_aci.models.fabric import ACIFabric
from netbox_aci.models.tenant import (
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
    ACIVRF,
)


class TenancyFilterSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab1 = ACIFabric.objects.create(name="DC1")
        cls.fab2 = ACIFabric.objects.create(name="DC2")
        cls.t1 = ACITenant.objects.create(aci_fabric=cls.fab1, name="acme")
        cls.t2 = ACITenant.objects.create(aci_fabric=cls.fab1, name="other")
        ACITenant.objects.create(aci_fabric=cls.fab2, name="acme")  # dup name, ok

        cls.vrf1 = ACIVRF.objects.create(aci_tenant=cls.t1, name="vrf-prod")
        ACIVRF.objects.create(aci_tenant=cls.t1, name="vrf-dev")
        ACIVRF.objects.create(aci_tenant=cls.t2, name="vrf-x")

        cls.ap1 = ACIAppProfile.objects.create(aci_tenant=cls.t1, name="ap")
        cls.bd1 = ACIBridgeDomain.objects.create(
            aci_tenant=cls.t1, aci_vrf=cls.vrf1, name="bd"
        )
        for i in range(3):
            ACIEndpointGroup.objects.create(
                aci_tenant=cls.t1,
                aci_app_profile=cls.ap1,
                aci_bridge_domain=cls.bd1,
                name=f"epg-{i}",
                is_useg=(i == 0),
            )

    def test_tenant_filter_by_fabric(self):
        qs = ACITenantFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACITenant.objects.all()
        ).qs
        self.assertEqual(qs.count(), 2)

    def test_vrf_filter_by_tenant(self):
        qs = ACIVRFFilterSet(
            {"aci_tenant_id": [self.t1.pk]}, ACIVRF.objects.all()
        ).qs
        self.assertEqual(qs.count(), 2)

    def test_bd_filter_by_tenant(self):
        qs = ACIBridgeDomainFilterSet(
            {"aci_tenant_id": [self.t1.pk]}, ACIBridgeDomain.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_epg_filter_by_useg(self):
        qs = ACIEndpointGroupFilterSet(
            {"is_useg": True}, ACIEndpointGroup.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)
