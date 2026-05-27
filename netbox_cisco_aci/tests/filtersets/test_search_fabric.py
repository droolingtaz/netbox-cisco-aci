"""FilterSet search() tests for fabric models (Bucket A)."""

from django.test import TestCase

from netbox_cisco_aci.filtersets.fabric import ACIFabricFilterSet, ACINodeFilterSet, ACIPodFilterSet
from netbox_cisco_aci.models.fabric import ACIFabric, ACINode, ACIPod


class ACIFabricFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab1 = ACIFabric.objects.create(name="fab-search-1", name_alias="", description="")
        cls.fab2 = ACIFabric.objects.create(
            name="fab-search-other", name_alias="fab-search-1-alias", description=""
        )
        cls.fab3 = ACIFabric.objects.create(
            name="fab-search-third",
            name_alias="",
            description="fab-search-1 in description",
        )

    def test_search_empty_value_returns_all(self):
        base_qs = ACIFabric.objects.filter(
            name__in=["fab-search-1", "fab-search-other", "fab-search-third"]
        )
        qs = ACIFabricFilterSet({"q": "  "}, base_qs).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        base_qs = ACIFabric.objects.filter(
            name__in=["fab-search-1", "fab-search-other", "fab-search-third"]
        )
        qs = ACIFabricFilterSet({"q": "fab-search-1"}, base_qs).qs
        self.assertEqual(qs.count(), 3)


class ACIPodFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-pod-search")
        ACIPod.objects.create(
            aci_fabric=cls.fab, name="iota-pod", pod_id=10, name_alias="", description=""
        )
        ACIPod.objects.create(
            aci_fabric=cls.fab,
            name="pod-other",
            pod_id=11,
            name_alias="iota-pod-alias",
            description="",
        )
        ACIPod.objects.create(
            aci_fabric=cls.fab,
            name="pod-third",
            pod_id=12,
            name_alias="",
            description="iota-pod in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACIPodFilterSet({"q": "  "}, ACIPod.objects.filter(aci_fabric=self.fab)).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACIPodFilterSet({"q": "iota-pod"}, ACIPod.objects.filter(aci_fabric=self.fab)).qs
        self.assertEqual(qs.count(), 3)


class ACINodeFilterSetSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-node-search")
        cls.pod = ACIPod.objects.create(aci_fabric=cls.fab, name="pod-node-search", pod_id=1)
        ACINode.objects.create(
            aci_pod=cls.pod,
            node_id=101,
            name="kappa-node",
            name_alias="",
            description="",
        )
        ACINode.objects.create(
            aci_pod=cls.pod,
            node_id=102,
            name="node-other",
            name_alias="kappa-node-alias",
            description="",
        )
        ACINode.objects.create(
            aci_pod=cls.pod,
            node_id=103,
            name="node-third",
            name_alias="",
            description="kappa-node in description",
        )

    def test_search_empty_value_returns_all(self):
        qs = ACINodeFilterSet({"q": "  "}, ACINode.objects.filter(aci_pod=self.pod)).qs
        self.assertEqual(qs.count(), 3)

    def test_search_matches_name_alias_and_description(self):
        qs = ACINodeFilterSet({"q": "kappa-node"}, ACINode.objects.filter(aci_pod=self.pod)).qs
        self.assertEqual(qs.count(), 3)
