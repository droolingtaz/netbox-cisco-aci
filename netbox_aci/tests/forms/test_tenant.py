"""Form tests for Phase 2."""

from django.test import TestCase

from netbox_aci.forms.tenant import (
    ACIBridgeDomainForm,
    ACIEndpointGroupForm,
    ACITenantForm,
    ACIVRFForm,
)
from netbox_aci.models.fabric import ACIFabric
from netbox_aci.models.tenant import ACIVRF, ACIAppProfile, ACIBridgeDomain, ACITenant


class TenancyFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.t = ACITenant.objects.create(aci_fabric=cls.fab, name="acme")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.t, name="vrf-prod")
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.t, name="ap")
        cls.bd = ACIBridgeDomain.objects.create(aci_tenant=cls.t, aci_vrf=cls.vrf, name="bd")

    def test_tenant_form_valid(self):
        form = ACITenantForm(data={"aci_fabric": self.fab.pk, "name": "shiny"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_vrf_form_valid(self):
        form = ACIVRFForm(
            data={
                "aci_tenant": self.t.pk,
                "name": "vrf-shiny",
                "policy_enforcement_preference": "enforced",
                "policy_enforcement_direction": "ingress",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_bd_form_valid(self):
        form = ACIBridgeDomainForm(
            data={
                "aci_tenant": self.t.pk,
                "aci_vrf": self.vrf.pk,
                "name": "bd-shiny",
                "unicast_routing_enabled": True,
                "limit_ip_learn_to_subnets": True,
                "l2_unknown_unicast": "proxy",
                "l3_unknown_multicast": "flood",
                "multi_destination_flooding": "bd-flood",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_epg_form_valid(self):
        form = ACIEndpointGroupForm(
            data={
                "aci_tenant": self.t.pk,
                "aci_app_profile": self.ap.pk,
                "aci_bridge_domain": self.bd.pk,
                "name": "epg-shiny",
                "qos_class": "unspecified",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
