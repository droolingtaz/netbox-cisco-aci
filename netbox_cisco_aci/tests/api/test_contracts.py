"""REST API tests for Phase 5: Contracts / Subjects / Filters / Relations."""

from utilities.testing import APITestCase, APIViewTestCases

from netbox_cisco_aci.choices import (
    ContractFilterEntryEtherTypeChoices,
    ContractRelationRoleChoices,
    ContractScopeChoices,
    SubjectFilterDirectionChoices,
)
from netbox_cisco_aci.models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.l3out import ACIExternalEPG, ACIL3Out
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
)

PLUGIN_API_NAMESPACE = "plugins-api:netbox_cisco_aci"


# ---------------------------------------------------------------------------
# ACIContract
# ---------------------------------------------------------------------------


class ACIContractAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIContract
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_tenant",
        "description",
        "display",
        "id",
        "name",
        "scope",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        # ACIContract is parent of ACISubject (CASCADE) and ACIContractRelation
        # (CASCADE) — no PROTECT children → no isolation needed.
        fab = ACIFabric.objects.create(name="API-ContractFab")
        tenant = ACITenant.objects.create(aci_fabric=fab, name="t-c")
        for i in range(3):
            ACIContract.objects.create(aci_tenant=tenant, name=f"c-{i}")
        cls.create_data = [
            {
                "aci_tenant": tenant.pk,
                "name": "c-a",
                "scope": ContractScopeChoices.SCOPE_VRF,
            },
            {
                "aci_tenant": tenant.pk,
                "name": "c-b",
                "scope": ContractScopeChoices.SCOPE_TENANT,
            },
        ]


# ---------------------------------------------------------------------------
# ACISubject
# ---------------------------------------------------------------------------


class ACISubjectAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACISubject
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_contract",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-SubjFab")
        tenant = ACITenant.objects.create(aci_fabric=fab, name="t-s")
        contract = ACIContract.objects.create(aci_tenant=tenant, name="c-s")
        for i in range(3):
            ACISubject.objects.create(aci_contract=contract, name=f"s-{i}")
        cls.create_data = [
            {"aci_contract": contract.pk, "name": "s-a"},
            {"aci_contract": contract.pk, "name": "s-b"},
        ]


# ---------------------------------------------------------------------------
# ACIFilter
#
# ACIFilter is referenced by ACISubjectFilter via on_delete=PROTECT. Two
# safety constraints must hold:
#   1. test_delete_object deletes _get_queryset().first() (ordered by `name`)
#      → the alphabetically-first filter must have no protected child. We
#      point the protected child at "f-1" (NOT "f-0").
#   2. test_bulk_delete_objects deletes the 3 most recently-created rows by
#      `-id`. We create THREE additional safe filters (f-3, f-4, f-5) AFTER
#      f-1, so the top-3-by-id are all unprotected.
# ---------------------------------------------------------------------------


class ACIFilterAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIFilter
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_tenant",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-FilterFab")
        tenant = ACITenant.objects.create(aci_fabric=fab, name="t-f")
        contract = ACIContract.objects.create(aci_tenant=tenant, name="c-f")
        # First batch — f-0, f-1, f-2. f-1 gets a PROTECT child.
        for i in range(3):
            ACIFilter.objects.create(aci_tenant=tenant, name=f"f-{i}")
        subj = ACISubject.objects.create(aci_contract=contract, name="s-prot")
        f1 = ACIFilter.objects.get(aci_tenant=tenant, name="f-1")
        ACISubjectFilter.objects.create(aci_subject=subj, aci_filter=f1, name="sf-prot")
        # Second batch — f-3, f-4, f-5. Created AFTER the protected child, so
        # the top-3-by-id are all safe for bulk delete.
        for i in range(3, 6):
            ACIFilter.objects.create(aci_tenant=tenant, name=f"f-{i}")
        cls.create_data = [
            {"aci_tenant": tenant.pk, "name": "f-a"},
            {"aci_tenant": tenant.pk, "name": "f-b"},
        ]


# ---------------------------------------------------------------------------
# ACIFilterEntry
# ---------------------------------------------------------------------------


class ACIFilterEntryAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIFilterEntry
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_filter",
        "description",
        "display",
        "ether_type",
        "id",
        "ip_protocol",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-EntryFab")
        tenant = ACITenant.objects.create(aci_fabric=fab, name="t-e")
        filt = ACIFilter.objects.create(aci_tenant=tenant, name="f-e")
        for i in range(3):
            ACIFilterEntry.objects.create(
                aci_filter=filt,
                name=f"e-{i}",
                ether_type=ContractFilterEntryEtherTypeChoices.UNSPECIFIED,
            )
        cls.create_data = [
            {
                "aci_filter": filt.pk,
                "name": "e-a",
                "ether_type": ContractFilterEntryEtherTypeChoices.IP,
            },
            {
                "aci_filter": filt.pk,
                "name": "e-b",
                "ether_type": ContractFilterEntryEtherTypeChoices.ARP,
            },
        ]


# ---------------------------------------------------------------------------
# ACISubjectFilter (through-model)
# ---------------------------------------------------------------------------


class ACISubjectFilterAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACISubjectFilter
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_filter",
        "aci_subject",
        "description",
        "direction",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-SFFab")
        tenant = ACITenant.objects.create(aci_fabric=fab, name="t-sf")
        contract = ACIContract.objects.create(aci_tenant=tenant, name="c-sf")
        subj = ACISubject.objects.create(
            aci_contract=contract,
            name="s-sf",
            apply_both_directions=False,
            reverse_filter_ports=False,
        )
        # Need distinct filters because (subject, filter, direction) is unique
        # and we keep direction=in for the seed rows.
        filters = [ACIFilter.objects.create(aci_tenant=tenant, name=f"f-sf-{i}") for i in range(5)]
        for i in range(3):
            ACISubjectFilter.objects.create(
                aci_subject=subj,
                aci_filter=filters[i],
                name=f"sf-{i}",
                direction=SubjectFilterDirectionChoices.IN,
            )
        cls.create_data = [
            {
                "aci_subject": subj.pk,
                "aci_filter": filters[3].pk,
                "name": "sf-a",
                "direction": SubjectFilterDirectionChoices.IN,
            },
            {
                "aci_subject": subj.pk,
                "aci_filter": filters[4].pk,
                "name": "sf-b",
                "direction": SubjectFilterDirectionChoices.IN,
            },
        ]


# ---------------------------------------------------------------------------
# ACIContractRelation
# ---------------------------------------------------------------------------


class ACIContractRelationAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIContractRelation
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_contract",
        "description",
        "display",
        "id",
        "name",
        "role",
        "url",
    ]
    # Only patch description to avoid XOR-field conflicts across the three
    # different FK paths (EPG / ESG / External EPG).
    update_data = {"description": "Updated via PATCH"}
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="API-RelFab")
        tenant = ACITenant.objects.create(aci_fabric=fab, name="t-r")
        vrf = ACIVRF.objects.create(aci_tenant=tenant, name="vrf-r")
        ap = ACIAppProfile.objects.create(aci_tenant=tenant, name="ap-r")
        bd = ACIBridgeDomain.objects.create(aci_tenant=tenant, aci_vrf=vrf, name="bd-r")
        # Distinct EPGs per relation to avoid (contract, epg, role) UC clashes.
        epgs = [
            ACIEndpointGroup.objects.create(
                aci_tenant=tenant, aci_app_profile=ap, aci_bridge_domain=bd, name=f"epg-{i}"
            )
            for i in range(5)
        ]
        contract = ACIContract.objects.create(aci_tenant=tenant, name="c-r")
        # Existing rows: 2 EPG-attached + 1 External EPG-attached
        for i in range(2):
            ACIContractRelation.objects.create(
                aci_contract=contract,
                aci_endpoint_group=epgs[i],
                role=ContractRelationRoleChoices.PROVIDER,
                name=f"r-{i}",
            )
        # External EPG path
        l3out = ACIL3Out.objects.create(
            aci_tenant=tenant,
            aci_vrf=vrf,
            name="c-r-l3out",
            protocol_static=True,
        )
        eepg = ACIExternalEPG.objects.create(aci_l3out=l3out, name="c-r-ext")
        ACIContractRelation.objects.create(
            aci_contract=contract,
            aci_external_epg=eepg,
            role=ContractRelationRoleChoices.CONSUMER,
            name="r-extepg",
        )
        cls.create_data = [
            {
                "aci_contract": contract.pk,
                "aci_endpoint_group": epgs[3].pk,
                "role": ContractRelationRoleChoices.PROVIDER,
                "name": "r-a",
            },
            {
                "aci_contract": contract.pk,
                "aci_endpoint_group": epgs[4].pk,
                "role": ContractRelationRoleChoices.CONSUMER,
                "name": "r-b",
            },
            {
                "aci_contract": contract.pk,
                "aci_external_epg": eepg.pk,
                "role": ContractRelationRoleChoices.PROVIDER,
                "name": "r-c",
            },
        ]
