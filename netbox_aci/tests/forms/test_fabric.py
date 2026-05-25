"""Form tests for Phase 1."""

from django.test import TestCase

from netbox_aci.forms.fabric import ACIFabricForm, ACINodeForm, ACIPodForm
from netbox_aci.models.fabric import ACIFabric, ACIPod


class ACIFabricFormTests(TestCase):
    def test_valid_payload(self):
        form = ACIFabricForm(data={"name": "DC1", "fabric_id": 1})
        self.assertTrue(form.is_valid(), form.errors)

    def test_bad_name_rejected(self):
        form = ACIFabricForm(data={"name": "bad name", "fabric_id": 1})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class ACIPodFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")

    def test_valid_payload(self):
        form = ACIPodForm(data={"aci_fabric": self.fab.pk, "name": "Pod-1", "pod_id": 1})
        self.assertTrue(form.is_valid(), form.errors)


class ACINodeFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fab = ACIFabric.objects.create(name="DC1")
        cls.pod = ACIPod.objects.create(aci_fabric=fab, name="Pod-1", pod_id=1)

    def test_valid_payload(self):
        form = ACINodeForm(
            data={
                "aci_pod": self.pod.pk,
                "name": "leaf-201",
                "node_id": 201,
                "role": "leaf",
                "node_type": "physical",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
