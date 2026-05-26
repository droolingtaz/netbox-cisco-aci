"""Form tests for Phase 5."""

from django.test import TestCase

from netbox_cisco_aci.choices import (
    ContractFilterEntryEtherTypeChoices,
    ContractFilterEntryIPProtocolChoices,
    ContractRelationRoleChoices,
    SubjectFilterDirectionChoices,
)
from netbox_cisco_aci.forms.contracts import (
    ACIContractForm,
    ACIContractRelationForm,
    ACIFilterEntryForm,
    ACIFilterForm,
    ACISubjectFilterForm,
    ACISubjectForm,
)
from netbox_cisco_aci.models.contracts import (
    ACIContract,
    ACIFilter,
    ACISubject,
)
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
)


class Phase5FormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="acme")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-prod")
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant, name="ap-web")
        cls.bd = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd-web"
        )
        cls.epg = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-web",
        )
        cls.contract = ACIContract.objects.create(aci_tenant=cls.tenant, name="c-1")
        cls.filter = ACIFilter.objects.create(aci_tenant=cls.tenant, name="f-1")
        cls.subject = ACISubject.objects.create(aci_contract=cls.contract, name="s-1")

    def test_acicontract_form_valid(self):
        form = ACIContractForm(
            data={"aci_tenant": self.tenant.pk, "name": "c-new", "scope": "context"}
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acicontract_form_requires_name(self):
        form = ACIContractForm(data={"aci_tenant": self.tenant.pk})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_acisubject_form_valid(self):
        form = ACISubjectForm(
            data={
                "aci_contract": self.contract.pk,
                "name": "s-new",
                "apply_both_directions": True,
                "reverse_filter_ports": True,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acifilter_form_valid(self):
        form = ACIFilterForm(data={"aci_tenant": self.tenant.pk, "name": "f-new"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_acifilterentry_form_valid(self):
        form = ACIFilterEntryForm(
            data={
                "aci_filter": self.filter.pk,
                "name": "e-new",
                "ether_type": ContractFilterEntryEtherTypeChoices.IP,
                "ip_protocol": ContractFilterEntryIPProtocolChoices.TCP,
                "source_port_from": 80,
                "source_port_to": 80,
                "destination_port_from": 8080,
                "destination_port_to": 8080,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acifilterentry_form_invalid_port_pair(self):
        form = ACIFilterEntryForm(
            data={
                "aci_filter": self.filter.pk,
                "name": "e-bad",
                "ether_type": ContractFilterEntryEtherTypeChoices.IP,
                "ip_protocol": ContractFilterEntryIPProtocolChoices.TCP,
                "source_port_from": 80,
            }
        )
        self.assertFalse(form.is_valid())

    def test_acisubjectfilter_form_valid(self):
        form = ACISubjectFilterForm(
            data={
                "aci_subject": self.subject.pk,
                "aci_filter": self.filter.pk,
                "name": "sf-1",
                "direction": SubjectFilterDirectionChoices.BOTH,
                "action": "permit",
                "priority": "default",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acicontractrelation_form_valid(self):
        form = ACIContractRelationForm(
            data={
                "aci_contract": self.contract.pk,
                "aci_endpoint_group": self.epg.pk,
                "role": ContractRelationRoleChoices.PROVIDER,
                "name": "r-1",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_acicontractrelation_form_invalid_no_target(self):
        form = ACIContractRelationForm(
            data={
                "aci_contract": self.contract.pk,
                "role": ContractRelationRoleChoices.PROVIDER,
                "name": "r-bad",
            }
        )
        # The XOR check fires on model clean → form should be invalid.
        self.assertFalse(form.is_valid())
