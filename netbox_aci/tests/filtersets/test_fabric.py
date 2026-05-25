"""FilterSet tests for Phase 1."""

from django.test import TestCase

from netbox_aci.filtersets.fabric import ACIFabricFilterSet, ACINodeFilterSet, ACIPodFilterSet
from netbox_aci.models.fabric import ACIFabric, ACINode, ACIPod


class ACIFabricFilterSetTests(TestCase):
    queryset = ACIFabric.objects.all()
    filterset = ACIFabricFilterSet

    @classmethod
    def setUpTestData(cls):
        ACIFabric.objects.create(name="DC1", fabric_id=1, description="primary")
        ACIFabric.objects.create(name="DC2", fabric_id=1, description="secondary")
        ACIFabric.objects.create(name="DC3", fabric_id=2, description="dr")

    def test_filter_by_fabric_id(self):
        params = {"fabric_id": 1}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_search_hits_description(self):
        params = {"q": "primary"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class ACIPodFilterSetTests(TestCase):
    queryset = ACIPod.objects.all()
    filterset = ACIPodFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.fab1 = ACIFabric.objects.create(name="DC1")
        cls.fab2 = ACIFabric.objects.create(name="DC2")
        ACIPod.objects.create(aci_fabric=cls.fab1, name="Pod-1", pod_id=1)
        ACIPod.objects.create(aci_fabric=cls.fab1, name="Pod-2", pod_id=2)
        ACIPod.objects.create(aci_fabric=cls.fab2, name="Pod-1", pod_id=1)

    def test_filter_by_fabric(self):
        params = {"aci_fabric_id": [self.fab1.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class ACINodeFilterSetTests(TestCase):
    queryset = ACINode.objects.all()
    filterset = ACINodeFilterSet

    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="DC1")
        cls.pod = ACIPod.objects.create(aci_fabric=fab, name="Pod-1", pod_id=1)
        ACINode.objects.create(aci_pod=cls.pod, name="spine-101", node_id=101, role="spine")
        ACINode.objects.create(aci_pod=cls.pod, name="leaf-201", node_id=201, role="leaf")
        ACINode.objects.create(aci_pod=cls.pod, name="leaf-202", node_id=202, role="leaf")

    def test_filter_by_role(self):
        params = {"role": ["leaf"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_filter_by_pod(self):
        params = {"aci_pod_id": [self.pod.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
