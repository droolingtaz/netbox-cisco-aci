"""REST API smoke tests for Phase 3."""

from utilities.testing import APITestCase, APIViewTestCases

from netbox_cisco_aci.choices import DomainTypeChoices, VLANPoolAllocationChoices
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

PLUGIN_API_NAMESPACE = "plugins-api:netbox_cisco_aci"


def _seed_access():
    fab = ACIFabric.objects.create(name="API-AccessFab")
    pool = ACIVLANPool.objects.create(
        aci_fabric=fab, name="pool-1", allocation_mode=VLANPoolAllocationChoices.STATIC
    )
    domain = ACIDomain.objects.create(
        aci_fabric=fab,
        name="phys-1",
        domain_type=DomainTypeChoices.PHYSICAL,
        aci_vlan_pool=pool,
    )
    aaep = ACIAAEP.objects.create(aci_fabric=fab, name="aaep-1")
    tenant = ACITenant.objects.create(aci_fabric=fab, name="acme")
    vrf = ACIVRF.objects.create(aci_tenant=tenant, name="vrf-prod")
    ap = ACIAppProfile.objects.create(aci_tenant=tenant, name="ap-web")
    bd = ACIBridgeDomain.objects.create(aci_tenant=tenant, aci_vrf=vrf, name="bd-web")
    epg = ACIEndpointGroup.objects.create(
        aci_tenant=tenant, aci_app_profile=ap, aci_bridge_domain=bd, name="epg-web"
    )
    return {
        "fab": fab,
        "pool": pool,
        "domain": domain,
        "aaep": aaep,
        "epg": epg,
    }


class ACIVLANPoolAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIVLANPool
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "allocation_mode",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        # NOTE: do not call _seed_access() here -- it creates an ACIDomain
        # protecting the first VLAN pool, which would block the inherited
        # test_delete_object case (it deletes ._get_queryset().first()).
        fab = ACIFabric.objects.create(name="API-PoolFab")
        for i in range(4):
            ACIVLANPool.objects.create(
                aci_fabric=fab, name=f"pool-{i}", allocation_mode="static"
            )
        cls.create_data = [
            {"aci_fabric": fab.pk, "name": "pool-a", "allocation_mode": "static"},
            {
                "aci_fabric": fab.pk,
                "name": "pool-b",
                "allocation_mode": "dynamic",
            },
        ]


class ACIVLANPoolBlockAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIVLANPoolBlock
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_vlan_pool",
        "description",
        "display",
        "from_vlan",
        "id",
        "to_vlan",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        d = _seed_access()
        cls.shared_pool = d["pool"]
        for i in range(3):
            ACIVLANPoolBlock.objects.create(
                aci_vlan_pool=d["pool"],
                name=f"blk-{i}",
                from_vlan=100 + i * 50,
                to_vlan=100 + i * 50 + 49,
            )
        cls.create_data = [
            {
                "aci_vlan_pool": d["pool"].pk,
                "name": "blk-a",
                "from_vlan": 500,
                "to_vlan": 550,
            },
            {
                "aci_vlan_pool": d["pool"].pk,
                "name": "blk-b",
                "from_vlan": 600,
                "to_vlan": 650,
            },
        ]


class ACIDomainAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIDomain
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "description",
        "display",
        "domain_type",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        d = _seed_access()
        for i in range(3):
            ACIDomain.objects.create(
                aci_fabric=d["fab"],
                name=f"dom-{i}",
                domain_type=DomainTypeChoices.PHYSICAL,
            )
        cls.create_data = [
            {
                "aci_fabric": d["fab"].pk,
                "name": "dom-a",
                "domain_type": "physical",
            },
            {
                "aci_fabric": d["fab"].pk,
                "name": "dom-b",
                "domain_type": "l3",
            },
        ]


class ACIAAEPAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIAAEP
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_fabric",
        "description",
        "display",
        "enable_infra_vlan",
        "id",
        "name",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        d = _seed_access()
        for i in range(3):
            ACIAAEP.objects.create(aci_fabric=d["fab"], name=f"aaep-extra-{i}")
        cls.create_data = [
            {"aci_fabric": d["fab"].pk, "name": "aaep-a"},
            {"aci_fabric": d["fab"].pk, "name": "aaep-b", "enable_infra_vlan": True},
        ]


class ACIAAEPEPGMappingAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIAAEPEPGMapping
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = [
        "aci_aaep",
        "aci_endpoint_group",
        "display",
        "encap_vlan",
        "id",
        "mode",
        "url",
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        d = _seed_access()
        for i in range(3):
            ACIAAEPEPGMapping.objects.create(
                aci_aaep=d["aaep"],
                aci_endpoint_group=d["epg"],
                name=f"map-{i}",
                encap_vlan=100 + i,
            )
        cls.create_data = [
            {
                "aci_aaep": d["aaep"].pk,
                "aci_endpoint_group": d["epg"].pk,
                "name": "map-a",
                "encap_vlan": 500,
                "mode": "regular",
            },
            {
                "aci_aaep": d["aaep"].pk,
                "aci_endpoint_group": d["epg"].pk,
                "name": "map-b",
                "encap_vlan": 600,
                "mode": "regular",
            },
        ]
