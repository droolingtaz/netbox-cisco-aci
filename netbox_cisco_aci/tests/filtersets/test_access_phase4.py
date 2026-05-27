"""FilterSet tests for Phase 4."""

from django.test import TestCase

from netbox_cisco_aci.choices import (
    InterfacePolicyGroupTypeChoices,
    LACPModeChoices,
    RangeAllChoices,
)
from netbox_cisco_aci.filtersets.access_groups import ACIInterfacePolicyGroupFilterSet
from netbox_cisco_aci.filtersets.access_policies import (
    ACICDPInterfacePolicyFilterSet,
    ACILACPInterfacePolicyFilterSet,
    ACILinkLevelPolicyFilterSet,
    ACILLDPInterfacePolicyFilterSet,
    ACIMCPInterfacePolicyFilterSet,
    ACISTPInterfacePolicyFilterSet,
)
from netbox_cisco_aci.filtersets.access_profiles import (
    ACIInterfaceProfileFilterSet,
    ACIInterfaceProfileSelectorFilterSet,
    ACISwitchProfileFilterSet,
    ACISwitchProfileInterfaceProfileAttachmentFilterSet,
    ACISwitchProfileSelectorFilterSet,
)
from netbox_cisco_aci.models.access import (
    ACICDPInterfacePolicy,
    ACIInterfacePolicyGroup,
    ACIInterfaceProfile,
    ACIInterfaceProfileSelector,
    ACILACPInterfacePolicy,
    ACILinkLevelPolicy,
    ACILLDPInterfacePolicy,
    ACIMCPInterfacePolicy,
    ACISTPInterfacePolicy,
    ACISwitchProfile,
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileSelector,
)
from netbox_cisco_aci.models.fabric import ACIFabric


