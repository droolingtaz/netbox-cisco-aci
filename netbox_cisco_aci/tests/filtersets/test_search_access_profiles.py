"""FilterSet search() tests for Phase 4 profile models (Bucket A)."""

from django.test import TestCase

from netbox_cisco_aci.choices import RangeAllChoices
from netbox_cisco_aci.filtersets.access_profiles import (
    ACIInterfaceProfileFilterSet,
    ACIInterfaceProfileSelectorFilterSet,
    ACISwitchProfileFilterSet,
    ACISwitchProfileInterfaceProfileAttachmentFilterSet,
    ACISwitchProfileSelectorFilterSet,
)
from netbox_cisco_aci.models.access import (
    ACIInterfaceProfile,
    ACIInterfaceProfileSelector,
    ACISwitchProfile,
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileSelector,
)
from netbox_cisco_aci.models.fabric import ACIFabric


class ACISwitchProfileFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-sp-search")
        ACISwitchProfile.objects.create(
            aci_fabric=cls.fab, name="phi", name_alias="", description=""
        )
        ACISwitchProfile.objects.create(
            aci_fabric=cls.fab, name="sp-other", name_alias="phi-alias", description=""
        )
        ACISwitchProfile.objects.create(
            aci_fabric=cls.fab,
            name="sp-third",
            name_alias="",
            description="phi in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACISwitchProfileFilterSet(
            {"q": "  "}, ACISwitchProfile.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACISwitchProfileFilterSet(
            {"q": "phi"}, ACISwitchProfile.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACISwitchProfileSelectorFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-spsel-search")
        cls.sp = ACISwitchProfile.objects.create(aci_fabric=cls.fab, name="sp-spsel-search")
        ACISwitchProfileSelector.objects.create(
            switch_profile=cls.sp,
            name="chi",
            selector_type=RangeAllChoices.ALL,
            description="",
        )
        ACISwitchProfileSelector.objects.create(
            switch_profile=cls.sp,
            name="sel-other",
            selector_type=RangeAllChoices.ALL,
            description="chi in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACISwitchProfileSelectorFilterSet(
            {"q": "  "}, ACISwitchProfileSelector.objects.filter(switch_profile=self.sp)
        ).qs
        self.assertEqual(qs.count(), 2)

    def test_search_matches_name_and_description(self):
        qs = ACISwitchProfileSelectorFilterSet(
            {"q": "chi"}, ACISwitchProfileSelector.objects.filter(switch_profile=self.sp)
        ).qs
        self.assertEqual(qs.count(), 2)


class ACIInterfaceProfileFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-ip-search")
        ACIInterfaceProfile.objects.create(
            aci_fabric=cls.fab, name="psi", name_alias="", description=""
        )
        ACIInterfaceProfile.objects.create(
            aci_fabric=cls.fab, name="ip-other", name_alias="psi-alias", description=""
        )
        ACIInterfaceProfile.objects.create(
            aci_fabric=cls.fab,
            name="ip-third",
            name_alias="",
            description="psi in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIInterfaceProfileFilterSet(
            {"q": "  "}, ACIInterfaceProfile.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIInterfaceProfileFilterSet(
            {"q": "psi"}, ACIInterfaceProfile.objects.filter(aci_fabric=self.fab)
        ).qs
        self.assertEqual(qs.count(), 3)


class ACIInterfaceProfileSelectorFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-ipsel-search")
        cls.ip = ACIInterfaceProfile.objects.create(aci_fabric=cls.fab, name="ip-ipsel-search")
        ACIInterfaceProfileSelector.objects.create(
            interface_profile=cls.ip,
            name="omega-sel",
            from_module=1,
            from_port=1,
            to_module=1,
            to_port=10,
            description="",
        )
        ACIInterfaceProfileSelector.objects.create(
            interface_profile=cls.ip,
            name="sel-other",
            from_module=1,
            from_port=11,
            to_module=1,
            to_port=20,
            description="omega-sel in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIInterfaceProfileSelectorFilterSet(
            {"q": "  "}, ACIInterfaceProfileSelector.objects.filter(interface_profile=self.ip)
        ).qs
        self.assertEqual(qs.count(), 2)

    def test_search_matches_name_and_description(self):
        qs = ACIInterfaceProfileSelectorFilterSet(
            {"q": "omega-sel"},
            ACIInterfaceProfileSelector.objects.filter(interface_profile=self.ip),
        ).qs
        self.assertEqual(qs.count(), 2)


class ACISwitchProfileInterfaceProfileAttachmentFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-attach-search")
        cls.sp1 = ACISwitchProfile.objects.create(aci_fabric=cls.fab, name="sp-attach-1")
        cls.sp2 = ACISwitchProfile.objects.create(aci_fabric=cls.fab, name="sp-attach-2")
        cls.ip1 = ACIInterfaceProfile.objects.create(aci_fabric=cls.fab, name="ip-attach-1")
        cls.ip2 = ACIInterfaceProfile.objects.create(aci_fabric=cls.fab, name="ip-attach-2")
        ACISwitchProfileInterfaceProfileAttachment.objects.create(
            switch_profile=cls.sp1, interface_profile=cls.ip1
        )
        ACISwitchProfileInterfaceProfileAttachment.objects.create(
            switch_profile=cls.sp2, interface_profile=cls.ip2
        )

    def test_search_empty_value_returns_all(self):
        qs = ACISwitchProfileInterfaceProfileAttachmentFilterSet(
            {"q": "  "}, ACISwitchProfileInterfaceProfileAttachment.objects.all()
        ).qs
        # At least 2 we created
        self.assertGreaterEqual(qs.count(), 2)

    def test_search_matches_switch_profile_name(self):
        qs = ACISwitchProfileInterfaceProfileAttachmentFilterSet(
            {"q": "sp-attach-1"},
            ACISwitchProfileInterfaceProfileAttachment.objects.filter(
                switch_profile__in=[self.sp1, self.sp2]
            ),
        ).qs
        self.assertEqual(qs.count(), 1)
