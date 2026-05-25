"""FilterSet tests for Phase 3."""

from django.test import TestCase

from netbox_cisco_aci.filtersets.access import (
    ACIAAEPFilterSet,
    ACIDomainFilterSet,
    ACIVLANPoolBlockFilterSet,
    ACIVLANPoolFilterSet,
)
from netbox_cisco_aci.models.access import (
    ACIAAEP,
    ACIDomain,
    ACIVLANPool,
    ACIVLANPoolBlock,
)
from netbox_cisco_aci.models.fabric import ACIFabric


class AccessFilterSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab1 = ACIFabric.objects.create(name="DC1")
        cls.fab2 = ACIFabric.objects.create(name="DC2")
        cls.pool1 = ACIVLANPool.objects.create(
            aci_fabric=cls.fab1, name="pool-prod", allocation_mode="static"
        )
        ACIVLANPool.objects.create(aci_fabric=cls.fab1, name="pool-dev", allocation_mode="dynamic")
        ACIVLANPool.objects.create(aci_fabric=cls.fab2, name="pool-prod", allocation_mode="static")
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=cls.pool1, name="b1", from_vlan=100, to_vlan=200
        )
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=cls.pool1, name="b2", from_vlan=300, to_vlan=400
        )
        ACIDomain.objects.create(aci_fabric=cls.fab1, name="phys-1", domain_type="physical")
        ACIDomain.objects.create(aci_fabric=cls.fab1, name="l3-1", domain_type="l3")
        ACIAAEP.objects.create(aci_fabric=cls.fab1, name="aaep-1")

    def test_pool_filter_by_fabric(self):
        qs = ACIVLANPoolFilterSet({"aci_fabric_id": [self.fab1.pk]}, ACIVLANPool.objects.all()).qs
        self.assertEqual(qs.count(), 2)

    def test_pool_filter_by_allocation(self):
        qs = ACIVLANPoolFilterSet({"allocation_mode": ["dynamic"]}, ACIVLANPool.objects.all()).qs
        self.assertEqual(qs.count(), 1)

    def test_block_contains_vlan(self):
        qs = ACIVLANPoolBlockFilterSet({"contains_vlan": 150}, ACIVLANPoolBlock.objects.all()).qs
        self.assertEqual(qs.count(), 1)
        qs2 = ACIVLANPoolBlockFilterSet({"contains_vlan": 250}, ACIVLANPoolBlock.objects.all()).qs
        self.assertEqual(qs2.count(), 0)

    def test_domain_filter_by_type(self):
        qs = ACIDomainFilterSet({"domain_type": ["l3"]}, ACIDomain.objects.all()).qs
        self.assertEqual(qs.count(), 1)

    def test_aaep_filter_by_fabric(self):
        qs = ACIAAEPFilterSet({"aci_fabric_id": [self.fab1.pk]}, ACIAAEP.objects.all()).qs
        self.assertEqual(qs.count(), 1)
