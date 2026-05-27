"""FilterSet search() tests for tenant models (Bucket A)."""

from django.test import TestCase

from netbox_cisco_aci.filtersets.tenant import (
    ACIAppProfileFilterSet,
    ACIBridgeDomainFilterSet,
    ACIBridgeDomainSubnetFilterSet,
    ACIEndpointGroupFilterSet,
    ACIEndpointSecurityGroupFilterSet,
    ACITenantFilterSet,
    ACIUSegAttributeFilterSet,
    ACIVRFFilterSet,
)
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
)


class ACITenantFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-tenant-search")
        cls.t1 = ACITenant.objects.create(
            aci_fabric=cls.fab, name="alpha", name_alias="", description=""
        )
        cls.t2 = ACITenant.objects.create(
            aci_fabric=cls.fab, name="beta", name_alias="alpha-alias", description=""
        )
        cls.t3 = ACITenant.objects.create(
            aci_fabric=cls.fab, name="gamma", name_alias="", description="alpha in description"
        )

    def test_search_empty_value_returns_all(self):
        qs = ACITenantFilterSet({"q": "  "}, ACITenant.objects.filter(aci_fabric=self.fab)).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACITenantFilterSet({"q": "alpha"}, ACITenant.objects.filter(aci_fabric=self.fab)).qs
        self.assertEqual(qs.count(), 3)


class ACIVRFFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-vrf-search")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-vrf-search")
        cls.vrf1 = ACIVRF.objects.create(
            aci_tenant=cls.tenant, name="zeta", name_alias="", description=""
        )
        cls.vrf2 = ACIVRF.objects.create(
            aci_tenant=cls.tenant, name="vrf-other", name_alias="zeta-alias", description=""
        )
        cls.vrf3 = ACIVRF.objects.create(
            aci_tenant=cls.tenant,
            name="vrf-third",
            name_alias="",
            description="zeta in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIVRFFilterSet({"q": "  "}, ACIVRF.objects.filter(aci_tenant=self.tenant)).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIVRFFilterSet({"q": "zeta"}, ACIVRF.objects.filter(aci_tenant=self.tenant)).qs
        self.assertEqual(qs.count(), 3)


class ACIBridgeDomainFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-bd-search")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-bd-search")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-bd-search")
        cls.bd1 = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="sigma", name_alias="", description=""
        )
        cls.bd2 = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant,
            aci_vrf=cls.vrf,
            name="bd-other",
            name_alias="sigma-alias",
            description="",
        )
        cls.bd3 = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant,
            aci_vrf=cls.vrf,
            name="bd-third",
            name_alias="",
            description="sigma in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIBridgeDomainFilterSet(
            {"q": "  "}, ACIBridgeDomain.objects.filter(aci_tenant=self.tenant)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIBridgeDomainFilterSet(
            {"q": "sigma"}, ACIBridgeDomain.objects.filter(aci_tenant=self.tenant)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACIBridgeDomainSubnetFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-bdsub-search")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-bdsub-search")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-bdsub")
        cls.bd = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd-bdsub"
        )
        # BD subnets use gateway_ip and name/description for search
        cls.sub1 = ACIBridgeDomainSubnet.objects.create(
            aci_bridge_domain=cls.bd, name="prim", gateway_ip="10.1.1.1/24", description=""
        )
        cls.sub2 = ACIBridgeDomainSubnet.objects.create(
            aci_bridge_domain=cls.bd, name="sec", gateway_ip="10.2.2.2/24", description="prim-desc"
        )
        cls.sub3 = ACIBridgeDomainSubnet.objects.create(
            aci_bridge_domain=cls.bd,
            name="third",
            gateway_ip="10.1.1.0/24",
            description="",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIBridgeDomainSubnetFilterSet(
            {"q": "  "}, ACIBridgeDomainSubnet.objects.filter(aci_bridge_domain=self.bd)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_and_description(self):
        qs = ACIBridgeDomainSubnetFilterSet(
            {"q": "prim"}, ACIBridgeDomainSubnet.objects.filter(aci_bridge_domain=self.bd)
        ).qs
        # matches name="prim" and description="prim-desc"
        self.assertEqual(qs.count(), 2)

    def test_search_matches_gateway_ip(self):
        qs = ACIBridgeDomainSubnetFilterSet(
            {"q": "10.1.1"}, ACIBridgeDomainSubnet.objects.filter(aci_bridge_domain=self.bd)
        ).qs
        # matches 10.1.1.1/24 and 10.1.1.0/24
        self.assertEqual(qs.count(), 2)


class ACIAppProfileFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-ap-search")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-ap-search")
        ACIAppProfile.objects.create(
            aci_tenant=cls.tenant, name="omega", name_alias="", description=""
        )
        ACIAppProfile.objects.create(
            aci_tenant=cls.tenant, name="ap-other", name_alias="omega-alias", description=""
        )
        ACIAppProfile.objects.create(
            aci_tenant=cls.tenant,
            name="ap-third",
            name_alias="",
            description="omega in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIAppProfileFilterSet(
            {"q": "  "}, ACIAppProfile.objects.filter(aci_tenant=self.tenant)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIAppProfileFilterSet(
            {"q": "omega"}, ACIAppProfile.objects.filter(aci_tenant=self.tenant)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACIEndpointGroupFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-epg-search")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-epg-search")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-epg-search")
        cls.bd = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd-epg-search"
        )
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant, name="ap-epg-search")
        ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="delta",
            name_alias="",
            description="",
        )
        ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-other",
            name_alias="delta-alias",
            description="",
        )
        ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-third",
            name_alias="",
            description="delta in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIEndpointGroupFilterSet(
            {"q": "  "}, ACIEndpointGroup.objects.filter(aci_tenant=self.tenant)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIEndpointGroupFilterSet(
            {"q": "delta"}, ACIEndpointGroup.objects.filter(aci_tenant=self.tenant)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACIUSegAttributeFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-useg-search")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-useg-search")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-useg-search")
        cls.bd = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd-useg-search"
        )
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant, name="ap-useg-search")
        cls.epg = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-useg-search",
            is_useg=True,
        )
        ACIUSegAttribute.objects.create(
            aci_endpoint_group=cls.epg,
            name="eta",
            attribute_type="ip",
            match_value="10.0.0.0/8",
            description="",
        )
        ACIUSegAttribute.objects.create(
            aci_endpoint_group=cls.epg,
            name="attr-other",
            attribute_type="ip",
            match_value="192.0.2.1",
            description="",
        )
        ACIUSegAttribute.objects.create(
            aci_endpoint_group=cls.epg,
            name="attr-third",
            attribute_type="ip",
            match_value="10.1.1.1",
            description="eta in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIUSegAttributeFilterSet(
            {"q": "  "}, ACIUSegAttribute.objects.filter(aci_endpoint_group=self.epg)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_and_description(self):
        qs = ACIUSegAttributeFilterSet(
            {"q": "eta"}, ACIUSegAttribute.objects.filter(aci_endpoint_group=self.epg)
        ).qs
        # name="eta" and description="eta in description"
        self.assertEqual(qs.count(), 2)

    def test_search_matches_match_value(self):
        qs = ACIUSegAttributeFilterSet(
            {"q": "192.0.2.1"}, ACIUSegAttribute.objects.filter(aci_endpoint_group=self.epg)
        ).qs
        self.assertEqual(qs.count(), 1)


class ACIEndpointSecurityGroupFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-esg-search")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="t-esg-search")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-esg-search")
        ACIEndpointSecurityGroup.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="theta", name_alias="", description=""
        )
        ACIEndpointSecurityGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_vrf=cls.vrf,
            name="esg-other",
            name_alias="theta-alias",
            description="",
        )
        ACIEndpointSecurityGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_vrf=cls.vrf,
            name="esg-third",
            name_alias="",
            description="theta in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIEndpointSecurityGroupFilterSet(
            {"q": "  "}, ACIEndpointSecurityGroup.objects.filter(aci_tenant=self.tenant)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIEndpointSecurityGroupFilterSet(
            {"q": "theta"}, ACIEndpointSecurityGroup.objects.filter(aci_tenant=self.tenant)
        ).qs
        self.assertEqual(qs.count(), 3)
