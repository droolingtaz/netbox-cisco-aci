"""FilterSet search() tests for Phase 3 access models (Bucket A)."""

from django.test import TestCase

from netbox_cisco_aci.filtersets.access import (
    ACIAAEPEPGMappingFilterSet,
    ACIAAEPFilterSet,
    ACIDomainFilterSet,
    ACIVLANPoolBlockFilterSet,
    ACIVLANPoolFilterSet,
)
from netbox_cisco_aci.models.access import (
    ACIAAEP,
    ACIAAEPEPGMapping,
    ACIDomain,
    ACIVLANPool,
    ACIVLANPoolBlock,
)
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
)


class ACIVLANPoolFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-pool-search")
        ACIVLANPool.objects.create(aci_fabric=cls.fab, name="pi", name_alias="", description="")
        ACIVLANPool.objects.create(
            aci_fabric=cls.fab, name="pool-other", name_alias="pi-alias", description=""
        )
        ACIVLANPool.objects.create(
            aci_fabric=cls.fab,
            name="pool-third",
            name_alias="",
            description="pi in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIVLANPoolFilterSet({"q": "  "}, ACIVLANPool.objects.filter(aci_fabric=self.fab)).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIVLANPoolFilterSet({"q": "pi"}, ACIVLANPool.objects.filter(aci_fabric=self.fab)).qs
        self.assertEqual(qs.count(), 3)


class ACIVLANPoolBlockFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-blk-search")
        cls.pool = ACIVLANPool.objects.create(aci_fabric=cls.fab, name="pool-blk-search")
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=cls.pool, name="rho", from_vlan=100, to_vlan=199, description=""
        )
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=cls.pool,
            name="blk-other",
            from_vlan=200,
            to_vlan=299,
            description="rho in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIVLANPoolBlockFilterSet(
            {"q": "  "}, ACIVLANPoolBlock.objects.filter(aci_vlan_pool=self.pool)
        ).qs
        self.assertEqual(qs.count(), 2)

    def test_search_matches_name_and_description(self):
        qs = ACIVLANPoolBlockFilterSet(
            {"q": "rho"}, ACIVLANPoolBlock.objects.filter(aci_vlan_pool=self.pool)
        ).qs
        self.assertEqual(qs.count(), 2)


class ACIDomainFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-dom-search")
        ACIDomain.objects.create(
            aci_fabric=cls.fab,
            name="sigma-dom",
            domain_type="physical",
            name_alias="",
            description="",
        )
        ACIDomain.objects.create(
            aci_fabric=cls.fab,
            name="dom-other",
            domain_type="physical",
            name_alias="sigma-dom-alias",
            description="",
        )
        ACIDomain.objects.create(
            aci_fabric=cls.fab,
            name="dom-third",
            domain_type="physical",
            name_alias="",
            description="sigma-dom in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIDomainFilterSet({"q": "  "}, ACIDomain.objects.filter(aci_fabric=self.fab)).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIDomainFilterSet(
            {"q": "sigma-dom"}, ACIDomain.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACIAAEPFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-aaep-search")
        ACIAAEP.objects.create(aci_fabric=cls.fab, name="tau", name_alias="", description="")
        ACIAAEP.objects.create(
            aci_fabric=cls.fab, name="aaep-other", name_alias="tau-alias", description=""
        )
        ACIAAEP.objects.create(
            aci_fabric=cls.fab,
            name="aaep-third",
            name_alias="",
            description="tau in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIAAEPFilterSet({"q": "  "}, ACIAAEP.objects.filter(aci_fabric=self.fab)).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIAAEPFilterSet({"q": "tau"}, ACIAAEP.objects.filter(aci_fabric=self.fab)).qs
        self.assertEqual(qs.count(), 3)


class ACIAAEPEPGMappingFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-epgmap-search")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-epgmap-search")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-epgmap-search")
        cls.bd = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd-epgmap-search"
        )
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant, name="ap-epgmap-search")
        cls.epg = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-epgmap-search",
        )
        cls.aaep = ACIAAEP.objects.create(aci_fabric=cls.fab, name="aaep-epgmap-search")
        ACIAAEPEPGMapping.objects.create(
            aci_aaep=cls.aaep,
            aci_endpoint_group=cls.epg,
            name="upsilon",
            encap_vlan=100,
            description="",
        )
        ACIAAEPEPGMapping.objects.create(
            aci_aaep=cls.aaep,
            aci_endpoint_group=cls.epg,
            name="map-other",
            encap_vlan=200,
            description="upsilon in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIAAEPEPGMappingFilterSet(
            {"q": "  "}, ACIAAEPEPGMapping.objects.filter(aci_aaep=self.aaep)
        ).qs
        self.assertEqual(qs.count(), 2)

    def test_search_matches_name_and_description(self):
        qs = ACIAAEPEPGMappingFilterSet(
            {"q": "upsilon"}, ACIAAEPEPGMapping.objects.filter(aci_aaep=self.aaep)
        ).qs
        self.assertEqual(qs.count(), 2)
