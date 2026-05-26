"""REST API smoke tests for Phase 4 (per-port policies, Policy Groups, Switch/Interface Profiles)."""

from utilities.testing import APITestCase, APIViewTestCases

from netbox_cisco_aci.choices import (
    EnabledDisabledChoices,
    InterfacePolicyGroupTypeChoices,
    LACPModeChoices,
    LinkLevelSpeedChoices,
    RangeAllChoices,
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

PLUGIN_API_NAMESPACE = "plugins-api:netbox_cisco_aci"


# ---------------------------------------------------------------------------
# Link Level
# ---------------------------------------------------------------------------


class ACILinkLevelPolicyAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACILinkLevelPolicy
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "description",
        "display",
        "id",
        "name",
        "speed",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-LLFab")
        for i in range(3):
            ACILinkLevelPolicy.objects.create(
                aci_fabric=fab, name=f"ll-{i}", speed=LinkLevelSpeedChoices.SPEED_10G
            )
        cls.create_data = [
            {"aci_fabric": fab.pk, "name": "ll-a", "speed": "1G"},
            {"aci_fabric": fab.pk, "name": "ll-b", "speed": "40G"},
        ]


# ---------------------------------------------------------------------------
# CDP
# ---------------------------------------------------------------------------


class ACICDPInterfacePolicyAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACICDPInterfacePolicy
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "admin_state",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-CDPFab")
        for i in range(3):
            ACICDPInterfacePolicy.objects.create(aci_fabric=fab, name=f"cdp-{i}")
        cls.create_data = [
            {"aci_fabric": fab.pk, "name": "cdp-a", "admin_state": "disabled"},
            {"aci_fabric": fab.pk, "name": "cdp-b", "admin_state": "enabled"},
        ]


# ---------------------------------------------------------------------------
# LLDP
# ---------------------------------------------------------------------------


class ACILLDPInterfacePolicyAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACILLDPInterfacePolicy
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "description",
        "display",
        "id",
        "name",
        "receive_state",
        "transmit_state",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-LLDPFab")
        for i in range(3):
            ACILLDPInterfacePolicy.objects.create(aci_fabric=fab, name=f"lldp-{i}")
        cls.create_data = [
            {
                "aci_fabric": fab.pk,
                "name": "lldp-a",
                "receive_state": "enabled",
                "transmit_state": "enabled",
            },
            {
                "aci_fabric": fab.pk,
                "name": "lldp-b",
                "receive_state": "disabled",
                "transmit_state": "disabled",
            },
        ]


# ---------------------------------------------------------------------------
# LACP
# ---------------------------------------------------------------------------


class ACILACPInterfacePolicyAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACILACPInterfacePolicy
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "description",
        "display",
        "id",
        "mode",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-LACPFab")
        for i in range(3):
            ACILACPInterfacePolicy.objects.create(
                aci_fabric=fab, name=f"lacp-{i}", mode=LACPModeChoices.ACTIVE
            )
        cls.create_data = [
            {"aci_fabric": fab.pk, "name": "lacp-a", "mode": "active"},
            {"aci_fabric": fab.pk, "name": "lacp-b", "mode": "passive"},
        ]


# ---------------------------------------------------------------------------
# MCP
# ---------------------------------------------------------------------------


class ACIMCPInterfacePolicyAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIMCPInterfacePolicy
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "admin_state",
        "description",
        "display",
        "id",
        "name",
        "strict_mode",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-MCPFab")
        for i in range(3):
            ACIMCPInterfacePolicy.objects.create(aci_fabric=fab, name=f"mcp-{i}")
        cls.create_data = [
            {
                "aci_fabric": fab.pk,
                "name": "mcp-a",
                "admin_state": EnabledDisabledChoices.ENABLED,
            },
            {
                "aci_fabric": fab.pk,
                "name": "mcp-b",
                "admin_state": EnabledDisabledChoices.DISABLED,
            },
        ]


# ---------------------------------------------------------------------------
# STP
# ---------------------------------------------------------------------------


class ACISTPInterfacePolicyAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACISTPInterfacePolicy
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "bpdu_filter",
        "bpdu_guard",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-STPFab")
        for i in range(3):
            ACISTPInterfacePolicy.objects.create(aci_fabric=fab, name=f"stp-{i}")
        cls.create_data = [
            {"aci_fabric": fab.pk, "name": "stp-a", "bpdu_guard": True},
            {"aci_fabric": fab.pk, "name": "stp-b", "bpdu_filter": True},
        ]


# ---------------------------------------------------------------------------
# Interface Policy Group
# ---------------------------------------------------------------------------


class ACIInterfacePolicyGroupAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIInterfacePolicyGroup
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "description",
        "display",
        "id",
        "name",
        "pg_type",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        # NOTE: ACIInterfaceProfileSelector references ACIInterfacePolicyGroup
        # via on_delete=PROTECT. The framework's test_delete_object deletes
        # ._get_queryset().first() (first by `name` ordering). Pin every
        # selector to a policy group whose name is NOT the first
        # alphabetically, so the first-by-name pg has no protected child
        # and is safe to delete.
        fab = ACIFabric.objects.create(name="API-PGFab")
        # "pg-0" is alphabetically first; selector references "pg-1" only.
        for i in range(3):
            ACIInterfacePolicyGroup.objects.create(
                aci_fabric=fab,
                name=f"pg-{i}",
                pg_type=InterfacePolicyGroupTypeChoices.ACCESS,
            )
        ip = ACIInterfaceProfile.objects.create(aci_fabric=fab, name="ip-isol")
        pg1 = ACIInterfacePolicyGroup.objects.get(aci_fabric=fab, name="pg-1")
        ACIInterfaceProfileSelector.objects.create(
            interface_profile=ip,
            name="isel",
            policy_group=pg1,
            from_module=1,
            from_port=1,
            to_module=1,
            to_port=1,
        )
        cls.create_data = [
            {"aci_fabric": fab.pk, "name": "pg-a", "pg_type": "access"},
            {"aci_fabric": fab.pk, "name": "pg-b", "pg_type": "access"},
        ]


# ---------------------------------------------------------------------------
# Switch Profile + Selector
# ---------------------------------------------------------------------------


class ACISwitchProfileAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACISwitchProfile
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-SPFab")
        for i in range(3):
            ACISwitchProfile.objects.create(aci_fabric=fab, name=f"sp-{i}")
        cls.create_data = [
            {"aci_fabric": fab.pk, "name": "sp-a"},
            {"aci_fabric": fab.pk, "name": "sp-b"},
        ]


class ACISwitchProfileSelectorAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACISwitchProfileSelector
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "description",
        "display",
        "from_node_id",
        "id",
        "name",
        "selector_type",
        "switch_profile",
        "to_node_id",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-SPSelFab")
        sp = ACISwitchProfile.objects.create(aci_fabric=fab, name="sp-sel")
        for i in range(3):
            ACISwitchProfileSelector.objects.create(
                switch_profile=sp,
                name=f"sel-{i}",
                selector_type=RangeAllChoices.RANGE,
                from_node_id=100 + i,
                to_node_id=100 + i,
            )
        cls.sp_pk = sp.pk
        cls.create_data = [
            {
                "switch_profile": sp.pk,
                "name": "sel-a",
                "selector_type": "range",
                "from_node_id": 200,
                "to_node_id": 210,
            },
            {
                "switch_profile": sp.pk,
                "name": "sel-b",
                "selector_type": "all",
            },
        ]


# ---------------------------------------------------------------------------
# Interface Profile + Selector
# ---------------------------------------------------------------------------


class ACIInterfaceProfileAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIInterfaceProfile
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-IPFab")
        for i in range(3):
            ACIInterfaceProfile.objects.create(aci_fabric=fab, name=f"ip-{i}")
        cls.create_data = [
            {"aci_fabric": fab.pk, "name": "ip-a"},
            {"aci_fabric": fab.pk, "name": "ip-b"},
        ]


class ACIInterfaceProfileSelectorAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIInterfaceProfileSelector
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "description",
        "display",
        "from_module",
        "from_port",
        "id",
        "interface_profile",
        "name",
        "policy_group",
        "to_module",
        "to_port",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-IPSelFab")
        ip = ACIInterfaceProfile.objects.create(aci_fabric=fab, name="ip-sel")
        for i in range(3):
            ACIInterfaceProfileSelector.objects.create(
                interface_profile=ip,
                name=f"isel-{i}",
                from_module=1,
                from_port=1 + i,
                to_module=1,
                to_port=1 + i,
            )
        cls.create_data = [
            {
                "interface_profile": ip.pk,
                "name": "isel-a",
                "from_module": 1,
                "from_port": 10,
                "to_module": 1,
                "to_port": 12,
            },
            {
                "interface_profile": ip.pk,
                "name": "isel-b",
                "from_module": 1,
                "from_port": 20,
                "to_module": 1,
                "to_port": 22,
            },
        ]


# ---------------------------------------------------------------------------
# Switch <-> Interface Profile attachment
# ---------------------------------------------------------------------------


class ACISwitchProfileInterfaceProfileAttachmentAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACISwitchProfileInterfaceProfileAttachment
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "display",
        "id",
        "interface_profile",
        "switch_profile",
        "url",
    ]
    # No description on this model -> bulk_update_data is omitted.

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-AttFab")
        # Five switch profiles, five interface profiles, three preexisting
        # attachments so list / count tests have rows; the create_data adds
        # two more distinct pairs.
        sps = [ACISwitchProfile.objects.create(aci_fabric=fab, name=f"sp-{i}") for i in range(5)]
        ips = [ACIInterfaceProfile.objects.create(aci_fabric=fab, name=f"ip-{i}") for i in range(5)]
        for i in range(3):
            ACISwitchProfileInterfaceProfileAttachment.objects.create(
                switch_profile=sps[i], interface_profile=ips[i]
            )
        cls.create_data = [
            {"switch_profile": sps[3].pk, "interface_profile": ips[3].pk},
            {"switch_profile": sps[4].pk, "interface_profile": ips[4].pk},
        ]
