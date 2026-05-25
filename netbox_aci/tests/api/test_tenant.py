"""REST API smoke tests for Phase 2."""

from utilities.testing import APITestCase, APIViewTestCases

from netbox_aci.models.fabric import ACIFabric
from netbox_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
)

PLUGIN_API_NAMESPACE = "plugins-api:netbox_aci"


def _seed():
    fab = ACIFabric.objects.create(name="API-Fab")
    tenant = ACITenant.objects.create(aci_fabric=fab, name="acme")
    vrf = ACIVRF.objects.create(aci_tenant=tenant, name="vrf-prod")
    ap = ACIAppProfile.objects.create(aci_tenant=tenant, name="ap-web")
    bd = ACIBridgeDomain.objects.create(aci_tenant=tenant, aci_vrf=vrf, name="bd-web")
    return {"fab": fab, "tenant": tenant, "vrf": vrf, "ap": ap, "bd": bd}


class ACITenantAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACITenant
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = ["display", "id", "name", "url"]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="TenantAPIFab")
        for i in range(3):
            ACITenant.objects.create(aci_fabric=fab, name=f"t-{i}")
        cls.create_data = [
            {"aci_fabric_id": fab.pk, "name": "api-tenant-a"},
            {"aci_fabric_id": fab.pk, "name": "api-tenant-b"},
        ]


class ACIVRFAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIVRF
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = ["display", "id", "name", "url"]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="VRFAPIFab")
        tenant = ACITenant.objects.create(aci_fabric=fab, name="acme")
        for i in range(3):
            ACIVRF.objects.create(aci_tenant=tenant, name=f"vrf-{i}")
        cls.create_data = [
            {"aci_tenant_id": tenant.pk, "name": "vrf-a"},
            {"aci_tenant_id": tenant.pk, "name": "vrf-b"},
        ]


class ACIBridgeDomainAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIBridgeDomain
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = ["display", "id", "name", "url"]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        d = _seed()
        for i in range(3):
            ACIBridgeDomain.objects.create(aci_tenant=d["tenant"], aci_vrf=d["vrf"], name=f"bd-{i}")
        cls.create_data = [
            {
                "aci_tenant_id": d["tenant"].pk,
                "aci_vrf_id": d["vrf"].pk,
                "name": "bd-a",
            },
            {
                "aci_tenant_id": d["tenant"].pk,
                "aci_vrf_id": d["vrf"].pk,
                "name": "bd-b",
            },
        ]


class ACIEndpointGroupAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIEndpointGroup
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = ["display", "id", "name", "url"]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        d = _seed()
        for i in range(3):
            ACIEndpointGroup.objects.create(
                aci_tenant=d["tenant"],
                aci_app_profile=d["ap"],
                aci_bridge_domain=d["bd"],
                name=f"epg-{i}",
            )
        cls.create_data = [
            {
                "aci_tenant_id": d["tenant"].pk,
                "aci_app_profile_id": d["ap"].pk,
                "aci_bridge_domain_id": d["bd"].pk,
                "name": "epg-a",
            },
            {
                "aci_tenant_id": d["tenant"].pk,
                "aci_app_profile_id": d["ap"].pk,
                "aci_bridge_domain_id": d["bd"].pk,
                "name": "epg-b",
            },
        ]


class ACIEndpointSecurityGroupAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIEndpointSecurityGroup
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = ["display", "id", "name", "url"]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        d = _seed()
        for i in range(3):
            ACIEndpointSecurityGroup.objects.create(
                aci_tenant=d["tenant"], aci_vrf=d["vrf"], name=f"esg-{i}"
            )
        cls.create_data = [
            {
                "aci_tenant_id": d["tenant"].pk,
                "aci_vrf_id": d["vrf"].pk,
                "name": "esg-a",
            },
            {
                "aci_tenant_id": d["tenant"].pk,
                "aci_vrf_id": d["vrf"].pk,
                "name": "esg-b",
            },
        ]
