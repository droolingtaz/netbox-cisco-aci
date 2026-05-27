"""Tests for table render methods (Bucket B — tables/access.py L140)."""

from django.test import TestCase

from netbox_cisco_aci.models.access import ACIAAEP
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.tables.access import ACIAAEPTable


class ACIAAEPTableRenderTests(TestCase):
    """Cover render_domain_count (L140 in tables/access.py)."""

    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="fab-table-test")
        cls.aaep = ACIAAEP.objects.create(aci_fabric=cls.fab, name="aaep-table-test")

    def test_render_domain_count_returns_zero_when_no_domains(self):
        table = ACIAAEPTable(ACIAAEP.objects.filter(pk=self.aaep.pk))
        # render_domain_count calls record.domains.count()
        count = table.render_domain_count(self.aaep)
        self.assertEqual(count, 0)
