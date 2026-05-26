"""FilterSet tests for Phase 5."""

from django.test import TestCase

from netbox_cisco_aci.choices import (
    ContractFilterEntryEtherTypeChoices,
    ContractFilterEntryIPProtocolChoices,
    ContractRelationRoleChoices,
    ContractScopeChoices,
    SubjectFilterDirectionChoices,
)
from netbox_cisco_aci.filtersets.contracts import (
    ACIContractFilterSet,
    ACIContractRelationFilterSet,
    ACIFilterEntryFilterSet,
    ACIFilterFilterSet,
    ACISubjectFilterFilterSet,
    ACISubjectFilterSet,
)
from netbox_cisco_aci.models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
)


class Phase5FilterSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.tenant1 = ACITenant.objects.create(aci_fabric=cls.fab, name="acme")
        cls.tenant2 = ACITenant.objects.create(aci_fabric=cls.fab, name="other")

        cls.c1 = ACIContract.objects.create(
            aci_tenant=cls.tenant1, name="c-vrf", scope=ContractScopeChoices.SCOPE_VRF
        )
        cls.c2 = ACIContract.objects.create(
            aci_tenant=cls.tenant2, name="c-global", scope=ContractScopeChoices.SCOPE_GLOBAL
        )

        cls.f1 = ACIFilter.objects.create(aci_tenant=cls.tenant1, name="f-1")
        cls.f2 = ACIFilter.objects.create(aci_tenant=cls.tenant2, name="f-2")

        ACIFilterEntry.objects.create(
            aci_filter=cls.f1,
            name="e-tcp",
            ether_type=ContractFilterEntryEtherTypeChoices.IP,
            ip_protocol=ContractFilterEntryIPProtocolChoices.TCP,
        )
        ACIFilterEntry.objects.create(
            aci_filter=cls.f1,
            name="e-udp",
            ether_type=ContractFilterEntryEtherTypeChoices.IP,
            ip_protocol=ContractFilterEntryIPProtocolChoices.UDP,
        )

        cls.s1 = ACISubject.objects.create(aci_contract=cls.c1, name="s-1")
        cls.s2 = ACISubject.objects.create(aci_contract=cls.c2, name="s-2")

        ACISubjectFilter.objects.create(
            aci_subject=cls.s1,
            aci_filter=cls.f1,
            name="sf-1",
            direction=SubjectFilterDirectionChoices.BOTH,
        )

        vrf = ACIVRF.objects.create(aci_tenant=cls.tenant1, name="vrf")
        ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant1, name="ap")
        bd = ACIBridgeDomain.objects.create(aci_tenant=cls.tenant1, aci_vrf=vrf, name="bd")
        cls.epg = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant1, aci_app_profile=ap, aci_bridge_domain=bd, name="epg"
        )
        ACIContractRelation.objects.create(
            aci_contract=cls.c1,
            aci_endpoint_group=cls.epg,
            role=ContractRelationRoleChoices.PROVIDER,
            name="r-prov",
        )

    def _run(self, fs_cls, qs, params):
        return fs_cls(params, queryset=qs).qs

    def test_contract_by_tenant(self):
        qs = self._run(
            ACIContractFilterSet, ACIContract.objects.all(), {"aci_tenant_id": [self.tenant1.pk]}
        )
        self.assertEqual(list(qs), [self.c1])

    def test_contract_by_scope(self):
        qs = self._run(ACIContractFilterSet, ACIContract.objects.all(), {"scope": ["global"]})
        self.assertEqual(list(qs), [self.c2])

    def test_contract_search(self):
        qs = self._run(ACIContractFilterSet, ACIContract.objects.all(), {"q": "vrf"})
        self.assertIn(self.c1, qs)

    def test_filter_by_tenant(self):
        qs = self._run(
            ACIFilterFilterSet, ACIFilter.objects.all(), {"aci_tenant_id": [self.tenant1.pk]}
        )
        self.assertEqual(list(qs), [self.f1])

    def test_filterentry_by_filter(self):
        qs = self._run(
            ACIFilterEntryFilterSet, ACIFilterEntry.objects.all(), {"aci_filter_id": [self.f1.pk]}
        )
        self.assertEqual(qs.count(), 2)

    def test_filterentry_by_ip_protocol(self):
        qs = self._run(
            ACIFilterEntryFilterSet, ACIFilterEntry.objects.all(), {"ip_protocol": ["tcp"]}
        )
        self.assertEqual(qs.count(), 1)

    def test_subject_by_contract(self):
        qs = self._run(
            ACISubjectFilterSet, ACISubject.objects.all(), {"aci_contract_id": [self.c1.pk]}
        )
        self.assertEqual(list(qs), [self.s1])

    def test_subjectfilter_by_subject(self):
        qs = self._run(
            ACISubjectFilterFilterSet,
            ACISubjectFilter.objects.all(),
            {"aci_subject_id": [self.s1.pk]},
        )
        self.assertEqual(qs.count(), 1)

    def test_subjectfilter_by_direction(self):
        qs = self._run(
            ACISubjectFilterFilterSet,
            ACISubjectFilter.objects.all(),
            {"direction": ["both"]},
        )
        self.assertEqual(qs.count(), 1)

    def test_contractrelation_by_contract(self):
        qs = self._run(
            ACIContractRelationFilterSet,
            ACIContractRelation.objects.all(),
            {"aci_contract_id": [self.c1.pk]},
        )
        self.assertEqual(qs.count(), 1)

    def test_contractrelation_by_role(self):
        qs = self._run(
            ACIContractRelationFilterSet,
            ACIContractRelation.objects.all(),
            {"role": ["provider"]},
        )
        self.assertEqual(qs.count(), 1)
