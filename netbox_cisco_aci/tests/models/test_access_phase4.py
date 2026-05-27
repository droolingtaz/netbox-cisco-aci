"""Model-level tests for Phase 4: per-port policies, Policy Groups, Switch/Interface Profiles."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from netbox_cisco_aci.choices import (
    EnabledDisabledChoices,
    InterfacePolicyGroupTypeChoices,
    LACPModeChoices,
    LinkLevelSpeedChoices,
    RangeAllChoices,
)
from netbox_cisco_aci.models.access import (
    ACIAAEP,
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


class _Phase4Fixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.fab2 = ACIFabric.objects.create(name="DC2")


# ---------------------------------------------------------------------------
# Link Level
# ---------------------------------------------------------------------------


class ACILinkLevelPolicyTests(_Phase4Fixture):
    def test_create(self):
        p = ACILinkLevelPolicy.objects.create(
            aci_fabric=self.fab, name="ll-100g", speed=LinkLevelSpeedChoices.SPEED_100G
        )
        self.assertEqual(p.speed, "100G")

    def test_str(self):
        p = ACILinkLevelPolicy.objects.create(aci_fabric=self.fab, name="ll-1g")
        self.assertEqual(str(p), "DC1 / LinkLevel ll-1g")

    def test_unique_inside_fabric(self):
        ACILinkLevelPolicy.objects.create(aci_fabric=self.fab, name="dup")
        with self.assertRaises(IntegrityError):
            ACILinkLevelPolicy.objects.create(aci_fabric=self.fab, name="dup")

    def test_same_name_in_different_fabric(self):
        ACILinkLevelPolicy.objects.create(aci_fabric=self.fab, name="ll-1g")
        ACILinkLevelPolicy.objects.create(aci_fabric=self.fab2, name="ll-1g")


# ---------------------------------------------------------------------------
# CDP
# ---------------------------------------------------------------------------


class ACICDPInterfacePolicyTests(_Phase4Fixture):
    def test_create(self):
        p = ACICDPInterfacePolicy.objects.create(
            aci_fabric=self.fab, name="cdp-on", admin_state=EnabledDisabledChoices.ENABLED
        )
        self.assertEqual(p.admin_state, "enabled")

    def test_str(self):
        p = ACICDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="cdp-on")
        self.assertEqual(str(p), "DC1 / CDP cdp-on")

    def test_unique_inside_fabric(self):
        ACICDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")
        with self.assertRaises(IntegrityError):
            ACICDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")

    def test_same_name_in_different_fabric(self):
        ACICDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="cdp")
        ACICDPInterfacePolicy.objects.create(aci_fabric=self.fab2, name="cdp")


# ---------------------------------------------------------------------------
# LLDP
# ---------------------------------------------------------------------------


class ACILLDPInterfacePolicyTests(_Phase4Fixture):
    def test_create(self):
        p = ACILLDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="lldp")
        self.assertEqual(p.receive_state, "enabled")

    def test_str(self):
        p = ACILLDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="lldp")
        self.assertEqual(str(p), "DC1 / LLDP lldp")

    def test_unique_inside_fabric(self):
        ACILLDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")
        with self.assertRaises(IntegrityError):
            ACILLDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")

    def test_same_name_in_different_fabric(self):
        ACILLDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="lldp")
        ACILLDPInterfacePolicy.objects.create(aci_fabric=self.fab2, name="lldp")


# ---------------------------------------------------------------------------
# LACP
# ---------------------------------------------------------------------------


class ACILACPInterfacePolicyTests(_Phase4Fixture):
    def test_create(self):
        p = ACILACPInterfacePolicy.objects.create(
            aci_fabric=self.fab, name="lacp", mode=LACPModeChoices.ACTIVE
        )
        self.assertEqual(p.mode, "active")

    def test_str(self):
        p = ACILACPInterfacePolicy.objects.create(aci_fabric=self.fab, name="lacp")
        self.assertEqual(str(p), "DC1 / LACP lacp")

    def test_min_links_le_max_links_ok(self):
        p = ACILACPInterfacePolicy(aci_fabric=self.fab, name="lacp", min_links=2, max_links=8)
        p.full_clean()

    def test_min_links_gt_max_links_rejected(self):
        p = ACILACPInterfacePolicy(aci_fabric=self.fab, name="bad", min_links=8, max_links=2)
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_unique_inside_fabric(self):
        ACILACPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")
        with self.assertRaises(IntegrityError):
            ACILACPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")

    def test_same_name_in_different_fabric(self):
        ACILACPInterfacePolicy.objects.create(aci_fabric=self.fab, name="lacp")
        ACILACPInterfacePolicy.objects.create(aci_fabric=self.fab2, name="lacp")


# ---------------------------------------------------------------------------
# MCP
# ---------------------------------------------------------------------------


class ACIMCPInterfacePolicyTests(_Phase4Fixture):
    def test_create(self):
        p = ACIMCPInterfacePolicy.objects.create(aci_fabric=self.fab, name="mcp")
        self.assertEqual(p.admin_state, "enabled")

    def test_str(self):
        p = ACIMCPInterfacePolicy.objects.create(aci_fabric=self.fab, name="mcp")
        self.assertEqual(str(p), "DC1 / MCP mcp")

    def test_unique_inside_fabric(self):
        ACIMCPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")
        with self.assertRaises(IntegrityError):
            ACIMCPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")

    def test_same_name_in_different_fabric(self):
        ACIMCPInterfacePolicy.objects.create(aci_fabric=self.fab, name="mcp")
        ACIMCPInterfacePolicy.objects.create(aci_fabric=self.fab2, name="mcp")


# ---------------------------------------------------------------------------
# STP
# ---------------------------------------------------------------------------


class ACISTPInterfacePolicyTests(_Phase4Fixture):
    def test_create(self):
        p = ACISTPInterfacePolicy.objects.create(
            aci_fabric=self.fab, name="stp-bpdu", bpdu_guard=True
        )
        self.assertTrue(p.bpdu_guard)

    def test_str(self):
        p = ACISTPInterfacePolicy.objects.create(aci_fabric=self.fab, name="stp")
        self.assertEqual(str(p), "DC1 / STP stp")

    def test_unique_inside_fabric(self):
        ACISTPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")
        with self.assertRaises(IntegrityError):
            ACISTPInterfacePolicy.objects.create(aci_fabric=self.fab, name="dup")

    def test_same_name_in_different_fabric(self):
        ACISTPInterfacePolicy.objects.create(aci_fabric=self.fab, name="stp")
        ACISTPInterfacePolicy.objects.create(aci_fabric=self.fab2, name="stp")


# ---------------------------------------------------------------------------
# Interface Policy Group
# ---------------------------------------------------------------------------


class ACIInterfacePolicyGroupTests(_Phase4Fixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.ll = ACILinkLevelPolicy.objects.create(aci_fabric=cls.fab, name="ll")
        cls.lacp = ACILACPInterfacePolicy.objects.create(
            aci_fabric=cls.fab, name="lacp", mode=LACPModeChoices.ACTIVE
        )
        cls.aaep = ACIAAEP.objects.create(aci_fabric=cls.fab, name="aaep")
        # Foreign-fabric refs for cross-fabric tests.
        cls.foreign_ll = ACILinkLevelPolicy.objects.create(aci_fabric=cls.fab2, name="ll-x")

    def test_create(self):
        pg = ACIInterfacePolicyGroup.objects.create(
            aci_fabric=self.fab,
            name="pg-1",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
            link_level_policy=self.ll,
            aaep=self.aaep,
        )
        self.assertEqual(pg.pg_type, "access")

    def test_str(self):
        pg = ACIInterfacePolicyGroup.objects.create(
            aci_fabric=self.fab, name="pg-1", pg_type=InterfacePolicyGroupTypeChoices.ACCESS
        )
        self.assertEqual(str(pg), "DC1 / Access pg-1")

    def test_cross_fabric_ref_rejected(self):
        pg = ACIInterfacePolicyGroup(
            aci_fabric=self.fab,
            name="pg-bad",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
            link_level_policy=self.foreign_ll,
        )
        with self.assertRaises(ValidationError):
            pg.full_clean()

    def test_same_fabric_ref_ok(self):
        pg = ACIInterfacePolicyGroup(
            aci_fabric=self.fab,
            name="pg-ok",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
            link_level_policy=self.ll,
        )
        pg.full_clean()
        pg.save()

    def test_pc_requires_lacp(self):
        pg = ACIInterfacePolicyGroup(
            aci_fabric=self.fab,
            name="pc-no-lacp",
            pg_type=InterfacePolicyGroupTypeChoices.PC,
        )
        with self.assertRaises(ValidationError):
            pg.full_clean()

    def test_pc_with_lacp_ok(self):
        pg = ACIInterfacePolicyGroup(
            aci_fabric=self.fab,
            name="pc-ok",
            pg_type=InterfacePolicyGroupTypeChoices.PC,
            lacp_policy=self.lacp,
        )
        pg.full_clean()
        pg.save()

    def test_unique_inside_fabric(self):
        ACIInterfacePolicyGroup.objects.create(
            aci_fabric=self.fab, name="pg-uniq", pg_type=InterfacePolicyGroupTypeChoices.ACCESS
        )
        with self.assertRaises(IntegrityError):
            ACIInterfacePolicyGroup.objects.create(
                aci_fabric=self.fab,
                name="pg-uniq",
                pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
            )

    def test_same_name_in_different_fabric(self):
        ACIInterfacePolicyGroup.objects.create(
            aci_fabric=self.fab, name="pg-x", pg_type=InterfacePolicyGroupTypeChoices.ACCESS
        )
        ACIInterfacePolicyGroup.objects.create(
            aci_fabric=self.fab2, name="pg-x", pg_type=InterfacePolicyGroupTypeChoices.ACCESS
        )


# ---------------------------------------------------------------------------
# Switch Profile + Selector
# ---------------------------------------------------------------------------


class ACISwitchProfileTests(_Phase4Fixture):
    def test_create(self):
        sp = ACISwitchProfile.objects.create(aci_fabric=self.fab, name="sp-1")
        self.assertEqual(sp.aci_fabric_id, self.fab.id)

    def test_str(self):
        sp = ACISwitchProfile.objects.create(aci_fabric=self.fab, name="sp-1")
        self.assertEqual(str(sp), "DC1 / SwitchProfile sp-1")

    def test_unique_inside_fabric(self):
        ACISwitchProfile.objects.create(aci_fabric=self.fab, name="dup")
        with self.assertRaises(IntegrityError):
            ACISwitchProfile.objects.create(aci_fabric=self.fab, name="dup")

    def test_same_name_in_different_fabric(self):
        ACISwitchProfile.objects.create(aci_fabric=self.fab, name="sp")
        ACISwitchProfile.objects.create(aci_fabric=self.fab2, name="sp")


class ACISwitchProfileSelectorTests(_Phase4Fixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.sp = ACISwitchProfile.objects.create(aci_fabric=cls.fab, name="sp-1")

    def test_create_range(self):
        sel = ACISwitchProfileSelector.objects.create(
            switch_profile=self.sp,
            name="leaves-101-102",
            selector_type=RangeAllChoices.RANGE,
            from_node_id=101,
            to_node_id=102,
        )
        self.assertEqual(sel.from_node_id, 101)

    def test_str(self):
        sel = ACISwitchProfileSelector.objects.create(
            switch_profile=self.sp,
            name="leaves",
            selector_type=RangeAllChoices.RANGE,
            from_node_id=101,
            to_node_id=102,
        )
        self.assertEqual(str(sel), "sp-1 / range:101-102")

    def test_range_requires_node_ids(self):
        sel = ACISwitchProfileSelector(
            switch_profile=self.sp,
            name="bad",
            selector_type=RangeAllChoices.RANGE,
        )
        with self.assertRaises(ValidationError):
            sel.full_clean()

    def test_range_from_le_to(self):
        sel = ACISwitchProfileSelector(
            switch_profile=self.sp,
            name="bad",
            selector_type=RangeAllChoices.RANGE,
            from_node_id=200,
            to_node_id=100,
        )
        with self.assertRaises(ValidationError):
            sel.full_clean()

    def test_all_must_not_have_node_ids(self):
        sel = ACISwitchProfileSelector(
            switch_profile=self.sp,
            name="bad-all",
            selector_type=RangeAllChoices.ALL,
            from_node_id=100,
            to_node_id=200,
        )
        with self.assertRaises(ValidationError):
            sel.full_clean()

    def test_all_without_node_ids_ok(self):
        sel = ACISwitchProfileSelector(
            switch_profile=self.sp,
            name="all",
            selector_type=RangeAllChoices.ALL,
        )
        sel.full_clean()
        sel.save()


# ---------------------------------------------------------------------------
# Interface Profile + Selector
# ---------------------------------------------------------------------------


class ACIInterfaceProfileTests(_Phase4Fixture):
    def test_create(self):
        ip = ACIInterfaceProfile.objects.create(aci_fabric=self.fab, name="ip-1")
        self.assertEqual(ip.aci_fabric_id, self.fab.id)

    def test_str(self):
        ip = ACIInterfaceProfile.objects.create(aci_fabric=self.fab, name="ip-1")
        self.assertEqual(str(ip), "DC1 / InterfaceProfile ip-1")

    def test_unique_inside_fabric(self):
        ACIInterfaceProfile.objects.create(aci_fabric=self.fab, name="dup")
        with self.assertRaises(IntegrityError):
            ACIInterfaceProfile.objects.create(aci_fabric=self.fab, name="dup")

    def test_same_name_in_different_fabric(self):
        ACIInterfaceProfile.objects.create(aci_fabric=self.fab, name="ip")
        ACIInterfaceProfile.objects.create(aci_fabric=self.fab2, name="ip")


class ACIInterfaceProfileSelectorTests(_Phase4Fixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.ip = ACIInterfaceProfile.objects.create(aci_fabric=cls.fab, name="ip-1")
        cls.pg = ACIInterfacePolicyGroup.objects.create(
            aci_fabric=cls.fab,
            name="pg-1",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
        )
        cls.foreign_pg = ACIInterfacePolicyGroup.objects.create(
            aci_fabric=cls.fab2,
            name="pg-x",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
        )

    def test_create(self):
        sel = ACIInterfaceProfileSelector.objects.create(
            interface_profile=self.ip,
            name="sel-1",
            from_module=1,
            from_port=1,
            to_module=1,
            to_port=24,
        )
        self.assertEqual(sel.from_port, 1)

    def test_str(self):
        sel = ACIInterfaceProfileSelector.objects.create(
            interface_profile=self.ip,
            name="sel-1",
            from_module=1,
            from_port=1,
            to_module=1,
            to_port=24,
        )
        self.assertEqual(str(sel), "ip-1 / 1/1-1/24")

    def test_range_ordering_ok(self):
        sel = ACIInterfaceProfileSelector(
            interface_profile=self.ip,
            name="sel-ok",
            from_module=1,
            from_port=1,
            to_module=2,
            to_port=24,
        )
        sel.full_clean()

    def test_range_ordering_bad(self):
        sel = ACIInterfaceProfileSelector(
            interface_profile=self.ip,
            name="sel-bad",
            from_module=2,
            from_port=1,
            to_module=1,
            to_port=24,
        )
        with self.assertRaises(ValidationError):
            sel.full_clean()

    def test_cross_fabric_policy_group_rejected(self):
        sel = ACIInterfaceProfileSelector(
            interface_profile=self.ip,
            name="sel-x",
            policy_group=self.foreign_pg,
            from_module=1,
            from_port=1,
            to_module=1,
            to_port=24,
        )
        with self.assertRaises(ValidationError):
            sel.full_clean()

    def test_same_fabric_policy_group_ok(self):
        sel = ACIInterfaceProfileSelector(
            interface_profile=self.ip,
            name="sel-good",
            policy_group=self.pg,
            from_module=1,
            from_port=1,
            to_module=1,
            to_port=24,
        )
        sel.full_clean()
        sel.save()


# ---------------------------------------------------------------------------
# Switch <-> Interface Profile attachment
# ---------------------------------------------------------------------------


class ACISwitchProfileInterfaceProfileAttachmentTests(_Phase4Fixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.sp = ACISwitchProfile.objects.create(aci_fabric=cls.fab, name="sp-1")
        cls.ip = ACIInterfaceProfile.objects.create(aci_fabric=cls.fab, name="ip-1")
        cls.ip_foreign = ACIInterfaceProfile.objects.create(aci_fabric=cls.fab2, name="ip-x")

    def test_create(self):
        a = ACISwitchProfileInterfaceProfileAttachment.objects.create(
            switch_profile=self.sp, interface_profile=self.ip
        )
        self.assertEqual(a.switch_profile_id, self.sp.id)

    def test_str(self):
        a = ACISwitchProfileInterfaceProfileAttachment.objects.create(
            switch_profile=self.sp, interface_profile=self.ip
        )
        self.assertEqual(str(a), "sp-1 \u2194 ip-1")

    def test_cross_fabric_rejected(self):
        a = ACISwitchProfileInterfaceProfileAttachment(
            switch_profile=self.sp, interface_profile=self.ip_foreign
        )
        with self.assertRaises(ValidationError):
            a.full_clean()

    def test_same_fabric_ok(self):
        a = ACISwitchProfileInterfaceProfileAttachment(
            switch_profile=self.sp, interface_profile=self.ip
        )
        a.full_clean()
        a.save()

    def test_unique_pair(self):
        ACISwitchProfileInterfaceProfileAttachment.objects.create(
            switch_profile=self.sp, interface_profile=self.ip
        )
        with self.assertRaises(IntegrityError):
            ACISwitchProfileInterfaceProfileAttachment.objects.create(
                switch_profile=self.sp, interface_profile=self.ip
            )

    def test_distinct_pair_allowed(self):
        ip2 = ACIInterfaceProfile.objects.create(aci_fabric=self.fab, name="ip-2")
        ACISwitchProfileInterfaceProfileAttachment.objects.create(
            switch_profile=self.sp, interface_profile=self.ip
        )
        ACISwitchProfileInterfaceProfileAttachment.objects.create(
            switch_profile=self.sp, interface_profile=ip2
        )


# ---------------------------------------------------------------------------
# Extra coverage (Bucket B) — missed lines in Phase 4 models
# ---------------------------------------------------------------------------


class ACILinkLevelPolicyExtraTests(_Phase4Fixture):
    """Cover get_absolute_url (L81 in link_level.py)."""

    def test_get_absolute_url(self):
        p = ACILinkLevelPolicy.objects.create(aci_fabric=self.fab, name="ll-url")
        self.assertIn(str(p.pk), p.get_absolute_url())


class ACICDPInterfacePolicyExtraTests(_Phase4Fixture):
    """Cover get_absolute_url (L48 in cdp.py)."""

    def test_get_absolute_url(self):
        p = ACICDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="cdp-url")
        self.assertIn(str(p.pk), p.get_absolute_url())


class ACILLDPInterfacePolicyExtraTests(_Phase4Fixture):
    """Cover get_absolute_url (L49 in lldp.py)."""

    def test_get_absolute_url(self):
        p = ACILLDPInterfacePolicy.objects.create(aci_fabric=self.fab, name="lldp-url")
        self.assertIn(str(p.pk), p.get_absolute_url())


class ACILACPInterfacePolicyExtraTests(_Phase4Fixture):
    """Cover get_absolute_url (L87 in lacp.py) and LACP required for PC/vPC."""

    def test_get_absolute_url(self):
        p = ACILACPInterfacePolicy.objects.create(
            aci_fabric=self.fab, name="lacp-url", mode=LACPModeChoices.ACTIVE
        )
        self.assertIn(str(p.pk), p.get_absolute_url())

    def test_pc_without_lacp_rejected(self):
        from netbox_cisco_aci.models.access import ACIInterfacePolicyGroup

        pg = ACIInterfacePolicyGroup(
            aci_fabric=self.fab,
            name="pg-pc-no-lacp",
            pg_type=InterfacePolicyGroupTypeChoices.PC,
        )
        with self.assertRaisesRegex(ValidationError, "LACP"):
            pg.full_clean()


class ACIMCPInterfacePolicyExtraTests(_Phase4Fixture):
    """Cover get_absolute_url (L47 in mcp.py)."""

    def test_get_absolute_url(self):
        p = ACIMCPInterfacePolicy.objects.create(aci_fabric=self.fab, name="mcp-url")
        self.assertIn(str(p.pk), p.get_absolute_url())


class ACISTPInterfacePolicyExtraTests(_Phase4Fixture):
    """Cover get_absolute_url (L48 in stp.py)."""

    def test_get_absolute_url(self):
        p = ACISTPInterfacePolicy.objects.create(aci_fabric=self.fab, name="stp-url")
        self.assertIn(str(p.pk), p.get_absolute_url())


class ACIInterfacePolicyGroupExtraTests(_Phase4Fixture):
    """Cover missed lines L116, 119, 141 in policy_groups.py."""

    def test_get_absolute_url(self):
        pg = ACIInterfacePolicyGroup.objects.create(
            aci_fabric=self.fab,
            name="pg-url",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
        )
        self.assertIn(str(pg.pk), pg.get_absolute_url())

    def test_get_pg_type_color(self):
        pg = ACIInterfacePolicyGroup(
            aci_fabric=self.fab, name="pg-color", pg_type=InterfacePolicyGroupTypeChoices.PC
        )
        self.assertEqual(pg.get_pg_type_color(), "blue")

    def test_pg_without_fabric_skips_cross_fabric_check(self):
        """Line 141: early return when aci_fabric_id is None."""
        pg = ACIInterfacePolicyGroup(
            name="pg-no-fabric", pg_type=InterfacePolicyGroupTypeChoices.ACCESS
        )
        # clean() should return without raising when there is no fabric set
        pg.clean()


class ACISwitchProfileExtraTests(_Phase4Fixture):
    """Cover get_absolute_url (L53) in switch_profiles.py."""

    def test_get_absolute_url(self):
        sp = ACISwitchProfile.objects.create(aci_fabric=self.fab, name="sp-url")
        self.assertIn(str(sp.pk), sp.get_absolute_url())


class ACISwitchProfileSelectorExtraTests(_Phase4Fixture):
    """Cover missed lines L98, 105, 109 in switch_profiles.py."""

    def test_str_all_type(self):
        sp = ACISwitchProfile.objects.create(aci_fabric=self.fab, name="sp-sel-all")
        sel = ACISwitchProfileSelector.objects.create(
            switch_profile=sp, name="sel-all", selector_type=RangeAllChoices.ALL
        )
        self.assertIn("all", str(sel))

    def test_get_absolute_url(self):
        sp = ACISwitchProfile.objects.create(aci_fabric=self.fab, name="sp-sel-url")
        sel = ACISwitchProfileSelector.objects.create(
            switch_profile=sp, name="sel-url", selector_type=RangeAllChoices.ALL
        )
        self.assertIn(str(sel.pk), sel.get_absolute_url())

    def test_aci_fabric_property(self):
        sp = ACISwitchProfile.objects.create(aci_fabric=self.fab, name="sp-fab-prop")
        sel = ACISwitchProfileSelector.objects.create(
            switch_profile=sp, name="sel-fab-prop", selector_type=RangeAllChoices.ALL
        )
        self.assertEqual(sel.aci_fabric, self.fab)


class ACIInterfaceProfileSelectorExtraTests(_Phase4Fixture):
    """Cover missed lines L45, 110, 114 in interface_profiles.py."""

    def test_from_gt_to_raises(self):
        ip = ACIInterfaceProfile.objects.create(aci_fabric=self.fab, name="ip-sel-range")
        sel = ACIInterfaceProfileSelector(
            interface_profile=ip,
            name="isel-bad",
            from_module=1,
            from_port=10,
            to_module=1,
            to_port=1,
        )
        with self.assertRaisesRegex(ValidationError, "from_module"):
            sel.full_clean()

    def test_cross_fabric_policy_group_rejected(self):
        ip = ACIInterfaceProfile.objects.create(aci_fabric=self.fab, name="ip-xfab")
        pg_fab2 = ACIInterfacePolicyGroup.objects.create(
            aci_fabric=self.fab2,
            name="pg-fab2",
            pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
        )
        sel = ACIInterfaceProfileSelector(
            interface_profile=ip,
            name="isel-xfab",
            from_module=1,
            from_port=1,
            to_module=1,
            to_port=10,
            policy_group=pg_fab2,
        )
        with self.assertRaisesRegex(ValidationError, "Fabric"):
            sel.full_clean()


class ACISwitchProfileInterfaceProfileAttachmentExtraTests(_Phase4Fixture):
    """Cover get_absolute_url (L49 in attachments.py)."""

    def test_get_absolute_url(self):
        sp = ACISwitchProfile.objects.create(aci_fabric=self.fab, name="sp-attach-url")
        ip = ACIInterfaceProfile.objects.create(aci_fabric=self.fab, name="ip-attach-url")
        attachment = ACISwitchProfileInterfaceProfileAttachment.objects.create(
            switch_profile=sp, interface_profile=ip
        )
        self.assertIn(str(attachment.pk), attachment.get_absolute_url())