class Phase4FilterSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab1 = ACIFabric.objects.create(name="DC1")
        cls.fab2 = ACIFabric.objects.create(name="DC2")

        ACILinkLevelPolicy.objects.create(aci_fabric=cls.fab1, name="ll-1")
        ACILinkLevelPolicy.objects.create(aci_fabric=cls.fab2, name="ll-2")

        ACICDPInterfacePolicy.objects.create(aci_fabric=cls.fab1, name="cdp-1")
        ACICDPInterfacePolicy.objects.create(aci_fabric=cls.fab2, name="cdp-2")

        ACILLDPInterfacePolicy.objects.create(aci_fabric=cls.fab1, name="lldp-1")
        ACILLDPInterfacePolicy.objects.create(aci_fabric=cls.fab2, name="lldp-2")

        ACILACPInterfacePolicy.objects.create(
            aci_fabric=cls.fab1, name="lacp-1", mode=LACPModeChoices.ACTIVE
        )
        ACILACPInterfacePolicy.objects.create(
            aci_fabric=cls.fab2, name="lacp-2", mode=LACPModeChoices.ACTIVE
        )

        ACIMCPInterfacePolicy.objects.create(aci_fabric=cls.fab1, name="mcp-1")
        ACIMCPInterfacePolicy.objects.create(aci_fabric=cls.fab2, name="mcp-2")

        ACISTPInterfacePolicy.objects.create(aci_fabric=cls.fab1, name="stp-1")
        ACISTPInterfacePolicy.objects.create(aci_fabric=cls.fab2, name="stp-2")

        cls.pg_access = ACIInterfacePolicyGroup.objects.create(
            aci_fabric=cls.fab1,
            name="pg-access",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
        )
        ACIInterfacePolicyGroup.objects.create(
            aci_fabric=cls.fab1,
            name="pg-vpc",
            pg_type=InterfacePolicyGroupTypeChoices.VPC,
            lacp_policy=ACILACPInterfacePolicy.objects.get(aci_fabric=cls.fab1, name="lacp-1"),
        )

        cls.sp1 = ACISwitchProfile.objects.create(aci_fabric=cls.fab1, name="sp-1")
        cls.sp2 = ACISwitchProfile.objects.create(aci_fabric=cls.fab2, name="sp-2")
        ACISwitchProfileSelector.objects.create(
            switch_profile=cls.sp1,
            name="sel-range",
            selector_type=RangeAllChoices.RANGE,
            from_node_id=101,
            to_node_id=102,
        )
        ACISwitchProfileSelector.objects.create(
            switch_profile=cls.sp1, name="sel-all", selector_type=RangeAllChoices.ALL
        )

        cls.ip1 = ACIInterfaceProfile.objects.create(aci_fabric=cls.fab1, name="ip-1")
        cls.ip2 = ACIInterfaceProfile.objects.create(aci_fabric=cls.fab2, name="ip-2")
        ACIInterfaceProfileSelector.objects.create(
            interface_profile=cls.ip1,
            name="isel-1",
            from_module=1,
            from_port=1,
            to_module=1,
            to_port=24,
        )

        ACISwitchProfileInterfaceProfileAttachment.objects.create(
            switch_profile=cls.sp1, interface_profile=cls.ip1
        )

    def test_acilinklevelpolicy_filter_by_fabric(self):
        qs = ACILinkLevelPolicyFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACILinkLevelPolicy.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_acicdpinterfacepolicy_filter_by_fabric(self):
        qs = ACICDPInterfacePolicyFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACICDPInterfacePolicy.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_acilldpinterfacepolicy_filter_by_fabric(self):
        qs = ACILLDPInterfacePolicyFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACILLDPInterfacePolicy.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_acilacpinterfacepolicy_filter_by_fabric(self):
        qs = ACILACPInterfacePolicyFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACILACPInterfacePolicy.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_acimcpinterfacepolicy_filter_by_fabric(self):
        qs = ACIMCPInterfacePolicyFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACIMCPInterfacePolicy.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_acistpinterfacepolicy_filter_by_fabric(self):
        qs = ACISTPInterfacePolicyFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACISTPInterfacePolicy.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_aciinterfacepolicygroup_filter_by_fabric(self):
        qs = ACIInterfacePolicyGroupFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACIInterfacePolicyGroup.objects.all()
        ).qs
        self.assertEqual(qs.count(), 2)

    def test_aciinterfacepolicygroup_filter_by_pg_type(self):
        qs = ACIInterfacePolicyGroupFilterSet(
            {"pg_type": ["vpc"]}, ACIInterfacePolicyGroup.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_aciswitchprofile_filter_by_fabric(self):
        qs = ACISwitchProfileFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACISwitchProfile.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_aciswitchprofileselector_filter_by_selector_type(self):
        qs = ACISwitchProfileSelectorFilterSet(
            {"selector_type": ["range"]}, ACISwitchProfileSelector.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_aciinterfaceprofile_filter_by_fabric(self):
        qs = ACIInterfaceProfileFilterSet(
            {"aci_fabric_id": [self.fab1.pk]}, ACIInterfaceProfile.objects.all()
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_aciinterfaceprofileselector_filter_by_interface_profile(self):
        qs = ACIInterfaceProfileSelectorFilterSet(
            {"interface_profile_id": [self.ip1.pk]},
            ACIInterfaceProfileSelector.objects.all(),
        ).qs
        self.assertEqual(qs.count(), 1)

    def test_attachment_filter_by_switch_profile(self):
        qs = ACISwitchProfileInterfaceProfileAttachmentFilterSet(
            {"switch_profile_id": [self.sp1.pk]},
            ACISwitchProfileInterfaceProfileAttachment.objects.all(),
        ).qs
        self.assertEqual(qs.count(), 1)


# ---------------------------------------------------------------------------
# Search() coverage (Bucket A) — filtersets/access_groups.py L26-28
# ---------------------------------------------------------------------------


class ACIInterfacePolicyGroupFilterSetSearchTests(TestCase):
    """Cover ACIInterfacePolicyGroupFilterSet.search() empty and match paths."""

    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-pg-srch")
        ACIInterfacePolicyGroup.objects.create(
            aci_fabric=cls.fab,
            name="pg-rho",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
            name_alias="",
            description="",
        )
        ACIInterfacePolicyGroup.objects.create(
            aci_fabric=cls.fab,
            name="pg-other",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
            name_alias="rho-alias",
            description="",
        )
        ACIInterfacePolicyGroup.objects.create(
            aci_fabric=cls.fab,
            name="pg-third",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
            name_alias="",
            description="rho in description",
        )

    def test_search_empty_returns_all(self):
        qs = ACIInterfacePolicyGroupFilterSet(
            {"q": "  "}, ACIInterfacePolicyGroup.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIInterfacePolicyGroupFilterSet(
            {"q": "rho"}, ACIInterfacePolicyGroup.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)
