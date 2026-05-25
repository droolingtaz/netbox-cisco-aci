"""Form tests for Phase 3."""

from django.test import TestCase

from netbox_cisco_aci.forms.access import (
    ACIAAEPEPGMappingForm,
    ACIAAEPForm,
    ACIDomainForm,
    ACIVLANPoolBlockForm,
    ACIVLANPoolForm,
)
from netbox_cisco_aci.models.access import ACIAAEP, ACIDomain, ACIVLANPool
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
)


class AccessFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.pool = ACIVLANPool.objects.create(
            aci_fabric=cls.fab, name="pool", allocation_mode="static"
        )
        cls.domain = ACIDomain.objects.create(
            aci_fabric=cls.fab,
            name="phys",
            domain_type="physical",
            aci_vlan_pool=cls.pool,
        )
        cls.aaep = ACIAAEP.objects.create(aci_fabric=cls.fab, name="aaep")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="acme")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-prod")
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant, name="ap")
        cls.bd = ACIBridgeDomain.objects.create(aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd")
        cls.epg = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg",
        )

    def test_pool_form_valid(self):
        form = ACIVLANPoolForm(
            data={
                "aci_fabric": self.fab.pk,
                "name": "pool-x",
                "allocation_mode": "dynamic",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_block_form_valid(self):
        form = ACIVLANPoolBlockForm(
            data={
                "aci_vlan_pool": self.pool.pk,
                "from_vlan": 100,
                "to_vlan": 200,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_domain_form_valid(self):
        form = ACIDomainForm(
            data={
                "aci_fabric": self.fab.pk,
                "name": "dom-x",
                "domain_type": "physical",
                "aci_vlan_pool": self.pool.pk,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_aaep_form_valid(self):
        form = ACIAAEPForm(
            data={
                "aci_fabric": self.fab.pk,
                "name": "aaep-x",
                "enable_infra_vlan": False,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_aaep_epg_mapping_form_valid(self):
        form = ACIAAEPEPGMappingForm(
            data={
                "aci_aaep": self.aaep.pk,
                "aci_endpoint_group": self.epg.pk,
                "name": "m1",
                "encap_vlan": 200,
                "mode": "regular",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
