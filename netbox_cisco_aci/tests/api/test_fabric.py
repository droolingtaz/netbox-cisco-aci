"""REST API smoke tests for Phase 1."""

from rest_framework import status
from utilities.testing import APITestCase, APIViewTestCases

from netbox_cisco_aci.models.fabric import ACIFabric, ACINode, ACIPod

# Plugin API namespaces live under ``plugins-api:``. NetBox's default
# ``_get_view_namespace`` returns ``{model._meta.app_label}-api``, which
# is correct for core apps but not plugins. Override it for every API
# test class.
PLUGIN_API_NAMESPACE = "plugins-api:netbox_cisco_aci"


class ACIFabricAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIFabric
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = ["description", "display", "fabric_id", "id", "name", "url"]
    create_data = [
        {"name": "ACI-API-DC1", "fabric_id": 1},
        {"name": "ACI-API-DC2", "fabric_id": 2},
        {"name": "ACI-API-DC3", "fabric_id": 1},  # shared fabric_id allowed
    ]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        for i in range(3):
            ACIFabric.objects.create(name=f"ACI-API-Existing-{i}", fabric_id=i + 1)


class ACIPodAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACIPod
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = ["aci_fabric", "description", "display", "id", "name", "pod_id", "url"]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="ACI-API-PodFab")
        for i in range(3):
            ACIPod.objects.create(aci_fabric=fab, name=f"Pod-{i + 1}", pod_id=i + 1)
        cls.create_data = [
            {"aci_fabric": fab.pk, "name": "Pod-10", "pod_id": 10},
            {"aci_fabric": fab.pk, "name": "Pod-11", "pod_id": 11},
        ]


class ACINodeAPITests(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    APITestCase,
):
    model = ACINode
    view_namespace = PLUGIN_API_NAMESPACE
    brief_fields = ["aci_pod", "description", "display", "id", "name", "node_id", "role", "url"]
    bulk_update_data = {"description": "Bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="ACI-API-NodeFab")
        pod = ACIPod.objects.create(aci_fabric=fab, name="Pod-1", pod_id=1)
        for i in range(3):
            ACINode.objects.create(
                aci_pod=pod, name=f"leaf-{200 + i}", node_id=200 + i, role="leaf"
            )
        cls.create_data = [
            {"aci_pod": pod.pk, "name": "leaf-300", "node_id": 300, "role": "leaf"},
            {"aci_pod": pod.pk, "name": "spine-101", "node_id": 101, "role": "spine"},
        ]


class ACIRootAPITest(APITestCase):
    """Tiny sanity test for the API root the plugin contributes."""

    def test_api_root_lists_endpoints(self):
        response = self.client.get("/api/plugins/cisco-aci/", **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        for key in ("fabrics", "pods", "nodes"):
            self.assertIn(key, body)
