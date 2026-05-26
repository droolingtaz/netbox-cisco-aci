"""Form tests for Phase 4."""

from django.test import TestCase

from netbox_cisco_aci.choices import (
    InterfacePolicyGroupTypeChoices,
    LACPModeChoices,
    RangeAllChoices,
)
from netbox_cisco_aci.forms.access_groups import ACIInterfacePolicyGroupForm
from netbox_cisco_aci.forms.access_policies import (
    ACICDPInterfacePolicyForm,
    ACILACPInterfacePolicyForm,
    ACILinkLevelPolicyForm,
    ACILLDPInterfacePolicyForm,
    ACIMCPInterfacePolicyForm,
    ACISTPInterfacePolicyForm,
)
from netbox_cisco_aci.forms.access_profiles import (
    ACIInterfaceProfileForm,
    ACIInterfaceProfileSelectorForm,
    ACISwitchProfileForm,
    ACISwitchProfileInterfaceProfileAttachmentForm,
    ACISwitchProfileSelectorForm,
)
from netbox_cisco_aci.models.access import (
    ACIInterfaceProfile,
    ACISwitchProfile,
)
from netbox_cisco_aci.models.fabric import ACIFabric


class Phase4FormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.sp = ACISwitchProfile.objects.create(aci_fabric=cls.fab, name="sp-1")
        cls.ip = ACIInterfaceProfile.objects.create(aci_fabric=cls.fab, name="ip-1")

    def test_acilinklevelpolicy_form_valid(self):
        form = ACILinkLevelPolicyForm(
            data={
                "aci_fabric": self.fab.pk,
                "name": "ll-1",
                "speed": "10G",
                "auto_negotiation": "on",
                "link_debounce_interval_ms": 100,
                "fec_mode": "inherit",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acicdpinterfacepolicy_form_valid(self):
        form = ACICDPInterfacePolicyForm(
            data={"aci_fabric": self.fab.pk, "name": "cdp-1", "admin_state": "disabled"}
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acilldpinterfacepolicy_form_valid(self):
        form = ACILLDPInterfacePolicyForm(
            data={
                "aci_fabric": self.fab.pk,
                "name": "lldp-1",
                "receive_state": "enabled",
                "transmit_state": "enabled",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acilacpinterfacepolicy_form_valid(self):
        form = ACILACPInterfacePolicyForm(
            data={
                "aci_fabric": self.fab.pk,
                "name": "lacp-1",
                "mode": LACPModeChoices.ACTIVE,
                "min_links": 1,
                "max_links": 8,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acilacpinterfacepolicy_form_invalid_min_gt_max(self):
        form = ACILACPInterfacePolicyForm(
            data={
                "aci_fabric": self.fab.pk,
                "name": "lacp-bad",
                "mode": LACPModeChoices.ACTIVE,
                "min_links": 8,
                "max_links": 2,
            }
        )
        self.assertFalse(form.is_valid())

    def test_acimcpinterfacepolicy_form_valid(self):
        form = ACIMCPInterfacePolicyForm(
            data={"aci_fabric": self.fab.pk, "name": "mcp-1", "admin_state": "enabled"}
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acistpinterfacepolicy_form_valid(self):
        form = ACISTPInterfacePolicyForm(data={"aci_fabric": self.fab.pk, "name": "stp-1"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_aciinterfacepolicygroup_form_valid(self):
        form = ACIInterfacePolicyGroupForm(
            data={
                "aci_fabric": self.fab.pk,
                "name": "pg-1",
                "pg_type": InterfacePolicyGroupTypeChoices.ACCESS,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_aciswitchprofile_form_valid(self):
        form = ACISwitchProfileForm(data={"aci_fabric": self.fab.pk, "name": "sp-x"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_aciswitchprofileselector_form_valid(self):
        form = ACISwitchProfileSelectorForm(
            data={
                "switch_profile": self.sp.pk,
                "name": "sel-1",
                "selector_type": RangeAllChoices.RANGE,
                "from_node_id": 101,
                "to_node_id": 102,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_aciswitchprofileselector_form_invalid_range(self):
        form = ACISwitchProfileSelectorForm(
            data={
                "switch_profile": self.sp.pk,
                "name": "sel-bad",
                "selector_type": RangeAllChoices.RANGE,
                "from_node_id": 200,
                "to_node_id": 100,
            }
        )
        self.assertFalse(form.is_valid())

    def test_aciinterfaceprofile_form_valid(self):
        form = ACIInterfaceProfileForm(data={"aci_fabric": self.fab.pk, "name": "ip-x"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_aciinterfaceprofileselector_form_valid(self):
        form = ACIInterfaceProfileSelectorForm(
            data={
                "interface_profile": self.ip.pk,
                "name": "isel-1",
                "from_module": 1,
                "from_port": 1,
                "to_module": 1,
                "to_port": 24,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_aciinterfaceprofileselector_form_invalid_range(self):
        form = ACIInterfaceProfileSelectorForm(
            data={
                "interface_profile": self.ip.pk,
                "name": "isel-bad",
                "from_module": 2,
                "from_port": 1,
                "to_module": 1,
                "to_port": 24,
            }
        )
        self.assertFalse(form.is_valid())

    def test_aciswitchprofileinterfaceprofileattachment_form_valid(self):
        form = ACISwitchProfileInterfaceProfileAttachmentForm(
            data={"switch_profile": self.sp.pk, "interface_profile": self.ip.pk}
        )
        self.assertTrue(form.is_valid(), form.errors)
