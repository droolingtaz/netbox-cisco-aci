"""Model-level tests for Phase 1: Fabric, Pod, Node."""

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from netbox_aci.choices import NodeRoleChoices, NodeTypeChoices
from netbox_aci.models.fabric import ACIFabric, ACINode, ACIPod
from netbox_aci.tests.base import make_dcim_device


class ACIFabricTests(TestCase):
    def test_str_returns_name(self):
        fab = ACIFabric.objects.create(name="ACI-DC1", fabric_id=1)
        self.assertEqual(str(fab), "ACI-DC1")

    def test_name_must_be_unique(self):
        ACIFabric.objects.create(name="ACI-DC1", fabric_id=1)
        with self.assertRaises(IntegrityError):
            ACIFabric.objects.create(name="ACI-DC1", fabric_id=2)

    def test_fabric_id_default_is_one(self):
        fab = ACIFabric.objects.create(name="ACI-DC2")
        self.assertEqual(fab.fabric_id, 1)

    def test_two_fabrics_may_share_fabric_id(self):
        # ACI Fabric IDs are not globally unique — multi-fabric deployments
        # routinely reuse them. Ensure we don't accidentally over-constrain.
        ACIFabric.objects.create(name="ACI-DC1", fabric_id=1)
        # Should not raise.
        ACIFabric.objects.create(name="ACI-DC2", fabric_id=1)

    def test_aci_name_validator_rejects_bad_characters(self):
        fab = ACIFabric(name="bad name with space")
        with self.assertRaises(ValidationError):
            fab.full_clean()


class ACIPodTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fabric = ACIFabric.objects.create(name="ACI-DC1")

    def test_pod_id_unique_inside_fabric(self):
        ACIPod.objects.create(aci_fabric=self.fabric, name="Pod-1", pod_id=1)
        with self.assertRaises(IntegrityError):
            ACIPod.objects.create(aci_fabric=self.fabric, name="Pod-1-dup", pod_id=1)

    def test_same_pod_id_allowed_in_different_fabric(self):
        other_fabric = ACIFabric.objects.create(name="ACI-DC2")
        ACIPod.objects.create(aci_fabric=self.fabric, name="Pod-1", pod_id=1)
        ACIPod.objects.create(aci_fabric=other_fabric, name="Pod-1", pod_id=1)

    def test_pod_id_range_validation(self):
        pod = ACIPod(aci_fabric=self.fabric, name="bad-pod", pod_id=999)
        with self.assertRaises(ValidationError):
            pod.full_clean()


class ACINodeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fabric = ACIFabric.objects.create(name="ACI-DC1")
        cls.pod = ACIPod.objects.create(aci_fabric=cls.fabric, name="Pod-1", pod_id=1)

    def test_node_id_unique_inside_pod(self):
        ACINode.objects.create(aci_pod=self.pod, name="leaf-201", node_id=201)
        with self.assertRaises(IntegrityError):
            ACINode.objects.create(aci_pod=self.pod, name="leaf-201-dup", node_id=201)

    def test_gfk_columns_must_be_set_together(self):
        # Only node_object_id set with no node_object_type → invalid.
        node = ACINode(
            aci_pod=self.pod,
            name="bad-node",
            node_id=202,
            role=NodeRoleChoices.ROLE_LEAF,
            node_object_id=1,
        )
        with self.assertRaises(ValidationError):
            node.full_clean()

    def test_link_to_dcim_device(self):
        device = make_dcim_device(name="leaf-201")
        node = ACINode.objects.create(
            aci_pod=self.pod,
            name="leaf-201",
            node_id=201,
            role=NodeRoleChoices.ROLE_LEAF,
            node_type=NodeTypeChoices.TYPE_PHYSICAL,
            node_object_type=ContentType.objects.get_for_model(device),
            node_object_id=device.pk,
        )
        self.assertEqual(node.node_object, device)

    def test_aci_fabric_passthrough(self):
        node = ACINode.objects.create(
            aci_pod=self.pod, name="leaf-201", node_id=201, role=NodeRoleChoices.ROLE_LEAF
        )
        self.assertEqual(node.aci_fabric, self.fabric)
