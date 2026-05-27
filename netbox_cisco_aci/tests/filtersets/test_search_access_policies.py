"""FilterSet search() tests for Phase 4 policy models (Bucket A)."""

from django.test import TestCase

from netbox_cisco_aci.choices import LACPModeChoices
from netbox_cisco_aci.filtersets.access_policies import (
    ACICDPInterfacePolicyFilterSet,
    ACILACPInterfacePolicyFilterSet,
    ACILinkLevelPolicyFilterSet,
    ACILLDPInterfacePolicyFilterSet,
    ACIMCPInterfacePolicyFilterSet,
    ACISTPInterfacePolicyFilterSet,
)
from netbox_cisco_aci.models.access import (
    ACICDPInterfacePolicy,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
)
from netbox_cisco_aci.models.fabric import ACIFabric


class ACILinkLevelPolicyFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-ll-search")
        ACILinkLevelPolicy.objects.create(
            aci_fabric=cls.fab, name="kappa", name_alias="", description=""
        )
        ACILinkLevelPolicy.objects.create(
            aci_fabric=cls.fab, name="ll-other", name_alias="kappa-alias", description=""
        )
        ACILinkLevelPolicy.objects.create(
            aci_fabric=cls.fab,
            name="ll-third",
            name_alias="",
            description="kappa in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACILinkLevelPolicyFilterSet(
            {"q": "  "}, ACILinkLevelPolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACILinkLevelPolicyFilterSet(
            {"q": "kappa"}, ACILinkLevelPolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACICDPInterfacePolicyFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-cdp-search")
        ACICDPInterfacePolicy.objects.create(
            aci_fabric=cls.fab, name="lambda", name_alias="", description=""
        )
        ACICDPInterfacePolicy.objects.create(
            aci_fabric=cls.fab, name="cdp-other", name_alias="lambda-alias", description=""
        )
        ACICDPInterfacePolicy.objects.create(
            aci_fabric=cls.fab,
            name="cdp-third",
            name_alias="",
            description="lambda in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACICDPInterfacePolicyFilterSet(
            {"q": "  "}, ACICDPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACICDPInterfacePolicyFilterSet(
            {"q": "lambda"}, ACICDPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACILLDPInterfacePolicyFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-lldp-search")
        ACILLDPInterfacePolicy.objects.create(
            aci_fabric=cls.fab, name="mu", name_alias="", description=""
        )
        ACILLDPInterfacePolicy.objects.create(
            aci_fabric=cls.fab, name="lldp-other", name_alias="mu-alias", description=""
        )
        ACILLDPInterfacePolicy.objects.create(
            aci_fabric=cls.fab,
            name="lldp-third",
            name_alias="",
            description="mu in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACILLDPInterfacePolicyFilterSet(
            {"q": "  "}, ACILLDPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACILLDPInterfacePolicyFilterSet(
            {"q": "mu"}, ACILLDPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACILACPInterfacePolicyFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-lacp-search")
        ACILACPInterfacePolicy.objects.create(
            aci_fabric=cls.fab,
            name="nu",
            name_alias="",
            description="",
            mode=LACPModeChoices.ACTIVE,
        )
        ACILACPInterfacePolicy.objects.create(
            aci_fabric=cls.fab,
            name="lacp-other",
            name_alias="nu-alias",
            description="",
            mode=LACPModeChoices.ACTIVE,
        )
        ACILACPInterfacePolicy.objects.create(
            aci_fabric=cls.fab,
            name="lacp-third",
            name_alias="",
            description="nu in description",
            mode=LACPModeChoices.ACTIVE,
        )

    def test_search_empty_value_returns_all(self):
        qs = ACILACPInterfacePolicyFilterSet(
            {"q": "  "}, ACILACPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACILACPInterfacePolicyFilterSet(
            {"q": "nu"}, ACILACPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACIMCPInterfacePolicyFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-mcp-search")
        ACIMCPInterfacePolicy.objects.create(
            aci_fabric=cls.fab, name="xi", name_alias="", description=""
        )
        ACIMCPInterfacePolicy.objects.create(
            aci_fabric=cls.fab, name="mcp-other", name_alias="xi-alias", description=""
        )
        ACIMCPInterfacePolicy.objects.create(
            aci_fabric=cls.fab,
            name="mcp-third",
            name_alias="",
            description="xi in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIMCPInterfacePolicyFilterSet(
            {"q": "  "}, ACIMCPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIMCPInterfacePolicyFilterSet(
            {"q": "xi"}, ACIMCPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACISTPInterfacePolicyFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-stp-search")
        ACISTPInterfacePolicy.objects.create(
            aci_fabric=cls.fab, name="omicron", name_alias="", description=""
        )
        ACISTPInterfacePolicy.objects.create(
            aci_fabric=cls.fab, name="stp-other", name_alias="omicron-alias", description=""
        )
        ACISTPInterfacePolicy.objects.create(
            aci_fabric=cls.fab,
            name="stp-third",
            name_alias="",
            description="omicron in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACISTPInterfacePolicyFilterSet(
            {"q": "  "}, ACISTPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACISTPInterfacePolicyFilterSet(
            {"q": "omicron"}, ACISTPInterfacePolicy.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)
